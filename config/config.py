import yaml
import os

def load_config():
    base_dir = os.path.dirname(__file__)   # config/
    path = os.path.join(base_dir, "config.yaml")

    with open(path, "r") as f:
        return yaml.safe_load(f)

config = load_config()
