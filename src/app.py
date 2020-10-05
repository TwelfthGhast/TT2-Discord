import discord
import datetime as dt
import asyncio
from tasks.raid_contribution import get_total_damage_by_player
from tasks.daily import print_daily

PREFIX = "tt2!"
# REPLACE THIS WITH YOUR ANNOUNCEMENT CHANNEL
MAIN_CHANNEL = 759393714275352610

client = discord.Client()

@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")
    while True:
        cur_time = dt.datetime.utcnow()
        if cur_time.time() >= dt.time(23, 59):
            channel = client.get_channel(MAIN_CHANNEL)
            await channel.send(f"[{cur_time.strftime('%d-%b-%Y %H:%M')}] {channel.guild.default_role} 4:58 Daily reset imminent!")
            await asyncio.sleep(60*(60*23 + 55))
        else:
            await asyncio.sleep(30)

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith(f"{PREFIX}raid"):
        try:
            assert len(message.content.split()) == 2
            cmd, url = message.content.split()
            df = get_total_damage_by_player(url)
            def chunk_df(df, rows=10):
                return (df.iloc[0+i:rows+i] for i in range(0, len(df.index), rows))
            for chunked_df in chunk_df(df):
                await message.channel.send(f"```{chunked_df.to_markdown()}```")
        except:
            await message.channel.send(f"Usage: {PREFIX}raid <pastebin-url>")
            raise
    
    if message.content.startswith(f"{PREFIX}daily"):
        msg = "Dailies reset at 12:00 AM UTC time.\n"
        msg += f"The current UTC time is {dt.datetime.utcnow().strftime('%H:%M %p')}."
        await message.channel.send(msg)

client.run("token")