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
logging.basicConfig(
    handlers=[logging.FileHandler(os.path.join(LOGGING_DIR, 'main.log'), 'w', 'utf-8')],
    level=logging.DEBUG)

cache.init(os.path.join(ROOT_DIR, 'cache'))


def fetch_comic(config, name):
    print("Config: {}".format(name))
    html = cache.request_cached_text(config['url'])
    soup = BeautifulSoup(html, 'html5lib')

    image_src = grab_attr(soup, config['selectors']['image'], 'src')
    if not image_src:
        logging.error("Bad selector for: {config}".format(config=config))
        print("Bad selector for: {config}".format(config=config))
        return {}


    parsed_html = urlparse(config['url'])
    parsed_image = urlparse(image_src)

    # print("_html: ", parsed_html)
    # print("_image: ", parsed_image)

    """
    >>> par.geturl()
    'imgs.xkcd.com/comics/safetysat.png'
    >>> par
    ParseResult(scheme='', netloc='', path='imgs.xkcd.com/comics/safetysat.png', params='', query='', fragment='')
    """

    # relative urls
    # if image_src.startswith('/'):
        # image_src = image_src.strip('//')
    args = {
        'scheme': parsed_image.scheme or parsed_html.scheme or 'http',
        'netloc': parsed_image.netloc or parsed_html.netloc,
        'path': parsed_image.path,
        'params': parsed_image.params,
        'query': parsed_image.query,
        'fragment': parsed_image.fragment,
    }
    # image_src = urlunparse(**args)
    image_src_full = '{scheme}://{netloc}/{path}'.format(**args)
    print("new: ", image_src_full)

    return {}

    if image_src.startswith('//'):
        # todo: try https, fallback to http
        image_src = "{scheme}:{image_src}".format(
            scheme=parsed.scheme,
            image_src=image_src)
    else:
        print(".img_src=. ", image_src)
        image_src = "{scheme}://{netloc}/{image_src}".format(
            scheme=parsed.scheme,
            netloc=parsed.netloc,
            image_src=parsed_src.path.strip())

    print(".configurl=. ", config['url'])
    print(".parse=. ", urlparse(config['url']))



    # if parsed.path:


    # using relative url
    # if not urlparse(image_src).scheme:
        # raise Exception("todo: instead of config['url'] base use urlparse output")
        # base = config['url'].rstrip('/')
        # path = image_src.lstrip('/')

        # image_src = "{base}/{path}".format(base=base, path=path)



    print(".img_src=. ", image_src)
    logging.debug("relative url, New source = {}".format(image_src))


    # print("http://sssscomic.com/comicpages/900.jpg")
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
