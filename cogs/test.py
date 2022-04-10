# this cog is only used for testing purposes
import discord 
from discord.ext import commands
import requests
from PIL import Image, ImageOps, ImageDraw
from datetime import datetime
from struc import colors
import json
from discord.commands import (
    slash_command,
    Option
)

class Test(commands.Cog):
    """
    Some other commands
    """

    def __init__(self, bot):
        self.bot = bot
    

    @slash_command(help="Apply to join our team.")
    async def team(self, ctx: discord.ApplicationContext):
        await ctx.message.delete()
        embedd = discord.Embed(title="Be a part of our team", colour=discord.Colour(
            0xf79800), timestamp=datetime.now())
        # embedd.set_thumbnail(url="https://i.ibb.co/FxPZc8Y/logoideadiscovery.png")
        embedd.set_footer(text="Last edited")
        embedd.description = """
        You can join our team by sending an application to one of the **owners** of this server.
        We are currently looking for any kind of team members: Developer, Moderator, etc. If you are interested, feel free to contact us!
        
        """
        await ctx.respond(embed=embedd)

    @slash_command(help="Sends a changelog of the bot.")
    async def changelog(self, ctx):
        embed = discord.Embed(title="v2.1.0 - GalacticHippo", timestamp=datetime.now(), color=colors.default)
        embed.description = """
        **Biggest release yet**
            • Ticket system
            • Warning system
            • Added Uptimerobot connection
            • Lots of fun commands, including `trash`, `m8ball`, `rip`, `google`, `ldva`, `rtfm`, `clown`
            • Added more miscellenaous commands
            • A help command
            • An error handler (finally)
            • *A lot* of bug fixes
        """ 
        embed.set_thumbnail(
            url="https://i.ibb.co/n3Dd1h9/5a5a8a2214d8c4188e0b08e4.png")
        await ctx.respond(embed=embed, content="<@&937389035343712327>")



    @slash_command(help="🤫")
    async def sussy(self, ctx: discord.ApplicationContext, member: discord.User=None):
        if member is None:
            member = ctx.author

        with requests.get(member.avatar.url) as r:
            img_data = r.content

        with open(f"./tmp/profile-{member.id}.jpg", "wb") as handler:
            handler.write(img_data)

        img = Image.open(f"./tmp/profile-{member.id}.jpg")
        img = img.resize((120, 120));
        bigsize = (img.size[0] * 3, img.size[1] * 3)
        mask = Image.new('L', bigsize, 0)
        draw = ImageDraw.Draw(mask) 
        draw.ellipse((0, 0) + bigsize, fill=255)
        mask = mask.resize(img.size, Image.ANTIALIAS)
        img.putalpha(mask)

        output = ImageOps.fit(img, mask.size, centering=(0.5, 0.5))
        output.putalpha(mask)
        output.save(f"./tmp/profile-output-{member.id}.png")

        await ctx.respond(file = discord.File(f"./tmp/profile-output-{member.id}.png", filename=f"profile-output-{ctx.author.id}.png"))

def setup(bot):
    bot.add_cog(Test(bot))
