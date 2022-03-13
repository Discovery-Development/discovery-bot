import discord
from discord.ext import commands
from struc import database
db = database

class ReactionRoles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(help="Makes a reaction add a role to the user")
    @commands.has_permissions(administrator=True)
    async def set_reaction_role(self, ctx, message_id: int, role: discord.Role, emoji: str):
        exists = db.fetch("guild", "SELECT * FROM reaction_roles WHERE message_id = ? AND emoji = ?", (message_id, emoji))

        if exists is not None:
            await ctx.reply("This message already was set to a reaction role.", mention_author=False)
            return

        message = await ctx.fetch_message(message_id)

        if message is None:
            await ctx.reply("Please provide an actual message ID.", mention_author=False)
            return

        db.modify("guild", "INSERT INTO reaction_roles(guild_id, message_id, role_id, emoji) VALUES(?,?,?,?)", (ctx.guild.id, message.id, role.id, emoji))

        await message.add_reaction(emoji)

        await ctx.reply("The reaction role has been set up.", mention_author=False)

    @commands.command(help="Lists all reaction roles in the guild.")
    @commands.has_permissions(administrator=True)
    async def list_reaction_roles(self, ctx):
        fetch = db.fetchall("guild", "SELECT * FROM reaction_roles WHERE guild_id = ?", (ctx.guild.id,))

        fetch_embed = discord.Embed(title=f"Reaction roles in {ctx.guild.name}", color=discord.Color(0xF37F7F), description="")
        for reaction_role in fetch:
            fetch_embed.description += f"\nMessage ID: {reaction_role[0]}\nRole: <@&{reaction_role[1]}>\nEmoji: {reaction_role[2]}\n"

        if fetch is None or fetch == () or fetch == []:
            fetch_embed.description = "No reaction roles have been added."

        await ctx.reply(embed=fetch_embed, mention_author=False)

    @commands.command(help="Remove a reaction role.")
    @commands.has_permissions(administrator=True)
    async def remove_reaction_role(self, ctx, message_id: int, emoji: str):
        exists = db.fetch("guild", "SELECT * FROM reaction_roles WHERE message_id = ? AND emoji = ?", (message_id, emoji))

        if exists is None:
            await ctx.reply("That reaction role does not exist!")
            return

        db.modify("guild", "DELETE FROM reaction_roles WHERE message_id = ? AND emoji = ?", (message_id, emoji))

        msg = await ctx.fetch_message(message_id)

        if msg is not None:
            await msg.remove_reaction(emoji, self.bot.user)

        await ctx.reply(f"Successfully deleted the specified reaction role.")

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        msg_exists = db.fetch("guild", "SELECT * FROM reaction_roles WHERE message_id = ? AND emoji = ?", (payload.message_id, str(payload.emoji)))

        if msg_exists:
            role_id = db.fetch("guild", "SELECT role_id FROM reaction_roles WHERE message_id = ? AND emoji = ?", (payload.message_id, str(payload.emoji)))
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
        msg_exists = db.fetch("guild", "SELECT * FROM reaction_roles WHERE message_id = ? AND emoji = ?", (payload.message_id, str(payload.emoji)))

        if msg_exists:
            role_id = db.fetch("guild", "SELECT role_id FROM reaction_roles WHERE message_id = ? AND emoji = ?", (payload.message_id, str(payload.emoji)))
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