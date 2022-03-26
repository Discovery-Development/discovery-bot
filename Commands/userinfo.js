const { colors } = require("../struc/colors");

module.exports = {
  name: "userinfo",
  options: [
    {
      name: "member",
      description: "The member to get information about",
      type: 6,
      required: true,
    },
  ],
  description: "Returns information about a member.",
  async run(bot, interaction, Eris) {
    if (!interaction.data.options)
      return await interaction.createMessage("Required Argument 'member' missing.");
    member = interaction.channel.guild.fetchMembers({
      userIDs: [interaction.data.options[0].value],
    });

    member.then(async (member) => {
      if (!member)
        return interaction.createMessage("Invalid argument provided.");
      member = member[0];

      let roles = "@everyone";
      let avatar =
        member.user.dynamicAvatarURL("png", 4096) || member.defaultAvatarURL;
      const nickname = member.nick || "None";
      const createdAt = new Date(member.createdAt).toUTCString();
      const joinedAt = new Date(member.joinedAt).toUTCString();
      let status = member.status || "Offline";
      if (status) status = status.charAt(0).toUpperCase() + status.slice(1);
      let activity;

      for (const role_id of member.roles) {
        roles += ` <@&${role_id}>`;
      }

      if (member.activities !== undefined) {
        activity = {
          name: member.activities[0].name,
          type: member.activities[0].type,
        };
        if (activity.type === 4) activity.name = member.activities[0].state;

        if (activity.type === 0) activity.type = "Playing";
        else if (activity.type === 1) activity.type = "Streaming";
        else if (activity.type === 2) activity.type = "Listening";
        else if (activity.type === 3) activity.type = "Watching";
        else if (activity.type === 4) activity.type = "Custom";
        else if (activity.type === 5) activity.type = "Competing in";
      }

      embed = {
        author: {
          name: `${member.username}#${member.discriminator} - ${nickname}`,
        },
        thumbnail: { url: avatar },
        fields: [
          { name: "ID", value: `\`${member.id}\``, inline: true },
          {
            name: "Account Creation Date",
            value: `\`${createdAt}\``,
            inline: true,
          },
          { name: `Join Date`, value: `\`${joinedAt}\``, inline: true },
          { name: "Roles", value: `${roles}`, inline: true },
          { name: "Status", value: `${status}`, inline: true },
        ],
        color: colors.default,
      };

      if (activity !== undefined) {
        embed.fields.push({
          name: "Activity",
          value: `${activity.type}: ${activity.name}`,
          inline: true,
        });
      }

      await interaction.createMessage({ embed: embed });
    });
  },
};
