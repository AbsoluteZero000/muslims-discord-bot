#!/usr/bin/env python3
import os
import discord
import asyncio
import dotenv
from azkar.channels import PING_CHANNEL_ID
import azkar.azkar_util as azkar_util

intents = discord.Intents.default()
intents.message_content = True

dotenv.load_dotenv()
client = discord.Client(intents=intents)


async def ping_staff(client):
    while True:
        channel = client.get_channel(PING_CHANNEL_ID)
        if channel is not None:
            await channel.send('<@&1220819948826398720> use /bump in this channel')
        else:
            print(f"Channel with ID {PING_CHANNEL_ID} not found")
        await asyncio.sleep(7260)


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    # client.loop.create_task(schedule_azkar())


@client.event
async def on_message(message):
    print(message.content)
    if message.author == client.user:
        return

    if message.content.startswith('!start-azkar'):
        await azkar_util.send_azkar(client, "morning")

    elif message.content.startswith('!send-azkar'):
        await azkar_util.send_azkar(client, "evening")

if __name__ == '__main__':

    try:
        token = os.environ.get("DISCORD_TOKEN")
        if token is None:
            raise Exception("Please add your token to the Secrets pane.")
        client.run(token)

    except discord.HTTPException as e:
        if e.status == 429:
            print(
                "The Discord servers denied the connection for making too many requests")
            print(
                "Get help from https://stackoverflow.com/questions/66724687/in-discord-py-how-to-solve-the-error-for-toomanyrequests")
        else:
            raise e
