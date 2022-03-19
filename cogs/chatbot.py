"""
this is still in development

idea:
"{{GUILD_ID}}": {
"muted": <true|false>,
"channel": {{CHANNEL_ID}},
"embed": <true|false>
-> Extra table in the database for this
}

"""
import discord
import requests
import urllib
import asyncio
import random
from main import *
from discord.ext import commands
from struc import db
from discord.commands import (
    slash_command,
    SlashCommandGroup,
    Option
)

class Chatbot(commands.Cog):
    """
    All commands that are related to the chatbot.
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.guild is None or message.author.bot:
            return
        
        if message.content.startswith(get_guild_values.prefix(self.bot, message)):
            return

        chatbot_guild = db.fetch("SELECT guild_id FROM chatbot;")
        chatbot_channel = db.fetch("SELECT channel_id FROM chatbot WHERE guild_id = %s;", (message.guild.id,))
        if message.guild == None:
            return
        if message.author == self.bot.user:
            return
        
        if message.guild.id == chatbot_guild:
            if message.channel.id == chatbot_channel:

                author_input = urllib.parse.quote(message.content, safe="")
                chat_endpoint = f"https://pixel-api-production.up.railway.app/fun/chatbot/?message={author_input}?name="
                await asyncio.sleep(random.uniform(0.6,2))
                async with message.channel.typing():
                    await asyncio.sleep(random.uniform(0.2,0.6))

                    chat_response = requests.get(chat_endpoint).json()
                    chat_message = chat_response["message"]
                await message.reply(chat_message)

    chatbot = SlashCommandGroup("chatbot", "Chatbot commands")

    @chatbot.command()
    async def set(self, ctx: discord.ApplicationContext, channel: Option(discord.TextChannel, "The Textchannel for the chatbot.")):
        if not ctx.author.guild_permissions.manage_channels:
            raise commands.MissingPermissions(["ManageChannels"])

        db.modify("INSERT INTO chatbot(guild_id, channel_id) VALUES(%s,%s) ON CONFLICT (guild_id) DO UPDATE SET channel_id = %s;", (ctx.guild.id, channel.id, channel.id))
        await ctx.respond(f"I successfully set {channel.mention} as chatbot channel. You can remove it by using `chatbot remove`.")

    @chatbot.command()
    async def remove(self, ctx: discord.ApplicationContext):
        if not ctx.author.guild_permissions.manage_channels:
            raise commands.MissingPermissions(["ManageChannels"])
            
        chatbot_channel = db.fetch("SELECT channel_id FROM chatbot WHERE guild_id = %s;", (ctx.guild.id,))
        if chatbot_channel:
            db.modify(f"DELETE FROM chatbot WHERE guild_id = {ctx.guild.id};")
            await ctx.respond(f"I successfully removed <#{chatbot_channel}> as chatbot channel.")
        else:
            await ctx.respond("A chatbot channel isn't set. You can add one by using `chatbot set`")


def setup(bot):
    bot.add_cog(Chatbot(bot))
