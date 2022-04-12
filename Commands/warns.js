const { colors } = require("../struc/colors");
const db = require("../struc/db");

module.exports = {
  name: "warns",
  options: [
    {
      type: 1,
      name: "remove",
      description: "Remove a warning.",
      options: [
        {
          name: "id",
          required: true,
          description: "The ID of the warning which is to be removed.",
          type: 4,
        },
      ],
    },
    {
      type: 1,
      name: "reset",
      description: "Reset a member's warnings.",
      options: [
        {
          name: "member",
          required: true,
          description: "Whose warnings to reset",
          type: 6,
        },
      ],
    },
    {
      type: 1,
      name: "list",
      description: "List all warnings.",
    },
  ],
  description: "The warning system.",
  async run(bot, interaction, Eris) {
    switch (interaction.data.options[0].name) {
      /*
      List command
      */
      case "list":
        await interaction.createMessage("Calculating...");
        fetch = await db.fetch("SELECT * FROM warnings WHERE guild_id = $1;", [interaction.channel.guild.id,]);

        list_embed = {
          title: "Warnings in this server",
          color: colors.default,
          description: `Total warnings: ${fetch.length}`,
          fields: [],
        };

        let warned_users = await db.fetch("SELECT user_id FROM warnings WHERE guild_id = $1;", [interaction.channel.guild.id]);

        // Remove all duplicates
        const seen = new Set();
        warned_users = warned_users.filter(el => {
          const duplicate = seen.has(el.user_id);
          seen.add(el.user_id);
          return !duplicate;
        });

        if (fetch !== undefined) {
          for (let user_id of warned_users) {
            user_id = user_id.user_id;
            user_warns = await db.fetch("SELECT * FROM warnings WHERE user_id = $1 AND guild_id = $2;", [user_id, interaction.channel.guild.id]);
            user = await bot.getRESTUser(user_id);
            let user_warn_text = "";
            for (const warning of user_warns) {
              user_warn_text += `\nModerator: <@${warning.mod_id}>\nID: ${warning.id}\nReason: \`\`\`${warning.reason}\`\`\`\n`;
            }
            list_embed.fields.push({
              name: `Warnings of ${user.username}#${user.discriminator}`,
              value: `Total: ${user_warns.length}\n${user_warn_text}`,
              inline: false,
            });
          }
        } else {
          list_embed.description = "No warnings in this server.";
        }

        await interaction.editOriginalMessage({content: "", embed: list_embed});
        break;
      /*
      Remove command
      */
      case "remove":
        await db.modify("DELETE FROM warnings WHERE guild_id = $1 AND id = $2;", [interaction.channel.guild.id, interaction.data.options[0].options[0].value,]);

        await interaction.createMessage(`Successfully removed warning ${interaction.data.options[0].options[0].value}`);
        break;
      /*
      Reset command
      */
      case "reset":
        await db.modify("DELETE FROM warnings WHERE user_id = $1 AND guild_id = $2;", [interaction.data.options[0].options[0].value, interaction.channel.guild.id]);

        await interaction.createMessage(`Successfully removed all warnings of <@${interaction.data.options[0].options[0].value}>.`);
        break;
    }
  }
};
