from discord.ext import commands
import discord
from datetime import datetime
import random
from struc import database, get_guild_values
db = database


class SuggestionChannels(commands.Cog):
    """
    Commands to setup the suggestions channel.
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.content.startswith(get_guild_values.prefix(self.bot, message)):
            return
        if message.guild == None:
            return
        if message.author == self.bot.user:
            return
        suggestion_guild = db.fetch("guild", "SELECT guild_id FROM suggestions")
        suggestion_channel = db.fetch("guild", "SELECT channel_id FROM suggestions WHERE guild_id = ?", (message.guild.id,))
        if not suggestion_guild:
            return
        if not suggestion_channel:
            return

        colors = [0x1abc9c, 0x11806a, 0x2ecc71, 0x1f8b4c, 0x3498db, 0x206694, 0x9b59b6, 0x71368a, 0xe91e63, 0xad1457, 0xf1c40f, 0xc27c0e, 0xe67e22, 0xa84300, 0xe74c3c, 0x992d22, 0x95a5a6, 0x607d8b, 0x979c9f, 0x546e7a, 0x7289da, 0x99aab5]
        if message.guild.id == suggestion_guild:
            if message.channel.id == suggestion_channel:
                channel = self.bot.get_channel(message.channel.id)
                suggestion = f"""{message.content}"""
                await message.delete()
                if not 8 <= len(message.content) <= 1000:
                    await channel.send(f"{message.author.mention} Too short/long", mention_author=False, delete_after=4)
                    return
                
                suggestion_embed = discord.Embed(title="Suggestion", description=f"{suggestion}", color=discord.Color(random.choice(colors)), timestamp=datetime.now())
                suggestion_embed.set_author(name=message.author, icon_url=message.author.avatar.url)
                suggestion_embed.set_footer(text="Submitted at", icon_url="https://i.ibb.co/6JThTdt/logoideadiscovery-3.png")
                suggestion_embed.set_image(url="https://i.ibb.co/1qfLq38/hr.png")
                msg = await channel.send(embed=suggestion_embed)
                direct = await message.author.create_dm()
                await direct.send(f"Thanks for your suggestion in **{message.guild}**! Your suggestion was:\n>>> {suggestion}")
                await msg.add_reaction("👍")
                await msg.add_reaction("🤷")
                await msg.add_reaction("👎")


    @commands.group(name='suggestions', invoke_without_command=True)
    @commands.has_permissions(manage_channels=True)
    async def suggestions(self, ctx):
        await ctx.reply("Use `help suggestions` for help.", mention_author=False)
    

    @suggestions.command(help="Sets the channel for suggestions.")
    @commands.has_permissions(manage_channels=True)
    async def set(self, ctx, channel: discord.TextChannel = None):
        if not channel:
            channel = ctx.channel

        db.modify("guild", "INSERT OR REPLACE INTO suggestions(guild_id, channel_id) VALUES(?,?)", (ctx.guild.id, channel.id))
        await ctx.reply(f"I successfully set {channel.mention} as suggestion channel. You can remove it by using `suggestions remove`.", mention_author=False)


    @suggestions.command(help="Removes the channel for suggestions.")
    @commands.has_permissions(manage_channels=True)
    async def remove(self, ctx):
        suggestions_channel = db.fetch("guild", "SELECT channel_id FROM suggestions WHERE guild_ID = ?", (ctx.guild.id,))
        if suggestions_channel:
            db.modify("guild", "DELETE FROM suggestions WHERE guild_id = ?", (ctx.guild.id,))
            await ctx.reply(f"I successfully removed <#{suggestions_channel}> as suggestion channel.", mention_author=False)
        else:
            await ctx.reply("A suggestion channel isn't set. You can add one by using `suggestions set`", mention_author=False)

def setup(bot):
    bot.add_cog(SuggestionChannels(bot))
