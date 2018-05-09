import json
import os

config = {}

def load_config():
    global config

    path = 'config'
    os.makedirs(path, exist_ok=True)
    with open(os.path.join(path, 'config.json')) as f:
        config = json.load(f)

load_config()