from discord.ext import commands, vbu

from cogs.GmailConnection.requester import Requester
from cogs.bot_start import BotStart

class GmailCommands(vbu.Cog):

    @commands.command()
    async def force_get_messages(self, ctx: vbu.Context):
        """
        Forces the bot to read all messages from the inbox
        """
        messages = self.bot.requester.get_messages()

        for message in messages:
            embed = BotStart.create_embed(message)
            await ctx.send(embed=embed)

        await ctx.okay()

def setup(bot: vbu.Bot):
    x = GmailCommands(bot)
    bot.add_cog(x)
