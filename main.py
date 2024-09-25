#!/usr/bin/env python3
import os
import discord
import asyncio
import dotenv
from datetime import datetime, timedelta
import pytz
import azkar

intents = discord.Intents.default()
intents.message_content = True
dotenv.load_dotenv()
client = discord.Client(intents=intents)
ping_task = None
PING_CHANNEL_ID = 1220847225543065761
AZKAR_CHANNEL_ID = 1147955942437179522


async def ping_staff():
    while True:
        channel = client.get_channel(PING_CHANNEL_ID)
        if channel is not None:
            await channel.send('<@&1220819948826398720> use /bump in this channel')
        else:
            print(f"Channel with ID {PING_CHANNEL_ID} not found")
        await asyncio.sleep(7260)


async def send_azkar(azkar_type):
    channel = client.get_channel(AZKAR_CHANNEL_ID)
    if channel is not None:
        if azkar_type == "morning":
            await channel.send("Good morning! Here's your morning azkar: [Insert morning azkar text here]")
        elif azkar_type == "evening":
            await channel.send("Good evening! Here's your evening azkar: [Insert evening azkar text here]")
    else:
        print(f"Channel with ID {AZKAR_CHANNEL_ID} not found")


async def schedule_azkar():
    while True:
        now = datetime.now(pytz.timezone('Asia/Riyadh'))

        # Schedule morning azkar
        morning_time = now.replace(hour=6, minute=0, second=0, microsecond=0)
        if now > morning_time:
            morning_time += timedelta(days=1)
        await asyncio.sleep((morning_time - now).total_seconds())
        await send_azkar("morning")

        # Schedule evening azkar
        evening_time = now.replace(hour=17, minute=0, second=0, microsecond=0)
        if now > evening_time:
            evening_time += timedelta(days=1)
        await asyncio.sleep((evening_time - now).total_seconds())
        await send_azkar("evening")


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    client.loop.create_task(schedule_azkar())


@client.event
async def on_message(message):
    global ping_task
    if message.author == client.user:
        return
    if message.content.startswith('$start'):
        if ping_task is None or ping_task.cancelled():
            ping_task = asyncio.create_task(ping_staff())
            for zikr in azkar.morning_azkar:
                await message.channel.send(zikr)
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
    token = os.environ.get("DISCORD_TOKEN")
    if token is None:
        raise Exception("Please add your token to the Secrets pane.")
    client.run(token)
except discord.HTTPException as e:
    if e.status == 429:
        print("The Discord servers denied the connection for making too many requests")
        print("Get help from https://stackoverflow.com/questions/66724687/in-discord-py-how-to-solve-the-error-for-toomanyrequests")
    else:
        raise e
