import hikari
import lightbulb
from dotenv import load_dotenv
import os

load_dotenv()

token = os.getenv("TOKEN") or os.environ.get("TOKEN")

bot = lightbulb.BotApp(token=token, default_enabled_guilds=(943824727242321980), intents=hikari.Intents.ALL)

@bot.listen(hikari.StartedEvent)
async def on_started(event: hikari.StartingEvent) -> None:
    print(f"Successfully connected to Discord API.")

@bot.command
@lightbulb.command("ping", "Says pong")
@lightbulb.implements(lightbulb.SlashCommand)
async def ping(ctx: lightbulb.ApplicationContext) -> None:
    await ctx.respond("Pong!")

@bot.command
@lightbulb.option("message", "Message to repeat", type=str)
@lightbulb.add_checks(lightbulb.has_guild_permissions(hikari.Permissions.KICK_MEMBERS))
@lightbulb.command("say", "Repeats your message")
@lightbulb.implements(lightbulb.SlashCommand)
async def say(ctx: lightbulb.ApplicationContext) -> None:
    await ctx.respond(ctx.options.message)

bot.load_extensions_from("./extensions", must_exist=True, recursive=True)

if __name__ == "__main__":
    if os.name != "nt":
        import uvloop
        uvloop.install()

    bot.run()