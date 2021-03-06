import discord
import main
import asyncio
import os
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from discord.ext import commands
import random
from struc import colors
from discord.commands import (
    slash_command,
    Option
)

class Fun(commands.Cog):
    """
    All the fun commands.
    """
    def __init__(self, bot):
        self.bot = bot

    @slash_command()
    async def trash(self, ctx: discord.ApplicationContext, target: Option(discord.User, "The user to move to the trash")):
        content = None
        if not target:
            target = ctx.author
        if target == ctx.author:
            content = "You want to delete yourself? Good!"
        if target == self.bot.user:
            await ctx.respond("I'm not trash.")
            return
        source_img = Image.open("./assets/trash.jpg")
        asset = target.avatar
        data = BytesIO(await asset.read())
        pic = Image.open(data)
        pic = pic.resize((203, 203))
        source_img.paste(pic, (116, 133))
        draw = ImageDraw.Draw(source_img)
        font = ImageFont.truetype("./assets/seguihis.ttf", 25)

        draw.text((12,8), f"Delete {target}",(0,0,0), font=font)
        source_img.save("./tmp/trash_gen.jpg")
        await ctx.respond(file = discord.File("./tmp/trash_gen.jpg", filename=f"trash_{target.id}.jpg"), content=content)
        os.remove("./tmp/trash_gen.jpg")
    
    @slash_command()
    async def m8ball(self, ctx: discord.ApplicationContext, question: Option(str, "Your question")):
        if not 5 <= len(question) <= 25:
            await ctx.respond("The minimium question lenght is **`5`** and the maximum **`25`**.")
            return
        responses = ["It is certain.",
                 "It is decidedly so.",
                 "Without a doubt.",
                 "Yes - definitely.",
                 "You may rely on it.",
                 "As I see it, yes.",
                 "Most likely.",
                 "Get out before I eat your cat",
                 "Yes.",
                 "Signs point to yes.",
                 "Reply hazy, try again.",
                 "Ask again later.",
                 "Cannot predict now.",
                 "Concentrate and ask again.",
                 "Don't count on it.",
                 "My reply is no.",
                 "My sources say no.",
                 "Very doubtful.",
                 "nerd",
                 "I AM TRYING TO SLEEP",
                 "idk",
                 "sorry I dont answer nerds"]

        answer = random.choice(responses)
        await ctx.respond(f'**`Your question:`** {question}\n\n**`My answer:`** "{answer}"')

    @slash_command()
    async def rip(self, ctx: discord.ApplicationContext, target: Option(discord.User, "The user... to ban from life")):
        if target is None:
            target = ctx.author

        tombstone_img = Image.open("./assets/death.jpg")
        pfp_asset = target.avatar
        pfp_data = BytesIO(await pfp_asset.read())
        pfp = Image.open(pfp_data)
        pfp = pfp.resize((116, 116))
        tombstone_img.paste(pfp, (260, 180))
        tombstone_img.save(f"./tmp/tombstone-{target.id}.jpg")

        await ctx.respond(file = discord.File(f"./tmp/tombstone-{target.id}.jpg", filename=f"rip_{target.id}.jpg"))
        os.remove(f"./tmp/tombstone-{target.id}.jpg")

    @slash_command()
    async def google(self, ctx: discord.ApplicationContext, text: Option(str, "The text to google")):
        if not 4 < len(text) < 40:
            await ctx.respond("Too short or too long")
            return

        userid = ctx.author.id
        google_screenshot = Image.open("./assets/google_search.jpg")

        draw = ImageDraw.Draw(google_screenshot)
        font = ImageFont.truetype("./assets/seguihis.ttf", 16)

        draw.text((324,237), text,(49,49,49), font=font)
        google_screenshot.save(f"./tmp/google-{userid}.jpg")
        await ctx.respond(file = discord.File(f"./tmp/google-{userid}.jpg", filename=f"google_{userid}.jpg"))
        os.remove(f"./tmp/google-{userid}.jpg")

    
    @slash_command()
    async def ldva(self, ctx):
        embed = discord.Embed(
            title="Lies die verfickte Anleitung!",
            description="Das angels??chsiche Akronym \"Read the f*ing manual\" (ins Deutsche ??bersetzt bedeutet jenes "
                        "etwa \"Lies die verdammte Anleitung\") mag anfangs zwar ziemlich r??de erscheinen, "
                        "jedoch existiert es haupts??chlich, um l??ngere Konversationen, die aufgrund eines bereits "
                        "gekl??rten Problemes entstehen k??nnten, zu vermeiden und Novizen das eigenst??ndige Beschaffen "
                        "hilfreicher Informationen zu vermitteln. Es wird verwendet, wenn die Antwort der gestellten "
                        "Frage bzw. die L??sung des gegebenen Problemes durch nur kurzes Suchen in einer "
                        "Dokumentation, Anleitung o.??. gefunden werden kann. Solche Dokumentationen und "
                        "Gebrauchsanweisungen sind meist von den Entwicklern selbst verfasst und sollten stets als "
                        "erste Informationsquelle bei jeglichen Problemen in Betracht gezogen werden.", 
            colour=discord.Colour.orange())
        async with ctx.typing():
            await asyncio.sleep(1.5)
        await ctx.respond(embed=embed)
    
    
    @slash_command()
    async def rtfm(self, ctx):
        embed = discord.Embed(
            title="Read the f*cking manual!",
            description="The acronym \"Read the f*ing manual\" may seem rather rude at first, but it exists mainly to "
                        "avoid lengthy conversations that could arise due to a problem that has already been solved "
                        "and to teach novices how to obtain helpful information on their own. It is used when the "
                        "answer to the question asked or the solution to the given problem can be found by only a "
                        "brief search in a documentation, manual or similar. Such documentation and instructions are "
                        "usually written by the developers themselves and should always be considered as the first "
                        "source of information for any problem.",
            colour=discord.Colour.orange())
        async with ctx.typing():
            await asyncio.sleep(1.5)
        await ctx.respond(embed=embed)

    @slash_command()
    async def clown(self, ctx: discord.ApplicationContext, target: Option(discord.User, "The user to make a clown")):
        if not target:
            target = ctx.author

        clown_image = Image.open("./assets/clown_license.jpeg")

        pfp_asset = target.avatar
        pfp_data = BytesIO(await pfp_asset.read())
        pfp = Image.open(pfp_data)
        pfp = pfp.resize((170, 170))

        draw = ImageDraw.Draw(clown_image)
        font = ImageFont.truetype("./assets/seguihis.ttf", 24)

        clown_image.paste(pfp, (130, 120))
        draw.text((360,230), f"{target}", (0,0,0), font=font)
        clown_image.save(f"./tmp/clown-{target.id}.jpg")

        await ctx.respond(file = discord.File(f"./tmp/clown-{target.id}.jpg", filename=f"clown-{target.id}.jpg"))
        os.remove(f"./tmp/clown-{target.id}.jpg")

def setup(bot):
    bot.add_cog(Fun(bot))
