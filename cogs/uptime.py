from discord.ext import commands
from discord.ext import tasks
import discord
import requests
from datetime import datetime
from struc import database, get_guild_values
db = database

@tasks.loop(seconds=9)
async def uptime_requests():
    url = "https://discovery-dev.cf/check/discovery-bot?key=15fb55f4-f098-41c4-a71c-d7081f0e1550"
    try:
        requests.get(url, timeout=3)
    except:
        pass

class uptime(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        uptime_requests.start()

def setup(bot):
    bot.add_cog(uptime(bot))