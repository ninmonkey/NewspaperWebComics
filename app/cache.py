import datetime
import json
import logging
import mimetypes
import os
import time
import urllib3
import threading

import requests

from app.str_const import(
    STR_DATE_FORMAT_MICROSECONDS,
    STR_DATE_FORMAT_SECONDS,
)
from app.app_locals import humanize_bytes

cache = {}
DOWNLOAD_DELAY_TIME = 0.4    # 0 to disable. Time in seconds.
MAX_DISK_USAGE = 200 * 1024 * 1024  # 200 Mb
PATH_CACHE = ''
DEFAULT_EXPIRE_HTML = datetime.timedelta(days=1)
DEFAULT_EXPIRE_BINARY = datetime.timedelta(days=15)
logging = logging.getLogger(__name__)


def init(path_cache, delay=None):
    global PATH_CACHE
    global cache
    global DOWNLOAD_DELAY_TIME

    if delay is not None:
        DOWNLOAD_DELAY_TIME = delay

    PATH_CACHE = path_cache
    os.makedirs(PATH_CACHE, exist_ok=True)
    cache = read_config()


def clear():
    # empty cache
    global cache

    logging.info("clearing cache")
    for file in os.listdir(PATH_CACHE):
        full_path = os.path.join(PATH_CACHE, file)
        if os.path.isfile(full_path):
            os.remove(full_path)

    cache = {}
    write_config()


def cache_usage():
    total_bytes = 0
    for name in cache:
        total_bytes += cache[name]['bytes']

    return total_bytes


def cache_delete_stale(size=MAX_DISK_USAGE):
    # delete oldest files first
    global cache

    compared = []
    for url in cache:
        compared.append({
            'url': url,
            'download_date': cache[url]['download_date'],
            'local_file': cache[url]['local_file'],
        })

    cache_by_age = sorted(compared, key=lambda x: x["download_date"])

    if cache_usage() >= size:
        print("Cache over limit: max = {}".format(humanize_bytes(size)))
        logging.info("Cache over limit: max = {}".format(humanize_bytes(size)))

    while cache_usage() >= size:
        if len(cache_by_age) == 0:
            break

        cur = cache_by_age[0]
        remove_cached_url(cur['url'])
        del cache_by_age[0]

    write_config()


def cache_is_expired(request_url, expire_timedelta):
    if request_url in cache:
        now = datetime.datetime.now()
        date_downloaded = datetime.datetime.strptime(cache[request_url]['download_date'], STR_DATE_FORMAT_SECONDS)
        use_cache = now - date_downloaded <= expire_timedelta
        return not use_cache
    else:
        return True


def read_config():
    global cache

    json_path = os.path.join(PATH_CACHE, 'cache.json')

    if not os.path.exists(json_path):
        write_config()

    try:
        with open(json_path, mode='r', encoding='utf-8') as f:
            cache = json.load(f)
    except (ValueError):
        cache = {}

    return cache


def write_config():
    json_path = os.path.join(PATH_CACHE, 'cache.json')
    with open(json_path, mode='w', encoding='utf-8') as f:
        json.dump(cache, f, indent=4, sort_keys=True)


def remove_cached_url(request_url):
    # cleanup cache.json and remove cached file
    global cache

    if request_url in cache:
        old_file = cache[request_url].get('local_file')
        if old_file:
            old_path = os.path.join(PATH_CACHE, old_file)
            print("deleting: {}".format(old_path))
            logging.info("deleting: {}".format(old_path))
            if os.path.isfile(old_path):
                os.remove(old_path)

        del cache[request_url]


def _request_cached(request_url, text=True, expire_time=DEFAULT_EXPIRE_HTML):
     # requests.get() but cached, and returns: request.text else file name
    global cache

    if not cache_is_expired(request_url, expire_time):
        if text:
            logging.debug("cached Text file: {}".format(request_url))
            print("cached Text file: {}".format(request_url))
            file = cache[request_url]['local_file']
            filepath = os.path.join(PATH_CACHE, file)
            # cache[request_url]['unread'] = False

            with open(filepath, mode='r', encoding='utf8') as f:
                return f.read()
        else:
            logging.info("cached Binary file: {}".format(request_url))
            print("cached Binary file: {}".format(request_url))
            file = cache[request_url]['local_file']
            # cache[request_url]['unread'] = False

            return os.path.join('cache', file)
    else:
        remove_cached_url(request_url)

        print(request_url)
        if text:
            logging.info("Requesting new Text file! {}".format(request_url))
            print("Requesting new Text file! {}".format(request_url))
        else:
            logging.info("Requesting new Binary file! {}".format(request_url))
            print("Requesting new Binary file! {}".format(request_url))

        r = None
        try:
            r = requests.get(request_url)
        except (requests.exceptions.ConnectionError,
                urllib3.exceptions.NewConnectionError,
                requests.exceptions.ConnectionError):
            logging.error("Exception!: Probably a typo in url = {url}".format(url=request_url), exc_info=True)

        # if r is None:
        #     logging.error("Error!: not r! Probably a typo in url = {url}".format(url=request_url))#, exc_info=True)
        #     print("Error! not r! No response for url = {}.\n! Check url for typos. !".format(request_url))
        #     return None
            # raise Exception("Error!: Probably a typo in url = {url}".format(url=request_url))

        if not r.ok:
            logging.error("Error!: not r.ok! code = {code}, reason = {reason}, url = {url}".format(
                code=r.status_code, reason=r.reason, url=r.url))
            print("Error!: not r.ok! code = {code}, reason = {reason}, url = {url}".format(
                code=r.status_code, reason=r.reason, url=r.url))  # , exc_info=True)
            return None
            # raise Exception("Error: {}, {}!".format(r.status_code, r.reason))

        time.sleep(DOWNLOAD_DELAY_TIME)

        mime_type = r.headers['content-type']
        ext_type = mimetypes.guess_extension(mime_type) or ''

        file = "{datetime}{ext}".format(
            datetime=datetime.datetime.now().strftime(STR_DATE_FORMAT_MICROSECONDS),
            ext=ext_type)
        path = os.path.join(PATH_CACHE, file)

        if text:
            with open(path, mode='w', encoding="utf8") as f:
                f.write(r.text)
        else:
            with open(path, mode='wb') as f:
                f.write(r.content)

        statinfo = os.stat(path)

        cache[request_url] = {
            'local_file': file,
            'download_date': datetime.datetime.now().strftime(STR_DATE_FORMAT_SECONDS),
            'content-type': mime_type,
            'extension': ext_type,
            'bytes': statinfo.st_size,
            # 'unread': True,
        }

        if text:
            return r.text
        else:
            return os.path.join('cache', file)


def request_cached_binary(request_url):
    # requests.get() but cached, binary, returns: filename
    return _request_cached(request_url, text=False, expire_time=DEFAULT_EXPIRE_BINARY)


def request_cached_text(request_url):
    # requests.get() but cached, and returns: request text
    return _request_cached(request_url, text=True, expire_time=DEFAULT_EXPIRE_HTML)

