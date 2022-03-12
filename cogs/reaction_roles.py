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

        db.modify("guild", "INSERT INTO reaction_roles(message_id, role_id, emoji) VALUES(?,?,?)", (message.id, role.id, emoji))

        await message.add_reaction(emoji)

        await ctx.reply("The reaction role has been set up.", mention_author=False)

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