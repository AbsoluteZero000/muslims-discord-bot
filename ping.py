# async def ping_staff(client):
#    if PING_CHANNEL_ID == -1:
#        print("Ping channel not set")
#        return
#    while True:
#        channel = client.get_channel(PING_CHANNEL_ID)
#        if channel is not None:
#            await channel.send('<@&1220819948826398720> use /bump in this channel')
#        else:
#            print(f"Channel with ID {PING_CHANNEL_ID} not found")
#        await asyncio.sleep(7260)
