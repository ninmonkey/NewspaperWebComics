import logging
import os
import random
import time
import threading

from bs4 import BeautifulSoup

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

class ComicListThreaded():
    def __init__(self):
        self.comics = []
        self.lock = threading.Lock()

    def add(self, comics):
        logging.debug("waiting for lock")
        with self.lock:
            logging.debug("acquire lock")
            self.comics.append(comics)
            # if not in self.comics:
            #     self.comics.append(c)
                # self.comics.append(comic['comic_url'])

comic_list_threaded = ComicListThreaded()

def fetch_comics_multiple(config, name, count=2):
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


def main_sync(count=3):
    comics = []
    print("main sync")
    for name in config.config:
        comic_list = fetch_comics_multiple(config.config[name], name, count)
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


def work(config, name, count=2):
    global comic_list_threaded

    fetched = fetch_comics_multiple(config, name, count)
    comic_list_threaded.add(fetched)


def main_threaded():
    # url_list = UrlListThreaded()
    threads = []
    count = 2

    print("main_threaded")

    for name in config.config:
        t = threading.Thread(target=work,args=(config.config[name], name, count))
        threads.append(t)
        t.start()

    main_thread = threading.main_thread()
    for t in threading.enumerate():
        if t is main_thread:
            continue

        logging.debug("Joining {}".format(t.getName()))
        t.join()

    html = view.render(comic_list_threaded.comics)
    cache.write_config()
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)

    print("comics = ", comic_list_threaded.comics)
    print("Done. Threaded")


if __name__ == "__main__":
    t_start = time.time()
    # main_sync()
    main_threaded()
    t_end = time.time()
    print("Time: {} seconds".format((t_end - t_start)))
