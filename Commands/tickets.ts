// TODO: Permissions stuff

import colors = require("../base/Colors");
import db = require("../base/Database");
import Eris = require("eris");
import fs = require("fs");

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
    },
    {
        type: 1,
        name: "log_channel",
        description: "Define the ticket log channel.",
        options: [
            {
                type: 7,
                name: "log_channel",
                description: "The ticket log channel.",
                required: true,
            },
        ],
    },
    {
        type: 1,
        name: "open_msg",
        description: "Define the ticket open message.",
        options: [
            {
                type: 3,
                name: "open_msg",
                description: "The ticket log channel.",
                required: true,
            },
        ],
    }
  ],
  permission: BigInt(1 << 5),
  description: "The ticket system.",
  async run(bot: Eris.Client, interaction: Eris.CommandInteraction) {
    const ticket_creation_embed = {
        title: "Ticket creation",
        description: "Press the button below to create a ticket.",
        color: colors.default
    }

    switch ((interaction as any).data.options[0].name) {
        case "send":
            interaction.createMessage({ content: "The embed has been created! If you haven't already make sure to define the required values using the other ticket commands, if you don't, it won't work.", flags: 64 })
            return interaction.channel.createMessage({
                embed: ticket_creation_embed,
                components: [
                    {
                        type: 1,
                        components: [
                            {
                                type: 2, label: "Create a ticket", style: 1, custom_id: "ticket_creation_button", disabled: false
                            }
                        ]
                    }
                ]
            });
        case "supporters":
            let support_roles = (interaction as any).data.options[0].options[0].value;

            support_roles = support_roles.replace(/\s/g, "");

            support_roles = support_roles.replace(/</g, "");
            support_roles = support_roles.replace(/>/g, "");

            support_roles = support_roles.replace(/@&/g, "");

            support_roles = support_roles.split(",");

            let final_support_roles = "";

            for (let i = 0; i < support_roles.length; i++) {
                let role = (interaction as any).channel.guild.roles.find((r: { id: any }) => r.id === support_roles[i]);

                if (role) {
                    final_support_roles += `${role.id},`;
                }
            }

            if (final_support_roles.length <= 0) {
                return interaction.createMessage("The given roles are invalid.");
            }

            const support_roles_exists = await db.fetch("SELECT * FROM tickets WHERE guild_id = $1", [(interaction as any).channel.guild.id]);

            if (support_roles_exists.length <= 0) {
                const sql = "INSERT INTO tickets (guild_id, ticket_mod_roles) VALUES ($1, $2)";
                const binds = [(interaction as any).channel.guild.id, final_support_roles];
                db.modify(sql, binds);
            } else if (support_roles_exists.length > 0) {
                const sql = "UPDATE tickets SET ticket_mod_roles = $1 WHERE guild_id = $2";
                const binds = [final_support_roles, (interaction as any).channel.guild.id];
                db.modify(sql, binds);
            }

            await interaction.createMessage(`Successfully set the ticket support roles!`);
            break;

        case "category":
            let category_id = (interaction as any).data.options[0].options[0].value;

            const category = bot.getChannel(category_id);

            const category_exists = await db.fetch("SELECT * FROM tickets WHERE guild_id = $1", [(interaction as any).channel.guild.id]);

            if (category_exists.length <= 0) {
                const sql = "INSERT INTO tickets (guild_id, ticket_category_id) VALUES ($1, $2)";
                const binds = [(interaction as any).channel.guild.id, category.id];
                db.modify(sql, binds);
            } else if (category_exists.length > 0) {
                const sql = "UPDATE tickets SET ticket_category_id = $1 WHERE guild_id = $2";
                const binds = [category.id, (interaction as any).channel.guild.id];
                db.modify(sql, binds);
            }

            await interaction.createMessage("Successfully set the ticket category!");
            break;
        case "log_channel":
            let log_channel_id = (interaction as any).data.options[0].options[0].value;

            const log_channel = bot.getChannel(log_channel_id);

            const log_channel_exists = await db.fetch("SELECT * FROM tickets WHERE guild_id = $1", [(interaction as any).channel.guild.id]);

            if (log_channel_exists.length <= 0) {
                const sql = "INSERT INTO tickets (guild_id, ticket_log_channel_id) VALUES ($1, $2)";
                const binds = [(interaction as any).channel.guild.id, log_channel.id];
                db.modify(sql, binds);
            } else if (log_channel_exists.length > 0) {
                const sql = "UPDATE tickets SET ticket_log_channel_id = $1 WHERE guild_id = $2";
                const binds = [log_channel.id, (interaction as any).channel.guild.id];
                db.modify(sql, binds);
            }
            
            await interaction.createMessage("Successfully set the ticket log channel!");
            break;
            
            case "open_msg":
                let open_msg = (interaction as any).data.options[0].options[0].value;
    
                const open_msg_exists = await db.fetch("SELECT * FROM tickets WHERE guild_id = $1", [(interaction as any).channel.guild.id]);
    
                if (log_channel_exists.length <= 0) {
                    const sql = "INSERT INTO tickets (guild_id, ticket_open_message) VALUES ($1, $2)";
                    const binds = [(interaction as any).channel.guild.id, open_msg];
                    db.modify(sql, binds);
                } else if (log_channel_exists.length > 0) {
                    const sql = "UPDATE tickets SET ticket_open_message = $1 WHERE guild_id = $2";
                    const binds = [open_msg, (interaction as any).channel.guild.id];
                    db.modify(sql, binds);
                }
                
                await interaction.createMessage("Successfully set the ticket open message!");
                break;
    }
  },
};
