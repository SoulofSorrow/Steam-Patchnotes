# Steam Workshop Changelog Monitor

Dieses Python-Skript wurde entwickelt, um Änderungen in Steam Workshop-Changelogs zu überwachen und Benachrichtigungen über Discord-Webhooks zu senden, wenn neue Patch Notes verfügbar sind.

## Funktionalität

- Das Skript durchsucht eine Steam Workshop-Seite nach Workshop-IDs und extrahiert sie.
- Es überwacht dann kontinuierlich die Workshop-IDs, um nach neuen Patch Notes zu suchen.
- Wenn neue Patch Notes gefunden werden, sendet es eine Benachrichtigung über einen Discord-Webhook.

## Verwendung

1. Setzen Sie die URL der Steam Workshop-Seite, die Sie überwachen möchten, in der `page_url` Variable.
2. Legen Sie die Discord-Webhook-URL in der `discord_webhook_url` Variable fest.
3. Führen Sie das Skript aus und es wird Änderungen in den Patch Notes überwachen und Benachrichtigungen senden.

## Abhängigkeiten

- [Requests](https://docs.python-requests.org/en/latest/) - Für HTTP-Anfragen.
- [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/) - Für das Parsen von HTML.
- [json](https://docs.python.org/3/library/json.html) - Zum Lesen und Schreiben von Konfigurationsdaten.
- [datetime](https://docs.python.org/3/library/datetime.html) - Zur Verarbeitung von Datums- und Uhrzeitinformationen.

## Konfiguration

- Das Skript speichert die letzten gesehenen Patch Notes in einer Konfigurationsdatei namens `config.json`. Sie können die Konfigurationsdatei nach Ihren Wünschen anpassen.

## Hinweis

Dieses Skript wurde zu Demonstrationszwecken erstellt und sollte mit Vorsicht verwendet werden. Stellen Sie sicher, dass Sie die Einhaltung der Steam-Nutzungsrichtlinien und der Discord-Richtlinien beachten, wenn Sie es verwenden.

Fühlen Sie sich frei, das Skript zu erweitern und anzupassen, um Ihren Anforderungen gerecht zu werden.
