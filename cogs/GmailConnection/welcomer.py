import discord
from discord.ext import commands, vbu


class Welcomer(vbu.Cog):

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        await self.send_welcome_message(member)

    @commands.command()
    async def force_welcome(self, ctx: vbu.Context, member: discord.Member = None):
        """
        Forcefully sends the welcome message to the user
        """

        member = member or ctx.author

        await self.send_welcome_message(member)
        await ctx.okay()

    async def send_welcome_message(self, member: discord.Member):
        self.bot.logger.info(f"Sending welcome message to {member.id}")
        await member.send(self.get_welcome_message()) 

    @staticmethod
    def get_welcome_message() -> str:
        return "Welcome to CFA discord server blah blah"

def setup(bot: vbu.Bot):
    x = Welcomer(bot)
    bot.add_cog(x)
