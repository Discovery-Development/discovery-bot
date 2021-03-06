import asyncio
from email.policy import default
import discord
from discord.ext import commands
from struc import db, funcs, colors
from discord.ui import Button, Select,View
import os
from discord.commands import (
    slash_command,
    Option,
    SlashCommandGroup
)

class ticket_components(View):
    def __init__(self):
        super().__init__()
        self.timeout = None

    @discord.ui.button(label="Close", style=discord.ButtonStyle.red, emoji="✖")
    async def close_ticket(self, button: Button, interaction: discord.Interaction):
        db.modify("UPDATE ticket_data SET closed_by_id = %s WHERE channel_id = %s;", (interaction.user.id, interaction.channel.id))
        db.modify("UPDATE ticket_data SET close_time = %s WHERE channel_id = %s;", (str(funcs.get_cur_time()), interaction.channel.id))
        
        ticket_log_channel_id = db.fetch(f"SELECT ticket_log_channel_id FROM tickets WHERE guild_id = {interaction.guild.id};")

        ticket_log_channel = discord.utils.get(interaction.guild.text_channels, id=ticket_log_channel_id)

        if ticket_log_channel is not None:
            ticket_name = db.fetch(f"SELECT name FROM ticket_data WHERE channel_id = {interaction.channel.id};")

            ticket_creator_id = db.fetch(f"SELECT creator_id FROM ticket_data WHERE channel_id = {interaction.channel.id};")

            ticket_creation_reason = db.fetch(f"SELECT ticket_open_reason FROM ticket_data WHERE channel_id = {interaction.channel.id};")

            ticket_open_time = db.fetch(f"SELECT open_time FROM ticket_data WHERE channel_id = {interaction.channel.id};")

            ticket_closed_by_id = db.fetch(f"SELECT closed_by_id FROM ticket_data WHERE channel_id = {interaction.channel.id};")

            ticket_close_time = db.fetch(f"SELECT close_time FROM ticket_data WHERE channel_id = {interaction.channel.id};")

            ticket_transcript = db.fetch(f"SELECT transcript FROM ticket_data WHERE channel_id = {interaction.channel.id};")

            ticket_log_embed = discord.Embed(title="Ticket has been closed.", description=f"Ticket name: **{ticket_name}**\nTicket creator: <@{ticket_creator_id}>\nTicket creation reason: `{ticket_creation_reason}`\nTicket opened at: **{ticket_open_time}**\nClosed by: <@{ticket_closed_by_id}>\nTicket closed at: **{ticket_close_time}**\nTicket closing reason: ```Undefined```", color=colors.default)

            with open(f"./tmp/ticket-{ticket_creator_id}-{interaction.guild.id}.log", "w", encoding="utf_8_sig") as f:
                f.write(str(ticket_transcript))

            await ticket_log_channel.send(embed=ticket_log_embed, file=discord.File(f"./tmp/ticket-{ticket_creator_id}-{interaction.guild.id}.log", filename=f"transcript-{ticket_name}.log"))
            os.remove(f"./tmp/ticket-{ticket_creator_id}-{interaction.guild.id}.log")

        db.modify(f"DELETE FROM ticket_data WHERE channel_id = {interaction.channel.id};")
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
        ticket_category_id = db.fetch(f"SELECT ticket_category_id FROM tickets WHERE guild_id = {interaction.guild.id};")

        ticket_category = discord.utils.get(interaction.guild.categories, id=ticket_category_id)

        ticket_open_message = db.fetch(f"SELECT ticket_open_message FROM tickets WHERE guild_id = {interaction.guild.id};")

        if ticket_open_message is None:
            sql = "UPDATE tickets SET ticket_open_message = %s WHERE guild_id = %s;"
            binds = ("Moderators will soon be with you, please be patient!", interaction.guild.id)
            db.modify(sql, binds)
        
        ticket_open_message = db.fetch(f"SELECT ticket_open_message FROM tickets WHERE guild_id = {interaction.guild.id};")

        ticket_opened_embed = discord.Embed(title="Your Ticket", description=ticket_open_message, color=colors.default)

        ticket_channel = await interaction.guild.create_text_channel(name=f"ticket-{interaction.user.name}", category=ticket_category)

        view = ticket_components()

        await ticket_channel.send(embed=ticket_opened_embed, view=view)

        binds = (interaction.guild.id, ticket_channel.id, str(ticket_channel.name), interaction.user.id, str(funcs.get_cur_time()), str(select.values[0]))

        db.modify("INSERT INTO ticket_data(guild_id, channel_id, name, creator_id, open_time, ticket_open_reason) VALUES(%s,%s,%s,%s,%s,%s);", binds)

        await ticket_channel.set_permissions(interaction.user, view_channel=True, read_message_history=True, send_messages=True, attach_files=True)

        ticket_log_channel_id = db.fetch(f"SELECT ticket_log_channel_id FROM tickets WHERE guild_id = {interaction.guild.id};")

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
        tickets_by_author_in_guild = db.fetch(f"SELECT guild_id FROM ticket_data WHERE guild_id = {interaction.guild.id} AND creator_id = {interaction.user.id};")

        if tickets_by_author_in_guild is not None:
            await interaction.response.send_message(content="You already have a ticket open on this server.", ephemeral=True)
            return

        ticket_mod_roles = db.fetch(f"SELECT ticket_mod_roles FROM tickets WHERE guild_id = {interaction.guild.id};")
        ticket_category_id = db.fetch(f"SELECT ticket_category_id FROM tickets WHERE guild_id = {interaction.guild.id};")

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
            ticket_channel_id = db.fetch(f"SELECT channel_id FROM ticket_data WHERE channel_id = {view.channel_id};")
            await interaction.edit_original_message(content=f"Your ticket has been opened, check it out at <#{ticket_channel_id}>", view=None)
        else:
            await interaction.edit_original_message(content="An unkown error has occured.", view=None)

        
class Tickets(commands.Cog):
    """
    Commands related to the ticket system.
    """
    def __init__(self, bot):
        self.bot = bot

    tickets = SlashCommandGroup("tickets", "The ticket system")

    @tickets.command()
    async def send(self, ctx: discord.ApplicationContext):
        if not ctx.author.guild_permissions.administrator:
            raise commands.MissingPermissions(["Administrator"])

        create_ticket_embed = discord.Embed(title="Ticket", description=f"Press the button below to create a ticket.", color=colors.default)

        view = View(timeout=None)
        view.add_item(create_ticket_button())

        await ctx.respond("Ticket embed created.", ephemeral=True)
        await ctx.send(embed=create_ticket_embed, view=view)

    @tickets.command()
    async def modroles(self, ctx: discord.ApplicationContext, mod_roles: Option(str, "The ticket moderation roles")):
        if not ctx.author.guild_permissions.administrator:
            raise commands.MissingPermissions(["Administrator"])

        mod_roles = mod_roles.replace(" ", "")
        mod_roles = mod_roles.split(";")

        mod_roles_modified = ""

        for mod_role in mod_roles:
            if mod_role == "":
                continue
            mod_role = await commands.RoleConverter().convert(ctx, mod_role)
            mod_roles_modified += f"{mod_role.id};"

        guild = db.fetch(f"SELECT guild_id FROM tickets WHERE guild_id = {ctx.guild.id};")

        if guild is None:
            sql = "INSERT INTO tickets(guild_id, ticket_mod_roles) VALUES(%s,%s);"
            binds = (ctx.guild.id, mod_roles_modified)
        elif guild is not None:
            sql = "UPDATE tickets SET ticket_mod_roles = %s WHERE guild_id = %s;"
            binds = (mod_roles_modified, ctx.guild.id)
        
        db.modify(sql, binds)

        await ctx.respond(f"Successfully set ticket moderation roles.")


    @tickets.command()
    async def category(self, ctx: discord.ApplicationContext, ticket_category: Option(discord.CategoryChannel, "The ticket category")):
        if not ctx.author.guild_permissions.administrator:
            raise commands.MissingPermissions(["Administrator"])

        ticket_mod_roles_txt = db.fetch(f"SELECT ticket_mod_roles FROM tickets WHERE guild_id = {ctx.guild.id};")

        if ticket_mod_roles_txt is None:
            await ctx.respond(f"Please set up ticket moderation roles first!")

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

        guild = db.fetch(f"SELECT guild_id FROM tickets WHERE guild_id = {ctx.guild.id};")

        if guild is None:
            sql = "INSERT INTO tickets(guild_id, ticket_category_id) VALUES(%s,%s)"
            binds = (ctx.guild.id, ticket_category.id)
        elif guild is not None:
            sql = "UPDATE tickets SET ticket_category_id = %s WHERE guild_id = %s"
            binds = (ticket_category.id, ctx.guild.id)
        
        db.modify(sql, binds)

        ticket_category_id = db.fetch(f"SELECT ticket_category_id FROM tickets WHERE guild_id = {ctx.guild.id};")

        await ctx.respond(f"The ticket category has been set to <#{ticket_category_id}>")

    @tickets.command()
    async def logchannel(self, ctx: discord.ApplicationContext, ticket_log_channel: Option(discord.TextChannel, "The ticket log channel")):
        if not ctx.author.guild_permissions.administrator:
            raise commands.MissingPermissions(["Administrator"])

        guild = db.fetch(f"SELECT guild_id FROM tickets WHERE guild_id = {ctx.guild.id};")

        if guild is None:
            sql = "INSERT INTO tickets(guild_id, ticket_log_channel_id) VALUES(%s,%s);"
            binds = (ctx.guild.id, ticket_log_channel.id)
        elif guild is not None:
            sql = "UPDATE tickets SET ticket_log_channel_id = %s WHERE guild_id = %s;"
            binds = (ticket_log_channel.id, ctx.guild.id)

        db.modify(sql, binds)

        ticket_log_channel_id = db.fetch(f"SELECT ticket_log_channel_id FROM tickets WHERE guild_id = {ctx.guild.id};")

        await ctx.respond(f"The ticket log channel has been set to <#{ticket_log_channel_id}>")

    @tickets.command()
    async def openmsg(self, ctx: discord.ApplicationContext, ticket_open_message: Option(str, "The ticket open message")):
        if not ctx.author.guild_permissions.administrator:
            raise commands.MissingPermissions(["Administrator"])

        guild = db.fetch(f"SELECT guild_id FROM tickets WHERE guild_id = {ctx.guild.id};")

        if guild is None:
            sql = "INSERT INTO tickets(guild_id, ticket_open_message) VALUES(%s,%s);"
            binds = (ctx.guild.id, ticket_open_message)
        elif guild is not None:
            sql = "UPDATE tickets SET ticket_open_message = %s WHERE guild_id = %s;"
            binds = (ticket_open_message, ctx.guild.id)

        db.modify(sql, binds)

        ticket_open_message = db.fetch(f"SELECT ticket_open_message FROM tickets WHERE guild_id = {ctx.guild.id};")

        await ctx.respond(f"The ticket open message has been set to ```{ticket_open_message}```")
    
    @slash_command()
    async def close(self, ctx: discord.ApplicationContext, reason: Option(str, "Reason for closing ticket", required=False, default="No reason was specified.")):
        if not ctx.author.guild_permissions.administrator:
            raise commands.MissingPermissions(["Administrator"])
            
        ticket = db.fetch(f"SELECT channel_id FROM ticket_data WHERE channel_id = {ctx.channel.id};")

        if ticket is None:
            await ctx.respond("This channel is not a ticket!")
            return

        db.modify("UPDATE ticket_data SET closed_by_id = %s WHERE channel_id = %s;", (ctx.author.id, ctx.channel.id))
        db.modify("UPDATE ticket_data SET close_time = %s WHERE channel_id = %s;", (str(funcs.get_cur_time()), ctx.channel.id))
        
        ticket_log_channel_id = db.fetch(f"SELECT ticket_log_channel_id FROM tickets WHERE guild_id = {ctx.guild.id};")

        ticket_log_channel = discord.utils.get(ctx.guild.text_channels, id=ticket_log_channel_id)

        if ticket_log_channel is not None:
            ticket_name = db.fetch(f"SELECT name FROM ticket_data WHERE channel_id = {ctx.channel.id};")

            ticket_creator_id = db.fetch(f"SELECT creator_id FROM ticket_data WHERE channel_id = {ctx.channel.id};")

            ticket_creation_reason = db.fetch(f"SELECT ticket_open_reason FROM ticket_data WHERE channel_id = {ctx.channel.id};")

            ticket_open_time = db.fetch(f"SELECT open_time FROM ticket_data WHERE channel_id = {ctx.channel.id};")

            ticket_closed_by_id = db.fetch(f"SELECT closed_by_id FROM ticket_data WHERE channel_id = {ctx.channel.id};")

            ticket_close_time = db.fetch(f"SELECT close_time FROM ticket_data WHERE channel_id = {ctx.channel.id};")

            ticket_transcript = db.fetch(f"SELECT transcript FROM ticket_data WHERE channel_id = {ctx.channel.id};")

            ticket_log_embed = discord.Embed(title="Ticket has been closed.", description=f"Ticket name: **{ticket_name}**\nTicket creator: <@{ticket_creator_id}>\nTicket creation reason: `{ticket_creation_reason}`\nTicket opened at: **{ticket_open_time}**\nClosed by: <@{ticket_closed_by_id}>\nTicket closed at: **{ticket_close_time}**\nTicket closing reason: ```{reason}```", color=colors.default)

            with open(f"./tmp/ticket-{ticket_creator_id}-{ctx.guild.id}.log", "w", encoding="utf_8_sig") as f:
                f.write(str(ticket_transcript))

            await ticket_log_channel.send(embed=ticket_log_embed, file=discord.File(f"./tmp/ticket-{ticket_creator_id}-{ctx.guild.id}.log", filename=f"transcript-{ticket_name}.log"))
            os.remove(f"./tmp/ticket-{ticket_creator_id}-{ctx.guild.id}.log")

        db.modify(f"DELETE FROM ticket_data WHERE channel_id = {ctx.channel.id};")

        await ctx.respond("This ticket will be closed in 3 seconds...")
        await asyncio.sleep(3)
        await ctx.channel.delete(reason=f"Ticket was closed by {ctx.author}.")
    
    @commands.Cog.listener()
    async def on_ready(self):
        view = View(timeout=None)
        view.add_item(create_ticket_button())

        self.bot.add_view(view)

    @commands.Cog.listener()
    async def on_message(self, message):
        ticket_channel_id = db.fetch(f"SELECT channel_id FROM ticket_data WHERE channel_id = {message.channel.id};")

        if ticket_channel_id is not None:
            ticket_transcript = db.fetch(f"SELECT transcript FROM ticket_data WHERE channel_id = {message.channel.id};")

            if ticket_transcript is None:
                ticket_transcript = f"Transcript of {message.channel} opened by {ticket_channel_id}"

            ticket_transcript += f"\n[Message from {message.author}, Message creation: {message.created_at}]\n{message.content}"

            db.modify("UPDATE ticket_data SET transcript = %s WHERE channel_id = %s;", (ticket_transcript, message.channel.id))
    
    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        ticket_channel = db.fetch(f"SELECT channel_id FROM ticket_data WHERE channel_id = {channel.id};")

        if ticket_channel is not None:
            db.modify("UPDATE ticket_data SET close_time = %s WHERE channel_id = %s;", (str(funcs.get_cur_time()), channel.id))
        
            ticket_log_channel_id = db.fetch(f"SELECT ticket_log_channel_id FROM tickets WHERE guild_id = {channel.guild.id};")

            ticket_log_channel = discord.utils.get(channel.guild.text_channels, id=ticket_log_channel_id)

            if ticket_log_channel is not None:
                ticket_name = db.fetch(f"SELECT name FROM ticket_data WHERE channel_id = {channel.id};")

                ticket_creator_id = db.fetch(f"SELECT creator_id FROM ticket_data WHERE channel_id = {channel.id};")

                ticket_creation_reason = db.fetch(f"SELECT ticket_open_reason FROM ticket_data WHERE channel_id = {channel.id};")

                ticket_open_time = db.fetch(f"SELECT open_time FROM ticket_data WHERE channel_id = {channel.id};")

                ticket_close_time = db.fetch(f"SELECT close_time FROM ticket_data WHERE channel_id = {channel.id};")

                ticket_transcript = db.fetch(f"SELECT transcript FROM ticket_data WHERE channel_id = {channel.id};")

                audit_entry = await channel.guild.audit_logs(limit=1, action=discord.AuditLogAction.channel_delete).get()

                ticket_closed_by_id = audit_entry.user.id

                ticket_log_embed = discord.Embed(title="Ticket has been closed.", description=f"Ticket name: **{ticket_name}**\nTicket creator: <@{ticket_creator_id}>\nTicket creation reason: `{ticket_creation_reason}`\nTicket opened at: **{ticket_open_time}**\nClosed by: <@{ticket_closed_by_id}>\nTicket closed at: **{ticket_close_time}**\nTicket closing reason: ```No reason provided.\nChannel was deleted manually.```", color=colors.default)

                with open(f"./tmp/ticket-{ticket_creator_id}-{channel.guild.id}.log", "w", encoding="utf_8_sig") as f:
                    f.write(str(ticket_transcript))

                await ticket_log_channel.send(embed=ticket_log_embed, file=discord.File(f"./tmp/ticket-{ticket_creator_id}-{channel.guild.id}.log", filename=f"transcript-{ticket_name}.log"))
                os.remove(f"./tmp/ticket-{ticket_creator_id}-{channel.guild.id}.log")

            db.modify(f"DELETE FROM ticket_data WHERE channel_id = {channel.id}")


def setup(bot):
    bot.add_cog(Tickets(bot))
