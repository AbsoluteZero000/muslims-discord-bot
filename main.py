#!/usr/bin/env python3
import os
import discord
import asyncio
import dotenv
import azkar.azkar_util as azkar_util

intents = discord.Intents.default()
intents.message_content = True

dotenv.load_dotenv()
client = discord.Client(intents=intents)

PING_CHANNEL_ID = -1
AZKAR_CHANNEL_ID = -1


async def ping_staff(client):
    if PING_CHANNEL_ID == -1:
        print("Ping channel not set")
        return
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


@client.event
async def on_message(message):
    print(message.content)
    if message.author == client.user:
        return

    global AZKAR_CHANNEL_ID
    global PING_CHANNEL_ID

    if message.content.startswith('!start-azkar'):
        if AZKAR_CHANNEL_ID == -1:
            await message.channel.send(
                "Please set the channel to send azkar to.\n eg. !set-azkar-channel #channel-name"
            )
            return

        await azkar_util.send_azkar(client, "morning", AZKAR_CHANNEL_ID)

    elif message.content.startswith('!send-azkar'):
        if AZKAR_CHANNEL_ID == -1:
            await message.channel.send(
                "Please set the channel to send azkar to.\n eg. !set-azkar-channel #channel-name"
            )
            return

        await azkar_util.send_azkar(client, "evening", AZKAR_CHANNEL_ID)

    elif message.content.startswith('!set-azkar-channel'):
        AZKAR_CHANNEL_ID = int(message.content.split(
            ' ')[1].strip('<>#'))

    elif message.content.startswith('!set-ping-channel'):
        PING_CHANNEL_ID = int(message.content.split(
            ' ')[1].strip('<>#'))

    elif message.content.startswith('!schedule-azkar'):
        if AZKAR_CHANNEL_ID == -1:
            await message.channel.send(
                "Please set the channel to send azkar to.\n eg. !set-azkar-channel #channel-name"
            )
            return

    elif message.content.startswith('!help'):
        await message.channel.send(
            """
Commands:
1. set the channel that the azkar will be sent to ```!set-azkar-channel #channel-name```
2. set the channel that the ping will be sent to ```!set-ping-channel #channel-name```
3. start scheduling azkar ```!schedule-azkar```
4. send azkar ```!send-azkar```
            """
        )
        await azkar_util.schedule_azkar(client, AZKAR_CHANNEL_ID)

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
