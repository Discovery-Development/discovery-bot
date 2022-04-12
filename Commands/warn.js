const { colors } = require("../struc/colors");
const db = require("../struc/db");

module.exports = {
  name: "warn",
  options: [
    {
      name: "member",
      required: true,
      description: "The member to warn",
      type: 6,
    },
    {
      name: "reason",
      required: false,
      description: "The reason for the warning",
      type: 3,
    },
  ],
  description: "Warns a member.",
  async run(bot, interaction, Eris) {
    await interaction.createMessage("Fetching member...");
    let prev_warn_id = await db.fetch("SELECT id FROM warnings ORDER BY id DESC LIMIT 1;");

    if (prev_warn_id.length === 0) {
      prev_warn_id = [{ id: "-1" }];
    }

    const next_warn_id = parseInt(prev_warn_id[0].id) + 1;

    let reason;

    if (!interaction.data.options[1]) {
      reason = "No reason given.";
    } else {
      reason = interaction.data.options[1].value;
    }

    await db.modify("INSERT INTO warnings VALUES($1,$2,$3,$4,$5)", [
      interaction.channel.guild.id,
      interaction.data.options[0].value,
      interaction.member.id,
      reason,
      next_warn_id,
    ]);
    await interaction.createMessage(`Successfully warned <@${interaction.data.options[0].value}>! Reason: \`\`\`${reason}\`\`\``);
  }
};
