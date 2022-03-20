import lightbulb
import hikari
from struc import db, colors
import asyncio

plugin = lightbulb.Plugin("Moderation")

@plugin.command
@lightbulb.option("limit", "Amount of messages to delete", type=int)
@lightbulb.add_checks(lightbulb.has_guild_permissions(hikari.Permissions.MANAGE_CHANNELS))
@lightbulb.command("clear", "Clears an amount of messages")
@lightbulb.implements(lightbulb.SlashCommand)
async def clear(ctx: lightbulb.ApplicationContext):

    if ctx.options.limit > 100 or ctx.options.limit < 1:
        await ctx.respond("The minimium value is **`1`** and the maximum **`200`**.")
        return

    msgs_deleted: int = 0
    try:
        iterator = plugin.bot.rest.fetch_messages(ctx.channel_id).limit(ctx.options.limit)
        async for messages in iterator.chunk(100):
            msgs_deleted += len(messages)
            await plugin.bot.rest.delete_messages(ctx.channel_id, messages)
    except hikari.ForbiddenError:
        pass
    msgs_deleted = msgs_deleted-1
    if msgs_deleted == 1:
        text = "one message"
    elif msgs_deleted <1:
        text = "no message"
    else:
        text = f"**`{msgs_deleted}`** messages"
    m = await ctx.respond(f"Successfully deleted {text}. This message will be deleted in 5 seconds.")
    await asyncio.sleep(5)
    try:
        await m.delete()
    except hikari.NotFoundError:
        pass

@plugin.command
@lightbulb.command("warns", "Warning system")
@lightbulb.implements(lightbulb.SlashCommandGroup)
async def warns(ctx: lightbulb.ApplicationContext):
    pass

@plugin.command
@lightbulb.option("member", "The member to warn", type=hikari.Member)
@lightbulb.option("reason", "Reason for warn", type=str)
@lightbulb.add_checks(lightbulb.has_guild_permissions(hikari.Permissions.MODERATE_MEMBERS))
@lightbulb.command("warn", "Warn a member")
@lightbulb.implements(lightbulb.SlashCommand)
async def warn(ctx: lightbulb.ApplicationContext):
    prev_warn_id = db.fetch("SELECT id FROM warnings ORDER BY id DESC LIMIT 1;")

    if prev_warn_id is None:
            prev_warn_id = -1

    next_warn_id = prev_warn_id + 1

    db.modify("INSERT INTO warnings VALUES(%s,%s,%s,%s,%s);", (ctx.guild_id, ctx.options.member.id, ctx.author.id, ctx.options.reason, next_warn_id))
    await ctx.respond(f"**Successfully warned** <@{ctx.options.member.id}>\n**`Reason`**: {ctx.options.reason}")

@warns.child
@lightbulb.add_checks(lightbulb.has_guild_permissions(hikari.Permissions.MODERATE_MEMBERS))
@lightbulb.command("list", "List all warns in this server")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def view(ctx: lightbulb.ApplicationContext):
    fetch = db.fetchall("SELECT * FROM warnings WHERE guild_id = %s;", (ctx.guild_id,))
    warning_count = len(db.fetchall("SELECT guild_id FROM warnings WHERE guild_id = %s;", (ctx.guild_id,)))

    fetch_embed = hikari.Embed(title=f"Warnings in {ctx.get_guild().name}", color=colors.default, description="")
    fetch_embed.description = f"**Total warns in this server:** {warning_count}\n"

    warned_users = db.fetchall("SELECT user_id FROM warnings WHERE guild_id = %s;", (ctx.guild_id,))

    warned_users = list(dict.fromkeys(warned_users))

    if fetch is not None:
        for user_id in warned_users:
            user_warns = db.fetchall("SELECT * FROM warnings WHERE guild_id = %s AND user_id = %s;", (ctx.guild_id, user_id))
            user = ctx.get_guild().get_member(user_id[0])
            if user is None:
                user = await plugin.bot.rest.fetch_user(user_id[0])
            user_warn_text = ""
            for warning in user_warns:
                user_warn_text += f"\nModerator: <@{warning[2]}>\nID: {warning[4]}\nReason: ```{warning[3]}```\n"
            fetch_embed.add_field(name=f"Warnings of {user.username}", value=f"Total: {len(user_warns)}{user_warn_text}", inline=False)
    else:
        fetch_embed.description = "No users have been warned!"

    await ctx.respond(embed=fetch_embed)

@warns.child
@lightbulb.option("warn_id", "The ID of the warning", type=int)
@lightbulb.add_checks(lightbulb.has_guild_permissions(hikari.Permissions.MODERATE_MEMBERS))
@lightbulb.command("remove", "Remove a warning")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def remove(ctx: lightbulb.ApplicationContext):
    db.modify("DELETE FROM warnings WHERE guild_id = %s AND id = %s;", (ctx.guild_id, ctx.options.warn_id,))
    await ctx.respond(f"Successfully removed warning with ID `{ctx.options.warn_id}`.")

@warns.child
@lightbulb.option("member", "Whose warnings to remove", type=hikari.Member)
@lightbulb.add_checks(lightbulb.has_guild_permissions(hikari.Permissions.MODERATE_MEMBERS))
@lightbulb.command("reset", "Remove all warnings of a user")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def reset(ctx: lightbulb.ApplicationContext):
    db.modify("DELETE FROM warnings WHERE user_id = %s AND guild_id = %s;", (ctx.options.member.id, ctx.guild_id,))
    await ctx.respond(f"Successfully removed all warnings of <@{ctx.options.member.id}>.")

def load(bot):
    bot.add_plugin(plugin)

def unload(bot):
    bot.unload_plugin(plugin)