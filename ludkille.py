# ludkille.py
import os
import dotenv
import discord
from discord.ext import commands
import json
from json.decoder import JSONDecodeError
from dyce import H, R
import icepool
from cogs.pub_sub import get_subs
import asyncio

dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)

TOKEN = os.getenv('DISCORD_TOKEN')

description = '''My bot with different functions. Ludcille is a friend. Use !help_me for help and command list.'''

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', description=description, intents=intents)

# When bot comes online
@bot.event
async def on_ready():
    """
    Prints how many servers the bot is connected to.
    """
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')
    
    guild_count = 0

    for guild in bot.guilds:
        print(f"- {guild.id} (name: {guild.name})")
        guild_count = guild_count + 1

    print(f"LudKILLe is in " + str(guild_count) + " guilds.")
    
async def load_extensions():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')

asyncio.run(load_extensions())

# Run Bot
bot.run(TOKEN)
