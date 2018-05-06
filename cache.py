import os

import requests
# 'date_cached': datetime.datetime.now(),

cache = {
    'https://xkcd.com/1912/': {
        'request_url': 'https://xkcd.com/1912/',
        'local_file': '1.html',
    },
}

path_root = 'C:\\Users\\cppmo_000\\Documents\\2018\\NewspaperWebComics\\cache'

def cache_read_config(cache):
    raise NotImplementedErrror('write cache JSON')

def cache_write_config(cache_json):
    # cache = json.load(json)
    raise NotImplementedErrror('read cache JSON')

def request_cached(request_url):
    # save url/read from cache

    if request_url in cache:
        file = cache[request_url]['local_file']
        file_path = os.path.join(path_root, file)
        with open(file_path, mode='r', encoding='utf8') as f:
            return f.read()
    else:

        r = requests.get(request_url)
        if not r.ok:
            raise Exception("Error: {}, {}!".format(r.status_code, r.reason))

        file = '2.html'
        file_path = os.path.join(path_root, file)
        with open(file_path, mode='w', encoding='utf-8') as f:
            f.write(r.text)

        print("""
fetch: {url},
local_file: {local_file},
        """.format(url=request_url, local_file=file))

'''
>>> pc = os.path.normpath('C:\\Users\\cppmo_000\\Documents\\2018\\New folder\\cache', '1.html')
'''