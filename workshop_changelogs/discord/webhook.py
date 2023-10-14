import logging
from datetime import datetime

import requests

from workshop_changelogs.config import config
from workshop_changelogs.i18n.translations import translate as t
from workshop_changelogs.steam.change_log_parser import CHANGE_LOG_BASE_URL


logger = logging.getLogger(__name__)


def send_discord_message(
    mod_id: int, update_timestamp: int, mod_title: str, change_log: str
) -> int:
    logger.info(t("Sending message", mod_id, mod_title))
    timestamp = datetime.fromtimestamp(update_timestamp)
    message = {
        "username": "Soul's Patchbot",
        "avatar_url": "https://i.imgur.com/4M34hi2.png",
        "embeds": [
            {
                "title": mod_title,
                "url": f"{CHANGE_LOG_BASE_URL}/{mod_id}",
                "description": t("Discord description", mod_title),
                "color": 15258703,
                "fields": [
                    {
                        "name": "News",
                        "value": t(
                            "Discord message",
                            timestamp.strftime("%H:%M:%S %d.%m.%Y"),
                            change_log,
                        ),
                        "inline": True,
                    }
                ],
                "footer": {
                    "text": "by SoulofSorrow",
                    "icon_url": "https://i.imgur.com/fKL31aD.jpg",
                },
            }
        ],
    }
    resp = requests.post(
        config.webhook_url, json=message, timeout=config.requests_timeout
    )
    logger.debug(t("Message sent debug", resp.status_code))
    logger.info(t("Message sent", mod_id, mod_title))
    return resp.status_code
