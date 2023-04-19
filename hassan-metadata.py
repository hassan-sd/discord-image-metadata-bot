import os
from io import BytesIO

import discord
import aiohttp
from discord.ext import commands
from PIL import Image, UnidentifiedImageError
import requests

intents = discord.Intents.all()
client = commands.Bot(command_prefix = ['!', '/'], intents=intents)
bot = commands.Bot(command_prefix='$', intents=intents, help_command=None)


env_names = ['BLACKLIST_CHANNEL_IDS', 'METADATA_CHANNEL_ID', 'DISCORD_API_KEY']
env_vals = {}
for env in env_names:
    val = os.getenv(env)
    if val is None:
        print(f"You must set {env} environment variable")
        exit()
    env_vals[env] = val
blacklist_channel_str = os.getenv('METADATA_BLACKLIST_IDS')

metadata_channel_id = int(env_vals['METADATA_CHANNEL_ID'])
blacklist_channel_ids = [int(x) for x in env_vals['BLACKLIST_CHANNEL_IDS']]
api_key = env_vals['DISCORD_API_KEY']

# Set up a set to store the processed messages
processed_messages = set()

async def download_image(url: str) -> bytes:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            return await resp.read()

@client.command()
async def metadata(ctx, *, url: str):
    # Send a message to indicate that the image is being processed
    message = await ctx.reply('Processing image...')

    # Download the image
    try:
        image_data = BytesIO(await download_image(url))
    except:
        await message.edit(content='The image could not be downloaded.')
        return

    # Open the image
    try:
        image = Image.open(image_data)
    except UnidentifiedImageError:
        await message.edit(content='The image is not a valid PNG image.')
        return

    # Extract metadata
    metadata = image.info
    
    # If the metadata is empty, send a message and return
    if not metadata:
        await message.edit(content='No metadata found for the image.')
        return
    metadata_text = '\n'.join(f'{k}: "{v}"' for k, v in metadata.items())
    # Edit the original message to show the metadata
    await message.edit(content=f"```yaml\n{metadata_text}```")
    

@client.event
async def on_message(message):
    # Check if the message is in a blacklisted category
    if message.channel.category_id in blacklist_channel_ids:
        return
    # If the message is a PNG image and it has not been processed before
    if message.attachments and message.attachments[0].filename.endswith('.png') and message.id not in processed_messages:
        # Add the message to the set of processed messages
        processed_messages.add(message.id)
        for attachment in message.attachments:
            # Download the image
            image_data = BytesIO(await attachment.read())
            # Open the image
            image = Image.open(image_data)
            # Extract metadata
            metadata = image.info
            # If the metadata is empty, skip the file
            if not metadata:
                continue

            # Format the metadata as a string
            metadata_text = '\n'.join(f'{k}: "{v}"' for k, v in metadata.items())
            message_link = f'[by {message.author}]({message.jump_url})'
            origin_channel = f'[{message.channel.mention}]({message.channel.jump_url})'
            # Create the embed construct
            embed = discord.Embed(title=os.getenv('BOT_NAME', "Hassan's Metadata Scraper"))
            embed.set_image(url=attachment.url)
            embed.add_field(name='Original Channel', value=origin_channel)
            embed.add_field(name='Message Link', value=(f'{message_link}'))

            # Send the embed to the dedicated channel
            metadata_channel = client.get_channel(metadata_channel_id)
            await metadata_channel.send(embed=embed)
            await metadata_channel.send(f'```yaml\n{metadata_text}```')
    await client.process_commands(message)

if __name__ == "__main__":
    client.run(api_key)
