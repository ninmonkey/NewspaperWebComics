import logging
import os

import requests
from bs4 import BeautifulSoup

from app import cache
from app import view
from app import config

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
LOGGING_DIR = os.path.join(ROOT_DIR, 'logs')

logging.basicConfig(
    handlers=[logging.FileHandler(os.path.join(LOGGING_DIR, 'main.log'), 'w', 'utf-8')],
    level=logging.DEBUG)

cache.init_cache(os.path.join(ROOT_DIR, 'cache'))
os.makedirs(LOGGING_DIR, exist_ok=True)


def grab_attr(soup, selector, attr):
    # return one or None
    element = soup.select(selector)
    if element:
        # attr = 'src'
        return element[0][attr]

    return None


def grab_text(soup, selector):
    # return one or None
    element = soup.select(selector)
    if element:
        return element[0].text

    return None


def fetch_comic(config):
    print("Config: {}".format(name)) # wait, `name` works?!
    print(name)
    print(config)
    html = cache.request_cached_text(config['url'])
    soup = BeautifulSoup(html, 'html5lib')

    image_src = grab_attr(soup, config['selectors']['image'], 'src')
    if image_src.startswith("//"):
        image_src = "http://" + image_src[2:]

    # cache.request_cached(image_src)
    # cached_image_src = cache.cache[image_src].get('local_file')
    # print(cached_image_src)
    # print("!!!")

    # image_src =cache.cache[image_src]
    # image_src = cache.cache[]

    image = cache.request_cached_binary(image_src)
    cached_image_src = cache.cache[image_src]['local_file']

    image_alt = grab_attr(soup, config['selectors']['image'], 'alt')
    comic_title = grab_text(soup, config['selectors']['comic_title'])

    comic = {
        'comic_class': config['class'],
        'comic_name': name,
        'comic_title': comic_title,
        'comic_url': config['url'],
        'image_alt': image_alt,
        'image_src': cached_image_src,
        # 'image_src': image_src,
    }

    return comic

if __name__ == "__main__":
    comics = []
    for name in config.config:
        comics.append(fetch_comic(config.config[name]))

    print(comics)
    logging.debug(comics)

    html = view.render(comics)
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)

    print("Done.")
