import os
from dotenv import load_dotenv

import discord


class StickountClient(discord.Client):
    async def on_connect(self):
        print("Connected to Discord")

    async def on_ready(self):
        print(f"Logged in as {self.user} ; {self.user.id}")


if __name__ == '__main__':
    load_dotenv()

    intents = discord.Intents.default()
    intents.emojis_and_stickers = True

    client = StickountClient(intents=intents)
    client.run(os.getenv('DISCORD_BOT_TOKEN'))
