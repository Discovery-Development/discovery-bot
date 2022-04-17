const Eris = require("eris");
const db = require("./struc/db");
const { colors } = require("./struc/colors");
require("dotenv").config();
const fs = require("fs");

const bot = new Eris(process.env.TOKEN, {
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
  restMode: true,
});

bot.commands = new Map();
["commandHandler"].forEach((handler) => {
  require(`./Handlers/${handler}`)(bot, Eris);
});

bot.on("ready", async () => {
  bot.editStatus("online", { name: "As JS Version", type: 0 });

  const selfUser = await bot.getSelf();

  console.log(`Successfully connected to Discord API. Logged in as ${selfUser.username}#${selfUser.discriminator}\nActive on ${Object.keys(bot.guilds).length.toLocaleString()} servers.`);

  const guildId = "943824727242321980";

  for (const cmd of bot.commands) {
    const command = bot.commands.get(cmd[0]);

    bot.createGuildCommand(guildId, {
      name: command.name,
      description: command.description,
      options: command.options || undefined,
      type: 1,
    });

    console.log(`Created "${command.name}" application command.`);
  }
});
/*
The error event doesn't seem to work.

bot.on("error", (err) => {
  console.error(err);
});
*/

// Slash-command handler
bot.on("interactionCreate", async (interaction) => {
  if (!(interaction instanceof Eris.CommandInteraction)) return;

  const command = bot.commands.get(interaction.data.name);

  if (command) await command.run(bot, interaction, Eris);
});

bot.on("messageReactionAdd", async (message, emoji, reactor) => {
  if (emoji.id !== null) {
    emoji.name = `<:${emoji.name}:${emoji.id}>`;
  }
  reaction_role = await db.fetch("SELECT * FROM reaction_roles WHERE message_id = $1 AND emoji = $2;", [message.id, emoji.name]);

  if (reaction_role.length > 0) {
    reaction_role = reaction_role[0];
    const role = message.channel.guild.roles.get(reaction_role.role_id);

    if (role) {
      const member = message.channel.guild.members.get(reactor.id);

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
  reaction_role = await db.fetch("SELECT * FROM reaction_roles WHERE message_id = $1 AND emoji = $2;", [message.id, emoji.name]);

  if (reaction_role.length > 0) {
    reaction_role = reaction_role[0];
    const role = message.channel.guild.roles.get(reaction_role.role_id);

    if (role) {
      const member = message.channel.guild.members.get(userID);

      if (member) {
        member.removeRole(role.id, "Reaction role added.").catch(() => {});
      }
    }
  }
});


bot.connect();
