import datetime
import json
import logging
import mimetypes
import os

import requests

# todo: check if html expired, expecially on front page. maybe not on foo.com/comic/<id>
from app.str_const import(
    STR_DATE_FORMAT_MICROSECONDS,
    STR_DATE_FORMAT_SECONDS,
)


cache = {}
PATH_ROOT = ''
DEFAULT_EXPIRE_TIME = datetime.timedelta(days=1)
logging = logging.getLogger(__name__)


def init(path_cache):
    global PATH_ROOT
    global cache

    PATH_ROOT = path_cache
    os.makedirs(PATH_ROOT, exist_ok=True)
    logging.debug("Cache: {}".format(path_cache))
    cache = read_config()


def read_config():
    global cache

    json_path = os.path.join(PATH_ROOT, 'cache.json')

    if not os.path.exists(json_path):
        write_config()

    try:
        with open(json_path, mode='r', encoding='utf-8') as f:
            cache = json.load(f)
    except (ValueError):
        cache = {}

    return cache


def write_config():
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
        cache[request_url]['unread'] = False

        return 'cache/' + filename
    else:
        logging.debug("Requesting new Binary file! {}\n{}".format(request_url, cache))
        print("Requesting new Binary file! {}".format(request_url))
        # todo: try/catch for badname/timeouts
            # log, then continue
        r = requests.get(request_url)
        if not r.ok:
            logging.error("Error!: code = {}, reason = {}".format(r.status_code, r.reason), exc_info=True)
            # raise Exception("Error: {}, {}!".format(r.status_code, r.reason))
            return None

        mime_type = r.headers['content-type']
        ext_type = mimetypes.guess_extension(mime_type) or ''

        filename = "{datetime}{ext}".format(
            datetime=datetime.datetime.now().strftime(STR_DATE_FORMAT_MICROSECONDS),
            ext=ext_type)
        filepath = os.path.join(PATH_ROOT, filename)
        with open(filepath, mode='wb') as f:
            f.write(r.content)

        cache[request_url] = {
            'content-type': mime_type,
            'download_date': datetime.datetime.now().strftime(STR_DATE_FORMAT_SECONDS),
            'extension': ext_type,
            'local_file': filename,
            'unread': True,
        }

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

        cache[request_url]['unread'] = False
    else:
        logging.debug("Requesting new Text file! {}\n{}".format(request_url, cache))
        r = requests.get(request_url)
        if not r.ok:
            logging.error("Error!: code = {}, reason = {}".format(r.status_code, r.reason), exc_info=True)
            raise Exception("Error: {}, {}!".format(r.status_code, r.reason))

        mime_type = r.headers['content-type']
        ext_type = mimetypes.guess_extension(mime_type) or ''

        filename = "{datetime}{ext}".format(
            datetime=datetime.datetime.now().strftime(STR_DATE_FORMAT_MICROSECONDS),
            ext=ext_type)
        filepath = os.path.join(PATH_ROOT, filename)
        with open(filepath, mode='w', encoding='utf-8') as f:
            f.write(r.text)

        cache[request_url] = {
            'local_file': filename,
            'download_date': datetime.datetime.now().strftime(STR_DATE_FORMAT_SECONDS),
            'content-type': mime_type,
            'extension': ext_type,
            'unread': True,
        }

    return r.text
