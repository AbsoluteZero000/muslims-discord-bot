#!/usr/bin/env python3
import os
import dotenv
import discord
from discord.ext import commands
import azkar.azkar_util as azkar_util

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='/', intents=intents)


PING_CHANNEL_ID = -1
AZKAR_CHANNEL_ID = -1


@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f'We have logged in as {bot.user}')


@bot.command(name="send_morning")
async def send_morning(ctx):
    await azkar_util.send_azkar(ctx, "morning", AZKAR_CHANNEL_ID)


@bot.command(name="send_evening")
async def send_evening(ctx):
    await azkar_util.send_azkar(ctx, "evening", AZKAR_CHANNEL_ID)


@bot.command(name="start-azkar")
async def start_azkar(ctx):
    """This command starts the azkar scheduler"""
    global AZKAR_CHANNEL_ID
    if AZKAR_CHANNEL_ID == -1:
        await ctx.send(
            """
            Please set the channel to send azkar to.
            eg. !set-azkar-channel #channel-name
            """
        )
        return

    await azkar_util.schedule_azkar(ctx, AZKAR_CHANNEL_ID)


@bot.command(name="set-azkar-channel")
async def set_azkar_channel(ctx, channel):
    """This command sets the channel to send azkar to"""
    global AZKAR_CHANNEL_ID
    AZKAR_CHANNEL_ID = int(channel.strip('<>#'))
    await ctx.send(f"Set azkar channel to {channel}")


if __name__ == '__main__':
    try:
        dotenv.load_dotenv()
        token = os.environ.get("DISCORD_TOKEN")
        if token is None:
            raise Exception("Please add your token to the Secrets pane.")
        bot.run(token)

    except discord.HTTPException as e:
        if e.status == 429:
            print(
                "The Discord servers denied the connection for making too many requests")
            print(
                "Get help from https://stackoverflow.com/questions/66724687/in-discord-py-how-to-solve-the-error-for-toomanyrequests")
        else:
            raise e
