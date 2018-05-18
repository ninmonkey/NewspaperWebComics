import logging

from bs4 import BeautifulSoup

from app import cache
from app.app_locals import (
    get_full_url,
    grab_attr,
    grab_text,
)


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

        print("next")
        print(config['url'])
        print(next_url)
        next_url = get_full_url(config['url'], next_url)
        print(next_url)

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
            'comic_class': config.get('class'),
            'comic_name': name,
            'comic_title': comic_title,
            'comic_url': config['url'],
            'image_alt': image_alt,
            'image_src': image_local_filename,
            'unread': cache.cache[image_src_full]['unread'],
            'has_prev': has_prev,
        }
        # if comic not in comic_list:
        # else:
        #     print("Uh oh!")
        #     logging.debug("Uh oh!")
        comic_list.append(comic)

    return comic_list
