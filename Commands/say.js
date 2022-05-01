module.exports = {
  name: "say",
  dm_permission: false,
  options: [
    {
      name: "message",
      type: 3,
      description: "The message to announce",
      required: true,
    },
  ],
  description: "Repeats your message.",
  async run(bot, interaction, Eris) {
    await interaction.createMessage(interaction.data.options[0].value);
  },
};
