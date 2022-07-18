import colors = require("../base/Colors")
import Eris = require("eris")

module.exports = {
  name: "help",
  description: "Returns a help Embed.",
  async run(bot: Eris.Client, interaction: Eris.CommandInteraction) {
    let embed = {
        title: "Help",
        description: "A help command is currently not implemented.",
        color: colors.default
    };
    await interaction.createMessage({ embeds: [embed] });
  },
};
