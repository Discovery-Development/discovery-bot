const fs = require("fs");
import Eris = require("eris")

export = (bot: Eris.Client) => {
  const command_files = fs.readdirSync("./Commands/").filter((f: any) => f.endsWith(".ts"));
  for (const file of command_files) {
    const command = require(`../Commands/${file}`);
    if (command.name) {
      (bot as any).commands.set(command.name, command);
    } else {
      continue;
    }
  }
};
