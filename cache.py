import os
import json

import requests
# 'date_cached': datetime.datetime.now(),
# todo: check if html expired, expecially on front page. maybe not on foo.com/comic/<id>

cache = {}
path_root = ''

def init_cache():
    os.makedirs(path_root, exist_ok=True)
    cache = cache_read_config()

def cache_read_config():
    global cache
    # todo: create if not existing
    json_path = os.path.join(path_root, 'cache.json')

    if not os.path.exists(json_path):
        cache_write_config(cache)

    with open(json_path, mode='r', encoding='utf-8') as f:
        cache = json.load(f)

    return cache

def cache_write_config(cache):
    json_path = os.path.join(path_root, 'cache.json')
    with open(json_path, mode='w', encoding='utf-8') as f:
        json.dump(cache, f, indent=4, sort_keys=True)

def request_cached(request_url):

    # save url/read from cache
    if request_url in cache:
        print("cached file")
        file = cache[request_url]['local_file']
        file_path = os.path.join(path_root, file)
        with open(file_path, mode='r', encoding='utf8') as f:
            return f.read()
    else:
        print("Requesting new file!")
        print(cache)
        # raise Exception("disabled real downloads")
        r = requests.get(request_url)
        if not r.ok:
            raise Exception("Error: {}, {}!".format(r.status_code, r.reason))

        file = '2.html'
        file_path = os.path.join(path_root, file)
        with open(file_path, mode='w', encoding='utf-8') as f:
            f.write(r.text)

        cache[request_url] = {'local_file': file,}


#         print("""
# fetch: {url},
# local_file: {local_file},
#         """.format(url=request_url, local_file=file))

    cache_write_config(cache)
    return r.text
'''
>>> pc = os.path.normpath('C:\\Users\\cppmo_000\\Documents\\2018\\New folder\\cache', '1.html')
'''