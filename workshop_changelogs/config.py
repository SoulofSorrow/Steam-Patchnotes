import json
import os
from dataclasses import dataclass
from functools import lru_cache


@lru_cache(maxsize=1)
def _load_json(path: str = "config.json") -> dict | None:
    if not os.path.isfile(path):
        return
    try:
        with open(path) as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return


def _config_from_json(key: str, default=None):
    json_config = _load_json(os.getenv("CONFIG_PATH", "config.json"))
    if json_config is None:
        return default
    return json_config.get(key, default)


@dataclass
class Config:
    language = os.getenv("LANG", "en")[:2]
    mod_ids = os.getenv("MOD_IDS", _config_from_json("mod_ids", []))
    collection_ids = os.getenv(
        "COLLECTION_IDS", _config_from_json("collection_ids", [])
    )
    webhook_url = os.getenv(
        "DISCORD_WEBHOOK_URL", _config_from_json("webhook_url")
    )
    sleep_interval = int(
        os.getenv("SLEEP_INTERVAL", _config_from_json("sleep_interval", 300))
    )
    log_level = os.getenv("LOG_LEVEL", _config_from_json("log_level", "INFO"))
    requests_timeout = int(
        os.getenv(
            "REQUESTS_TIMEOUT", _config_from_json("requests_timeout", 10)
        )
    )
    cache = _config_from_json("cache", {})

    if isinstance(mod_ids, str):
        mod_ids = mod_ids.split(",")
    if isinstance(collection_ids, str):
        collection_ids = collection_ids.split(",")

    def write_config(self):
        with open(os.getenv("CONFIG_PATH", "config.json"), "w") as f:
            json.dump(self.__dict__, f)


@lru_cache(maxsize=1)
def get_config() -> Config:
    return Config()


config = get_config()
