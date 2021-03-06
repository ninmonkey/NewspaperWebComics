import logging

from bs4 import BeautifulSoup

from app import cache
from app.app_locals import (
    get_full_url,
    grab_attr,
    grab_text,
)


def fetch_comics_multiple(config, name, order, count=2):
    # fetch image and metadata from cache/requests, returns `{}` on failure
    print("Config: {}".format(name))
    comic_list = []
    next_url = config['url']
    has_prev = False

    for i in range(count):
        if not next_url:
            continue

        next_url = get_full_url(config['url'], next_url)

        html = cache.request_cached_text(next_url)
        if not html:
            continue

        soup = BeautifulSoup(html, 'html5lib')
        # next_url = None
        if config['selectors'].get('prev'):
            next_url = grab_attr(soup, config['selectors']['prev'], 'href')
            if next_url:
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
            'class': config.get('class'),
            'name': name,
            'title': comic_title,
            'url': config['url'],
            'image_alt': image_alt,
            'image_src': image_local_filename,
            'has_prev': has_prev,
            'order': order,
        }
        comic_list.append(comic)

    return comic_list
