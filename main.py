import os
from dotenv import load_dotenv

import discord
from discord import app_commands


class CountingSticker:
    def __init__(self, name):
        self.name = name
        self.count = 0


SOURCE_GUILD = 952633596336803911
STICKER_USE_COUNT = {
    1057466126478614638: CountingSticker(name="Consume"),
    1120097780581552139: CountingSticker(name="Consume?"),
    1057464977411297330: CountingSticker(name="Unsume"),
    1099240856902434868: CountingSticker(name="shermatwirl"),  # Funny hollow knight sausage spin sticker
}


intents = discord.Intents.default()
intents.emojis_and_stickers = True

client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)


@tree.command(name="stickount", description="Counts stickers", guild=discord.Object(id=SOURCE_GUILD))
async def stickount(interaction):
    msg = "Stickers statistics:\n"
    for sticker_id in STICKER_USE_COUNT:
        sticker = STICKER_USE_COUNT[sticker_id]
        uses = sticker.count
        msg += f"- {sticker.name} was used {uses} time{'' if uses == 1 else 's'}\n"
    await interaction.response.send_message(msg)


@tree.command(name="setcount", description="Set sticker count on a sticker", guild=discord.Object(id=SOURCE_GUILD))
@app_commands.checks.has_permissions(manage_expressions=True)
async def setcount(interaction, count: int, sticker_name: str):
    if count < 0:
        await interaction.response.send_message("Cannot set negative sticker count", ephemeral=True)
        return
    stickers = await client.get_guild(SOURCE_GUILD).fetch_stickers()
    for sticker in stickers:
        if sticker.name == sticker_name:
            STICKER_USE_COUNT[sticker.id].count = count
            await interaction.response.send_message(f"Successfully set sticker `{sticker_name}` count to {count}", ephemeral=True)
            break
    else:
        await interaction.response.send_message(f"Failed to find sticker matching name `{sticker_name}`", ephemeral=True)


@client.event
async def on_connect():
    print("Connected to Discord")


@client.event
async def on_ready():
    print(f"Logged in as {client.user} ; {client.user.id}")
    await tree.sync(guild=discord.Object(id=SOURCE_GUILD))


@client.event
async def on_message(message):
    if message.author == client.user or message.author.bot:
        return

    if message.guild.id != SOURCE_GUILD:
        return

    if len(message.stickers) <= 0:
        return

    for sticker in message.stickers:
        if sticker.id in STICKER_USE_COUNT:
            STICKER_USE_COUNT[sticker.id].count += 1


if __name__ == '__main__':
    load_dotenv()
    client.run(os.getenv('DISCORD_BOT_TOKEN'))
