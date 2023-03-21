# discord-image-metadata-bot
Discord bot that 
* Auto scrapes any images posted in channels on your server and auto logs the metadata into a dedicated channel
* Allows users to grab metadata from any image by using a command


Patreon: https://www.patreon.com/sd_hassan

# Setup
* Setup a discord bot  - https://discord.com/developers
* Modify the python files api key in line 112 with your discord key from the application you created
* Setup any "blacklisted" channels where the bot should ignore in line 69 with the Channel ID (Right click any channel and copy the ID)
* Modify your bot name and post format line 102 through 105
* Put in the channel ID you want  the logs to be posted to in line 108
* Install requirements `pip install -r requirements.txt` 
* Run the bot, `python hassan-metadata.py` 


# Usage
* In any non blacklisted channel, upload an image that has metadata
  * The bot should auto detect the metadata and post the metadata to your dedicated channel
* In any channel where the bot is present, use the command `!metadata url` and replace the word URL with an actual direct image URL such as a discord image on another server, a web hosted image etc.
  * The bot should reply with status messages and eventually provide the metadata


# Screenshot
![image](https://user-images.githubusercontent.com/119671806/226760753-94f4d3b0-12e1-44a4-bfb1-c7d418e72e1d.png)
![image](https://user-images.githubusercontent.com/119671806/226760847-7b9ac3ed-8c2a-4d52-9b64-571395694df1.png)
