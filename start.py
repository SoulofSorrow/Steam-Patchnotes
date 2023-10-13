import requests
from bs4 import BeautifulSoup
import re
import time
import json
from datetime import datetime

# The URL of the page where you want to search for URLs/ Steam Workshop Collection URL
page_url = "https://steamcommunity.com/sharedfiles/filedetails/?id="

# HTTP request to retrieve the page
response = requests.get(page_url)

if response.status_code == 200:
    # HTML parsing with BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all links on the page
    links = soup.find_all("a", href=True)

    # Extract only the IDs from the found URLs and remove duplicates
    workshop_ids = set()
    for link in links:
        href = link['href']
        match = re.search(r'https://steamcommunity.com/sharedfiles/filedetails/\?id=(\d+)', href)
        if match:
            workshop_id = match.group(1)
            workshop_ids.add(workshop_id)

    # You can further process or print the changelog URLs here
    for workshop_id in workshop_ids:
        changelog_url = f"https://steamcommunity.com/sharedfiles/filedetails/changelog/{workshop_id}"
        print("Changelog URL for Workshop ID", workshop_id, ":", changelog_url)

    # Create the regular expression pattern for the ID
    target_id_pattern = r'(\d+)'  # This regex allows 10-digit numbers

    # Discord webhook URL
    discord_webhook_url = '<DISCORD-WEBHOOK>'

    # Function to fetch the first entry and title
    def get_entry_and_title(url):
        # Send an HTTP request to the website
        response = requests.get(url)

        # Parse the HTML content of the website
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the first <p> element with a matching ID
        target_element = soup.find('p', id=re.compile(target_id_pattern))

        # Find the element with the CSS class "workshopItemTitle"
        title_element = soup.find(class_='workshopItemTitle')

        # If the element is found, output the text content
        if target_element:
            entry = target_element.get_text()
            title = title_element.get_text() if title_element else 'No title found'
            return entry, title
        else:
            return None, None

    # Function to save the entry and title in a configuration file
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

    # Function to load entries and titles from the configuration file
    def load_entries_and_titles():
        try:
            with open('config.json', 'r') as config_file:
                return json.load(config_file)
        except FileNotFoundError:
            return {}

    # Enable/disable debug mode
    debug_mode = True

    # Debug function for console timing and debug messages
    def debug(message):
        if debug_mode:
            print(f'[DEBUG] {message}')

    while True:
        # Load all workshop URLs from the configuration file
        saved_entries = load_entries_and_titles()

        for workshop_id in workshop_ids:
            url = f"https://steamcommunity.com/sharedfiles/filedetails/changelog/{workshop_id}"
            last_saved_entry = saved_entries.get(url, {}).get('entry')
            last_saved_title = saved_entries.get(url, {}).get('title')

            # Fetch the current entry and title
            current_entry, current_title = get_entry_and_title(url)

            if current_entry:
                # If there's a last saved entry and it's different from the current entry or title
                if (last_saved_entry != current_entry) or (last_saved_title != current_title):
                    debug(f"There is a change in {url}:")
                    debug(f'Title: {current_title}')
                    debug(f'Entry: {current_entry}')

                    # Get the current date and time
                    current_datetime = datetime.now().strftime("%H:%M:%S %d.%m.%Y")

                    # Create a Discord webhook message
                    discord_message = {
                        "username": "Soul's Patchbot",
                        "avatar_url": "https://i.imgur.com/4M34hi2.png",
                        "embeds": [
                            {
                                "title": current_title,
                                "url": url,
                                "description": f"Patch Notes for: {current_title}",
                                "color": 15258703,
                                "fields": [
                                    {
                                        "name": "News",
                                        "value": f"Date and Time: {current_datetime}\n\n{current_entry}",
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

                    # Send the Discord message to the webhook
                    response = requests.post(discord_webhook_url, json=discord_message)

                    # You can check the response here and add error handling if needed

                    # Save the current entry and title in the configuration file
                    save_entry_and_title(url, current_entry, current_title)

        # Wait for 5 minutes before checking again
        time.sleep(300)

else:
    print("Error retrieving the page.")
