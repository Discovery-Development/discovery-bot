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

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        error_embed = discord.Embed(title="Error", description="An error has occured.",color=colors.fail) # Template for error embed, just change descriptions

        if isinstance(error, commands.MemberNotFound):
            error_embed.description = f"Couldn't find that member."
            await ctx.reply(embed=error_embed, mention_author=False)
        elif isinstance(error, commands.MissingRequiredArgument):
            error_embed.description = f"You are missing a required argument for that command."
            await ctx.reply(embed=error_embed, mention_author=False)
        elif isinstance(error, commands.BadArgument):
            error_embed.description = f"You provided an invalid argument."
            await ctx.reply(embed=error_embed, mention_author=False)
        elif isinstance(error, commands.CommandNotFound):
            pass
        elif isinstance(error, commands.CommandOnCooldown):
            cooldown_active_embed = discord.Embed(title=f"**On cooldown**", description=f"You're still on cooldown! Please try again in **{round(error.retry_after / 60)}** minutes.", color=colors.default)
            await ctx.reply(embed=cooldown_active_embed, mention_author=False)
        elif isinstance(error, commands.MissingPermissions):
            if len(error.missing_permissions) <= 1:
                permission = error.missing_permissions[0]
                text = f"don't have the permission `{permission}` to use this command."
                title = "Missing permission"
            else:
                permission_list = error.missing_permissions
                permissions = '{} and {}'.format(', '.join(permission_list[:-1]), permission_list[-1])
                text = f"don't have the following permissions to run this command: `{permissions}`"
                title = "Missing permissions"

            embed = discord.Embed(color=colors.fail, title=title, description=f"You, {ctx.author} {text}")
            await ctx.reply(embed=embed, mention_author=False)
        else:
            print(error)
            channel = self.bot.get_channel(939928959536218162)
            if channel:
                await channel.send(f"{error}\nHas been caused by the message: '{ctx.message.content}'")


def setup(bot):
    bot.add_cog(local_events(bot))