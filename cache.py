from datetime import datetime
import os
import json

import requests
# 'date_cached': datetime.datetime.now(),
# todo: check if html expired, expecially on front page. maybe not on foo.com/comic/<id>

cache = {}
PATH_ROOT = ''

def init_cache(path_cache):
    global PATH_ROOT

    PATH_ROOT = path_cache
    os.makedirs(PATH_ROOT, exist_ok=True)
    print("Cache: {}".format(path_cache))
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
    global cache

    # save url/read from cache
    if request_url in cache:
        print("cached file")
        file = cache[request_url]['local_file']
        file_path = os.path.join(PATH_ROOT, file)
        with open(file_path, mode='r', encoding='utf8') as f:
            return f.read()
    else:
        print("Requesting new file!")
        print(cache)
        # raise Exception("disabled real downloads")
        r = requests.get(request_url)
        if not r.ok:
            raise Exception("Error: {}, {}!".format(r.status_code, r.reason))

        # FILENAME
        filename = "{datetime}.html".format(datetime=datetime.now().strftime("%Y %m %d - %H %M %S %f"))
        file_path = os.path.join(PATH_ROOT, filename)
        with open(file_path, mode='w', encoding='utf-8') as f:
            f.write(r.text)

        cache[request_url] = {'local_file': filename,}

    cache_write_config(cache)
    return r.text
'''
>>> pc = os.path.normpath('C:\\Users\\cppmo_000\\Documents\\2018\\New folder\\cache', '1.html')
'''