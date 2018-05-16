import logging
import os
import random
import time
import threading

from bs4 import BeautifulSoup
import requests

from app import cache
from app import config
from app import view
from app.app_locals import (
    get_full_url,
    grab_attr,
    grab_text,
)

ALWAYS_RANDOM = False
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
LOGGING_DIR = os.path.join(ROOT_DIR, 'logs')
os.makedirs(LOGGING_DIR, exist_ok=True)

logging.getLogger("chardet").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.basicConfig(
    handlers=[logging.FileHandler(os.path.join(LOGGING_DIR, 'main.log'), 'w', 'utf-8')],
    level=logging.DEBUG)

cache.init(os.path.join(ROOT_DIR, 'cache'))

class UrlListThreaded():
    def __init__(self):
        self.urls = []
        self.lock = threading.Lock()

    def add(self, comic):
        logging.debug("waiting for lock")
        self.lock.acquire()
        try:
            logging.debug("acquire lock")
            if not comic['comic_url'] in self.urls:
                self.urls.append(comic['comic_url'])
        finally:
            self.lock.release()


def fetch_comics_multiple(config, name, count=1):
    # fetch image and metadata from cache/requests, returns `{}` on failure
    print("Config: {}".format(name))
    comic_list = []
    next_url = config['url']
    has_prev = False

    for i in range(count):
        if not next_url:
            # logging.error("Bad selector for next_url for count {0} of {1}".format(i, name))
            # raise Exception("No next_Url for count {0} of {1}".format(i, name))
            continue

        next_url = get_full_url(config['url'], next_url)

        html = cache.request_cached_text(next_url)
        if not html:
            continue

        soup = BeautifulSoup(html, 'html5lib')
        if config['selectors'].get('prev'):
            next_url = grab_attr(soup, config['selectors']['prev'], 'href')
            has_prev = True
        else:
            next_url = None
        image_src = grab_attr(soup, config['selectors']['image'], 'src')

        if not image_src:
            logging.error("Bad selector for: {config}".format(config=config))
            print("Error: Bad selector for: {config}".format(config=config))
            continue

        image_src_full = get_full_url(config['url'], image_src)

        logging.debug("relative url, New source = {}".format(image_src_full))
        image_local_filename = cache.request_cached_binary(image_src_full)

        if not image_local_filename:
            logging.error("Error: Something went wrong with: {}".format(image_src_full))
            raise Exception("Something went wrong with image_local_filename. src = {}".format(image_src_full))
            continue

        image_alt = grab_attr(soup, config['selectors']['image'], 'alt')
        comic_title = grab_text(soup, config['selectors']['comic_title'])

        comic_title = comic_title or image_alt or ''
        comic = {
            'comic_class': config.get('class'),
            'comic_name': name,
            'comic_title': comic_title,
            'comic_url': config['url'],
            'image_alt': image_alt,
            'image_src': image_local_filename,
            'unread': cache.cache[image_src_full]['unread'],
            'has_prev': has_prev,
        }
        comic_list.append(comic)

    return comic_list


def main_sync():

    comics = []
    for name in config.config:
        comic_list = fetch_comics_multiple(config.config[name], name, 3)
        if comic_list:
            # ALL_URLS.append(comic_list[0]['comic_url'])
            comics.append(comic_list)

    if ALWAYS_RANDOM:
        random.shuffle(comics)

    html = view.render(comics)
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)

    cache.write_config()

    print(comics)
    print("Done.")
    # print(ALL_URLS)


def work(url_list, config, name, count):
    comic_list = fetch_comics_multiple(config, name, count)
    # print(comic_list)
    # for c in comic_list:
    #     url_list.add(c)


def main_threaded():
    url_list = UrlListThreaded()
    threads = []
    comics = []
    count = 3

    for name in config.config:
        t = threading.Thread(target=work,args=(url_list, config.config[name], name, count))
        threads.append(t)
        t.start()

    main_thread = threading.main_thread()
    for t in threading.enumerate():
        if t is main_thread:
            continue

        logging.debug("Joining {}".format(t.getName()))
        t.join()

    print("threads joined")

        #
        # work(config.config[name], name, 1)
        # if comic_list:
        #     url_list.add(comic_list)

    # for name in config.config:
    #     comic_list = work(config.config[name], name, 1)
    #     if comic_list:
    #         comics.append(comic_list)

    # html = view.render(comics)
    # with open('index.html', 'w', encoding='utf-8') as f:
    #     f.write(html)
    #
    cache.write_config()

    print(comics)
    print("url_thread = {}".format(url_list.urls))
    print("Done.")


if __name__ == "__main__":
    # import profile
    # profile.run('main(); print()')
    t_start = time.time()
    # main_sync()
    main_threaded()
    t_end = time.time()

    print("Time: {} seconds".format((t_end - t_start)))
    print("full cache: ~= 0.14-0.19 [len = 4]")
    print("Full empty: ~= 6.8       [len = 4]")

    print("Full empty: ~= 15.37     [len = 4, count=3]")
    print("Full empty: ~= 5 secs     thread[len = 4, count=3]")

    print("Full empty: ~= xxx       thread[len = 4]")