import discord
from discord.ext import commands
from struc import colors

class guild_events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        sys_channel = guild.system_channel
        if sys_channel is not None:
            sup_embed = discord.Embed(title=f"Hi, I'm <@{self.bot.user.id}>!", description=f"Thanks for inviting me! My prefix is `!`, but you can change it to whatever you want!\nUse `!help` to learn what I can do!", color=colors.default)
            await sys_channel.send(embed=sup_embed)

def setup(bot):
    bot.add_cog(guild_events(bot))