from typing import Optional, Union

import discord
from discord.ext import commands
from discord.ui import View, Select


class CategoryChooser(Select):
    def __init__(self, command: "HelpEmbed()", options: list[discord.SelectOption]):
        super().__init__(
            placeholder="Choose the category to get help for",
            custom_id="help:category_chooser",
            options=options
        )
        self.command = command

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.edit_message(
            embed=await self.command.send_cog_help_embed(self.command.context.bot.get_cog(self.values[0]))
            if self.values[0] != self.options[0].value
            else await self.command.send_bot_help_embed(self.command.get_bot_mapping())
        )


class CategoryChooseView(View):
    def __init__(self, command: "HelpEmbed()", options: list[discord.SelectOption]):
        super().__init__(timeout=600)
        self.add_item(CategoryChooser(command=command, options=options))
        self.command = command

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        return self.command.context.author == interaction.user


class HelpEmbed(commands.MinimalHelpCommand):
    def get_command_signature(self, command):
        return f"{self.context.clean_prefix}{command.qualified_name} {command.signature}"

    async def create_select_options(self) -> list[discord.SelectOption]:
        select_options: list[discord.SelectOption] = [discord.SelectOption(
            label="Overview",
            emoji="📒",
            description="Go back to the overview"
        )]

        for cog, cog_commands in self.get_bot_mapping().items():
            visible = await self.filter_commands(cog_commands, sort=True)
            if not visible:
                continue
            if cog:
                select_options.append(
                    discord.SelectOption(
                        label=cog.qualified_name,
                        emoji=getattr(cog, "EMOTE", "🤖"),
                        description=cog.description if cog.description else None
                    )
                )

        return select_options

    async def create_help_embed(
            self,
            title: str,
            description: Optional[str] = None,
            bot_help: Optional[dict] = None,
            group_or_cog: Optional[Union[set[commands.Command], list[commands.Command]]] = None
    ) -> discord.Embed:
        help_menu = discord.Embed(
            title=title,
            description=description if description else None,
            colour=discord.Colour.dark_purple()
        ).set_footer(
            text="<> = required argument, [] = optional argument"
        )
        if group_or_cog:
            visible = await self.filter_commands(group_or_cog, sort=True)
            for command in visible:
                help_menu.add_field(
                    name=self.get_command_signature(command),
                    value=f"`{command.help}`",
                    inline=False
                )
        elif bot_help:
            help_menu.set_author(name=self.context.me.name, icon_url=self.context.me.display_avatar.url)
            help_menu.description = f"Use {self.context.clean_prefix}help [command] to get more information about a " \
                                    f"command or group and {self.context.clean_prefix}help [category] to get more " \
                                    f"information about a category"
            for cog, commands_set in bot_help.items():
                visible = await self.filter_commands(commands_set, sort=True)
                if not visible:
                    continue
                if cog and cog.description:
                    field_value = f"{cog.description}\n{' '.join(f'`{self.context.clean_prefix}{command.name}`' for command in visible)}"
                else:
                    field_value = " ".join(f"`{self.context.clean_prefix}{command.name}`" for command in visible)

                help_menu.add_field(
                    name=cog.qualified_name if cog else "Uncategorised",
                    value=field_value,
                    inline=False
                )

        return help_menu

    async def send_bot_help_embed(self, mapping: dict) -> discord.Embed:
        return await self.create_help_embed(
            title="Help",
            bot_help=mapping
        )

    async def send_bot_help(self, mapping: dict):
        await self.get_destination().send(
            embed=await self.send_bot_help_embed(mapping),
            view=CategoryChooseView(self, await self.create_select_options())
        )

    async def send_cog_help_embed(self, cog: commands.Cog) -> discord.Embed:
        return await self.create_help_embed(
            title=cog.qualified_name,
            description=cog.description if cog.description else None,
            group_or_cog=cog.get_commands()
        )

    async def send_cog_help(self, cog: commands.Cog):
        await self.get_destination().send(
            embed=await self.send_cog_help_embed(cog),
            view=CategoryChooseView(self, await self.create_select_options())
        )

    async def send_command_help_embed(self, command: commands.Command) -> discord.Embed:
        return await self.create_help_embed(
            title=self.get_command_signature(command),
            description=command.help,
            group_or_cog=command.commands if isinstance(command, commands.Group) else None
        )

    async def send_command_help(self, command: commands.Command):
        await self.get_destination().send(
            embed=await self.send_command_help_embed(command),
            view=CategoryChooseView(self, await self.create_select_options())
        )

    async def send_group_help_embed(self, command: commands.Command) -> discord.Embed:
        return await self.create_help_embed(
            title=command.qualified_name,
            description=command.help,
            group_or_cog=command.commands if isinstance(command, commands.Group) else None
        )

    async def send_group_help(self, group: commands.Group):
        await self.get_destination().send(
            embed=await self.send_group_help_embed(group),
            view=CategoryChooseView(self, await self.create_select_options())
        )

    async def send_error_message(self, error):
        await self.get_destination().send(
            embed=discord.Embed(
                title="Error",
                description=error,
                colour=discord.Colour.brand_red()
            ),
            delete_after=4
        )


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        bot.help_command = HelpEmbed()


def setup(bot: commands.Bot):
    bot.add_cog(Help(bot))
