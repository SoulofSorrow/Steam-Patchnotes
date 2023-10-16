import logging
from time import sleep

from workshop_changelogs.config import config
from workshop_changelogs.discord.webhook import send_discord_message
from workshop_changelogs.i18n.translations import translate as t
from workshop_changelogs.steam.api_client import (
    get_mod_info,
    get_mod_info_from_collection,
)
from workshop_changelogs.steam.change_log_parser import get_change_log


logger = logging.getLogger(__name__)


def _run():
    mod_info = get_mod_info(config.mod_ids)
    collection_mod_info = get_mod_info_from_collection(config.collection_ids)
    # Ensure we have lists to concat
    mod_info = mod_info if mod_info else []
    collection_mod_info = collection_mod_info if collection_mod_info else []

    # Store if this is the installing run, as it gets invalidated on first mod
    # info added to cache.
    first_install = config.first_install

    # Iterate over infos
    for info in mod_info + collection_mod_info:
        if not info["result"]:
            logger.warning(
                t(
                    "Mod returned non-zero result",
                    info["publishedfileid"],
                    info["result"],
                )
            )
            continue

        if info["publishedfileid"] not in config.cache:
            logger.info(t("Adding info for Mod ID", info["publishedfileid"]))
            config.cache[info["publishedfileid"]] = info["time_updated"]

        if (
            config.cache[info["publishedfileid"]] != info["time_updated"]
            or (config.send_on_startup and not config.started)
            or (config.send_on_install and first_install)
        ):
            logger.info(
                t("Mod updated", info["publishedfileid"], info["title"])
            )
            send_discord_message(
                info["publishedfileid"],
                info["time_updated"],
                info["title"],
                get_change_log(info["publishedfileid"]),
            )
            config.cache[info["publishedfileid"]] = info["time_updated"]
    config.started = True
    config.write_config()


def run():
    logger.info(t("Starting"))
    while True:
        _run()
        logger.info(t("Sleep", config.sleep_interval))
        sleep(config.sleep_interval)


def root_run():
    _logger = logging.getLogger()
    _logger.addHandler(logging.StreamHandler())
    _logger.setLevel(config.log_level)
    _logger.propagate = True
    run()


if __name__ == "__main__":
    root_run()
