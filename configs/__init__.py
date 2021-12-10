from pathlib import Path
from functools import lru_cache

import yaml
from pydantic import parse_obj_as

from .models import Config

CONFIG_DIR = Path(__file__).parent
ROOT_DIR = CONFIG_DIR.parent

CONFIG_FILE = CONFIG_DIR / 'config.yaml'


@lru_cache()
def load_config() -> Config:
    raw_config = yaml.safe_load(CONFIG_FILE.read_text())
    return parse_obj_as(Config, raw_config)


config = load_config()
