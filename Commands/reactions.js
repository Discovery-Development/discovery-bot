const { colors } = require("../struc/colors");
const db = require("../struc/db")

// TODO: Permissions stuff

module.exports = {
  name: "reactions",
  
  options: [
    {
      type: 1,
      name: "add",
      description: "Add a reaction role.",
      options: [
        {
          name: "message_id",
          required: true,
          description: "The message's ID.",
          type: 3,
        },
        {
          name: "role",
          required: true,
          description: "The role to add on reaction.",
          type: 8,
        },
        {
          name: "emoji",
          required: true,
          description: "The emoji to use.",
          type: 3,
        }
      ],
    },
    {
      type: 1,
      name: "list",
      description: "List all reaction roles.",
    },
    {
      type: 1,
      name: "remove",
      description: "Remove a reaction role.",
      options: [
        {
          name: "message_id",
          required: true,
          description: "The message's ID.",
          type: 3,
        },
        {
          name: "emoji",
          required: true,
          description: "The emoji of the reaction role.",
          type: 3
        }
      ]
    }
  ],
  description: "Reaction role system",
  async run(bot, interaction, Eris) {
    switch (interaction.data.options[0].name) {
      case "add":
        const exists = await db.fetch("SELECT * FROM reaction_roles WHERE message_id = $1 AND emoji = $2;", [interaction.data.options[0].options[0].value, interaction.channel.guild.id]);
        
        if (exists.length > 0) {
          await interaction.createMessage("This reaction role has already been set.");
          return;
        }

        message = await bot.getMessage(interaction.channel.id, interaction.data.options[0].options[0].value);
        if (!message) {
          await interaction.createMessage("Message not found.");
          return;
        }

        let role_id = interaction.data.options[0].options[1].value;
        let emoji = interaction.data.options[0].options[2].value;

        // Check if the emoji starts with <: and ends with >
        if (emoji.startsWith("<:") && emoji.endsWith(">")) {
          // Replace the <: and > with nothing
          emoji = emoji.replace(/<:/g, "").replace(/>/g, "");
        }

        await db.modify("INSERT INTO reaction_roles(guild_id, message_id, role_id, emoji) VALUES ($1, $2, $3, $4);", [interaction.channel.guild.id, message.id, role_id, interaction.data.options[0].options[2].value]);

        await message.addReaction(emoji);
        await interaction.createMessage("Reaction role added.");
        break;

      case "list":
        const fetched_reaction_roles = await db.fetch("SELECT * FROM reaction_roles WHERE guild_id = $1;", [interaction.channel.guild.id]);

        let list_embed = {
          "title": "Reaction roles in this server",
          "color": colors.default,
          "description": "",
        }
        if (fetched_reaction_roles.length > 0) {
          for (let reaction_role of fetched_reaction_roles) {
            list_embed.description += `\nMessage ID: ${reaction_role.message_id}\nRole: <@&${reaction_role.role_id}>\nEmoji: ${reaction_role.emoji}\n`;
          }
        } else {
          list_embed.description = "No reaction roles have been added.";
        }

        await interaction.createMessage({embed: list_embed});
        break;
      
      case "remove":
        let msg;

        const exists_remove = await db.fetch("SELECT * FROM reaction_roles WHERE message_id = $1 AND emoji = $2;", [interaction.data.options[0].options[0].value, interaction.data.options[0].options[1].value]);

        if (exists_remove.length === 0) {
          await interaction.createMessage("This reaction role does not exist.");
          return;
        }

        db.modify("DELETE FROM reaction_roles WHERE message_id = $1 AND emoji = $2;", [interaction.data.options[0].options[0].value, interaction.data.options[0].options[1].value]);

        try {
          msg = await bot.getMessage(interaction.channel.id, interaction.data.options[0].options[0].value);
        } catch(err) {
          () => {};
        }

        if (msg) {
          let emoji = interaction.data.options[0].options[1].value;

          // Check if the emoji starts with <: and ends with >
          if (emoji.startsWith("<:") && emoji.endsWith(">")) {
            // Replace the <: and > with nothing
            emoji = emoji.replace(/<:/g, "").replace(/>/g, "");
          }

          await msg.removeReaction(emoji);
        }
        await interaction.createMessage("Successfully removed reaction role.");
        break;
      }
  },
};
