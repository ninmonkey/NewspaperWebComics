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
    print("Config: {}".format(name))
    print(name)
    print(config)
    html = cache.request_cached(config['url'])
    soup = BeautifulSoup(html, 'html5lib')

    image_src = grab_attr(soup, config['selectors']['image'], 'src')
    image_alt = grab_attr(soup, config['selectors']['image'], 'alt')
    comic_title = grab_text(soup, config['selectors']['comic_title'])

    return {
        'image_src': image_src,
        'image_alt': image_alt,
        'comic_title': comic_title,
    }

if __name__ == "__main__":
    comics = []
    for name in config.config:
        comics.append(fetch_comic(config.config[name]))

    print(comics)
    print("Done.")

def new_stuff():
    print('new: start')
    html_xkcd = cache.request_cached('https://xkcd.com/1912/')
    soup = BeautifulSoup(html_xkcd, 'html5lib')

    selectors = {
        'image': '#comic img',
        'comic_title': '#ctitle',
    }

    image_src = grab_attr(selectors['image'], 'src')
    image_alt = grab_attr(selectors['image'], 'alt')
    # todo: xkcd requires title but some reason it fails
    # image_title = grab_attr(selectors['image'], 'title')
    comic_title = grab_text(selectors['comic_title'])

    comic = {
        'image_src': image_src,
        'image_alt': image_alt,
        # 'image_title': image_title,
        'comic_title': comic_title,
    }
    """
    image_src = #comic img
    """
    print(image_src)
    print(comic)


    html_pa = cache.request_cached('https://www.penny-arcade.com/comic')
    soup = BeautifulSoup(html_pa, 'html5lib')

    selectors = {
        'image': '#comicFrame img',
        'comic_title': '#comic div div h2',
    }

    image_src = grab_attr(selectors['image'], 'src')
    image_alt = grab_attr(selectors['image'], 'alt')
    comic_title = grab_text(selectors['comic_title'])

    comic = {
        'image_src': image_src,
        'image_alt': image_alt,
        # 'image_title': image_title,
        'comic_title': comic_title,
    }
    """
    image_src = #comic img
    """
    print(comic)
    print('new: end')

if False:
    html_xkcd = cache.request_cached('https://xkcd.com/1912/')
    html_pa = cache.request_cached('https://www.penny-arcade.com/comic')

    # xkcd
    print('config: xkcd')
    soup = BeautifulSoup(html_xkcd, 'html5lib')  # 'html.parser'
    container_id = 'comic'
    header_id = 'ctitle'

    elem_comic = soup.find(id=container_id)
    elem_header = soup.find(id=header_id)
    comic = {
        # 'url': 'https://xkcd.com/1912/',
        'src': elem_comic.img['src'],
        'alt': elem_comic.img['alt'],
        'title': elem_comic.img['title'],
        'header': elem_header.text
        # 'prev':,
    }
    logging.debug(comic)
    print(comic)

    print("config: PA")
    soup = BeautifulSoup(html_pa, 'html.parser')
    container_id = 'comicFrame'
    elem_comic = soup.find(id=container_id)
    comic_kwargs = {
        'src': elem_comic.img['src'],
        'alt': elem_comic.img['alt'],
        'header': elem_comic.img['alt'],
    }
    logging.debug(comic_kwargs)
    print(comic_kwargs)

    html = view.render(comic_kwargs)
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)

    print(html)

    new_stuff()

    print('done')