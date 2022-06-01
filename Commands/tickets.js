// TODO: Permissions stuff

const { colors } = require("../struc/colors");
const db = require("../struc/db");

module.exports = {
  name: "tickets",
  options: [
    {
        type: 1,
        name: "send",
        description: "Send the ticket creation embed.",
    },
    {
        type: 1,
        name: "supporters",
        description: "Define the ticket support roles.",
        options: [
            {
                type: 3,
                name: "supporter_roles",
                description: "The ticket support roles, each one is seperated by a ','.",
                required: true,
            },
        ],
    },
    {
        type: 1,
        name: "category",
        description: "Define the ticket category.",
        options: [
            {
                type: 7,
                name: "category",
                description: "The ticket category.",
                required: true,
            },
        ],
    }
  ],
  description: "The ticket system.",
  async run(bot, interaction, Eris) {
    const ticket_creation_embed = {
        title: "Ticket creation",
        description: "Press the button below to create a ticket.",
        color: colors.default
    }

    switch (interaction.data.options[0].name) {
        case "send":
            return interaction.channel.createMessage({
                embed: ticket_creation_embed,
                components: [
                    {
                        type: 1,
                        components: [
                            {
                                type: 2, label: "Create a ticket", style: 1, custom_id: "ticket_creation_button"
                            }
                        ]
                    }
                ]
            });
        case "supporters":
            let support_roles = interaction.data.options[0].options[0].value;

            support_roles = support_roles.replace(/\s/g, "");

            support_roles = support_roles.replace(/</g, "");
            support_roles = support_roles.replace(/>/g, "");

            support_roles = support_roles.replace(/@&/g, "");

            support_roles = support_roles.split(",");

            let final_support_roles = "";

            for (let i = 0; i < support_roles.length; i++) {
                let role = interaction.channel.guild.roles.find(r => r.id === support_roles[i]);

                if (role) {
                    final_support_roles += `${role.id},`;
                }
            }

            if (final_support_roles.length <= 0) {
                return interaction.channel.createMessage("The given roles are invalid.");
            }

            const exists = await db.fetch("SELECT * FROM tickets WHERE guild_id = $1", [interaction.channel.guild.id]);

            if (exists.length <= 0) {
                const sql = "INSERT INTO tickets (guild_id, ticket_mod_roles) VALUES ($1, $2)";
                const binds = [interaction.channel.guild.id, final_support_roles];
                db.modify(sql, binds);
            } else if (exists.length > 0) {
                const sql = "UPDATE tickets SET ticket_mod_roles = $1 WHERE guild_id = $2";
                const binds = [final_support_roles, interaction.channel.guild.id];
                db.modify(sql, binds);
            }

            await interaction.createMessage(`Successfully set the ticket support roles!`);
            break;

        case "category":
            // Gotta do the rest of this later
            let category_id = interaction.data.options[0].options[0].value;

            break;
    }
  },
};
