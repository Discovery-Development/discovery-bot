import colors = require("../base/Colors")
import Eris = require("eris")

module.exports = {
  name: "pfp",
  options: [
    {
        name: "member",
        required: true,
        description: "The member whose profile picture you want.",
        type: 6,
    }
  ],
  description: "Returns current API ping and shard ping.",
  async run(bot: Eris.Client, interaction: Eris.CommandInteraction) {
    const member_id = (interaction as any).data.options[0].value;
    const member = await (interaction as any).channel.guild.fetchMembers({userIDs: [member_id]});

    let avatar = member[0].user.dynamicAvatarURL("png", 4096) || member[0].defaultAvatarURL;

    const pfpEmbed = {
        title: `Profile picture of ${member[0].user.username}`,
        color: colors.default,
        image: { url: avatar }
    }

    await interaction.createMessage({ embeds: [ pfpEmbed ] })
  }
};
