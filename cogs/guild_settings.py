import discord
from struc import db, colored, emojis, colors, get_guild_values
from discord.ext import commands

class GuildSettings(commands.Cog):
    """
    Guild specific settings
    """
    EMOTE = "⚙️"
    def __init__(self, bot):
        self.bot = bot

    @commands.command(help="Sets the prefix for the bot on this server.")
    async def set_prefix(self, ctx, prefix: str):
        guild = db.fetch(f"SELECT guild_id FROM settings WHERE guild_id = %s;", (ctx.guild.id,))

        if guild is None:
            sql = (f"INSERT INTO settings(guild_id, prefix) VALUES(%s,%s);")
            binds = (ctx.guild.id, prefix)
            await ctx.reply(f"Prefix has been set to `{prefix}`.", mention_author=False)
        elif guild is not None:
            sql = (f"UPDATE settings SET prefix = %s WHERE guild_id = %s;")
            binds = (prefix, ctx.guild.id)
            await ctx.reply(f"Prefix has been updated to `{prefix}`.", mention_author=False)
        
        db.modify(sql, binds)


def setup(bot):
    bot.add_cog(GuildSettings(bot))
