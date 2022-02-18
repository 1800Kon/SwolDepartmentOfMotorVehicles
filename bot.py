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
        if len(message.content.lower().split(" ")) == 2:
            await message.add_reaction('✅')
            swolNo = message.content.lower().split()[1]
            await message.channel.send('Generating your license...')
            image_url_template = "https://www.smolverse.lol/_next/image?url=https%3A%2F%2Ftreasure-marketplace.mypinata.cloud%2Fipfs%2FQmSqwxNFMeFtgdCnjBTTixx46Wi6TH9FtQ5jAp98JnAoeR%2F" + swolNo + "%2F5.png&w=750&q=100"

            with BytesIO() as image_binary:
                try:
                    swol = Image.open(requests.get(
                        image_url_template, stream=True).raw).convert("RGBA")
                    zoomed_swol = zoom_at(swol, 200, 100, 5)
                    bg = Image.open('images/beach.jpg').convert("RGBA")
                    bg.paste(zoomed_swol, (0, 0), zoomed_swol)
                    bg.save(image_binary, 'PNG')
                    image_binary.seek(0)
                    await message.channel.send(file=discord.File(fp=image_binary, filename='image.png'))
                except:
                    await message.channel.send('Something went wrong. Please try again.')
        else:
            return


def zoom_at(img, x, y, zoom):
    w, h = img.size
    zoom2 = zoom * 2
    img = img.crop((x - w / zoom2, y - h / zoom2,
                    x + w / zoom2, y + h / zoom2))
    return img.resize((w, h), Image.LANCZOS)


client.run(token)
