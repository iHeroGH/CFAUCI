from discord.ext import commands, vbu

from cogs.GmailConnection.requester import Requester

class GmailCommands(vbu.Cog):

    @commands.command()
    async def force_get_messages(self, ctx: vbu.Context):
        """
        Forces the bot to read all messages from the inbox
        """
        messages = self.bot.requester.get_messages()

        for message in messages:
            embed = self.create_embed(message)
            await ctx.send(embed=embed)

        await ctx.okay()

    def create_embed(self, message):
        embed = vbu.Embed()

        embed.title = "New Email!"
        embed.color = 0xFF00FF

        embed.add_field(name = message["subject"], value = message["body"][0:1000] + "\n*...\n Content Cropped*", inline=False)

        embed.description = "*Make sure to check the email through your inbox! Messages displayed here may be incorrect or incomplete*\n.\n.\n.\n"

        return embed



def setup(bot: vbu.Bot):
    x = GmailCommands(bot)
    bot.add_cog(x)
