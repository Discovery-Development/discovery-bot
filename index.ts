import Eris from "eris";
import { fetch } from "./base/Database"
import dotEnv from "dotenv";
import colors from "./base/Colors";
import cliColors from "./base/CLIColors";
import db = require("./base/Database");
import fs = require("fs");
dotEnv.config();

const bot = new Eris.Client((process.env.TOKEN as string), {
  firstShardID: 0,
  lastShardID: 15,
  maxShards: 16,
  getAllUsers: true,
  intents: [
    "guilds",
    "guildMessages",
    "guildMembers",
    "guildEmojisAndStickers",
    "directMessages",
    "guildPresences",
    "guildMessageReactions"
  ],
  restMode: false
});

(bot as any).commands = new Map();
["commandHandler" /* Just so you can add multiple handlers flexibly */].forEach(async (handler) => {
  const handler_func = await import(`./Handlers/${handler}`);
  handler_func.default(bot);
});

bot.on("ready", async () => {
  bot.editStatus("online", { name: "i forgor", type: 0 });

  const selfUser: Eris.ExtendedUser = await bot.getSelf();

  console.log(`Successfully connected to Discord API. Logged in as ${selfUser.username}#${selfUser.discriminator}\nActive on ${Object.keys(bot.guilds).length} servers.`);

  const guildId: string = "943824727242321980";

  for (const cmd of (bot as any).commands) {
    const command = (bot as any).commands.get(cmd[0]);

    bot.createGuildCommand(guildId, {
      name: command.name,
      description: command.description,
      options: command.options || undefined,
      type: 1,
    });

    console.log(`Created "${command.name}" application command.`);
    //db.modify("DELETE FROM ticket_data"); // ONLY for testing purposes
  }
  console.timeEnd("ready");
});

bot.on("shardReady", (id) => {
  console.log(`Shard ${id} ready!`);
});

// Slash-command handler
bot.on("interactionCreate", async (interaction: Eris.Interaction) => {
//######################################################
//##                Command Handling                  ##
//######################################################
  if ((interaction instanceof Eris.CommandInteraction)) {
    const command = (bot as any).commands.get(interaction.data.name);

    const permission = command.permission;

    if (command && permission) {
      if (interaction.member?.permissions.has(permission)) await command.run(bot, interaction);
      else return interaction.createMessage({ content: `You are missing the following permission: ${permission}\n\nIf you think this is a mistake, please contact the bot's developer.`, flags: 64});
    } else if (command && !permission) {
      await command.run(bot, interaction);
    }
  }
//######################################################
//##                 Ticket System                    ##
//######################################################

  if (interaction instanceof Eris.ComponentInteraction) {
    if (interaction.data.custom_id === "ticket_creation_button") {
      const ticketCreationReasonEmbed = {
        title: "Ticket creation reason",
        description: "Please choose the reason for creating this ticket.",
        color: colors.default,
      };

      const options = [
        {
          label: "Support",
          value: "support",
          description: "Your ticket will be about support",
          emoji: {name: "⛑", id:null}
        },
        {
          label: "Question",
          value: "question",
          description: "Your ticket will be about a question.",
          emoji: {name: "❓", id: null}
        },
        {
          label: "Report",
          value: "report",
          description: "Your ticket will be about a report.",
          emoji: { name: "♻", id: null}
        },
        {
          label: "Application",
          value: "application",
          description: "Your ticket will be about an application.",
          emoji: { name: "🎯", id: null}
        }
      ];
      
      await interaction.createMessage({
        embeds: [ticketCreationReasonEmbed],
        components: [
          {
            type: 1,
            components: [
              {
                type: 3,
                options: options,
                custom_id: "ticket_creation_reason_dropdown",
                min_values: 1,
                max_values: 1,
              },
            ],
          },
        ], flags: 64
      });
    } else if (interaction.data.custom_id === "ticket_creation_reason_dropdown") {
      await interaction.deferUpdate();
      const options = [
        {
          label: "Support",
          value: "support",
          description: "Your ticket will be about support",
          emoji: {name: "⛑", id:null}
        },
        {
          label: "Question",
          value: "question",
          description: "Your ticket will be about a question.",
          emoji: {name: "❓", id: null}
        },
        {
          label: "Report",
          value: "report",
          description: "Your ticket will be about a report.",
          emoji: { name: "♻", id: null}
        },
        {
          label: "Application",
          value: "application",
          description: "Your ticket will be about an application.",
          emoji: { name: "🎯", id: null}
        }
      ];

      let ticket_category_id = await db.fetch("SELECT ticket_category_id FROM tickets WHERE guild_id = $1", [ (interaction as any).channel.guild.id ]);
      let ticket_open_message = await db.fetch("SELECT ticket_open_message FROM tickets WHERE guild_id = $1", [ (interaction as any).channel.guild.id ]);

      let ticket_category = bot.getChannel(ticket_category_id[0].ticket_category_id);

      if (!ticket_open_message) {
        const sql = "UPDATE tickets SET ticket_open_message = $1 WHERE guild_id = $2;";
        const binds = ["Moderators will soon be with you, please be patient!", (interaction as any).channel.guild.id];
        await db.modify(sql, binds);
      }

      ticket_open_message = await db.fetch("SELECT ticket_open_message FROM tickets WHERE guild_id = $1", [ (interaction as any).channel.guild.id ]);

      let ticket_opened_embed = {
        title: "Your Ticket",
        description: ticket_open_message[0].ticket_open_message,
        color: colors.default
      };

      let ticket_channel = await bot.createChannel((interaction as any).channel.guild.id, `ticket-${interaction.member?.username}`, 0, { parentID: ticket_category.id });

      const now = Math.round((new Date()).getTime() / 1000);

      await ticket_channel.createMessage({ embeds: [ticket_opened_embed], 
      components: [
        {
          type: 1,
          components: [
            {
              type: 2,
              label: "Close Ticket",
              style: 1,
              custom_id: "ticket_close_button",
              disabled: false
            },
          ],
        },
      ]
    });

      await ticket_channel.editPermission((interaction.member?.id as string), 0x0000000000000400, 0x0000010000000000, 1, "PLACEHOLDER");

      await (interaction as any).editParent({ embeds: null, content: `Your new ticket has been created! Check it out at <#${ticket_channel.id}>`, 
      components: [
        {
          type: 1,
          components: [
            {
              type: 3,
              options: options,
              custom_id: "ticket_creation_reason_dropdown",
              min_values: 1,
              max_values: 1,
              disabled: true
            },
          ],
        },
      ] 
    });
      // TODO: Ticket logging
      let ticket_binds = [ (interaction as any).channel.guild.id, ticket_channel.id, ticket_channel.name, interaction.member?.id, now.toString(), (interaction as any).data.values[0] ];

      db.modify("INSERT INTO ticket_data(guild_id, channel_id, name, creator_id, open_time, ticket_open_reason) VALUES($1,$2,$3,$4,$5,$6);", ticket_binds);

      const ticket_log_channel_id = await db.fetch("SELECT ticket_log_channel_id FROM tickets WHERE guild_id = $1", [interaction.channel.guild.id]);

      const ticket_log_channel: Eris.TextChannel = await (bot as any).getChannel(ticket_log_channel_id[0].ticket_log_channel_id);

      if (ticket_log_channel) {
        const ticket_embed = {
          title: "New ticket has been opened",
          color: colors.default,
          fields: [
            { name: "Creator", value: `<@!${interaction.member?.id}>` },
            { name: "Channel", value: `<#${ticket_channel.id}>` },
            { name: "Opened at", value: `<t:${now}>` },
            { name: "Creation Reason", value: (interaction as any).data.values[0] }
          ]
        };
        await ticket_log_channel.createMessage({embeds: [ ticket_embed ]});
      }
    } else if (interaction.data.custom_id === "ticket_close_button") {
      const now = Math.round((new Date()).getTime() / 1000);

      await db.modify("UPDATE ticket_data SET closed_by_id = $1 WHERE channel_id = $2", [interaction.member?.id, interaction.channel.id]);
      await db.modify("UPDATE ticket_data SET close_time = $1 WHERE channel_id = $2", [now.toString(), interaction.channel.id]);

      let ticket_log_channel_id = await db.fetch("SELECT ticket_log_channel_id FROM tickets WHERE guild_id = $1", [(interaction as any).channel.guild.id]);

      let ticket_log_channel: Eris.TextChannel = (bot as any).getChannel(ticket_log_channel_id[0].ticket_log_channel_id);

      await interaction.deferUpdate();

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
                {name: "Ticket Closing Reason", value: `\`\`\`No reason provided.\`\`\``}
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
  }
});

bot.on("messageReactionAdd", async (message:Eris.Message, emoji: { name: string; id: string}, reactor: Eris.User) => {
  if (emoji.id !== null) {
    emoji.name = `<:${emoji.name}:${emoji.id}>`;
  }
  let reaction_role = await fetch("SELECT * FROM reaction_roles WHERE message_id = $1 AND emoji = $2;", [message.id, emoji.name]);

  if (reaction_role.length > 0) {
    reaction_role = reaction_role[0];
    const role: Eris.Role = (message as any).channel.guild.roles.get(reaction_role.role_id);

    if (role) {
      const member: Eris.Member = (message as any).channel.guild.members.get(reactor.id);

      if (member) {
        member.addRole(role.id, "Reaction role added.").catch(() => {}); // Catching it because it usually means the bot doesn't have necessary permissions and 
      }                                                                  // I don't want it to crash because of that.
    }
  }
});

bot.on("messageReactionRemove", async (message:Eris.Message, emoji: { name: string; id: string}, userID: string) => {
  if (emoji.id !== null) {
    emoji.name = `<:${emoji.name}:${emoji.id}>`;
  }
  let reaction_role = await fetch("SELECT * FROM reaction_roles WHERE message_id = $1 AND emoji = $2;", [message.id, emoji.name]);

  if (reaction_role.length > 0) {
    reaction_role = reaction_role[0];
    const role: Eris.Role = (message as any).channel.guild.roles.get(reaction_role.role_id);

    if (role) {
      const member: Eris.Member = (message as any).channel.guild.members.get(userID);

      if (member) {
        member.removeRole(role.id, "Reaction role added.").catch(() => {}); // Catching it because it usually means the bot doesn't have necessary permissions and
      }                                                                     // I don't want it to crash because of that.
    }
  }
});

bot.on("messageCreate", async (message: Eris.Message) => {
  let ticket_channel_id = await db.fetch("SELECT channel_id FROM ticket_data WHERE channel_id = $1", [message.channel.id]);

  if (ticket_channel_id.length > 0) {
    let ticket_transcript = await db.fetch("SELECT transcript FROM ticket_data WHERE channel_id = $1", [message.channel.id]);
    ticket_transcript = ticket_transcript[0].transcript;

    if(!ticket_transcript) ticket_transcript = `Transcript of ${(message as any).channel.name}`;

    ticket_transcript += `\n[Message from ${(message as any).member?.username + (message as any).member?.discriminator}, Creation Time: ${message.createdAt}]\n${message.content}`;

    await db.modify("UPDATE ticket_data SET transcript = $1 WHERE channel_id = $2", [ ticket_transcript, message.channel.id]);
  }
});

bot.on("channelDelete", async (channel: Eris.AnyChannel) => {
  const now = Math.round((new Date()).getTime() / 1000);

      await db.modify("UPDATE ticket_data SET closed_by_id = $1 WHERE channel_id = $2", [0, channel.id]);
      await db.modify("UPDATE ticket_data SET close_time = $1 WHERE channel_id = $2", [now.toString(), channel.id]);

      let ticket_log_channel_id = await db.fetch("SELECT ticket_log_channel_id FROM tickets WHERE guild_id = $1", [(channel as any).guild.id]);

      let ticket_log_channel: Eris.TextChannel = (bot as any).getChannel(ticket_log_channel_id[0].ticket_log_channel_id);

      if (ticket_log_channel) {
        let ticket_data = await db.fetch("SELECT * FROM ticket_data WHERE channel_id = $1", [channel.id]);
        let ticket_log_embed = {
            title: "Ticket has been closed",
            fields: [
                {name: "Ticket Name", value: `${ticket_data[0].name}`},
                {name: "Ticket Creator", value: `<@${ticket_data[0].creator_id}>`},
                {name: "Ticket Creation Reason", value: `${ticket_data[0].ticket_open_reason}`},
                {name: "Ticket Creation Time", value: `<t:${ticket_data[0].open_time}>`},
                {name: "Ticket Closer", value: `<@${ticket_data[0].closed_by_id}>`},
                {name: "Ticket Closing Time", value: `<t:${now}>`},
                {name: "Ticket Closing Reason", value: `\`\`\`No reason provided.\`\`\``}
            ],
            color: colors.default
        }
        
        fs.writeFile(`./tmp/ticket-${ticket_data[0].channel_id}.txt`, ticket_data[0].transcript, async () => {
          await ticket_log_channel.createMessage({ embeds: [ticket_log_embed] }, {file: fs.readFileSync(`./tmp/ticket-${ticket_data[0].channel_id}.txt`), name: `ticket-transcript.txt`});
          fs.unlinkSync(`./tmp/ticket-${ticket_data[0].channel_id}.txt`)
        });
      }
});

console.time("ready");
bot.connect();

/*process.on("uncaughtException", (err) => {
  console.log(`[${cliColors.red}ERROR${cliColors.reset}] An error unrelated to Eris occured in the main process => \n\n${err}\n`);
  process.exit();
});*/