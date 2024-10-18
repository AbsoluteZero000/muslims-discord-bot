from .azkar import morning_azkar, evening_azkar
import asyncio
from datetime import datetime, timedelta
import pytz


async def send_azkar(ctx, azkar_type, Azkar_channel):
    channel = ctx.bot.get_channel(Azkar_channel)

    if channel is not None:
        if azkar_type == "morning":
            await channel.send("Good morning! Here's your morning azkar: ")
            for zikr in morning_azkar:
                await asyncio.sleep(2)
                await channel.send(zikr)

        elif azkar_type == "evening":
            await channel.send("Good evening! Here's your evening azkar: ")
            for zikr in evening_azkar:
                await asyncio.sleep(2)
                await channel.send(zikr)
    else:
        print(f"Channel with ID {Azkar_channel} not found")


async def schedule_azkar(ctx, Azkar_channel):
    timezone = pytz.timezone('Asia/Riyadh')

    while True:
        now = datetime.now(timezone)

        morning_time = now.replace(hour=6, minute=0, second=0, microsecond=0)
        if now > morning_time:
            morning_time += timedelta(days=1)

        evening_time = now.replace(hour=17, minute=0, second=0, microsecond=0)
        if now > evening_time:
            evening_time += timedelta(days=1)

        next_alarm = min(morning_time, evening_time)
        sleep_duration = (next_alarm - now).total_seconds()

        print(f"Sleeping for {sleep_duration} seconds until the next alarm.")
        await asyncio.sleep(sleep_duration)

        if next_alarm == morning_time:
            await send_azkar(ctx, "morning", Azkar_channel)
        elif next_alarm == evening_time:
            await send_azkar(ctx, "evening", Azkar_channel)
