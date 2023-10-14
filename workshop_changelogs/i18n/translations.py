# ruff: noqa: E501
import logging

from workshop_changelogs.config import config


logger = logging.getLogger(__name__)


EN_MESSAGES = {
    "Starting": "Starting Mod Change Log detector...",
    "Sleep": "Sleep for {} seconds...",
    "Mod returned non-zero result": "Mod ID {} returned a non-zero result: {}",
    "Adding info for Mod ID": "Adding info for Mod ID {}",
    "Mod updated": "{}:{} has updated!",
    "Sending message": "Sending Discord message for {}:{}...",
    "Message sent debug": "Discord message send status code: {}",
    "Message sent": "Discord message sent for {}:{}",
    "Discord description": "Patch Notes for: {}",
    "Discord message": "Date and Time: {} UTC\n\n{}",
    "Getting Change Log": "Failed to get Change Log for Mod ID: {}",
    "Failed to get Change Log": "Failed to get Change Log for Mod ID: {}",
    "Received valid response for Change Logs": "Received valid response for Change Logs for Mod ID {}",
    "Parsing Change Logs": "Parsing Change Logs for Mod ID {}...",
    "Unable to extract change log": "Unable to extract change log for Mod ID: {}",
    "Extracted Change Log": "Extracted Change Log for Mod ID: {}",
    "Received a single int": "Received a single int for ID ({}), consider passing a list next time",
    "Passed in no IDs for Steam API": "Passed in no IDs for Steam API. Aborting.",
    "Getting Steam API info": "Getting Steam API info for {} items...",
    "Adding ID to query": "Adding #{} ID to query: {}",
    "Making Steam API Request": "Making Steam API Request...",
    "Steam API Response status code": "Steam API Response status code: {}",
    "Unable to retrieve data from Steam": "Unable to retrieve data from Steam!",
}

# Translated by ChatGPT
DE_MESSAGES = {
    "Starting": "Starte Mod-Änderungsprotokoll-Detektor...",
    "Sleep": "Warte {} Sekunden...",
    "Mod returned non-zero result": "Mod ID {} lieferte ein nicht-null Ergebnis: {}",
    "Adding info for Mod ID": "Füge Informationen für Mod ID {} hinzu",
    "Mod updated": "{}:{} wurde aktualisiert!",
    "Sending message": "Sende Discord-Nachricht für {}:{}...",
    "Message sent debug": "Discord-Nachricht Sendestatuscode: {}",
    "Message sent": "Discord-Nachricht gesendet für {}:{}",
    "Discord description": "Patch Notes für die: {}",
    "Discord message": "Datum und Uhrzeit: {} UTC\n\n{}",
    "Getting Change Log": "Fehler beim Abrufen des Änderungsprotokolls für Mod ID: {}",
    "Failed to get Change Log": "Fehler beim Abrufen des Änderungsprotokolls für Mod ID: {}",
    "Received valid response for Change Logs": "Gültige Antwort für Änderungsprotokolle für Mod ID {} erhalten",
    "Parsing Change Logs": "Parse Änderungsprotokolle für Mod ID {}...",
    "Unable to extract change log": "Kann Änderungsprotokoll für Mod ID: {} nicht extrahieren",
    "Extracted Change Log": "Änderungsprotokoll extrahiert für Mod ID: {}",
    "Received a single int": "Einzelne Ganzzahl für ID ({}) erhalten, erwägen Sie das nächste Mal eine Liste zu übergeben",
    "Passed in no IDs for Steam API": "Keine IDs für Steam API übergeben. Abbruch.",
    "Getting Steam API info": "Hole Steam API-Informationen für {} Elemente...",
    "Adding ID to query": "Füge #{} ID zur Abfrage hinzu: {}",
    "Making Steam API Request": "Stelle Steam API-Anfrage...",
    "Steam API Response status code": "Steam API-Antwortstatuscode: {}",
    "Unable to retrieve data from Steam": "Daten können nicht von Steam abgerufen werden!",
}

MESSAGES = {
    "en": EN_MESSAGES,
    "de": DE_MESSAGES,
}

if list(MESSAGES["en"].keys()) != list(MESSAGES["de"].keys()):
    logger.warning("Translation keys do not match! This can cause a crash!!!")


def translate(message_id: str, *args):
    message = MESSAGES[config.language][message_id]
    if args:
        return message.format(*args)
    return message
