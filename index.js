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
  ],
  restMode: true,
});

bot.commands = new Eris.Collection();
["commandHandler"].forEach((handler) => {
  require(`./Handlers/${handler}`)(bot, Eris);
});

bot.on("ready", async () => {
  bot.editStatus("online", { name: "JS Version", type: 0 });

  const selfUser = bot.getSelf(); // Make promise to get the Bot's ExtendedUser
  selfUser.then((user) => {
    console.log(
      `Successfully connected to Discord API. Logged in as ${user.username}#${
        user.discriminator
      }\nActive on ${Object.keys(bot.guilds).length.toLocaleString()} servers.`
    ); // Confirm login and give data about the logged in user
  });

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

bot.on("error", (err) => {
  console.error(err);
});

bot.on("interactionCreate", async (interaction) => {
  if (!(interaction instanceof Eris.CommandInteraction)) return;

  const command = bot.commands.get(interaction.data.name);

  if (command) await command.run(bot, interaction, Eris);
});

bot.connect();
