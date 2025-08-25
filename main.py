import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
from database import Database

load_dotenv()

token = os.getenv('DISCORD_TOKEN')
GUILD_ID = discord.Object(id=1407929885816782928)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='/', intents=intents)

db = Database()

@bot.event
async def on_ready():
    await db.connect()
    await bot.tree.sync(guild=GUILD_ID)
    print(f'Logged in as {bot.user.name} and ready to serve!')

bot.run(token, log_handler=handler, log_level=logging.DEBUG)