const Eris = require("eris");
const { colors } = require("./Struc/colors");
require("dotenv").config();
const fs = require("fs");

// TODO: yes

// Replace TOKEN with your bot account's token
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
["CommandHandler"].forEach((handler) => {
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

bot.on("messageCreate", (message) => {
  if (message.author.bot) return;
});

bot.on("interactionCreate", async (interaction) => {
  if (!(interaction instanceof Eris.CommandInteraction)) return;

  const command = bot.commands.get(interaction.data.name);

  if (command) await command.run(bot, interaction, Eris);
});

bot.connect();
