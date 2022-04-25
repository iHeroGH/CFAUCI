from discord.ext import commands, vbu

from cogs.GmailAPI.requester import Requester

class BotStart(vbu.Cog):

    @vbu.Cog.listener()
    async def on_ready(self):
        """
        Create a new requester object when the bot starts
        """
        requester = Requester()
        self.bot.requester = requester


def setup(bot: vbu.Bot):
    x = BotStart(bot)
    bot.add_cog(x)
