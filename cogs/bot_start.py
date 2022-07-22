from discord.ext import commands, vbu
from cogs.GmailConnection.requester import Requester

class BotStart(vbu.Cog):

    @vbu.Cog.listener()
    async def on_ready(self):
        """
        Create a new requester object when the bot starts
        """
        self.create_requester_hard(self.bot)

    @staticmethod
    def create_requester_soft(bot):
        bot.requester: Requester
        if not bot.requester:
            requester = Requester()
            bot.requester = requester
            bot.logger.info("Created new requester object")

    @staticmethod
    def create_requester_hard(bot):
        requester = Requester()
        bot.requester = requester
        bot.logger.info("Force created new requester object")

    @commands.command(aliases=["fcr", "force_create"])
    @commands.has_permissions(manage_guild=True)
    async def force_create_requester(self, ctx: vbu.Context):
        """
        Forces the bot to create a new requester object
        """
        self.create_requester_hard(self.bot)
        await ctx.okay()

def setup(bot: vbu.Bot):
    x = BotStart(bot)
    bot.add_cog(x)
