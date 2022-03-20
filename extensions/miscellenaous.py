import lightbulb
from lightbulb import commands
import hikari
from struc import colors
import aiohttp

plugin = lightbulb.Plugin("Miscellenaous")

@plugin.command
@lightbulb.option("message", "Message to repeat", type=str)
@lightbulb.option("title", "Title of embed", type=str, required=False, default=None)
@lightbulb.option("url", "URL of the title", type=str, required=False, default=None)
@lightbulb.add_checks(lightbulb.has_guild_permissions(hikari.Permissions.KICK_MEMBERS))
@lightbulb.command("say", "Repeats your message")
@lightbulb.implements(lightbulb.SlashCommand)
async def say(ctx: lightbulb.ApplicationContext) -> None:
    # Check if the provided URL is valid, set the option to None if not
    url = ctx.options.url
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(ctx.options.url) as response:
                pass
    except aiohttp.ClientError:
        url = None

    say_embed = hikari.Embed(title=ctx.options.title, description=ctx.options.message, color=colors.default, url=url)
    await ctx.respond(embed=say_embed)

@plugin.command()
@lightbulb.command("ping", "Returns ping of the bot")
@lightbulb.implements(lightbulb.SlashCommand)
async def ping(ctx: lightbulb.ApplicationContext) -> None:
    await ctx.respond(f"🏓Pong! Latency: **{round(plugin.bot.heartbeat_latency*1000)}**ms.")

@plugin.command
@lightbulb.command("version", "Returns version of the bot")
@lightbulb.implements(lightbulb.SlashCommand)
async def version(ctx: lightbulb.ApplicationContext) -> None:
    await ctx.respond(f"You are currently using version 0.0.1")

@plugin.command
@lightbulb.option("member", "The member to get information about", type=hikari.Member, required=False, default=None)
@lightbulb.command("userinfo", "Get information about a member")
@lightbulb.implements(lightbulb.SlashCommand)
async def userinfo(ctx: lightbulb.ApplicationContext):
    member: hikari.Member = ctx.options.member or ctx.member
    
    member_roles = ""
    member_nickname = member.nickname or "No nickname"
    if plugin.bot.cache.get_presence(ctx.guild_id, member.id):
        member_activity: hikari.Activity = plugin.bot.cache.get_presence(ctx.guild_id, member.id)
    else:
        member_activity = ""
    #membery_activity_type = member_activity.type or "Doing"
    #member_activity = member_activity.name or "Nothing"

    created_at = member.created_at.strftime("%b %d, %Y, %H:%M")
    joined_at = member.joined_at.strftime("%b %d, %Y, %H:%M")

    userinfo_embed = hikari.Embed(color=colors.default)

    member_pfp_url = member.avatar_url or member.default_avatar_url

    userinfo_embed.set_author(name=f"{member} - {member_nickname}", icon=f"{member_pfp_url}")

    member_roles += "@everyone"
    roles = await member.fetch_roles()

    for role in roles:
        if role.id != ctx.guild_id:
            member_roles += f" <@&{role.id}>"

    userinfo_embed.add_field(name="ID", value=f"{member.id}")
    userinfo_embed.add_field(name="Created account on", value=f"{created_at}", inline=True)
    userinfo_embed.add_field(name=f"Joined {ctx.get_guild().name} on", value=f"{joined_at}", inline=True)
    userinfo_embed.add_field(name="Roles", value=f"{member_roles}", inline=True)
    userinfo_embed.add_field(name="Status", value=f"{str(member_activity.visible_status).capitalize()}")

    await ctx.respond(embed=userinfo_embed)

@plugin.command
@lightbulb.command("serverinfo", "Send information about this server")
@lightbulb.implements(lightbulb.SlashCommand)
async def serverinfo(ctx: lightbulb.ApplicationContext):
    server_info_embed = hikari.Embed(title=ctx.get_guild().name, color=colors.default)

    if ctx.get_guild().icon_url is not None:
        server_info_embed.set_thumbnail(ctx.get_guild().icon_url)

    humans = await plugin.bot.rest.fetch_members(ctx.get_guild()).filter(("is_bot", True)).count()
    bots = await plugin.bot.rest.fetch_members(ctx.get_guild()).filter(("is_bot", False)).count()

    voice_channels = (await plugin.bot.rest.fetch_guild_channels(ctx.get_guild())).filter("type", hikari.ChannelType.GUILD_VOICE).count()
    text_channels = (await plugin.bot.rest.fetch_guild_channels(ctx.get_guild())).filter("type", hikari.ChannelType.GUILD_TEXT).count()
    categories = (await plugin.bot.rest.fetch_guild_channels(ctx.get_guild())).filter("type", hikari.ChannelType.GUILD_CATEGORY).count()

    non_animated_emojis = (await plugin.bot.rest.fetch_guild_emojis(ctx.get_guild())).filter(("is_animated", False)).count()
    animated_emojis = (await plugin.bot.rest.fetch_guild_emojis(ctx.get_guild())).filter(("is_animated", True)).count()

    server_info_embed.description = f"**ID**: {ctx.get_guild().id}\n**Owner**: <@{ctx.get_guild().owner_id}>\n**Creation Time**: `{ctx.get_guild().created_at.strftime('%d-%m-%Y--%H-%M-%S')}`"
    server_info_embed.add_field(name="Members", value=f"Humans: {humans}\nBots: {bots}", inline=False)
    server_info_embed.add_field(name="Channels", value=f"🔊 Voice channels: {voice_channels}\n💬 Text Channels: {text_channels}\nCategories: {categories}", inline=False)
    server_info_embed.add_field(name="Emojis", value=f"Regular: {non_animated_emojis}\nAnimated: {animated_emojis}", inline=False)
    server_info_embed.add_field(name="Boosts", value=f"Boost Level: {ctx.get_guild().premium_tier}\nBoosts: {ctx.get_guild().premium_subscription_count}", inline=False)
    server_info_embed.add_field(name="Roles", value=f"Roles: {len(await ctx.get_guild().fetch_roles())}", inline=False)

def load(bot):
    bot.add_plugin(plugin)

def unload(bot):
    bot.unload_plugin(plugin)