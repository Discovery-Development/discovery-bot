import Eris from "eris";
import { fetch } from "./struc/db"
import dotEnv from "dotenv";
dotEnv.config();

const bot = new Eris.Client((process.env.TOKEN as string), {
  getAllUsers: true,
  intents: [
    "guilds",
    "guildMessages",
    "guildMembers",
    "guildEmojisAndStickers",
    "directMessages",
    "guildPresences",
    "guildMessageReactions"
  ],
  restMode: true
});

(bot as any).commands = new Map();
["commandHandler"].forEach(async (handler) => {
  const handler_func = await import(`./Handlers/${handler}`);
  handler_func.default(bot);
});

bot.on("ready", async () => {
  bot.editStatus("online", { name: "i forgor", type: 0 });

  const selfUser = await bot.getSelf();

  console.log(`Successfully connected to Discord API. Logged in as ${selfUser.username}#${selfUser.discriminator}\nActive on ${Object.keys(bot.guilds).length} servers.`);

  const guildId = "943824727242321980";
  console.log((bot as any).commands);

  for (const cmd of (bot as any).commands) {
    const command = (bot as any).commands.get(cmd[0]);

    bot.createGuildCommand(guildId, {
      name: command.name,
      description: command.description,
      options: command.options || undefined,
      type: 1,
    });

    console.log(`Created "${command.name}" application command.`);
  }
});

// Slash-command handler
bot.on("interactionCreate", async (interaction) => {
  if (!(interaction instanceof Eris.CommandInteraction)) return;

  const command = (bot as any).commands.get(interaction.data.name);

  if (command) await command.run(bot, interaction, Eris);
});

bot.on("messageReactionAdd", async (message, emoji, reactor) => {
  if (emoji.id !== null) {
    emoji.name = `<:${emoji.name}:${emoji.id}>`;
  }
  let reaction_role = await fetch("SELECT * FROM reaction_roles WHERE message_id = $1 AND emoji = $2;", [message.id, emoji.name]);

  if (reaction_role.length > 0) {
    reaction_role = reaction_role[0];
    const role = (message as any).channel.guild.roles.get(reaction_role.role_id);

    if (role) {
      const member = (message as any).channel.guild.members.get(reactor.id);

      if (member) {
        member.addRole(role.id, "Reaction role added.").catch(() => {});
      }
    }
  }
});

bot.on("messageReactionRemove", async (message, emoji, userID) => {
  if (emoji.id !== null) {
    emoji.name = `<:${emoji.name}:${emoji.id}>`;
  }
  let reaction_role = await fetch("SELECT * FROM reaction_roles WHERE message_id = $1 AND emoji = $2;", [message.id, emoji.name]);

  if (reaction_role.length > 0) {
    reaction_role = reaction_role[0];
    const role = (message as any).channel.guild.roles.get(reaction_role.role_id);

    if (role) {
      const member = (message as any).channel.guild.members.get(userID);

      if (member) {
        member.removeRole(role.id, "Reaction role added.").catch(() => {});
      }
    }
  }
});

bot.connect();