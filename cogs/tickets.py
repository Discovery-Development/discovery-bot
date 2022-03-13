import asyncio
from click import style
import discord
from discord.ext import commands
from struc import database, funcs, colors
from discord.ui import Button, Select,View
import os
db = database

class ticket_components(View):
    def __init__(self):
        super().__init__()
        self.timeout = None

    @discord.ui.button(label="✖ Close", style=discord.ButtonStyle.red)
    async def close_ticket(self, button: Button, interaction: discord.Interaction):
        db.modify("guild", f"UPDATE ticket_data SET closed_by_id = ? WHERE channel_id = ?", (interaction.user.id, interaction.channel.id))
        db.modify("guild", f"UPDATE ticket_data SET close_time = ? WHERE channel_id = ?", (str(funcs.get_cur_time()), interaction.channel.id))
        
        ticket_log_channel_id = db.fetch("guild", f"SELECT ticket_log_channel_id FROM tickets WHERE guild_id = {interaction.guild.id}")

        ticket_log_channel = discord.utils.get(interaction.guild.text_channels, id=ticket_log_channel_id)

        if ticket_log_channel is not None:
            ticket_name = db.fetch("guild", f"SELECT name FROM ticket_data WHERE channel_id = {interaction.channel.id}")

            ticket_creator_id = db.fetch("guild", f"SELECT creator_id FROM ticket_data WHERE channel_id = {interaction.channel.id}")

            ticket_creation_reason = db.fetch("guild", f"SELECT ticket_open_reason FROM ticket_data WHERE channel_id = {interaction.channel.id}")

            ticket_open_time = db.fetch("guild", f"SELECT open_time FROM ticket_data WHERE channel_id = {interaction.channel.id}")

            ticket_closed_by_id = db.fetch("guild", f"SELECT closed_by_id FROM ticket_data WHERE channel_id = {interaction.channel.id}")

            ticket_close_time = db.fetch("guild", f"SELECT close_time FROM ticket_data WHERE channel_id = {interaction.channel.id}")

            ticket_transcript = db.fetch("guild", f"SELECT transcript FROM ticket_data WHERE channel_id = {interaction.channel.id}")

            ticket_log_embed = discord.Embed(title="Ticket has been closed.", description=f"Ticket name: **{ticket_name}**\nTicket creator: <@{ticket_creator_id}>\nTicket creation reason: `{ticket_creation_reason}`\nTicket opened at: **{ticket_open_time}**\nClosed by: <@{ticket_closed_by_id}>\nTicket closed at: **{ticket_close_time}**\nTicket closing reason: ```Undefined```", color=colors.default)

            with open(f"./tmp/ticket-{ticket_creator_id}-{interaction.guild.id}.log", "w", encoding="utf_8_sig") as f:
                f.write(str(ticket_transcript))

            await ticket_log_channel.send(embed=ticket_log_embed, file=discord.File(f"./tmp/ticket-{ticket_creator_id}-{interaction.guild.id}.log", filename=f"transcript-{ticket_name}.log"))
            os.remove(f"./tmp/ticket-{ticket_creator_id}-{interaction.guild.id}.log")

        db.modify("guild", f"DELETE FROM ticket_data WHERE channel_id = {interaction.channel.id}")
        await interaction.response.send_message(content="This ticket will be closed in 3 seconds...")
        await asyncio.sleep(3)
        await interaction.channel.delete(reason=f"Ticket was closed by {interaction.user}.")

class choose_ticket_reason(View):
    def __init__(self):
        super().__init__()
        self.value = None
        self.timeout = 10
        self.channel_id = None

    options = [
            discord.SelectOption(label="Support", description="Your ticket will be about support.", emoji="⛑"),
            discord.SelectOption(label="Question", description="Your ticket will be about a question.", emoji="❓"),
            discord.SelectOption(label="Report", description="Your ticket will be about a report.", emoji="♻"),
            discord.SelectOption(label="Application", description="Your ticket will be about an application.", emoji="🎯")
    ]

    @discord.ui.select(options=options, placeholder="Choose the reason you're opening a ticket.", min_values=1, max_values=1)
    async def choose_reason(self, select: Select,  interaction: discord.Interaction):
        ticket_category_id = db.fetch("guild", f"SELECT ticket_category_id FROM tickets WHERE guild_id = {interaction.guild.id}")

        ticket_category = discord.utils.get(interaction.guild.categories, id=ticket_category_id)

        ticket_open_message = db.fetch("guild", f"SELECT ticket_open_message FROM tickets WHERE guild_id = {interaction.guild.id}")

        if ticket_open_message is None:
            sql = f"UPDATE tickets SET ticket_open_message = ? WHERE guild_id = ?"
            binds = ("Moderators will soon be with you, please be patient!", interaction.guild.id)
            db.modify("guild", sql, binds)
        
        ticket_open_message = db.fetch("guild", f"SELECT ticket_open_message FROM tickets WHERE guild_id = {interaction.guild.id}")

        ticket_opened_embed = discord.Embed(title="Your Ticket", description=ticket_open_message, color=colors.default)

        ticket_channel = await interaction.guild.create_text_channel(name=f"ticket-{interaction.user.name}", category=ticket_category)

        view = ticket_components()

        await ticket_channel.send(embed=ticket_opened_embed, view=view)

        binds = (interaction.guild.id, ticket_channel.id, str(ticket_channel.name), interaction.user.id, str(funcs.get_cur_time()), str(select.values[0]))

        db.modify("guild","INSERT INTO ticket_data(guild_id, channel_id, name, creator_id, open_time, ticket_open_reason) VALUES(?,?,?,?,?,?)", binds)

        await ticket_channel.set_permissions(interaction.user, view_channel=True, read_message_history=True, send_messages=True, attach_files=True)

        ticket_log_channel_id = db.fetch("guild", f"SELECT ticket_log_channel_id FROM tickets WHERE guild_id = {interaction.guild.id}")

        ticket_log_channel = discord.utils.get(interaction.guild.text_channels, id=ticket_log_channel_id)

        if ticket_log_channel is not None:
            ticket_opened_embed_log = discord.Embed(title="Ticket has been opened.", description=f"Ticket channel: <#{ticket_channel.id}>\nTicket name: `{ticket_channel.name}`\nOpened by: <@{interaction.user.id}>\nOpened at: **{str(funcs.get_cur_time())}**\nTicket creation reason: `{select.values[0]}`",color=colors.default)

            await ticket_log_channel.send(embed=ticket_opened_embed_log)

        self.value = True
        self.channel_id = ticket_channel.id
        self.stop()

class create_ticket_button(Button):
    def __init__(self):
        super().__init__(
            label = "Create ticket",
            style = discord.ButtonStyle.primary,
            custom_id = "create_ticket_button"
        )

    async def callback(self, interaction: discord.Interaction):
        tickets_by_author_in_guild = db.fetch("guild", f"SELECT guild_id FROM ticket_data WHERE guild_id = {interaction.guild.id} AND creator_id = {interaction.user.id}")

        if tickets_by_author_in_guild is not None:
            await interaction.response.send_message(content="You already have a ticket open on this server.", ephemeral=True)
            return

        ticket_mod_roles = db.fetch("guild", f"SELECT ticket_mod_roles FROM tickets WHERE guild_id = {interaction.guild.id}")
        ticket_category_id = db.fetch("guild", f"SELECT ticket_category_id FROM tickets WHERE guild_id = {interaction.guild.id}")

        ticket_category = discord.utils.get(interaction.guild.categories, id=ticket_category_id)

        if ticket_mod_roles is None or ticket_category is None:
            await interaction.response.send_message(f"The ticket system on this server has not been set up yet!", ephemeral=True)
            return

        view = choose_ticket_reason()
        await interaction.response.send_message(view=view, ephemeral=True)

        await view.wait()
        if view.value is None:
            await interaction.edit_original_message(content="Ticket opening request has timed out.", view=None)
        elif view.value is True:
            ticket_channel_id = db.fetch("guild", f"SELECT channel_id FROM ticket_data WHERE channel_id = {view.channel_id}")
            await interaction.edit_original_message(content=f"Your ticket has been opened, check it out at <#{ticket_channel_id}>", view=None)
        else:
            await interaction.edit_original_message(content="An unkown error has occured.", view=None)

        
class Tickets(commands.Cog):
    """
    Commands related to the ticket system.
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.command(help="Sends the button to open a ticket.")
    @commands.has_permissions(administrator=True)
    async def ticket_embed(self, ctx):
        create_ticket_embed = discord.Embed(title="Ticket", description=f"Press the button below to create a ticket.", color=colors.default)

        view = View(timeout=None)
        view.add_item(create_ticket_button())

        await ctx.send(embed=create_ticket_embed, view=view)

    @commands.command(help="Sets the roles to answer tickets.")
    @commands.has_permissions(administrator=True)
    async def setticketmodroles(self, ctx, mod_roles: str):
        mod_roles = mod_roles.replace(" ", "")
        mod_roles = mod_roles.split(";")

        mod_roles_modified = ""

        for mod_role in mod_roles:
            if mod_role == "":
                continue
            mod_role = await commands.RoleConverter().convert(ctx, mod_role)
            mod_roles_modified += f"{mod_role.id};"

        guild = db.fetch("guild", f"SELECT guild_id FROM tickets WHERE guild_id = {ctx.guild.id}")

        if guild is None:
            sql = f"INSERT INTO tickets(guild_id, ticket_mod_roles) VALUES(?,?)"
            binds = (ctx.guild.id, mod_roles_modified)
        elif guild is not None:
            sql = f"UPDATE tickets SET ticket_mod_roles = ? WHERE guild_id = ?"
            binds = (mod_roles_modified, ctx.guild.id)
        
        db.modify("guild", sql, binds)

        await ctx.reply(f"Successfully set ticket moderation roles.", mention_author=False)


    @commands.command(help="Set the category to open tickets in.")
    @commands.has_permissions(administrator=True)
    async def setticketcategory(self, ctx, ticket_category: discord.CategoryChannel):
        ticket_mod_roles_txt = db.fetch("guild", f"SELECT ticket_mod_roles FROM tickets WHERE guild_id = {ctx.guild.id}")

        if ticket_mod_roles_txt is None:
            await ctx.reply(f"Please set up ticket moderation roles first!", mention_author=False)

        ticket_mod_roles = str(ticket_mod_roles_txt).split(";")

        default_role = ctx.guild.default_role
        await ticket_category.set_permissions(default_role, view_channel=False, send_messages=False, read_message_history=False, attach_files=False)

        for ticket_mod_role in ticket_mod_roles:
            if ticket_mod_role == "":
                continue
            ticket_mod_role = discord.utils.get(ctx.guild.roles, id=int(ticket_mod_role))
            if ticket_mod_role is None:
                continue
            await ticket_category.set_permissions(ticket_mod_role, view_channel=True, send_messages=True, read_message_history=True, attach_files=True)

        guild = db.fetch("guild", f"SELECT guild_id FROM tickets WHERE guild_id = {ctx.guild.id}")

        if guild is None:
            sql = f"INSERT INTO tickets(guild_id, ticket_category_id) VALUES(?,?)"
            binds = (ctx.guild.id, ticket_category.id)
        elif guild is not None:
            sql = f"UPDATE tickets SET ticket_category_id = ? WHERE guild_id = ?"
            binds = (ticket_category.id, ctx.guild.id)
        
        db.modify("guild", sql, binds)

        ticket_category_id = db.fetch("guild", f"SELECT ticket_category_id FROM tickets WHERE guild_id = {ctx.guild.id}")

        await ctx.send(f"The ticket category has been set to <#{ticket_category_id}>")

    @commands.command(help="Sets the channel to send ticket logs.")
    @commands.has_permissions(administrator=True)
    async def setticketlogchannel(self, ctx, ticket_log_channel: discord.TextChannel):
        guild = db.fetch("guild", f"SELECT guild_id FROM tickets WHERE guild_id = {ctx.guild.id}")

        if guild is None:
            sql = f"INSERT INTO tickets(guild_id, ticket_log_channel_id) VALUES(?,?)"
            binds = (ctx.guild.id, ticket_log_channel.id)
        elif guild is not None:
            sql = f"UPDATE tickets SET ticket_log_channel_id = ? WHERE guild_id = ?"
            binds = (ticket_log_channel.id, ctx.guild.id)

        db.modify("guild", sql, binds)

        ticket_log_channel_id = db.fetch("guild", f"SELECT ticket_log_channel_id FROM tickets WHERE guild_id = {ctx.guild.id}")

        await ctx.send(f"The ticket log channel has been set to <#{ticket_log_channel_id}>")

    @commands.command(help="Sets the message that will appear when you open a ticket.")
    @commands.has_permissions(administrator=True)
    async def setticketopenmsg(self, ctx, *, ticket_open_message: str):
        guild = db.fetch("guild", f"SELECT guild_id FROM tickets WHERE guild_id = {ctx.guild.id}")

        if guild is None:
            sql = f"INSERT INTO tickets(guild_id, ticket_open_message) VALUES(?,?)"
            binds = (ctx.guild.id, ticket_open_message)
        elif guild is not None:
            sql = f"UPDATE tickets SET ticket_open_message = ? WHERE guild_id = ?"
            binds = (ticket_open_message, ctx.guild.id)

        db.modify("guild", sql, binds)

        ticket_open_message = db.fetch("guild", f"SELECT ticket_open_message FROM tickets WHERE guild_id = {ctx.guild.id}")

        await ctx.send(f"The ticket open message has been set to ```{ticket_open_message}```")
    
    @commands.command(help="Closes a ticket.")
    async def close(self, ctx, reason="No reason was specified."):
        ticket = db.fetch("guild", f"SELECT channel_id FROM ticket_data WHERE channel_id = {ctx.channel.id}")

        if ticket is None:
            await ctx.reply("This channel is not a ticket!", mention_author=False)
            return

        db.modify("guild", f"UPDATE ticket_data SET closed_by_id = ? WHERE channel_id = ?", (ctx.author.id, ctx.channel.id))
        db.modify("guild", f"UPDATE ticket_data SET close_time = ? WHERE channel_id = ?", (str(funcs.get_cur_time()), ctx.channel.id))
        
        ticket_log_channel_id = db.fetch("guild", f"SELECT ticket_log_channel_id FROM tickets WHERE guild_id = {ctx.guild.id}")

        ticket_log_channel = discord.utils.get(ctx.guild.text_channels, id=ticket_log_channel_id)

        if ticket_log_channel is not None:
            ticket_name = db.fetch("guild", f"SELECT name FROM ticket_data WHERE channel_id = {ctx.channel.id}")

            ticket_creator_id = db.fetch("guild", f"SELECT creator_id FROM ticket_data WHERE channel_id = {ctx.channel.id}")

            ticket_creation_reason = db.fetch("guild", f"SELECT ticket_open_reason FROM ticket_data WHERE channel_id = {ctx.channel.id}")

            ticket_open_time = db.fetch("guild", f"SELECT open_time FROM ticket_data WHERE channel_id = {ctx.channel.id}")

            ticket_closed_by_id = db.fetch("guild", f"SELECT closed_by_id FROM ticket_data WHERE channel_id = {ctx.channel.id}")

            ticket_close_time = db.fetch("guild", f"SELECT close_time FROM ticket_data WHERE channel_id = {ctx.channel.id}")

            ticket_transcript = db.fetch("guild", f"SELECT transcript FROM ticket_data WHERE channel_id = {ctx.channel.id}")

            ticket_log_embed = discord.Embed(title="Ticket has been closed.", description=f"Ticket name: **{ticket_name}**\nTicket creator: <@{ticket_creator_id}>\nTicket creation reason: `{ticket_creation_reason}`\nTicket opened at: **{ticket_open_time}**\nClosed by: <@{ticket_closed_by_id}>\nTicket closed at: **{ticket_close_time}**\nTicket closing reason: ```{reason}```", color=colors.default)

            with open(f"./tmp/ticket-{ticket_creator_id}-{ctx.guild.id}.log", "w", encoding="utf_8_sig") as f:
                f.write(str(ticket_transcript))

            await ticket_log_channel.send(embed=ticket_log_embed, file=discord.File(f"./tmp/ticket-{ticket_creator_id}-{ctx.guild.id}.log", filename=f"transcript-{ticket_name}.log"))
            os.remove(f"./tmp/ticket-{ticket_creator_id}-{ctx.guild.id}.log")

        db.modify("guild", f"DELETE FROM ticket_data WHERE channel_id = {ctx.channel.id}")

        await ctx.reply("This ticket will be closed in 3 seconds...", mention_author=False)
        await asyncio.sleep(3)
        await ctx.channel.delete(reason=f"Ticket was closed by {ctx.author}.")
    
    @commands.Cog.listener()
    async def on_ready(self):
        view = View(timeout=None)
        view.add_item(create_ticket_button())

        self.bot.add_view(view)

    @commands.Cog.listener()
    async def on_message(self, message):
        ticket_channel_id = db.fetch("guild", f"SELECT channel_id FROM ticket_data WHERE channel_id = {message.channel.id}")

        if ticket_channel_id is not None:
            ticket_transcript = db.fetch("guild", f"SELECT transcript FROM ticket_data WHERE channel_id = {message.channel.id}")

            if ticket_transcript is None:
                ticket_creator_id = db.fetch("guild", f"SELECT creator_id FROM ticket_data WHERE channel_id = {message.channel.id}")
                ticket_transcript = f"Transcript of {message.channel} opened by {ticket_channel_id}"

            ticket_transcript += f"\n[Message from {message.author}, Message creation: {message.created_at}]\n{message.content}"

            db.modify("guild", f"UPDATE ticket_data SET transcript = ? WHERE channel_id = ?", (ticket_transcript, message.channel.id))
    
    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        ticket_channel = db.fetch("guild", f"SELECT channel_id FROM ticket_data WHERE channel_id = {channel.id}")

        if ticket_channel is not None:
            db.modify("guild", f"UPDATE ticket_data SET close_time = ? WHERE channel_id = ?", (str(funcs.get_cur_time()), channel.id))
        
            ticket_log_channel_id = db.fetch("guild", f"SELECT ticket_log_channel_id FROM tickets WHERE guild_id = {channel.guild.id}")

            ticket_log_channel = discord.utils.get(channel.guild.text_channels, id=ticket_log_channel_id)

            if ticket_log_channel is not None:
                ticket_name = db.fetch("guild", f"SELECT name FROM ticket_data WHERE channel_id = {channel.id}")

                ticket_creator_id = db.fetch("guild", f"SELECT creator_id FROM ticket_data WHERE channel_id = {channel.id}")

                ticket_creation_reason = db.fetch("guild", f"SELECT ticket_open_reason FROM ticket_data WHERE channel_id = {channel.id}")

                ticket_open_time = db.fetch("guild", f"SELECT open_time FROM ticket_data WHERE channel_id = {channel.id}")

                ticket_close_time = db.fetch("guild", f"SELECT close_time FROM ticket_data WHERE channel_id = {channel.id}")

                ticket_transcript = db.fetch("guild", f"SELECT transcript FROM ticket_data WHERE channel_id = {channel.id}")

                audit_entry = await channel.guild.audit_logs(limit=1, action=discord.AuditLogAction.channel_delete).get()

                ticket_closed_by_id = audit_entry.user.id

                ticket_log_embed = discord.Embed(title="Ticket has been closed.", description=f"Ticket name: **{ticket_name}**\nTicket creator: <@{ticket_creator_id}>\nTicket creation reason: `{ticket_creation_reason}`\nTicket opened at: **{ticket_open_time}**\nClosed by: <@{ticket_closed_by_id}>\nTicket closed at: **{ticket_close_time}**\nTicket closing reason: ```No reason provided.\nChannel was deleted manually.```", color=colors.default)

                with open(f"./tmp/ticket-{ticket_creator_id}-{channel.guild.id}.log", "w", encoding="utf_8_sig") as f:
                    f.write(str(ticket_transcript))

                await ticket_log_channel.send(embed=ticket_log_embed, file=discord.File(f"./tmp/ticket-{ticket_creator_id}-{channel.guild.id}.log", filename=f"transcript-{ticket_name}.log"))
                os.remove(f"./tmp/ticket-{ticket_creator_id}-{channel.guild.id}.log")

            db.modify("guild", f"DELETE FROM ticket_data WHERE channel_id = {channel.id}")


def setup(bot):
    bot.add_cog(Tickets(bot))
