import sqlite3
from abc import ABC

import discord
import os
from discord.ext import commands
from struc import database, colored, emojis, colors, get_guild_values
from apscheduler.schedulers.asyncio import AsyncIOScheduler

db = database

intents = discord.Intents.all()


def get_token():
    # create config table
    token = db.fetch("bot", "SELECT token FROM config")
    if not token:
        print(f"{colored.FAIL}NO TOKEN SPECIFIED.{colored.RESET}")
        token_input = input(f"{colored.HINT}Please paste the token here to run the bot: {colored.RESET}")
        try:
            db.modify("bot", "INSERT INTO config(token) VALUES(?)", (token_input,))
            print(f"{colored.SUCCESS}TOKEN SAVED{colored.RESET}")
        except:
            print(f"{colored.WARNING}SOMETHING WENT WRONG.{colored.RESET}")
    # Fetch the token once it was entered by the user
    token = db.fetch("bot", "SELECT token FROM config")
    return token


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
        super().run(get_token(), reconnect=True)

    async def on_ready(self):
        if not self.ready:
            self.scheduler.start()
            self.ready = True
            print("Bot is ready.")
        else:
            print("Bot reconnected.")


bot = Bot()
bot.run()
