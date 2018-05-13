from urllib.parse import urlparse, urlunparse
import logging
import os
import random

from bs4 import BeautifulSoup
import requests

from app import cache
from app import config
from app import view
from app.app_locals import grab_attr, grab_text

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
def get_full_url(url_html, url_image):
    # convert relative urls to fully resolvable url
    parsed_html = urlparse(url_html)
    parsed_image = urlparse(url_image)

    image_src_full = '{scheme}://{netloc}/{path}'.format(
        scheme=parsed_image.scheme or parsed_html.scheme or 'http',
        netloc=parsed_image.netloc or parsed_html.netloc,
        path=parsed_image.path.strip(),
        # 'params': parsed_image.params,
        # 'query': parsed_image.query,
        # 'fragment': parsed_image.fragment,
    )
    return image_src_full

def fetch_comic_multiple(config, name, count=1):
    # fetch image and metadata from cache/requests, returns `{}` on failure
    print("Config: {}".format(name))
    comic_list = []
    prev_url = None # config['url']
    # prev_html_url = None

    for i in range(count):
        if i == 0:
            html = cache.request_cached_text(config['url'])
            soup = BeautifulSoup(html, 'html5lib')
            prev_url = grab_attr(soup, config['selectors']['prev'], 'href')
            if not prev_url:
                raise Exception("Should not happen yet")

            image_src = grab_attr(soup, config['selectors']['image'], 'src')
            if not image_src:
                logging.error("Bad selector for: {config}".format(config=config))
                print("Bad selector for: {config}".format(config=config))
                continue

            image_src_full = get_full_url(config['url'], image_src)

            logging.debug("relative url, New source = {}".format(image_src_full))
            image_local_filename = cache.request_cached_binary(image_src_full)
            if not image_local_filename:
                logging.error("Something went wrong with: {}".format(image_src_full))
                raise Exception("Something went wrong with: {}".format(image_src_full))

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
            }
            comic_list.append(comic)
        else:
            continue
            if not prev_url:
                continue
            print("prev: ", prev_url)
            html = cache.request_cached_text(prev_url)
            soup = BeautifulSoup(html, 'html5lib')
            prev_url = grab_attr(soup, config['selectors']['prev'], 'href')
            if not prev_url:
                raise Exception("Should not happen yet")

            image_src = grab_attr(soup, config['selectors']['image'], 'src')
            if not image_src:
                logging.error("Bad selector for: {config}".format(config=config))
                print("Bad selector for: {config}".format(config=config))



        # image_src = grab_attr(soup, config['selectors']['image'], 'src')
        # if not image_src:
        #     logging.error("Bad selector for: {config}".format(config=config))
        #     print("Bad selector for: {config}".format(config=config))



        # return comic
    return comic_list

if __name__ == "__main__":
    comics = []
    for name in config.config:
        comic_list = fetch_comic_multiple(config.config[name], name, 3)
        if comic_list:
            comics.append(comic_list)

    if ALWAYS_RANDOM:
        random.shuffle(comics)

    html = view.render(comics)
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)

    cache.write_config()

    # print(comics)
    print("Done.")
