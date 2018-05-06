import os
# 'date_cached': datetime.datetime.now(),

cache = {
    "https://xkcd.com/1912/": {
        'request_url': 'https://xkcd.com/1912/',
        'local_file': '1.html',
    },
}

def cache_read_config(cache):
    raise NotImplementedErrror('write cache JSON')

def cache_write_config(cache_json):
    # cache = json.load(json)
    raise NotImplementedErrror('read cache JSON')

def request_cached(request_url):
    # save url/read from cache
    path = os.path.join('C:\\Users\\cppmo_000\\Documents\\2018\\NewspaperWebComics\\cache', '1.html')
    f = open(path, mode='r', encoding='utf8')
    return f.read()

    if request_url in cache:
        raise Exception("read file from disk")
        # return cache[request_url]
    else:
        raise NotImplementedError('not exists so download it')

"""
>>> pc = os.path.normpath('C:\\Users\\cppmo_000\\Documents\\2018\\New folder\\cache', '1.html')
"""