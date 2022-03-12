import discord
import asyncio
from discord.ext import commands
from struc import database
db = database

class Moderation(commands.Cog):
    """
    Commands related to moderating the server.
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.command(help="Purges the channel.")
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, limit: int):
        if limit > 200 or limit < 1:
            await ctx.reply("The minimium value is **`1`** and the maximum **`200`**.", mention_author=False)
            return
        msgs_deleted = await ctx.channel.purge(limit=limit+1)
        msgs_deleted = len(msgs_deleted)-1
        if msgs_deleted == 1:
            text = "one message"
        elif msgs_deleted <1:
            text = "no message"
        else:
            text = f"**`{msgs_deleted}`** messages"
        m = await ctx.send(f"Successfully deleted {text}. This message will be deleted in 5 seconds.")
        await asyncio.sleep(5)
        await m.delete()

    # Warning System

    @commands.group(name='warns', invoke_without_command=True, help="Warning system")
    @commands.has_permissions(moderate_members=True)
    async def warns(self, ctx):
        await ctx.reply("Use the help command.",mention_author=False)

    @commands.command(help="Warns someone.")
    @commands.has_permissions(moderate_members=True)
    async def warn(self, ctx, user: discord.Member = None, *,   reason="**No reason specified.**"):
        if not user:
            await ctx.reply("Please specify a member.", mention_author=False)
            return

        prev_warn_id = db.fetch("guild", "SELECT id FROM warnings ORDER BY id DESC LIMIT 1")

        if prev_warn_id is None:
            prev_warn_id = -1

        next_warn_id = prev_warn_id + 1

        db.modify("guild", "INSERT INTO warnings VALUES(?,?,?,?,?)", (ctx.guild.id, user.id, ctx.author.id, reason, next_warn_id))
        await ctx.reply(f"**`User`**: {user.mention}\n**`Reason`**: {reason}", mention_author=False)


    @warns.command(aliases=["list"], help="Shows someone's warnings.")
    @commands.has_permissions(moderate_members=True)
    async def view(self, ctx):
        fetch = db.fetchall("guild", "SELECT * FROM warnings WHERE guild_id = ?", (ctx.guild.id,))
        warning_count = len(db.fetchall("guild", "SELECT guild_id FROM warnings WHERE guild_id = ?", (ctx.guild.id,)))

        fetch_embed = discord.Embed(title=f"Warnings in {ctx.guild.name}", color=discord.Color(0xF37F7F), description="")
        fetch_embed.description = f"**Total count:** {warning_count}\n"
        for warning in fetch:
            fetch_embed.description += f"User: <@{warning[1]}>\nModerator: <@{warning[2]}>\nID: {warning[4]}\nReason: ```{warning[3]}```\n"

        if fetch is None or fetch == () or fetch == []:
            fetch_embed.description = "No users have been warned!"

        await ctx.reply(embed=fetch_embed, mention_author=False)


    @warns.command(aliases=["delete", "rm", "del"], help="Removes a warning from someone.")
    @commands.has_permissions(manage_channels=True)
    async def remove(self, ctx, warn_id: int = None):
        if warn_id is None:
            await ctx.reply("Please specify the warning ID.\nYou can find this ID by using `warn list`", mention_author=False)
            return

        db.modify("guild", "DELETE FROM warnings WHERE guild_id = ? AND id = ?", (ctx.guild.id, warn_id,))
        await ctx.reply(f"Successfully removed warning with ID `{warn_id}`.", mention_author=False)

    @warns.command(help="Resets someone's warnings.")
    @commands.has_permissions(manage_channels=True)
    async def reset(self, ctx, user: discord.Member = None):
        if not user:
            await ctx.reply("Please specify a member.", mention_author=False)
            return
        
        await ctx.reply(f"Deleting all warnings of <@{user.id}>...", mention_author=False)
        db.modify("guild", "DELETE FROM warnings WHERE user_id = ? AND guild_id = ?", (user.id, ctx.guild.id,))
        await ctx.reply(f"Successfully removed all warnings of <@{user.id}>.", mention_author=False)

def setup(bot):
    bot.add_cog(Moderation(bot))
