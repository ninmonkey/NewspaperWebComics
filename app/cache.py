from datetime import datetime
import os
import json
import logging
import mimetypes

import requests
# 'date_cached': datetime.datetime.now(),
# todo: check if html expired, expecially on front page. maybe not on foo.com/comic/<id>
from app.str_const import(
    STR_DATE_FORMAT_MICROSECONDS,
    STR_DATE_FORMAT_SECONDS,
)


cache = {}
PATH_ROOT = ''
logging = logging.getLogger(__name__)


def init(path_cache):
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


def request_cached_binary(request_url):
    # requests.get() but cached, binary, returns: filename
    global cache

    if request_url in cache:
        logging.debug("cached Binary file: {}".format(request_url))
        filename = cache[request_url]['local_file']
        filepath = os.path.join(PATH_ROOT, filename)
        return 'cache/' + filename
    else:
        logging.debug("Requesting new Binary file! {}\n{}".format(request_url, cache))
        print("Requesting new Binary file! {}".format(request_url))
        # todo: try/catch for badname/timeouts
            # log, then continue
        r = requests.get(request_url)
        if not r.ok:
            logging.error("Error!: code = {}, reason = {}".format(r.status_code, r.reason), exc_info=True)
            raise Exception("Error: {}, {}!".format(r.status_code, r.reason))

        mime_type = r.headers['content-type']
        ext_type = mimetypes.guess_extension(mime_type) or ''

        filename = "{datetime}{ext}".format(
            datetime=datetime.now().strftime(STR_DATE_FORMAT_MICROSECONDS),
            ext=ext_type)
        filepath = os.path.join(PATH_ROOT, filename)
        with open(filepath, mode='wb') as f:
            f.write(r.content)

        cache[request_url] = {
            'local_file': filename,
            'download_date': datetime.now().strftime(STR_DATE_FORMAT_SECONDS),
            # 'content-type': '?binary?',
            'content-type': mime_type,
            'extension': ext_type,
        }

    cache_write_config(cache)
    return 'cache/' + filename


def request_cached_text(request_url):
    # requests.get() but cached, and returns: request text
    global cache

    if request_url in cache:
        logging.debug("cached Text file: {}".format(request_url))
        file = cache[request_url]['local_file']
        filepath = os.path.join(PATH_ROOT, file)

        with open(filepath, mode='r', encoding='utf8') as f:
            return f.read()
    else:
        logging.debug("Requesting new Text file! {}\n{}".format(request_url, cache))
        # todo: try/catch for badname/timeouts
            # log, then continue
        r = requests.get(request_url)
        if not r.ok:
            logging.error("Error!: code = {}, reason = {}".format(r.status_code, r.reason), exc_info=True)
            raise Exception("Error: {}, {}!".format(r.status_code, r.reason))

        mime_type = r.headers['content-type']
        ext_type = mimetypes.guess_extension(mime_type) or ''

        filename = "{datetime}{ext}".format(
            datetime=datetime.now().strftime(STR_DATE_FORMAT_MICROSECONDS),
            ext=ext_type)
        filepath = os.path.join(PATH_ROOT, filename)
        with open(filepath, mode='w', encoding='utf-8') as f:
            f.write(r.text)

        cache[request_url] = {
            'local_file': filename,
            'download_date': datetime.now().strftime(STR_DATE_FORMAT_SECONDS),
            'content-type': mime_type,
            'extension': ext_type,
        }

    cache_write_config(cache)
    return r.text
