import discord
from discord.ext import commands
from discord.ui import Button, View
import os
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

VERIFY_CHANNEL_ID = 1372940208923742289 

class VerifyButton(Button):
    def __init__(self):
        super().__init__(label="Verify Here", url="http://127.0.0.1:5000", style=discord.ButtonStyle.link)

class VerifyView(View):
    def __init__(self):
        super().__init__()
        self.add_item(VerifyButton())

@bot.event
async def on_ready():
    print(f"✅ Bot is ready as {bot.user}")
    channel = bot.get_channel(VERIFY_CHANNEL_ID)
    if channel:
        await channel.send(
            "👋 Welcome! Click the button below to verify your account:",
            view=VerifyView()
        )
    else:
        print("❌ Channel not found. Check VERIFY_CHANNEL_ID.")

bot.run(os.getenv("BOT_TOKEN"))
