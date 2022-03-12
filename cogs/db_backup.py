"""
Create a database backup of the guild data on startup.
"""
import discord
import os
from discord.ext import commands
import os, shutil, socket, secrets, time

class DbBackup(commands.Cog):
    """
    All commands to control the bot.
    """
    def __init__(self, bot):
        self.bot = bot
    @commands.Cog.listener()
    async def on_ready(self):
        if socket.gethostname() == "pons":
            try:
                print("Creating db backup...")
                filename = f"{secrets.token_urlsafe(20)}.db"
                shutil.copyfile("guild_data.db", filename)
                backup_channel = self.bot.get_channel(948110680429576202)
                backup = discord.File(filename)
                await backup_channel.send(content=f"💾 <t:{int(time.time())}:f>",file=backup)
                os.remove(filename)
            except:
                print(f"Failed to create database backup.")
            else:
                print("Done.")
def setup(bot):
    bot.add_cog(DbBackup(bot))
