from discord.ext import commands
import discord
from datetime import datetime
import random
from struc import db, get_guild_values
from discord.commands import (
    slash_command,
    Option,
    SlashCommandGroup
)


class SuggestionChannels(commands.Cog):
    """
    Commands to setup the suggestions channel.
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if not type(message.channel) == discord.TextChannel or message.guild is None or message.content.startswith(get_guild_values.prefix(self.bot, message.channel)) is None or message.author == self.bot.user:
            return
        
        suggestion_guild = db.fetch("SELECT guild_id FROM suggestions;")
        suggestion_channel = db.fetch("SELECT channel_id FROM suggestions WHERE guild_id = %s;", (message.guild.id,))
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
                    await channel.send(f"{message.author.mention} Too short/long", delete_after=4)
                    return
                
                suggestion_embed = discord.Embed(title="Suggestion", description=f"{suggestion}", color=discord.Color(random.choice(colors)), timestamp=datetime.now())
                suggestion_embed.set_author(name=message.author, icon_url=message.author.avatar.url)
                suggestion_embed.set_footer(text="Submitted at", icon_url="https://i.ibb.co/6JThTdt/logoideadiscovery-3.png")
                suggestion_embed.set_image(url="https://i.ibb.co/1qfLq38/hr.png")
                msg = await channel.send(embed=suggestion_embed)
                direct = await message.author.create_dm()
                try:
                    await direct.send(f"Thanks for your suggestion in **{message.guild}**! Your suggestion was:\n>>> {suggestion}")
                except discord.errors.Forbidden:
                    pass
                await msg.add_reaction("👍")
                await msg.add_reaction("🤷")
                await msg.add_reaction("👎")

    suggestions = SlashCommandGroup("suggestions", "Suggestions system")
    

    @suggestions.command()
    async def set(self, ctx: discord.ApplicationContext, channel: Option(discord.TextChannel, "The suggestions channel")):
        if not ctx.author.guild_permissions.manage_channels:
            raise commands.MissingPermissions(["ManageChannels"])

        if not channel:
            channel = ctx.channel

        db.modify("INSERT INTO suggestions(guild_id, channel_id) VALUES(%s,%s) ON CONFLICT (guild_id) DO UPDATE SET channel_id = %s;", (ctx.guild.id, channel.id, channel.id))
        await ctx.respond(f"I successfully set {channel.mention} as suggestion channel. You can remove it by using `suggestions remove`.")


    @suggestions.command()
    async def remove(self, ctx: discord.ApplicationContext):
        if not ctx.author.guild_permissions.manage_channels:
            raise commands.MissingPermissions(["ManageChannels"])

        suggestions_channel = db.fetch("SELECT channel_id FROM suggestions WHERE guild_id = %s;", (ctx.guild.id,))
        if suggestions_channel:
            db.modify("DELETE FROM suggestions WHERE guild_id = %s;", (ctx.guild.id,))
            await ctx.respond(f"I successfully removed <#{suggestions_channel}> as suggestion channel.")
        else:
            await ctx.respond("A suggestion channel isn't set. You can add one by using `suggestions set`")

def setup(bot):
    bot.add_cog(SuggestionChannels(bot))
