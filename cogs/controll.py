"""
This cog is intended to be a controller for the admins of this bot.
"""
import asyncio
import discord
from main import *
import os
from struc import database
db = database
from discord.ext import commands

class Controller(commands.Cog):
    """
    All commands to control the bot.
    """
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(help="Stops the bot.")
    async def stop(self, ctx):
        print(f"{ctx.author.name}")
        await ctx.reply("Shutting down...", mention_author=False)
        await self.bot.close()


def setup(bot):
    bot.add_cog(Controller(bot))
