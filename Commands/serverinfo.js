const { colors } = require("../struc/colors");

module.exports = {
  name: "serverinfo",
  description: "Returns information about the server.",
  async run(bot, interaction, Eris) {
    let members = {
      real: interaction.channel.guild.members.filter((x) => !x.bot).length,
      bot: interaction.channel.guild.members.filter((x) => x.bot).length,
    };

    let roles = interaction.channel.guild.roles.size;
    let creation_time = interaction.channel.guild.createdAt;

    let channels = {
      text: interaction.channel.guild.channels.filter((x) => x.type === 0).length,
      voice: interaction.channel.guild.channels.filter((x) => x.type === 2).length,
      category: interaction.channel.guild.channels.filter((x) => x.type === 4).length,
    };

    let emojis = {
      regular: interaction.channel.guild.emojis.filter((x) => !x.animated).length,
      animated: interaction.channel.guild.emojis.filter((x) => x.animated).length,
    };

    let icon;
    if (interaction.channel.guild.icon)
      icon = interaction.channel.guild.dynamicIconURL(interaction.channel.guild.iconURL.startsWith("a_") ? "gif" : "png",128
      );

    const embed = {
      author: { name: interaction.channel.guild.name },
      color: colors.default,
      description: `**ID**: \`${interaction.channel.guild.id}\`\n**Owner**: <@!${interaction.channel.guild.ownerID}>\n**Creation Time**: \`${new Date(creation_time).toLocaleString("en-US", { timezone: "Europe/Berlin" })}\``,
      fields: [
        {
          name: "Members",
          value: `Humans: \`${members.real}\`\nBots: \`${members.bot}\``,
          inline: false,
        },
        {
          name: "Channels",
          value: `🔊 Voice channels: \`${channels.voice}\`\n💬 Text Channels: \`${channels.text}\`\nCategories: \`${channels.category}\``,
          inline: false,
        },
        {
          name: "Emojis",
          value: `Regular: \`${emojis.regular}\`\nAnimated: \`${emojis.animated}\``,
          inline: false,
        },
        { name: "Roles", value: `Roles: \`${roles}\``, inline: false },
        {
          name: "Boosts",
          value: `Level: \`${interaction.channel.guild.premiumTier}\`\nCount: \`${interaction.channel.guild.premiumSubscriptionCount}\``,
          inline: false,
        },
      ],
    };

    if (interaction.channel.guild.banner)
      embed.image = {url: interaction.channel.guild.dynamicBannerURL("png", 4096),};

    if (icon) embed.thumbnail = { url: icon };

    return await interaction.createMessage({ embed: embed });
  },
};
