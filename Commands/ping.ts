import colors = require("../base/Colors")
import Eris = require("eris")

module.exports = {
  name: "ping",
  permission: BigInt(1 << 3),
  description: "Returns current API ping and shard ping.",
  async run(bot: Eris.Client, interaction: Eris.CommandInteraction) {
    const shard = (interaction as any).channel.guild.shard;
    const before = new Date().getTime();
    const msg = await interaction.createMessage("🏓Pong!");
    const after = new Date().getTime();
    const ping = after - before;

    const embed = {title: "🏓 Pong!", description: `Shard Latency: **${shard.latency}**ms.\nAPI Latency: **${ping}**ms.`, color: colors.default,};

    await interaction.editOriginalMessage({ content: "", embeds: [embed] });
  },
};
