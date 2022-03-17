import sqlite3
from abc import ABC
#from dotenv import load_dotenv
import discord
import os
from discord.ext import commands
from struc import database, colored, emojis, colors, get_guild_values
from apscheduler.schedulers.asyncio import AsyncIOScheduler

db = database

#load_dotenv()

intents = discord.Intents.all()


class Bot(commands.Bot, ABC):
    def __init__(self):
        super().__init__(
            command_prefix=get_guild_values.prefix,
            case_insensitive=True,
            intents=discord.Intents.all()
        )
        self.ready = False
        self.scheduler = AsyncIOScheduler(timezone="utc")
        self.persistent_views_added = False

    def setup(self):
        for ext in os.listdir("./cogs"):
            if ext.endswith(".py"):
                bot.load_extension(f"cogs.{ext[:-3]}")
                print(f"Extension {ext[:-3]} was loaded.")
        print("Setup completed.")

    def run(self):
        print("Running setup...")
        self.setup()
        print("Starting bot.")
        super().run(os.environ.get("TOKEN"), reconnect=True)

    async def on_ready(self):
        if not self.ready:
            self.scheduler.start()
            self.ready = True
            print("Bot is ready.")
        else:
            print("Bot reconnected.")


bot = Bot()
bot.run()
