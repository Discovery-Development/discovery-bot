import hikari
import lightbulb
from dotenv import load_dotenv
import os
from struc import colors_cli

load_dotenv()

token = os.getenv("TOKEN") or os.environ.get("TOKEN")

bot = lightbulb.BotApp(token=token, default_enabled_guilds=(943824727242321980), intents=hikari.Intents.ALL)

bot.load_extensions_from("./extensions", must_exist=True, recursive=True)

@bot.listen(hikari.StartedEvent)
async def on_started(event: hikari.StartingEvent) -> None:
    print(f"{colors_cli.SUCCESS}Successfully connected to Discord API.{colors_cli.RESET}")

@bot.command
@lightbulb.add_checks(lightbulb.owner_only)
@lightbulb.command("reload", "Reload all extensions")
@lightbulb.implements(lightbulb.SlashCommand)
async def reload(ctx: lightbulb.ApplicationContext):
    bot.unload_extensions(bot.extensions)

    bot.load_extensions_from("./extensions", must_exist=True, recursive=True)

    await ctx.respond("All extensions have been reloaded.")

if __name__ == "__main__":
    if os.name != "nt":
        import uvloop
        uvloop.install()

    bot.run()