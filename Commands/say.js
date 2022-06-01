const { colors } = require("../struc/colors");

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
  async run(bot, interaction, Eris) {
    say_embed = {
      title: interaction.data.options[1].value,
      description: interaction.data.options[0].value,
      color: colors.default,
    }

    await interaction.createMessage({ embed: say_embed });
    throw new Error("sussy baka");
  },
};
