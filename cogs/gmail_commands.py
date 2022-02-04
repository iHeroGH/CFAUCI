from discord.ext import commands, vbu
from GmailAPI import Requester

class GmailCommands(vbu.Cog):

    @commands.command()
    async def partial(self, ctx: vbu.Context):
        """
        messages
        """
        requester = Requester()
        await ctx.send(requester.get_partial_message_list())

    @commands.command()
    async def full(self, ctx: vbu.Context, message_id: str):
        """
        messages
        """
        requester = Requester()
        await ctx.send(requester.get_message(message_id))


def setup(bot: vbu.Bot):
    x = GmailCommands(bot)
    bot.add_cog(x)
