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
)
from app.comics import fetch_comics_multiple

ALWAYS_RANDOM = False
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
LOGGING_DIR = os.path.join(ROOT_DIR, 'logs')
os.makedirs(LOGGING_DIR, exist_ok=True)

logging.getLogger("chardet").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.basicConfig(
    handlers=[logging.FileHandler(os.path.join(LOGGING_DIR, 'main.log'), 'w', 'utf-8')],
    level=logging.WARNING)

cache.init(os.path.join(ROOT_DIR, 'cache'))
comic_list_threaded = ComicListThreaded()


def main_sync(count=3):
    comics = []
    print("main sync")
    for name in config.config:
        comic_list = fetch_comics_multiple(config.config[name], name, count)
        if comic_list:
            comics.append(comic_list)

    if ALWAYS_RANDOM:
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


def main_threaded():
    # url_list = UrlListThreaded()
    threads = []
    count = 2

    print("main_threaded")

    for name in config.config:
        t = threading.Thread(target=work,args=(config.config[name], name, count))
        threads.append(t)
        t.start()

    main_thread = threading.main_thread()
    for t in threading.enumerate():
        if t is main_thread:
            continue

        logging.debug("Joining {}".format(t.getName()))
        t.join()

    if ALWAYS_RANDOM:
        random.shuffle(comic_list_threaded.comics)

    html = view.render(comic_list_threaded.comics)
    cache.write_config()
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)

    print("Done. Threaded")


if __name__ == "__main__":
    t_start = time.time()
    # main_sync()
    main_threaded()
    t_end = time.time()
    print("Time: {} seconds".format((t_end - t_start)))
