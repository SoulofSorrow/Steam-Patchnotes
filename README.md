# Steam Workshop Changelog Monitor
[![de](https://img.shields.io/badge/lang-de-yello)](README.de.md)

This Python script has been developed to monitor changes in Steam Workshop changelogs and send notifications via Discord webhooks when new patch notes are available.

## Functionality

- The script can scan a Steam Workshop Collection page for workshop IDs and extract them.
- It continuously monitors these workshop IDs to detect new patch notes.
- When new patch notes are found, it sends a notification via a Discord webhook.

## Configuration
### Environment Variables
Environment Variables always take priority over JSON config.

See [`.env.SAMPLE`](.env.SAMPLE) for the variable list

### JSON
You can also define a config via JSON. By default, the path is `config.json`, but can be set by
the environment variable `CONFIG_PATH`.

This file's keys should match the variable names listed in [`.env.SAMPLE`](.env.SAMPLE), but in lowercase.
This file is also automatically generated, and will be used to store the cache under the `cache` key.

## Usage
### Docker (Recommended)
[Install Docker](https://www.docker.com/get-started/) (if you haven't already)

#### docker-compose
1. Copy [`.env.SAMPLE`](.env.SAMPLE) to `.env` and fill out the variables
2. Run the following command


    docker-compose up -d

#### docker
Run the following command, filling in your variables (see [`.env.SAMPLE`](.env.SAMPLE) for the list)

    docker run --restart=always -d \
      -e MOD_IDS=id1,id2,id3 \
      -e COLLECTION_IDS=id1,id2,id3 \
      -e DISCORD_WEBHOOK_URL=https://mywebookurl \
      -v ./config.json:/app/config.json \
      ghcr.io/soulofsorrow/steam-patchnotes

### Python
1. Set your environment variables (see [`.env.SAMPLE`](.env.SAMPLE) for the list) or make a `config.json`
with lowercase keys.
2. Run the following command


    git clone https://SoulofSorrow/Steam-Patchnotes.git && \
      cd Steam-Patchnotes && \
      pip install -e .


## Dependencies

- [Requests](https://docs.python-requests.org/en/latest/) - For making HTTP requests to Steam API and Discord Webhook.
- [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/) - For parsing HTML.
- [json](https://docs.python.org/3/library/json.html) - For parsing config and Steam API responses.
- [datetime](https://docs.python.org/3/library/datetime.html) - For processing date and time information.

## Note

Ensure that you comply with Steam usage policies and Discord guidelines when using it.

Feel free to extend and customize the script to meet your requirements.

### Development Setup
Set up a virtual environment for the project

    python -m venv venv
    source venv/bin/activate

Install the development dependencies by running the following command

    pip install -e '.[dev]'

Once this completes, install the `pre-commit` hooks for auto-linting on commit

    pre-commit install

#### Testing
Run tox with no arguments or with the `unittest` environment argument

    tox
    tox -e unittest

#### Linting
Run tox with no arguments or with the `lint` environment argument

    tox
    tox -e lint

#### Docker Development
##### Build
You can build the image by running the following command

    docker build . -f Dockerfile -t ghcr.io/soulofsorrow/steam-patchnotes

##### Debug
You can pop a shell on a built image/existing container, by overriding the entrypoint with `/bin/ash`

    docker run -it --rm --entrypoint=/bin/ash ghcr.io/soulofsorrow/steam-patchnotes  # New container
    docker exec -it container-name /bin/ash  # Running container
