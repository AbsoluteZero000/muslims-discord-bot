from .azkar import morning_azkar, evening_azkar
import asyncio
from datetime import datetime, timedelta
import pytz


async def send_azkar(client, azkar_type, Azkar_channel):
    channel = client.get_channel(Azkar_channel)

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


async def schedule_azkar():
    while True:
        now = datetime.now(pytz.timezone('Asia/Riyadh'))

        morning_time = now.replace(hour=6, minute=0, second=0, microsecond=0)
        if now > morning_time:
            morning_time += timedelta(days=1)
        await asyncio.sleep((morning_time - now).total_seconds())
        await send_azkar("morning")

        evening_time = now.replace(hour=17, minute=0, second=0, microsecond=0)
        if now > evening_time:
            evening_time += timedelta(days=1)
        await asyncio.sleep((evening_time - now).total_seconds())
        await send_azkar("evening")
