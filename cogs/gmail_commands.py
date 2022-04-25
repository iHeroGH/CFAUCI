from discord.ext import commands, vbu

from cogs.GmailConnection.requester import Requester

class GmailCommands(vbu.Cog):

    @commands.command()
    async def partial(self, ctx: vbu.Context):
        """
        messages
        """
        await ctx.send(self.bot.requester.get_partial_message_list())

    @commands.command()
    async def full(self, ctx: vbu.Context, message_id: str):
        """
        messages
        """
        f = self.bot.requester.get_message(message_id)
        await ctx.send(f['snippet'])


def setup(bot: vbu.Bot):
    x = GmailCommands(bot)
    bot.add_cog(x)
