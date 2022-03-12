import random
from datetime import datetime, timedelta

import discord
from discord.commands import slash_command
from discord.ext import commands
from discord.ui import View, Button


class GiveawaySystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.active_giveaways = []

    @slash_command(description="Create a giveaway")
    @commands.has_permissions(manage_messages=True)
    async def giveaway(self, ctx: discord.ApplicationContext, hours: int, prize: str, description: str = None):
        embed = discord.Embed(
            title="Giveaway",
            description=description if description else None,
            colour=discord.Colour.blurple()
        ).add_field(
            name="Ending",
            value=discord.utils.format_dt(datetime.now() + timedelta(hours=hours), 'R'),
            inline=False
        ).add_field(
            name="Prize",
            value=prize,
            inline=False
        ).set_footer(
            text="React with 🎉 to enter."
        )
        await ctx.respond(f"Giveaway started. A winner will be announced in {hours} hours.", ephemeral=True)
        message = await ctx.send(embed=embed)
        await message.add_reaction("🎉")
        await message.add_reaction("✖")
        self.active_giveaways.append((message.channel.id, message.id))
        self.bot.scheduler.add_job(
            self.announce_winner,
            "date",
            run_date=datetime.utcnow() + timedelta(hours=hours),
            args=[message.channel.id, message.id],
            id=str(message.id)
        )

    async def announce_winner(self, channel_id: int, message_id: int):
        message: discord.Message = await self.bot.get_channel(channel_id).fetch_message(message_id)
        if message is None:
            return
        entrants = [m for m in await message.reactions[0].users().flatten() if not m.bot]
        button = Button(label="Reroll", style=discord.ButtonStyle.blurple, emoji="🔄")

        async def button_callback(interaction: discord.Interaction):
            if interaction.user.guild_permissions.manage_messages:
                await self.announce_winner(interaction.channel_id, interaction.message.reference.message_id)
                await interaction.message.delete()
            else:
                await interaction.response.send_message("You do not have permission to do this.", ephemeral=True)

        button.callback = button_callback

        view = View(button, timeout=60 * 60 * 5)

        if len(entrants) > 0:
            winner = random.choice(entrants)
            await message.reply(winner.mention, embed=discord.Embed(
                title="Giveaway ended",
                description=f"The giveaway ended and {winner.mention} won the giveaway. Congratulations!",
                colour=discord.Colour.blurple()
            ), view=view)

        else:
            await message.reply(embed=discord.Embed(
                title="Giveaway ended",
                description="The giveaway ended but no one had entered.",
                colour=discord.Colour.blurple()
            ))
        new_embed = discord.Embed(
            title=message.embeds[0].title,
            description=message.embeds[0].description,
            colour=discord.Colour.blurple()
        ).add_field(
            name="Ended",
            value=discord.utils.format_dt(datetime.now(), "R"),
            inline=False
        ).add_field(
            name=message.embeds[0].fields[1].name,
            value=message.embeds[0].fields[1].value,
            inline=False
        )
        await message.edit(embed=new_embed)
        if (channel_id, message_id) in self.active_giveaways:
            self.active_giveaways.remove((channel_id, message_id))

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        member: discord.Member = self.bot.get_guild(payload.guild_id).get_member(payload.user_id)
        channel: discord.TextChannel = self.bot.get_channel(payload.channel_id)
        message: discord.Message = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
        if payload.message_id in (msg[1] for msg in self.active_giveaways) and not member.bot:
            if channel.permissions_for(member).manage_messages:
                if payload.emoji.name == "✖":
                    self.bot.scheduler.remove_job(job_id=str(payload.message_id))
                    self.active_giveaways.remove((payload.channel_id, payload.message_id))
                    await message.remove_reaction(payload.emoji, member)
                    await self.announce_winner(payload.channel_id, payload.message_id)


def setup(bot: discord.Bot):
    bot.add_cog(GiveawaySystem(bot))
