import discord
from struc import db, colored, emojis, colors, get_guild_values
from discord.ext import commands
from discord.commands import (
    slash_command,
    Option
)

class GuildSettings(commands.Cog):
    """
    Guild specific settings
    """
    EMOTE = "⚙️"
    def __init__(self, bot):
        self.bot = bot


def setup(bot):
    bot.add_cog(GuildSettings(bot))
