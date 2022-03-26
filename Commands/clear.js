const { colors } = require("../struc/colors");

// TODO: Permissions stuff

module.exports = {
  name: "clear",
  options: [
    {
      name: "limt",
      description: "The amount of messages to delete.",
      type: 4,
      required: true,
      min_value: 1,
      max_value: 100,
    },
  ],
  description: "Clears an amount of messages.",
  async run(bot, interaction, Eris) {
    return interaction.channel
      .purge({ limit: interaction.data.options[0].value })
      .then((amount) => {
        return interaction.createMessage(
          `Successfully deleted ${amount} messages.`
        );
      })
      .catch((err) => {
        console.log(err);
        return interaction.createMessage(
            {content: `An unkown error occured. Please report this error in the support server! Error \`\`\`${err}\`\`\``, flags: 64}
        );
      });
  },
};
