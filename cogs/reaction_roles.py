import discord
from discord.ext import commands
from struc import db
from discord.commands import (
    slash_command,
    Option
)

class ReactionRoles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command()
    async def set_reaction_role(self, ctx: discord.ApplicationContext, message_id: Option(int, "The message's ID"), role: Option(discord.Role, "The role to be given on reaction"), emoji: Option(str, "The emoji that is to be reacted with")):
        if not ctx.author.guild_permissions.administrator:
            raise commands.MissingPermissions(["Administrator"])

        exists = db.fetch("SELECT * FROM reaction_roles WHERE message_id = %s AND emoji = %s;", (message_id, emoji))

        if exists is not None:
            await ctx.respond("This message already was set to a reaction role.")
            return

        message = await ctx.fetch_message(message_id)

        if message is None:
            await ctx.respond("Please provide an actual message ID.")
            return

        db.modify("INSERT INTO reaction_roles(guild_id, message_id, role_id, emoji) VALUES(%s,%s,%s,%s);", (ctx.guild.id, message.id, role.id, emoji))

        await message.add_reaction(emoji)

        await ctx.respond("The reaction role has been set up.")

    @slash_command()
    async def list_reaction_roles(self, ctx: discord.ApplicationContext):
        if not ctx.author.guild_permissions.administrator:
            raise commands.MissingPermissions(["Administrator"])

        fetch = db.fetchall("SELECT * FROM reaction_roles WHERE guild_id = %s;", (ctx.guild.id,))

        fetch_embed = discord.Embed(title=f"Reaction roles in {ctx.guild.name}", color=discord.Color(0xF37F7F), description="")
        if fetch and fetch != () and fetch != []:
            for reaction_role in fetch:
                fetch_embed.description += f"\nMessage ID: {reaction_role[0]}\nRole: <@&{reaction_role[1]}>\nEmoji: {reaction_role[2]}\n"

        if fetch is None or fetch == () or fetch == []:
            fetch_embed.description = "No reaction roles have been added."

        await ctx.respond(embed=fetch_embed)

    @slash_command()
    async def remove_reaction_role(self, ctx: discord.ApplicationContext, message_id: Option(int, "The message's ID"), emoji: Option(str, "The emoji reaction which is to be removed")):
        if not ctx.author.guild_permissions.administrator:
            raise commands.MissingPermissions(["Administrator"])

        exists = db.fetch("SELECT * FROM reaction_roles WHERE message_id = %s AND emoji = %s;", (message_id, emoji))

        if exists is None:
            await ctx.respond("That reaction role does not exist!")
            return

        db.modify("DELETE FROM reaction_roles WHERE message_id = %s AND emoji = %s;", (message_id, emoji))

        msg = await ctx.fetch_message(message_id)

        if msg is not None:
            await msg.remove_reaction(emoji, self.bot.user)

        await ctx.respond(f"Successfully deleted the specified reaction role.")

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        msg_exists = db.fetch("SELECT * FROM reaction_roles WHERE message_id = %s AND emoji = %s;", (payload.message_id, str(payload.emoji)))

        if msg_exists:
            role_id = db.fetch("SELECT role_id FROM reaction_roles WHERE message_id = %s AND emoji = %s;", (payload.message_id, str(payload.emoji)))
            guild = discord.utils.find(lambda g : g.id == payload.guild_id, self.bot.guilds)
            
            role = discord.utils.get(guild.roles, id=role_id)

            if role is None:
                return

            member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)

            if member is not None and member.bot is False:
                try:
                    await member.add_roles(role)
                except discord.HTTPException:
                    pass

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        msg_exists = db.fetch("SELECT * FROM reaction_roles WHERE message_id = %s AND emoji = %s;", (payload.message_id, str(payload.emoji)))

        if msg_exists:
            role_id = db.fetch("SELECT role_id FROM reaction_roles WHERE message_id = %s AND emoji = %s;", (payload.message_id, str(payload.emoji)))
            guild = discord.utils.find(lambda g : g.id == payload.guild_id, self.bot.guilds)
            
            role = discord.utils.get(guild.roles, id=role_id)

            if role is None:
                return

            member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
            
            if member is not None and member.bot is False:
                try:
                    await member.remove_roles(role)
                except discord.HTTPException:
                    pass

def setup(bot):
    bot.add_cog(ReactionRoles(bot))