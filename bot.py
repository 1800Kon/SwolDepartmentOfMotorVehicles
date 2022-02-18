import os
from urllib import response
import discord
import requests
from PIL import Image
from io import BytesIO
from dotenv import load_dotenv
load_dotenv('.env')

client = discord.Client()
token = os.getenv('DISCORD_TOKEN')


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.lower().startswith('swol'):
        await message.channel.send('Generating your license...')
        swolNo = message.content.lower().split()[1]
        image_url_template = "https://www.smolverse.lol/_next/image?url=https%3A%2F%2Ftreasure-marketplace.mypinata.cloud%2Fipfs%2FQmSqwxNFMeFtgdCnjBTTixx46Wi6TH9FtQ5jAp98JnAoeR%2F" + swolNo + "%2F5.png&w=750&q=100"
        
        with BytesIO() as image_binary:
            img = Image.open(requests.get(image_url_template, stream=True).raw)
            img.save(image_binary, 'PNG')
            image_binary.seek(0)
            await message.channel.send(file=discord.File(fp=image_binary, filename='image.png'))


client.run(token)
