from discord.ext import commands, vbu, tasks
from discord import AllowedMentions

from cogs.GmailConnection.requester import Requester
from cogs.bot_start import BotStart

from bs4 import BeautifulSoup
import re

class OsatNotifier(vbu.Cog):

    TIME_TO_WAIT = 0.25 # in hours
    CHANNEL_ID = 913280990145830922 # Admin Bot Commands

    def __init__(self, bot: vbu.Bot):
        super().__init__(bot)
        self.send_osat_email.start()

        self.latest_osat_message: dict = None

        self.bot: vbu.Bot

    @tasks.loop(seconds=TIME_TO_WAIT * 3600)
    async def send_osat_email(self):
        """
        The email check task that checks if any new OSAT emails were sent and announes them in the announcement channel
        """

        await self.get_osat_email()

    async def get_osat_email(self, is_task: bool = True, ctx: vbu.Context = None, override: dict = None):
        await self.bot.wait_until_ready()

        bot_owner = self.bot.get_user(322542134546661388)
        self.bot.logger.info("Restarting OSAT Task!")

        if not is_task and self.latest_osat_message and not override:
            message = self.latest_osat_message
        else:
            try:
                message = self.bot.requester.get_osat_email(is_task)
            except Exception as e:
                if bot_owner:
                    await bot_owner.send(e)
                self.bot.requester.__login__()
                self.send_osat_email.restart()
                return

        if not message and not override:
            return

        message = override or message

        # Store the newest message
        old_osat = self.latest_osat_message
        self.latest_osat_message = message

        # Make the OSAT email parseable
        osat_info = BeautifulSoup(message['html_body']).get_text()
        osat_info = "|".join(osat_info.split("\n")[2:])

        # Parse the osat message and create an embed
        score_matches = re.finditer(r'(?P<Category>\|[a-zA-Z /]*\|)(?P<Score>|\d\d)%', osat_info)
        score_string = '\n'.join([f"{i.group('Category').replace('|', '**')}: {i.group('Score')}%" for i in score_matches])
        embed = self.create_embed(score_string)

        if old_osat != self.latest_osat_message: # Announce
            await self.bot.get_channel(self.CHANNEL_ID).send(embed=embed)
        else: # Don't announce
            await ctx.send(embed=embed)

    @staticmethod
    def create_embed(message):
        """
        Makes a nice lookin' embed given an OSAT message
        """
        embed = vbu.Embed(use_random_colour=True)

        embed.title = "OSAT Scores!"
        embed.description = message

        return embed

    @commands.command(aliases=['get_osat_email', 'get_osat_scores', 'scores', 'get_osat'])
    async def osat(self, ctx: vbu.Context):
        """
        Gets the latest OSAT scores
        """
        await self.get_osat_email(False, ctx)
        await ctx.okay()

    def cog_unload(self):
        self.send_osat_email.cancel()

def setup(bot: vbu.Bot):
    x = OsatNotifier(bot)
    bot.add_cog(x)
