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
    },
    {
        type: 1,
        name: "close",
        description: "Close a ticket.",
        options: [
            {
                type: 3,
                name: "reason",
                description: "Reason for closing the ticket.",
                required: false,
            },
        ],
    }
  ],
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
                
            case "close":
                let ticket_id = await db.fetch("SELECT * FROM ticket_data WHERE channel_id = $1", [interaction.channel.id]);

                if (ticket_id.length <= 0) return interaction.createMessage({content: "This channel is not a ticket!", flags: 64});

                const now = Math.round((new Date()).getTime() / 1000);

                await db.modify("UPDATE ticket_data SET closed_by_id = $1 WHERE channel_id = $2", [interaction.member?.id, interaction.channel.id]);
                await db.modify("UPDATE ticket_data SET close_time = $1 WHERE channel_id = $2", [now.toString(), interaction.channel.id]);

                let ticket_log_channel_id = await db.fetch("SELECT ticket_log_channel_id FROM tickets WHERE guild_id = $1", [(interaction as any).channel.guild.id]);

                let ticket_log_channel: Eris.TextChannel = (bot as any).getChannel(ticket_log_channel_id[0].ticket_log_channel_id);

                await interaction.defer();

                if (ticket_log_channel) {
                    let ticket_data = await db.fetch("SELECT * FROM ticket_data WHERE channel_id = $1", [interaction.channel.id]);

                    let ticket_log_embed = {
                        title: "Ticket has been closed",
                        fields: [
                            {name: "Ticket Name", value: `${ticket_data[0].name}`},
                            {name: "Ticket Creator", value: `<@${ticket_data[0].creator_id}>`},
                            {name: "Ticket Creation Reason", value: `${ticket_data[0].ticket_open_reason}`},
                            {name: "Ticket Creation Time", value: `<t:${ticket_data[0].open_time}>`},
                            {name: "Ticket Closer", value: `<@${ticket_data[0].closed_by_id}>`},
                            {name: "Ticket Closing Time", value: `<t:${now}>`},
                            {name: "Ticket Closing Reason", value: `\`\`\`${(interaction as any).data.options[0].value || "No reason provided."}\`\`\``}
                        ],
                        color: colors.default
                    }
                    fs.writeFile(`./tmp/ticket-${ticket_data[0].channel_id}.txt`, ticket_data[0].transcript, async () => {
                        await ticket_log_channel.createMessage({ embeds: [ticket_log_embed] }, {file: fs.readFileSync(`./tmp/ticket-${ticket_data[0].channel_id}.txt`), name: `ticket-${interaction.member?.username}.txt`});
                        fs.unlinkSync(`./tmp/ticket-${ticket_data[0].channel_id}.txt`)
                    });
                }

                await db.modify("DELETE FROM ticket_data WHERE channel_id = $1", [interaction.channel.id]);
                await interaction.createMessage("Ticket will be closed in 5 seconds.");
                setTimeout(async () => {
                    await bot.deleteChannel(interaction.channel.id, "Ticket was closed.");
                }, 5000);
    }
  },
};
