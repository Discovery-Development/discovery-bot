import discord
from discord.ext import commands, pages
from struc import colors
from discord.commands import (
    slash_command
)

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.pages = [
            discord.Embed(title="Discovery - Discord Bot", url="https://github.com/Discovery-Development/discovery-bot", color=colors.default, description=f"""
            I'm a powerful, multi-functional, open-source Discord Bot.

            `<>` - Required Argument
            `[]` - Optional Argument

            **Miscellenaous commands**

            **`announce <message>`** - Sends your important message in an embed
            **`ping`** - Latency of <@925404589023445062>
            **`version`** - Current version of <@925404589023445062>
            **`pfp [user]`** - Get the profile picture of an user
            **`userinfo [member]`** - Get information about a member
            **`serverinfo`** - Get information about this server

            **Quick Links**
            [Invite](https://discord.com/api/oauth2/authorize?client_id=925404589023445062&permissions=8&scope=bot%20applications.commands) ● [Support Server](https://discord.gg/7fFmXSzK9E) ● [GitHub](https://github.com/Discovery-Development/discovery-bot)
            """),
            discord.Embed(title="Discovery - Discord Bot", url="https://github.com/Discovery-Development/discovery-bot", color=colors.default, description=f"""
            **Fun commands**

            **`trash [member]`** - Move someone to the trash
            **`m8ball <question>`** - Use the magic 8ball
            **`rip [member]`** - Ban someone from life
            **`google <question>`** - Google something
            **`ldva`** - Lies die verfickte Anleitung
            **`rtfm`** - Read the fucking manual
            **`clown [member]`** - Give someone their clown license

            **Quick Links**
            [Invite](https://discord.com/api/oauth2/authorize?client_id=925404589023445062&permissions=8&scope=bot%20applications.commands) ● [Support Server](https://discord.gg/7fFmXSzK9E) ● [GitHub](https://github.com/Discovery-Development/discovery-bot)
            """),
            discord.Embed(title="Discovery - Discord Bot", url="https://github.com/Discovery-Development/discovery-bot", color=colors.default, description=f"""
            **Reaction Roles**

            **`set_reaction_role <message_id> <role> <emoji>`** - Add a reaction role
            **`list_reaction_roles`** - Get a list of all reaction roles
            **`remove_reaction_role <message_id> <emoji>`** - Remove a reaction role

            **Quick Links**
            [Invite](https://discord.com/api/oauth2/authorize?client_id=925404589023445062&permissions=8&scope=bot%20applications.commands) ● [Support Server](https://discord.gg/7fFmXSzK9E) ● [GitHub](https://github.com/Discovery-Development/discovery-bot)
            """),
            discord.Embed(title="Discovery - Discord Bot", url="https://github.com/Discovery-Development/discovery-bot", color=colors.default, description=f"""
            **Suggestions**

            **`set <channel>`** - Set the suggestion channel
            **`remove`** - Remove the suggestion channel

            **Quick Links**
            [Invite](https://discord.com/api/oauth2/authorize?client_id=925404589023445062&permissions=8&scope=bot%20applications.commands) ● [Support Server](https://discord.gg/7fFmXSzK9E) ● [GitHub](https://github.com/Discovery-Development/discovery-bot)
            """),
            discord.Embed(title="Discovery - Discord Bot", url="https://github.com/Discovery-Development/discovery-bot", color=colors.default, description=f"""
            **Tickets**

            **`send`** - Sends the ticket creation embed
            **`modroles <roles(seperated by ';')>`** - Set the roles that can see tickets
            **`category <category>`** - Sets the category under which tickets are created
            **`logchannel <channel>`** - Set the ticket log channel 
            **`openmsg <message>`** - The message that is sent in a ticket
            **`close [reason]`** - Reason for closing ticket 

            **Quick Links**
            [Invite](https://discord.com/api/oauth2/authorize?client_id=925404589023445062&permissions=8&scope=bot%20applications.commands) ● [Support Server](https://discord.gg/7fFmXSzK9E) ● [GitHub](https://github.com/Discovery-Development/discovery-bot)
            """)
        ]

    def get_pages(self):
        return self.pages

    @slash_command()
    async def help(self, ctx: discord.ApplicationContext):
        paginator = pages.Paginator(pages=self.get_pages())
        await paginator.respond(ctx.interaction, ephemeral=False)



def setup(bot):
    bot.add_cog(Help(bot))