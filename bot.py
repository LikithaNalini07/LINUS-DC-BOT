import os
import discord
from discord.ext import commands
from aiohttp import web

# ===== DEPLOYMENT LAYER: HTTP Server for Render =====
async def health_check(request):
    """This function runs when someone visits /health endpoint.
    Returns 'I'm alive!' with status 200 (OK)"""
    return web.Response(text="Bot is running!", status=200)

async def start_web_server():
    """Create and start the HTTP server on port 8080"""
    app = web.Application()
    app.router.add_get("/health", health_check)
    
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 8080)
    await site.start()
    print("[DEPLOYMENT] HTTP server started on port 8080")

# ===== CORE BOT: Your Discord Bot (UNCHANGED) =====
intents = discord.Intents.default()

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)

@bot.event
async def on_ready():
    # Start HTTP server once, when bot connects
    if not hasattr(bot, 'http_server_started'):
        bot.http_server_started = True
        await start_web_server()
    
    print(f"Bot is online as {bot.user}")

    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(f"Sync error: {e}")


@bot.tree.command(name="hello", description="Say hello!")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message("Hello! 👋")

print("DEBUG TOKEN VALUE:", repr(os.getenv("DISCORD_TOKEN")))
bot.run(os.getenv("DISCORD_TOKEN"))