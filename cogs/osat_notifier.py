from discord.ext import commands, vbu, tasks
from discord import AllowedMentions

from cogs.GmailConnection.requester import Requester
from cogs.bot_start import BotStart

from bs4 import BeautifulSoup
import re

class OsatNotifier(vbu.Cog):

    TIME_TO_WAIT = 0.25 # in hours
    CHANNEL_ID = 913280556169592893 # Announcements

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

        # We try to get the latest email
        try:
            message = self.bot.requester.get_osat_email()
        # Send a message to the owner if we run into a problem
        except Exception as e:
            if bot_owner:
                await bot_owner.send(e)
            self.bot.requester.__login__()
            self.send_osat_email.restart()
            return

        # If we couldn't find a message and we aren't overriding the scores, we don't have any scores to display
        if not message and not override:
            if not is_task:
                await ctx.send("No OSAT scores found! :(")
            return

        # Override the message if there's an override provided
        message = override or message

        # Store the newest message
        old_osat = self.latest_osat_message
        self.latest_osat_message = message

        curr_scores_dict = self.get_scores_from_message(message)
        old_scores_dict = self.get_scores_from_message(old_osat)

        embed = self.create_embed(curr_scores_dict, old_scores_dict)

        if old_osat != self.latest_osat_message: # Announce
            if is_task:
                await self.bot.get_channel(self.CHANNEL_ID).send(embed=embed)
            else:
                await ctx.send(embed=embed)
        else: # Don't announce
            await ctx.send(embed=embed)

    @staticmethod
    def get_scores_from_message(message: dict):
        # Make the OSAT email parseable
        osat_info = BeautifulSoup(message['html_body']).get_text()
        osat_info = "|".join(osat_info.split("\n"))

        # Parse the osat message and create an embed
        score_matches = re.finditer(r'\|(?P<Category>[a-zA-Z /]*)\|(?P<Score>\d*)%\|(?P<NSurveys>\d*)\|', osat_info)

        score_dict = {}
        for match in score_matches:
            score_dict[match.group('Category')] = int(match.group('Score'))

            if match.group('Category') == 'Overall Satisfaction':
                score_dict['NSurveys'] = match.group('NSurveys')

        return score_dict

    @staticmethod
    def create_embed(scores_dict: dict, old_scores_dict: dict = None):
        """
        Makes a nice lookin' embed given an OSAT score dictionary
        """
        embed = vbu.Embed()

        embed.title = "OSAT Scores"

        if "NSurveys" in scores_dict.keys():
            embed.title = f"OSAT Scores - {scores_dict['NSurveys']} surveys"

        overall_sat = scores_dict["Overall Satisfaction"]
        if overall_sat >= 70:
            embed.colour = 0x00ff00 # Green
            embed.set_footer("We are currently beating the OSAT scores for the region!")
        elif overall_sat > 67:
            embed.colour = 0xffff00 # Yellow
            embed.set_footer("We are *close* to beating the OSAT scores for the region!")
        else:
            embed.colour = 0xff0000 # Red
            embed.set_footer("We are currently **not** beating the OSAT scores for the region :(")

        score_message = ""
        # Go through each category to get its score
        for category, score in scores_dict.items():
            if category == "NSurveys":
                continue
            # If we have a set of old scores, then we want to compare the old score to the new score
            if old_scores_dict:
                old_score = old_scores_dict[category]

                # Get an identifier for the score change
                if old_score < score:
                    ident = ":green_heart:"
                elif old_score == score:
                    score_message += f"**{category}**: {score}%\n"
                    continue
                else:
                    ident = ":heart:"

                # Add the score change to the message
                score_message += f"**{category}**: {old_score}% -> {score}% {ident}\n"
            else:
                score_message += f"**{category}**: {score}%\n"

        # Set the embed description to the score message
        embed.description = score_message

        # Return the embed
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