import datetime as dt
import time
import discord

MAIN_CHANNEL = 759393714275352610

async def print_daily(client):
    print(type(client))
    while True:
        cur_time = dt.datetime.utcnow()
        if cur_time >= dt.time(23, 59):
            channel = client.get_channel(MAIN_CHANNEL)
            await channel.send(f"{cur_time.strftime('%d %b %Y')} | {channel.guild.default_role} Dailies are resetting...")
            time.sleep(60*(60*23 + 55))
        else:
            time.sleep(30)