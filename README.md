# Telegram Docker Bot
telegram-docker-bot is a minimal Telegram bot for Docker moderation, The bot interacts with Telegram via a bot token and can help automate or moderate Docker-related activities using configurable text responses.

## Features
- Monitor your Docker containers, images and volumes in Telegram
- Start & stop your Docker containers.
- Simple configurable settings and texts via YAML

## Requirements
- Python 3.12 (or later versions)
- Docker installed and available

## Configurations
> [!NOTE]
> 
> The only required change in the config files is the Telegram bot token.

| Filename   | Description                                  |
|------------|----------------------------------------------|
| config.yml | Basic bot settings (Including **BOT TOKEN**) |
| texts.yml  | Bot texts and responses                      |
| config.py  | Loads and performs the configurations        |

## Quick Start
1. Clone the repository
```shell
git clone https://github.com/MohammadHosseinGhorbani/telegram-docker-bot
```
2. Install the requirement libraries
```shell
pip install -r requirements.txt
```
3. Set your bot token in config.yml.example and rename it to config.yml
4. Run the program in the source directory.
```shell
cd source
python main.py
```
## Run with Docker (DIND - Unrecommended)
> [!CAUTION]
> Unsafe
> 
> 
> To run the project with Docker, the host machine's docker sock will be mounted to the container. So It will be exposed and unsecure. Proceed with caution and awareness.

Clone the config.yml.example file, edit the variables and rename the file to config.yml
### `docker run` command
```shell
docker run -d --name telegram-docker-bot \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v $(pwd)/config.yml:/config.yml \
  msghorbani27/telegram-docker-bot:latest
```
### docker compose file
```yaml
version: '3.8'

services:
  telegram-docker-bot:
    image: msghorbani27/telegram-docker-bot:latest
    container_name: telegram-docker-bot
    restart: unless-stopped
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - ./config.yml:/config.yml
```
## License
This project is licensed under the **MIT License**.