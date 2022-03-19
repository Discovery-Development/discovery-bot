import asyncio
import discord
from main import *
import os
from struc import funcs, colors, colored
from discord.ext import commands

class local_events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{len(bot.guilds)} servers"))

        print(f"{colored.SUCCESS}Logged in as {bot.user} {colored.RESET}{colored.HINT}[{bot.user.id}]{colored.RESET}{colored.SUCCESS}.{colored.RESET}")
        bot.version = "1.1.0"

def setup(bot):
    bot.add_cog(local_events(bot))