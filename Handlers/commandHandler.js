const fs = require("fs");

module.exports = (bot, Eris) => {
  const command_files = fs
    .readdirSync("./Commands/")
    .filter((f) => f.endsWith(".js"));
  for (const file of command_files) {
    const command = require(`../Commands/${file}`);
    if (command.name) {
      bot.commands.set(command.name, command);
    } else {
      continue;
    }
  }
};
