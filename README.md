# discord-image-metadata-bot
Discord bot that 
* Auto scrapes any images posted in channels on your server and auto logs the metadata into a dedicated channel
* Allows users to grab metadata from any image by using a command


Patreon: https://www.patreon.com/sd_hassan

# Setup
* Setup a discord bot  - https://discord.com/developers
* You must define some environment variables:
 * `DISCORD_API_KEY`: your discord api key
 * `BLACKLIST_CHANNEL_IDS`: comma separated list of channel id or channel category ids that you don't want to be scraped (Right click any channel or channel group and copy the ID)
 * `METADATA_CHANNEL_ID`: channel id to send all metadata to
 * `BOT_NAME`: the name of the bot (you can leave the default)
* Install requirements `pip install -r requirements.txt` 
* Run the bot: 
 ```shell
 export DISCORD_API_KEY=12345
 export METADATA_CHANNEL_ID=5678
 export BLACKLIST_CHANNEL_IDS=123,456,678
 python hassan-metadata.py
 ``` 

# Usage
* In any non blacklisted channel, upload an image that has metadata
  * The bot should auto detect the metadata and post the metadata to your dedicated channel
* In any channel where the bot is present, use the command `!metadata url` and replace the word URL with an actual direct image URL such as a discord image on another server, a web hosted image etc.
  * The bot should reply with status messages and eventually provide the metadata


# Screenshot
![image](https://user-images.githubusercontent.com/119671806/226760753-94f4d3b0-12e1-44a4-bfb1-c7d418e72e1d.png)
![image](https://user-images.githubusercontent.com/119671806/226760847-7b9ac3ed-8c2a-4d52-9b64-571395694df1.png)
