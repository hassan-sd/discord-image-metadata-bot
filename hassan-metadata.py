import os
import discord
import aiohttp
from discord.ext import commands
from PIL import Image
import requests

intents = discord.Intents.all()
client = commands.Bot(command_prefix = ['!', '/'], intents=intents)
bot = commands.Bot(command_prefix='$', intents=intents, help_command=None)


# Set up a set to store the processed messages
processed_messages = set()

async def download_image(url: str) -> bytes:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            return await resp.read()

@client.command()
async def metadata(ctx, *, url: str):
    # Send a message to indicate that the image is being processed
    message = await ctx.send('Processing image...')

    # Download the image
    response = requests.get(url)
    if response.status_code == 200:
        image_data = response.content
    else:
        await message.edit(content='The image could not be downloaded.')
        return

    # Save the image data to a file
    with open('image.png', 'wb') as f:
        f.write(image_data)

    # Open the image
    try:
        with open('image.png', 'rb') as f:
            image = Image.open(f)
    except OSError:
        await message.edit(content='The image is not a valid PNG image.')
        os.remove('image.png')
        return

    # Extract metadata
    metadata = image.info

    # If the metadata is empty, send a message and return
    if not metadata:
        await message.edit(content='No metadata found for the image.')
        os.remove('image.png')
        return

    # Delete the temporary image file
    os.remove('image.png')

    # Format the metadata as a string
    metadata_text = '\n'.join(f'{k}: {v}' for k, v in metadata.items())

    # Edit the original message to show the metadata
    await message.edit(content=metadata_text)
    

@client.event
async def on_message(message):
    # Check if the message is in a blacklisted category
    if message.channel.category_id in [234, 234]:
        return
    # If the message is a PNG image and it has not been processed before
    if message.attachments and message.attachments[0].filename.endswith('.png') and message.id not in processed_messages:
        # Add the message to the set of processed messages
        processed_messages.add(message.id)
        
        # Download the image
        image_data = await message.attachments[0].read()
        with open('image.png', 'wb') as f:
            f.write(image_data)
        
        # Open the image
        image = Image.open('image.png')
        
        # Extract metadata
        metadata = image.info
        
        #close the image
        image.close()

        # If the metadata is empty, skip the image
        if not metadata:
            return
        
        # Delete the temporary image file
        os.remove('image.png')
        
        # Format the metadata as a string
        metadata_text = '\n'.join(f'{k}: {v}' for k, v in metadata.items())
        message_link = f'[by {message.author}]({message.jump_url})'
        origin_channel = f'[{message.channel.mention}]({message.channel.jump_url})'
        # Create the embed construct
        embed = discord.Embed(title="Hassan's Metadata Scraper")
        embed.set_image(url=message.attachments[0].url)
        embed.add_field(name='Original Channel', value=origin_channel)
        embed.add_field(name='Message Link', value=(f'{message_link}'))
        
        # Send the embed to the dedicated channel
        metadata_channel = client.get_channel(123)
        await metadata_channel.send(embed=embed)
        await metadata_channel.send('```' + metadata_text + '```')
    await client.process_commands(message)
client.run('discordapikey')
