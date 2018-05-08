from datetime import datetime
import os
import json
import logging

import requests
# 'date_cached': datetime.datetime.now(),
# todo: check if html expired, expecially on front page. maybe not on foo.com/comic/<id>

cache = {}
PATH_ROOT = ''
logging = logging.getLogger(__name__)


def init_cache(path_cache):
    global PATH_ROOT

    PATH_ROOT = path_cache
    os.makedirs(PATH_ROOT, exist_ok=True)
    logging.debug("Cache: {}".format(path_cache))
    cache = cache_read_config()


def cache_read_config():
    global cache
    # todo: create if not existing
    json_path = os.path.join(PATH_ROOT, 'cache.json')

    if not os.path.exists(json_path):
        cache_write_config(cache)

    try:
        with open(json_path, mode='r', encoding='utf-8') as f:
            cache = json.load(f)
    except (ValueError):
        cache = {}

    return cache


def cache_write_config(cache):
    json_path = os.path.join(PATH_ROOT, 'cache.json')
    with open(json_path, mode='w', encoding='utf-8') as f:
        json.dump(cache, f, indent=4, sort_keys=True)


def request_cached(request_url):
    # regular requests.get() with caching
    global cache

    # save url/read from cache
    if request_url in cache:
        logging.debug("cached file: {}".format(request_url))
        file = cache[request_url]['local_file']
        file_path = os.path.join(PATH_ROOT, file)
        with open(file_path, mode='r', encoding='utf8') as f:
            return f.read()
    else:
        logging.debug("Requesting new file! {}".format(request_url))
        logging.debug(cache)
        # todo: try/catch for badname/timeouts
            # log, then continue
        r = requests.get(request_url)
        if not r.ok:
            logging.error("Error!: code = {}, reason = {}".format(r.status_code, r.reason))
            raise Exception("Error: {}, {}!".format(r.status_code, r.reason))

        # FILENAME
        filename = "{datetime}".format(datetime=datetime.now().strftime("%Y %m %d - %H %M %S %f"))
        file_path = os.path.join(PATH_ROOT, filename)
        with open(file_path, mode='w', encoding='utf-8') as f:
            f.write(r.text)

        cache[request_url] = {
            'local_file': filename,
            'download_date': datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
        }

    cache_write_config(cache)
    return r.text
