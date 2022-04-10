import discord
import asyncio
from discord.ext import commands
from struc import db, colors
from discord.commands import (
    slash_command,
    Option,
    SlashCommandGroup,
    permissions
)


class Moderation(commands.Cog):
    """
    Commands related to moderating the server.
    """
    def __init__(self, bot):
        self.bot = bot

    @slash_command()
    async def purge(self, ctx: discord.ApplicationContext, limit: Option(str, "The amount of messages to delete")):
        if not ctx.author.guild_permissions.manage_channels:
            raise commands.MissingPermissions(["ManageChannels"])

        limit = int(limit)

        if limit > 100 or limit < 1:
            await ctx.respond("The minimium value is **`1`** and the maximum **`200`**.")
            return
        try:
            msgs_deleted = await ctx.channel.purge(limit=limit+1)
        except discord.HTTPException:
            pass
        msgs_deleted = len(msgs_deleted)-1
        if msgs_deleted == 1:
            text = "one message"
        elif msgs_deleted <1:
            text = "no message"
        else:
            text = f"**`{msgs_deleted}`** messages"
        m = await ctx.respond(f"Successfully deleted {text}. This message will be deleted in 5 seconds.")
        await asyncio.sleep(5)
        try:
            await m.message.delete()
        except discord.HTTPException:
            pass

    # Warning System

    warns = SlashCommandGroup("warns", "Warning system")

    @slash_command()
    async def warn(self, ctx: discord.ApplicationContext, user: Option(discord.Member, "The member to warn"), reason: Option(str, "Reason for warn", required=False, default="No reason specified.")):
        if not ctx.author.guild_permissions.moderate_members:
            raise commands.MissingPermissions(["ModerateMembers"])
            
        if not user:
            await ctx.respond("Please specify a member.")
            return

        prev_warn_id = db.fetch("SELECT id FROM warnings ORDER BY id DESC LIMIT 1;")

        if prev_warn_id is None:
            prev_warn_id = -1

        next_warn_id = prev_warn_id + 1

        db.modify("INSERT INTO warnings VALUES(%s,%s,%s,%s,%s);", (ctx.guild.id, user.id, ctx.author.id, reason, next_warn_id))
        await ctx.respond(f"**`User`**: {user.mention}\n**`Reason`**: {reason}")


    @warns.command()
    async def list(self, ctx: discord.ApplicationContext):
        if not ctx.author.guild_permissions.moderate_members:
            raise commands.MissingPermissions(["ModerateMembers"])

        fetch = db.fetchall("SELECT * FROM warnings WHERE guild_id = %s;", (ctx.guild.id,))
        warning_count = len(db.fetchall("SELECT guild_id FROM warnings WHERE guild_id = %s;", (ctx.guild.id,)))

        fetch_embed = discord.Embed(title=f"Warnings in {ctx.guild.name}", color=colors.default, description="")
        fetch_embed.description = f"**Total warns in this server:** {warning_count}\n"

        users = db.fetchall("SELECT user_id FROM warnings WHERE guild_id = %s;", (ctx.guild.id,))

        users = list(dict.fromkeys(users))

        for user_id in users:
            user_warns = db.fetchall("SELECT * FROM warnings WHERE guild_id = %s AND user_id = %s;", (ctx.guild.id, user_id))
            user = await self.bot.fetch_user(user_id[0])
            user_warn_text = ""
            for warning in user_warns:
                user_warn_text += f"\nModerator: <@{warning[2]}>\nID: {warning[4]}\nReason: ```{warning[3]}```\n"
            fetch_embed.add_field(name=f"Warnings of {user.name}", value=f"Total: {len(user_warns)}{user_warn_text}", inline=False)

        #for warning in fetch:
        #    fetch_embed.description += f"User: <@{warning[1]}>\nModerator: <@{warning[2]}>\nID: {warning[4]}\nReason: ```{warning[3]}```\n"

        if fetch is None or fetch == () or fetch == []:
            fetch_embed.description = "No users have been warned!"

        await ctx.respond(embed=fetch_embed)


    @warns.command()
    async def remove(self, ctx: discord.ApplicationContext, warn_id: Option(str, "The ID of the warn")):
        if not ctx.author.guild_permissions.moderate_members:
            raise commands.MissingPermissions(["ModerateMembers"])

        warn_id = int(warn_id)

        if warn_id is None:
            await ctx.respond("Please specify the warning ID.\nYou can find this ID by using `warns list`")
            return

        db.modify("DELETE FROM warnings WHERE guild_id = %s AND id = %s;", (ctx.guild.id, warn_id,))
        await ctx.respond(f"Successfully removed warning with ID `{warn_id}`.")

    @warns.command()
    async def reset(self, ctx: discord.ApplicationContext, user: Option(discord.Member, "The member's warns whose to reset")):
        if not ctx.author.guild_permissions.moderate_members:
            raise commands.MissingPermissions(["ModerateMembers"])

        if not user:
            await ctx.respond("Please specify a member.")
            return
        
        db.modify("DELETE FROM warnings WHERE user_id = %s AND guild_id = %s;", (user.id, ctx.guild.id,))
        await ctx.respond(f"Successfully removed all warnings of <@{user.id}>.")

def setup(bot):
    bot.add_cog(Moderation(bot))
