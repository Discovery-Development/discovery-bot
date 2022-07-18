import colors = require("../base/Colors");
import Eris = require("eris");
import db = require("../base/Database");
import fs = require("fs");

module.exports = {
  name: "close",
  description: "Closes a ticket.",
  options: [
    {
        type: 3,
        name: "reason",
        description: "Reason for closing the ticket.",
        required: false,
    },
  ],
  async run(bot: Eris.Client, interaction: Eris.CommandInteraction) {
    let ticket_id = await db.fetch("SELECT * FROM ticket_data WHERE channel_id = $1", [interaction.channel.id]);

    let reason;

    if(!(interaction as any).data.options) reason = "No reason provided.";
    else reason = (interaction as any).data.options[0].value

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
                {name: "Ticket Closing Reason", value: `\`\`\`${reason}\`\`\``}
            ],
            color: colors.default
        }
        if (ticket_data[0].transcript) {
          fs.writeFile(`./tmp/ticket-${ticket_data[0].channel_id}.txt`, ticket_data[0].transcript, async () => {
            await ticket_log_channel.createMessage({ embeds: [ticket_log_embed] }, {file: fs.readFileSync(`./tmp/ticket-${ticket_data[0].channel_id}.txt`), name: `ticket-${interaction.member?.username}.txt`});
            fs.unlinkSync(`./tmp/ticket-${ticket_data[0].channel_id}.txt`)
          });
        } else {
          await ticket_log_channel.createMessage({ embeds: [ticket_log_embed] });
        }
    }

    await db.modify("DELETE FROM ticket_data WHERE channel_id = $1", [interaction.channel.id]);
    await interaction.createMessage("Ticket will be closed in 10 seconds.");
    setTimeout(async () => {
        await bot.deleteChannel(interaction.channel.id, "Ticket was closed.");
    }, 10000);
  },
};
