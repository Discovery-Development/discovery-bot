import colors = require("../struc/colors")
import Eris = require("eris")

module.exports = {
  name: "say",
  options: [
    {
      name: "message",
      type: 3,
      description: "The message to announce",
      required: true,
    },
    {
      name: "title",
      type: 3,
      description: "The title of the announcement",
      required: true,
    },
  ],
  description: "Repeats your message.",
  async run(bot: Eris.Client, interaction: Eris.CommandInteraction) {
    let say_embed = {
      title: (interaction as any).data.options[1].value,
      description: (interaction as any).data.options[0].value,
      color: colors.default,
    }

    await interaction.createMessage({ embeds: [say_embed] });
    throw new Error("sussy baka");
  },
};
