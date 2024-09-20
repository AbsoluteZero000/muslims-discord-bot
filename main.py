#!/usr/bin/env python3

import os
import discord
import asyncio
import dotenv


intents = discord.Intents.default()
intents.message_content = True
dotenv.load_dotenv()

client = discord.Client(intents=intents)
ping_task = None
CHANNEL_ID = 1220847225543065761


async def ping_staff():
    while True:
        channel = client.get_channel(CHANNEL_ID)
        if channel is not None:
            await channel.send('<@&1220819948826398720> use /bump in this channel')
        else:
            print(f"Channel with ID {CHANNEL_ID} not found")
        await asyncio.sleep(7260)


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):
    global ping_task

    if message.author == client.user:
        return

    if message.content.startswith('$start'):
        if ping_task is None or ping_task.cancelled():
            ping_task = asyncio.create_task(ping_staff())
            await message.channel.send('Started pinging Staff every 2 hours and 1 minute.')
        else:
            await message.channel.send('Already pinging Staff.')

    elif message.content.startswith('$end'):
        if ping_task is not None and not ping_task.cancelled():
            ping_task.cancel()
            await message.channel.send('Stopped pinging @Staff.')
        else:
            await message.channel.send('No ongoing pinging to stop.')

try:
    token = os.environ.get("DISCORD_TOKEN=")
    if token == os.environ.get("DISCORD_TOKEN="):
        raise Exception("Please add your token to the Secrets pane.")
    client.run(token)
except discord.HTTPException as e:
    if e.status == 429:
        print("The Discord servers denied the connection for making too many requests")
        print("Get help from https://stackoverflow.com/questions/66724687/in-discord-py-how-to-solve-the-error-for-toomanyrequests")
    else:
        raise e
