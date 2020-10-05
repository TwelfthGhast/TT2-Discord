import discord
from raids.raid_contribution import get_total_damage_by_player

PREFIX = "tt2!"

client = discord.Client()

@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")

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

client.run("token")