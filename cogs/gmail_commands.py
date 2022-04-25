from discord.ext import commands, vbu

from cogs.GmailConnection.requester import Requester
from cogs.bot_start import get_messages, create_embed

class GmailCommands(vbu.Cog):

    @commands.command()
    async def force_get_messages(self, ctx: vbu.Context):
        """
        Forces the bot to read all messages from the inbox
        """
        messages = get_messages()

        for message in messages:
            embed = create_embed(message)
            await ctx.send(embed=embed)

        await ctx.okay()


def setup(bot: vbu.Bot):
    x = GmailCommands(bot)
    bot.add_cog(x)
