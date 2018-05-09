import json
import os

config = {}

def load_config():
    global config

    path = os.path.join('config', 'config.json')
    with open(path) as f:
        config = json.load(f)

load_config()