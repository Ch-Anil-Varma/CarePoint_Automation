import json
import os

def load_config():
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config", "config.json")
    with open(config_path, "r", encoding="utf-8") as file:
        return json.load(file)