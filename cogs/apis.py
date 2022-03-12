from discord.ext import commands
import requests

class APIs(commands.Cog):
    """
    All API related commands.
    """
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(help="Sends a random image of a very cute fox")
    async def fox(self, ctx, opt=None):
        response = requests.get("https://randomfox.ca/floof/").json()
        fox_image_url = response["image"]
        if opt == 'dm':
            direct = await ctx.author.create_dm()
            await direct.send(fox_image_url)
            await ctx.message.add_reaction("☑️")
            return
        
        await ctx.reply(fox_image_url, mention_author=False)

def setup(bot):
    bot.add_cog(APIs(bot))
