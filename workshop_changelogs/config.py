import json
import os
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


class Config(object):
    def __init__(self):
        self.language = os.getenv("LANG", "en")[:2]
        self.mod_ids = os.getenv("MOD_IDS", _config_from_json("mod_ids", []))
        self.collection_ids = os.getenv(
            "COLLECTION_IDS", _config_from_json("collection_ids", [])
        )
        self.webhook_url = os.getenv(
            "DISCORD_WEBHOOK_URL", _config_from_json("webhook_url")
        )
        self.sleep_interval = int(
            os.getenv(
                "SLEEP_INTERVAL", _config_from_json("sleep_interval", 300)
            )
        )
        self.log_level = os.getenv(
            "LOG_LEVEL", _config_from_json("log_level", "INFO")
        )
        self.requests_timeout = int(
            os.getenv(
                "REQUESTS_TIMEOUT", _config_from_json("requests_timeout", 10)
            )
        )

        if isinstance(self.mod_ids, str):
            self.mod_ids.split(",")
        if isinstance(self.collection_ids, str):
            self.collection_ids.split(",")

        self.cache = _config_from_json("cache", {})

    def write_config(self):
        with open(os.getenv("CONFIG_PATH", "config.json"), "w") as f:
            json.dump(self.__dict__, f)


@lru_cache(maxsize=1)
def get_config() -> Config:
    return Config()


config = get_config()
