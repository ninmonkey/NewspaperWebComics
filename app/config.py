import json
import os

comics = {}
config = {}


def load_config():
    global comics
    global config

    path = 'config'
    os.makedirs(path, exist_ok=True)
    with open(os.path.join(path, 'comics.json')) as f:
        comics = json.load(f)

    with open(os.path.join(path, 'config.json')) as f:
        config = json.load(f)

load_config()