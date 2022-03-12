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
from struc import database
db = database
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

        chatbot_guild = db.fetch("guild", "SELECT guild_id FROM chatbot")
        chatbot_channel = db.fetch("guild", "SELECT channel_id FROM chatbot WHERE guild_id = ?", (message.guild.id,))
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
                await message.reply(chat_message, mention_author=False)


    @commands.group(name='chatbot', invoke_without_command=True)
    @commands.has_permissions(manage_channels=True)
    async def chatbot(self, ctx):
        # await ctx.reply("This feature has been disabled.")
        # return
        await ctx.reply("Use `help chatbot` for help.", mention_author=False)
    
    @chatbot.command(help="Sets the channel for the chatbot.")
    @commands.has_permissions(manage_channels=True)
    async def set(self, ctx, channel: discord.TextChannel = None):
        # await ctx.reply("This feature has been disabled.")
        # return
        if not channel:
            channel = ctx.channel

        db.modify("guild", "INSERT OR REPLACE INTO chatbot(guild_id, channel_id) VALUES(?,?)", (ctx.guild.id, channel.id))
        await ctx.reply(f"I successfully set {channel.mention} as chatbot channel. You can remove it by using `chatbot remove`.", mention_author=False)


    @chatbot.command(help="Removes the chatbot from the current chanel.")
    @commands.has_permissions(manage_channels=True)
    async def remove(self, ctx):
        await ctx.reply("This feature has been disabled.")
        return
        chatbot_channel = db.fetch("guild", "SELECT channel_id FROM chatbot WHERE guild_ID = ?", (ctx.guild.id,))
        if chatbot_channel:
            db.modify("guild", "DELETE FROM chatbot WHERE guild_id = ?", (ctx.guild.id,))
            await ctx.reply(f"I successfully removed <#{chatbot_channel}> as chatbot channel.", mention_author=False)
        else:
            await ctx.reply("A chatbot channel isn't set. You can add one by using `chatbot set`", mention_author=False)


def setup(bot):
    bot.add_cog(Chatbot(bot))
