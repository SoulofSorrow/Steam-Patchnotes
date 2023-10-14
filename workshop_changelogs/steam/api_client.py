import json
import logging
from enum import Enum

import requests

from workshop_changelogs.config import config
from workshop_changelogs.i18n.translations import translate as t


logger = logging.getLogger(__name__)

API_BASE_URL = "https://api.steampowered.com/ISteamRemoteStorage"


class RequestType(Enum):
    MOD = "/GetPublishedFileDetails"
    COLLECTION = "/GetCollectionDetails"


def _client(
    ids: int | list[int], request_type: RequestType
) -> list[dict] | None:
    """
    Basic Steam API Client for getting Mod/Collection info
    :param ids: Mod/Collection IDs (must be Mod or Collection in a single list,
    not a mixed list)
    :type ids: int | list[int]
    :param request_type: The type of ids in the list,
    either RequestType.MOD or RequestType.COLLECTION
    :type request_type: RequestType
    :return: The items' info. Returns None if error
    :rtype: list[dict]
    """
    # Ensure we have a list
    if not isinstance(ids, list):
        logger.warning(t("Received a single int", ids))
        ids = [ids]

    # Build request body and make request
    item_count = len(ids)
    if not item_count:
        logger.debug(t("Passed in no IDs for Steam API"))
        return
    logger.debug(t("Getting Steam API info", item_count))
    item_key = "itemcount"
    pop_key = "publishedfiledetails"
    if request_type == RequestType.COLLECTION:
        # Swap keys for collections
        item_key = "collectioncount"
        pop_key = "collectiondetails"
    data = {item_key: item_count}
    for index, _id in enumerate(ids):
        logger.debug(t("Adding ID to query", index, _id))
        data[f"publishedfileids[{index}]"] = _id
    logger.debug(t("Making Steam API Request"))
    logger.debug(f"{API_BASE_URL}{request_type.value}/v1/")
    resp = requests.post(
        f"{API_BASE_URL}{request_type.value}/v1/",
        data=data,
        timeout=config.requests_timeout,
    )

    # Parse response
    logger.debug(t("Steam API Response status code", resp.status_code))
    if resp.status_code != 200:
        # Non-200 status code
        logger.warning(t("Unable to retrieve data from Steam"))
        return

    # Pop out the data we care about
    data = resp.json()
    logger.debug(json.dumps(data, indent=4))
    return data["response"][pop_key]


def get_mod_info(mod_ids: int | list[int]) -> list[dict] | None:
    """
    Get Mod Info from Steam API
    :param mod_ids: A List of mod IDs to get info for
    :type mod_ids: int | list[int]
    :return: The mod infos. Returns None if error
    :rtype: dict | None
    """
    return _client(mod_ids, RequestType.MOD)


def get_mod_info_from_collection(
    collection_ids: int | list[int],
) -> list[int] | None:
    """
    Get Mod infos from a Collection
    :param collection_ids: A list of collection IDs to get mod infos for
    :type collection_ids: int | list[int]
    :return: The mod infos. Returns None if error
    :rtype: dict | None
    """
    # Get Mod IDs from Collection
    data = _client(collection_ids, RequestType.COLLECTION)
    if data is None:
        # We received no info (could be no IDs were passed)
        return

    # We could do a massive list comprehension, but let's make it simple
    mod_ids = []
    for collection in data:
        if not collection["result"]:
            # Invalid collection or has no IDs
            continue
        mod_ids += [mod["publishedfileid"] for mod in collection["children"]]

    # Go get mod info
    return _client(mod_ids, RequestType.MOD)
