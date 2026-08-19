import os
import discord
from discord.ext import commands

intents = discord.Intents.default()

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)

@bot.event
async def on_ready():
    print(f"Bot is online as {bot.user}")

    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(f"Sync error: {e}")


@bot.tree.command(name="hello", description="Say hello!")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message("Hello! 👋")


bot.run(os.getenv("DISCORD_TOKEN"))