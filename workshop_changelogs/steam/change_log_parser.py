import logging
import re

import requests
from bs4 import BeautifulSoup

from workshop_changelogs.config import config
from workshop_changelogs.i18n.translations import translate as t


logger = logging.getLogger(__name__)


CHANGE_LOG_BASE_URL = (
    "https://steamcommunity.com/sharedfiles/filedetails/changelog"
)


def get_change_log(mod_id: int, timestamp: int | None = None) -> str | None:
    """
    Get a Mod Change Log for a given epoch timestamp.
    If no timestamp is provided, the most recent change log is returned.
    :param mod_id: The Mod ID to get the Change Log for
    :type mod_id: int
    :param timestamp: The epoch timestamp for the update
    :type timestamp: int | None
    :return: The change log
    :rtype: str
    """
    logger.debug(t("Getting Change Log", mod_id))
    resp = requests.get(
        f"{CHANGE_LOG_BASE_URL}/{mod_id}", timeout=config.requests_timeout
    )
    if resp.status_code != 200:
        logger.warning(t("Failed to get Change Log", mod_id))
        return

    logger.debug(t("Received valid response for Change Logs", mod_id))
    logger.debug(resp.text)
    logger.debug(t("Parsing Change Logs", mod_id))
    soup = BeautifulSoup(resp.text, "html.parser")
    if not timestamp:
        timestamp = re.compile(r"(\d+)")
    change_log_element = soup.find("p", id=timestamp)
    if not change_log_element:
        logger.warning(t("Unable to extract change log", mod_id))
        return
    logger.debug(t("Extracted Change Log", mod_id))
    change_log = change_log_element.get_text("\n")
    logger.debug(change_log)
    return change_log
