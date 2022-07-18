// TODO: Permissions stuff
import Eris = require("eris")

module.exports = {
  name: "clear",
  options: [
    {
      name: "limit",
      description: "The amount of messages to delete.",
      type: 4,
      required: true,
      min_value: 1,
      max_value: 100,
    },
  ],
  permission: BigInt(1 << 13),
  description: "Clears an amount of messages.",
  async run(bot: Eris.Client, interaction: Eris.CommandInteraction) {
    return (interaction as any).channel.purge({ limit: (interaction as any).data.options[0].value }).then((amount: number) => {return interaction.createMessage(`Successfully deleted ${amount} messages.`);})
    .catch((err: Error) => {
        console.log(err);
        return interaction.createMessage({content: `An unkown error occured. Please report this error in the support server! Error \`\`\`${err}\`\`\``, flags: 64});
      });
  },
};
