import logging
import os

import requests
from bs4 import BeautifulSoup

from app import cache
from app import view

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
LOGGING_DIR = os.path.join(ROOT_DIR, "logs")

logging.basicConfig(
    handlers=[logging.FileHandler(os.path.join(LOGGING_DIR, "main.log"), 'w', 'utf-8')],
    level=logging.DEBUG)

cache.init_cache(os.path.join(ROOT_DIR, "cache"))
os.makedirs(LOGGING_DIR, exist_ok=True)


if __name__ == "__main__":
    html_xkcd = cache.request_cached('https://xkcd.com/1912/')
    html_pa = cache.request_cached('https://www.penny-arcade.com/comic')

    # xkcd
    print("config: xkcd")
    soup = BeautifulSoup(html_xkcd, 'html.parser')
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
    comic = {
        'src': elem_comic.img['src'],
        'alt': elem_comic.img['alt'],
        'header': elem_comic.img['alt'],
    }
    logging.debug(comic)
    print(comic)

    html = view.render()
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)

    print('done')