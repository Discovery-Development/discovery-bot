const { colors } = require("../Struc/colors");

module.exports = {
  name: "ping",
  description: "Says pong.",
  async run(bot, interaction, Eris) {
    shard = interaction.channel.guild.shard;
    const before = new Date().getTime();
    msg = await interaction.createMessage("🏓Pong!");
    const after = new Date().getTime();
    const ping = after - before;

    embed = {
      title: "🏓 Pong!",
      description: `Shard Latency: **${shard.latency}**ms.\nAPI Latency: **${ping}**ms.`,
      color: colors.default,
    };

    await interaction.editOriginalMessage({ content: "", embed: embed });
  },
};
