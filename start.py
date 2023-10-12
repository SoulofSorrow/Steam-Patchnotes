import requests
from bs4 import BeautifulSoup
import re
import time
import json
from datetime import datetime

# Die URL der Seite, auf der Sie nach den URLs suchen möchten
page_url = "https://steamcommunity.com/sharedfiles/filedetails/?id="

# HTTP-Anfrage, um die Seite abzurufen
response = requests.get(page_url)

if response.status_code == 200:
    # HTML-Parsing mit BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Suchen Sie alle Links auf der Seite
    links = soup.find_all("a", href=True)

    # Extrahieren Sie nur die IDs aus den gefundenen URLs und entfernen Sie Duplikate
    workshop_ids = set()
    for link in links:
        href = link['href']
        match = re.search(r'https://steamcommunity.com/sharedfiles/filedetails/\?id=(\d+)', href)
        if match:
            workshop_id = match.group(1)
            workshop_ids.add(workshop_id)

    # Hier können Sie die Changelog-URLs weiterverarbeiten oder drucken
    for workshop_id in workshop_ids:
        changelog_url = f"https://steamcommunity.com/sharedfiles/filedetails/changelog/{workshop_id}"
        print("Changelog-URL für Workshop-ID", workshop_id, ":", changelog_url)

    # Den regulären Ausdruck für die ID erstellen
    target_id_pattern = r'(\d+)'  # Dieser Regex erlaubt Zahlen von 10 Stellen

    # Discord-Webhook-URL
    discord_webhook_url = '<DISCORD-WEBHOOK>'

    # Funktion zum Auslesen des ersten Eintrags und des Titels
    def get_entry_and_title(url):
        # Eine HTTP-Anfrage an die Website senden
        response = requests.get(url)

        # Den HTML-Inhalt der Website analysieren
        soup = BeautifulSoup(response.text, 'html.parser')

        # Das erste <p>-Element mit passender ID finden
        target_element = soup.find('p', id=re.compile(target_id_pattern))

        # Das Element mit der CSS-Klasse "workshopItemTitle" finden
        title_element = soup.find(class_='workshopItemTitle')

        # Wenn das Element gefunden wurde, den Textinhalt ausgeben
        if target_element:
            entry = target_element.get_text()
            title = title_element.get_text() if title_element else 'Kein Titel gefunden'
            return entry, title
        else:
            return None, None

    # Funktion zum Speichern des Eintrags und des Titels in einer Konfigurationsdatei
    def save_entry_and_title(url, entry, title):
        config = {}
        try:
            with open('config.json', 'r') as config_file:
                config = json.load(config_file)
        except FileNotFoundError:
            pass

        config[url] = {'entry': entry, 'title': title}
        with open('config.json', 'w') as config_file:
            json.dump(config, config_file)

    # Funktion zum Laden der Einträge und Titel aus der Konfigurationsdatei
    def load_entries_and_titles():
        try:
            with open('config.json', 'r') as config_file:
                return json.load(config_file)
        except FileNotFoundError:
            return {}

    # Debug-Modus aktivieren/deaktivieren
    debug_mode = True

    # Debug-Funktion zum Konsolentimer und Debug-Nachrichten
    def debug(message):
        if debug_mode:
            print(f'[DEBUG] {message}')

    while True:
        # Alle Workshop-URLs in der Konfigurationsdatei laden
        saved_entries = load_entries_and_titles()

        for workshop_id in workshop_ids:
            url = f"https://steamcommunity.com/sharedfiles/filedetails/changelog/{workshop_id}"
            last_saved_entry = saved_entries.get(url, {}).get('entry')
            last_saved_title = saved_entries.get(url, {}).get('title')

            # Den aktuellen Eintrag und den Titel abrufen
            current_entry, current_title = get_entry_and_title(url)

            if current_entry:
                # Wenn es einen letzten gespeicherten Eintrag gibt und er sich vom aktuellen Eintrag oder Titel unterscheidet
                if (last_saved_entry != current_entry) or (last_saved_title != current_title):
                    debug(f"Es gibt eine Änderung in {url}:")
                    debug(f'Titel: {current_title}')
                    debug(f'Eintrag: {current_entry}')

                    # Aktuelles Datum und Uhrzeit abrufen
                    current_datetime = datetime.now().strftime("%H:%M:%S %d.%m.%Y")

                    # Discord-Webhook-Nachricht erstellen
                    discord_message = {
                        "username": "Soul's Patchbot",
                        "avatar_url": "https://i.imgur.com/4M34hi2.png",
                        "embeds": [
                            {
                                "title": current_title,
                                "url": url,
                                "description": f"Patch Notes für die: {current_title}",
                                "color": 15258703,
                                "fields": [
                                    {
                                        "name": "News",
                                        "value": f"Datum und Uhrzeit: {current_datetime}\n\n{current_entry}",
                                        "inline": True
                                    }
                                ],
                                "footer": {
                                    "text": "by SoulofSorrow",
                                    "icon_url": "https://i.imgur.com/fKL31aD.jpg"
                                }
                            }
                        ]
                    }

                    # Die Discord-Nachricht an den Webhook senden
                    response = requests.post(discord_webhook_url, json=discord_message)

                    # Hier können Sie die Antwort überprüfen und bei Bedarf Fehlerbehandlung hinzufügen

                    # Den aktuellen Eintrag und Titel in der Konfigurationsdatei speichern
                    save_entry_and_title(url, current_entry, current_title)

        # Warten Sie 5 Minuten, bevor Sie erneut überprüfen
        time.sleep(300)

else:
    print("Fehler beim Abrufen der Seite.")
