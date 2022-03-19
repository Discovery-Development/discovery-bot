import lightbulb
from lightbulb import commands
import hikari

plugin = lightbulb.Plugin("LocalEvents")

@plugin.listener(lightbulb.CommandErrorEvent)
async def on_error(event: lightbulb.CommandErrorEvent) -> None:
    if isinstance(event.exception, lightbulb.CommandInvocationError):
        await event.context.respond(f"Something went wrong during invocation of command `{event.context.command.name}`.")
        raise event.exception

    exception = event.exception.__cause__ or event.exception

    if isinstance(exception, lightbulb.MissingRequiredPermission):
        await event.context.respond(f"You are missing the permissions `{exception.missing_perms}` to execute this command.")
    elif isinstance(exception, lightbulb.CommandNotFound):
        pass

def load(bot):
    bot.add_plugin(plugin)

def unload(bot):
    bot.unload_plugin(plugin)