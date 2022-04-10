from dotenv import load_dotenv
import discord
import os
from struc import colored
from discord.ext import commands

load_dotenv()

intents = discord.Intents.all()

bot = commands.Bot(case_insensitive=True, intents=intents)

for ext in os.listdir("./cogs"):
        if ext.endswith(".py"):
            bot.load_extension(f"cogs.{ext[:-3]}")
            print(f"Extension {ext[:-3]} was loaded.")
print(f"{colored.SUCCESS}All extensions were loaded.{colored.RESET}")

try:
    if os.getenv("TOKEN"):
        bot.run(os.getenv("TOKEN"))
    elif os.environ.get("TOKEN"):
        bot.run(os.environ.get("TOKEN"))
except RuntimeError:
    print(f"\n{colored.SUCCESS}Disconnected from Discord API.{colored.RESET}")