import asyncio
import discord
import main
from discord.ext import commands 
from struc import colors
from datetime import datetime

class Miscellaneous(commands.Cog):
    """
    Miscellaneous commands.
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.command(help="Announces something for you in an embed message.")
    async def announce(self, ctx, *, content):
        announce_embed = discord.Embed(description=f"{content}", timestamp=datetime.now(), color=discord.Color(0xF37F7F))
        announce_embed.set_footer(icon_url=f"{ctx.author.avatar.url}", text=f"Announcement from {ctx.author}")
        await ctx.reply(embed=announce_embed, mention_author=False)

    @commands.command(help="Gets the bot's latency.")
    async def ping(self, ctx):
        ping_embed = discord.Embed(title=f"🏓 Pong", description=f"**Ping:** {round(self.bot.latency*1000)}ms", color=discord.Color(0xF37F7F))
        await ctx.reply("Here ya go!" ,embed=ping_embed, mention_author=False)
        
    @commands.command(help="Gets the bot's version.")
    async def version(self, ctx):
        version_embed = discord.Embed(title="Version", description=f"You are currently using version **{self.bot.version}**.", color=discord.Color(0xF37F7F))
        await ctx.reply(embed=version_embed, mention_author=False)

    @commands.command(help="Sends someone's avatar.")
    async def pfp(self, ctx, target: discord.User=None):
        if target is None:
            target = ctx.author
            pfp_title = "Your avatar"
        else:
            pfp_title = f"{target.name}'s avatar"

        pfp_embed = discord.Embed(title=pfp_title, url=target.avatar.url)
        pfp_embed.set_image(url=target.avatar.url)

        await ctx.reply(embed=pfp_embed, mention_author=False)


    @commands.command(help="Sends some information about someone.")
    async def userinfo(self, ctx, member: discord.Member=None):
        if not member:
            member = ctx.author

        member_roles = ""
        member_nickname = member.nick
        member_activity = member.activity.name
        member_activity_type = str(member.activity.type).split('.')[-1].title()

        created_at = member.created_at.strftime("%b %d, %Y, %H:%M")
        joined_at = member.joined_at.strftime("%b %d, %Y, %H:%M")

        userinfo_embed = discord.Embed(color=colors.default)

        member_roles += "@everyone"
        for role in member.roles:
            if role.id != ctx.guild.id:
                member_roles += f"<@&{role.id}>"

        if member.nick is None:
            member_nickname = "No nickname"

        if member.activity is None:
            member_activity_type = "Doing"
            member_activity = "Nothing"

        userinfo_embed.set_author(name=f"{member} - {member_nickname}")

        try:
            userinfo_embed.set_author(name=userinfo_embed.author.name, icon_url=member.avatar.url)
        except AttributeError:
            pass

        userinfo_embed.add_field(name=f"ID", value=f"{member.id}")
        userinfo_embed.add_field(name=f"Created account on", value=f"{created_at}", inline=True)
        userinfo_embed.add_field(name=f"Joined {ctx.guild.name} on", value=f"{joined_at}", inline=True)
        userinfo_embed.add_field(name=f"Roles", value=f"{member_roles}", inline=True)
        userinfo_embed.add_field(name="Status", value=f"{str(member.status).capitalize()}", inline=True)
        userinfo_embed.add_field(name="Activity", value=f"{member_activity_type}: {str(member_activity).capitalize()}", inline=True)

        await ctx.reply(embed=userinfo_embed, mention_author=False)

def setup(bot):
    bot.add_cog(Miscellaneous(bot))
