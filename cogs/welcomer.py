import discord
from discord.ext import commands, vbu


class Welcomer(vbu.Cog):

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        await self.send_welcome_message(member)

    @commands.command()
    @commands.has_permissions(manage_guild=True)
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
        embed = vbu.Embed(title = "Welcome to Chick-Fil-A!")
        embed.description = ("Hello, hello! Welcome to the team and to the *Unofficial* CFA UCI Discord server!\n\n"
                            "As of right now you aren't able to see much of the server but we can fix that in a jiffy :D"
                            "**Just go ahead and make sure to grab you roles in the <#913262423585202278> channel on the server.**\n\n"
                            "Once you do so, you should have access to the rest of the server!"
                            "Make sure you also read the <#913258973057126440> of the server so you don't get banned ;)\n\n Thanks for joining us for the ride <3")

def setup(bot: vbu.Bot):
    x = Welcomer(bot)
    bot.add_cog(x)
