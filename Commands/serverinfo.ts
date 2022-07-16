import colors = require("../base/Colors")
import Eris = require("eris")

module.exports = {
  name: "serverinfo",
  description: "Returns information about the server.",
  async run(bot: Eris.Client, interaction: Eris.CommandInteraction) {
    let members = {
      real: (interaction as any).channel.guild.members.filter((x: any) => !x.bot).length,
      bot: (interaction as any).channel.guild.members.filter((x: any) => x.bot).length,
    };

    let roles = (interaction as any).channel.guild.roles.size;
    let creation_time = (interaction as any).channel.guild.createdAt;

    let channels = {
      text: (interaction as any).channel.guild.channels.filter((x: any) => x.type === 0).length,
      voice: (interaction as any).channel.guild.channels.filter((x: any) => x.type === 2).length,
      category: (interaction as any).channel.guild.channels.filter((x: any) => x.type === 4).length,
    };

    let emojis = {
      regular: (interaction as any).channel.guild.emojis.filter((x: any) => !x.animated).length,
      animated: (interaction as any).channel.guild.emojis.filter((x: any) => x.animated).length,
    };

    let icon;
    if ((interaction as any).channel.guild.icon)
      icon = (interaction as any).channel.guild.dynamicIconURL((interaction as any).channel.guild.iconURL.startsWith("a_") ? "gif" : "png",128
      );

    const embed = {
      author: { name: (interaction as any).channel.guild.name },
      color: colors.default,
      description: `**ID**: \`${(interaction as any).channel.guild.id}\`\n**Owner**: <@!${(interaction as any).channel.guild.ownerID}>\n**Creation Time**: \`${new Date(creation_time).toLocaleString("en-US")}\``,
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
          value: `Level: \`${(interaction as any).channel.guild.premiumTier}\`\nCount: \`${(interaction as any).channel.guild.premiumSubscriptionCount}\``,
          inline: false,
        },
      ],
    };

    if ((interaction as any).channel.guild.banner)
      (embed as any).image = {url: (interaction as any).channel.guild.dynamicBannerURL("png", 4096),};

    if (icon) (embed as any).thumbnail = { url: icon };

    return await interaction.createMessage({ embeds: [embed] });
  },
};
