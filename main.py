import logging
import os
import random
import time
import threading

from app import cache
from app import config
from app import view
from app.app_locals import (
    ComicListThreaded,
    humanize_bytes,
)
from app.comics import fetch_comics_multiple

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
LOGGING_DIR = os.path.join(ROOT_DIR, 'logs')
os.makedirs(LOGGING_DIR, exist_ok=True)

logging.getLogger("chardet").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.basicConfig(
    handlers=[logging.FileHandler(os.path.join(LOGGING_DIR, 'main.log'), 'w', 'utf-8')],
    level=logging.ERROR)

cache.init(os.path.join(ROOT_DIR, 'cache'))
comic_list_threaded = ComicListThreaded()


def main_sync(count=3):
    comics = []
    print("main sync, count = {}".format(count))
    for name in config.comics:
        comic_list = fetch_comics_multiple(config.comics[name], name, count)
        if comic_list:
            comics.append(comic_list)

    if config.config["randomize_comics"]:
        random.shuffle(comics)

    html = view.render(comics)
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)

    cache.write_config()

    print(comics)
    print("Done. Sync.")


def work(config_name, name, count=2):
    global comic_list_threaded

    fetched = fetch_comics_multiple(config_name, name, count)
    comic_list_threaded.add(fetched)


def main_threaded(count=3):
    threads = []

    print("main_threaded. count = {}".format(count))

    for name in config.comics:
        t = threading.Thread(target=work,args=(config.comics[name], name, count))
        threads.append(t)
        t.start()

    main_thread = threading.main_thread()
    for t in threading.enumerate():
        if t is main_thread:
            continue

        t.join()

    if config.config["randomize_comics"]:
        random.shuffle(comic_list_threaded.comics)

    html = view.render(comic_list_threaded.comics)
    cache.write_config()
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)

    print("Done. Threaded")


if __name__ == "__main__":
    t_start = time.time()

    # main_sync(count=1)
    main_threaded(count=3)

    t_end = time.time()
    print("Time: {:.3f} seconds".format((t_end - t_start)))

    cache.cache_delete_stale()
    cache_bytes = humanize_bytes(cache.cache_usage())
    print("Cache: {0}".format(cache_bytes))

    if config.config["auto_open_browser"]:
        print("auto open browser: NYI")

