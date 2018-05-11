from urllib.parse import urlparse
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

logging.getLogger("chardet").setLevel(logging.WARNING)
logging.basicConfig(
    handlers=[logging.FileHandler(os.path.join(LOGGING_DIR, 'main.log'), 'w', 'utf-8')],
    level=logging.DEBUG)

cache.init(os.path.join(ROOT_DIR, 'cache'))
os.makedirs(LOGGING_DIR, exist_ok=True)


def fetch_comic(config, name):
    print("Config: {}".format(name))
    html = cache.request_cached_text(config['url'])
    soup = BeautifulSoup(html, 'html5lib')

    image_src = grab_attr(soup, config['selectors']['image'], 'src')
    if not image_src:
        logging.error("Bad selector for: {config}".format(config=config))
        print("Bad selector for: {config}".format(config=config))
        return {}

    if image_src.startswith("//"):
        # todo: try https, fallback to http
        image_src = "http:" + image_src

    # using relative url
    if not urlparse(image_src).scheme:
        raise Exception("todo: instead of config['url'] base use urlparse output")
        base = config['url'].rstrip('/')
        path = image_src.lstrip('/')

        image_src = "{base}/{path}".format(base=base, path=path)
        logging.debug("relative url, New source = {}".format(image_src))

    image_local_filename = cache.request_cached_binary(image_src)
    if not image_local_filename:
        logging.error("Something went wrong with: {}".format(image_src))
        raise Exception("Something went wrong with: {}".format(image_src))

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
    }

    return comic

if __name__ == "__main__":
    comics = []
    for name in config.config:
        comic = fetch_comic(config.config[name], name)
        if comic:
            comics.append(comic)

    if ALWAYS_RANDOM:
        random.shuffle(comics)

    logging.debug(comics)

    html = view.render(comics)
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)

    print("Done.")
