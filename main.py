#!/usr/bin/env python3
import os
import pytz
import dotenv
import asyncio
import discord
from discord.ext import commands
from discord import Embed
import azkar.azkar_util as azkar_util
from datetime import datetime, timedelta

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='/', intents=intents)


PING_CHANNEL_ID = -1
AZKAR_CHANNEL_ID = -1
QURAN_CHANNEL_ID = -1

QURAN_URL = "https://surahquran.com/img/pages-quran/page"


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
            eg. /set-azkar-channel #channel-name
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


@bot.command(name="set-quran-channel")
async def set_quran_channel(ctx, channel):
    """This command sets the channel to send quran to"""
    global QURAN_CHANNEL_ID
    QURAN_CHANNEL_ID = int(channel.strip('<>#'))
    await ctx.send(f"Set quran channel to {channel}")


@bot.command(name="start-werd")
async def start_werd(ctx, startingPage=1, numOfPages=2):
    numOfPages = int(numOfPages)
    startingPage = int(startingPage)
    quranChannel = ctx.bot.get_channel(QURAN_CHANNEL_ID)
    timezone = pytz.timezone('Asia/Riyadh')

    while True:
        now = datetime.now(timezone)
        next_time = now.replace(hour=12, minute=0, second=0, microsecond=0)

        if now > next_time:
            next_time += timedelta(days=1)

        sleep_duration = (next_time - now).total_seconds()
        print(f"Sleeping for {sleep_duration} seconds until the next alarm.")
        await asyncio.sleep(sleep_duration)

        main_message = f"""
<@&1220848108934529145>

**🌸 وعليكم السلام ورحمة الله وبركاته 🌸**

إليكم صفحاتكم اليومية من القرآن الكريم 📖
**اليوم من الصفحة {startingPage} إلى الصفحة {startingPage + numOfPages - 1}.**
نسأل الله أن يفتح علينا وعليكم فهم كتابه 🌹

---

**🌸 As-salamu alaykum wa rahmatullahi wa barakatuh 🌸**

Here are your daily Quran pages 📖
**Today, from page {startingPage} to page {startingPage + numOfPages - 1}.**
May Allah grant us understanding of His Book 🌹
        """

        # Create embeds for each Quran page
        embeds = []
        for i in range(startingPage, startingPage + numOfPages):
            page_num = i if i <= 604 else 1  # Wrap around if page exceeds 604
            embed = Embed(title=f"📖 Quran Page {page_num}")
            embed.set_image(url=f"{QURAN_URL}{str(page_num).zfill(3)}.png")
            embeds.append(embed)

        startingPage += numOfPages
        await quranChannel.send(content=main_message, embeds=embeds)

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
