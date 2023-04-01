from discord.ext import commands, vbu, tasks
from discord import TextChannel, AllowedMentions

from cogs.GmailConnection.requester import Requester
from cogs.bot_start import BotStart

from bs4 import BeautifulSoup
import re

class EmailNotifier(vbu.Cog):

    TIME_TO_WAIT = 0.1 # in hours
    CHANNEL_ID = 913280556169592893 # Announcements

    def __init__(self, bot: vbu.Bot):
        super().__init__(bot)
        self.send_new_emails.start()

        self.bot: vbu.Bot

    @tasks.loop(seconds=TIME_TO_WAIT * 3600)
    async def send_new_emails(self):
        """
        The main email check task that checks if any new emails were sent and announes them in the announcement channel
        """
        await self.bot.wait_until_ready()
        self.bot.logger.info("Restarting Email Task!")

        try:
            messages = self.bot.requester.get_new_emails()
        except Exception as e:
            self.bot.requester.__login__()
            self.send_new_emails.restart()
            return

        channel = self.bot.get_channel(self.CHANNEL_ID)

        for message in messages:
            if "weeklyemail" in message["subject"].replace(" ", "").lower():
                if 'html_body' in message.keys():
                    match = re.search(r"This email was sent by (?P<name>[a-zA-Z]+ [a-zA-Z]+) using the Email My Team application", message['html_body'])
                else:
                    match = re.search(r"This email was sent by (?P<name>[a-zA-Z]+ [a-zA-Z]+) using the Email My Team application", message['body'])
                        
                sender = None
                if match:
                    sender = match.group("name")

                self.bot.logger.info(f"Found Weekly Email")

                if sender:
                    sender_id = 0
                    async with self.bot.database() as db:
                        sender_id = await db(
                            """UPDATE 
                            user_settings 
                            SET is_sent = $1 WHERE user_name = $2 
                            RETURNING (user_id)""", 
                            True, sender
                        )
                        
                    if sender_id:
                        sender_id = sender_id[0]['user_id']
                        await self.bot.get_user(sender_id).send(
                            "Your weekly email has been recieved!"
                            )

                    self.bot.logger.info(f"Found Weekly Email Sender by name {sender}")
                    if sender.lower().replace(' ', '') == self.bot.config['cfa']['weekly_email_trigger']:
                        self.bot.logger.info(f"Sent Weekly Email Mass Reminder")
                        embed = self.get_weekly_embed()
                        await channel.send(embed=embed)

            else:
                embed = self.create_embed(message)
                await channel.send(content="@everyone", embed=embed, allowed_mentions=AllowedMentions.all())

    @staticmethod
    def create_embed(message):
        """
        Makes a nice lookin' embed given an email info dictionary
        """
        embed = vbu.Embed(use_random_colour=True)

        embed.title = "New Email!"

        body = message['body']
        if 'html_body' in message.keys():
            body = BeautifulSoup(message['html_body']).get_text()
        body = body.split('\n')
        if body[0] == "---------- Forwarded message ---------":
            body = body[5:]
        body = '\n'.join(body)
        body = "No Body Found" if body == "" else body[0:500] + ("\n*...\n Content Cropped*" if len(body) > 500 else "")
        subject = "No Subject Found" if message["subject"] == "" else message["subject"]

        embed.add_field(name = subject , value = body, inline = False)

        embed.description = "*Make sure to check the email through your inbox! Messages displayed here may be incorrect or incomplete*\n.\n.\n.\n"

        return embed
        
    @staticmethod
    def get_weekly_embed():
        """
        Creates the nice lookin embed for the weekly email - this doesn't change based on any parameters
        It's the same embed every time (with a random color)
        """
        embed = vbu.Embed(use_random_colour=True)

        embed.title = "Weekly Email!"
        embed.description = "Make sure to check your inbox for your trainer's email! (There might be a survey!)"

        return embed

    @staticmethod
    def get_no_weekly_embed():
        """
        Creates the nice lookin embed for when there's no weekly email - this doesn't change based on any parameters
        It's the same embed every time (with a random color)
        """
        embed = vbu.Embed(use_random_colour=True)

        embed.title = "No Weekly Email!"
        embed.description = "There will not be a weekly email this week. Make sure to check your inbox for the most up-to-date info."

        return embed

    @commands.command(aliases=['fse', 'send_emails'])
    @commands.has_permissions(manage_guild=True)
    async def force_send_emails(self, ctx: vbu.Context, channel: TextChannel = None):
        """
        Forces the bot to read all messages from the inbox
        """
        messages = self.bot.requester.get_new_emails()
        channel = channel or ctx.channel

        for message in messages:
            embed = self.create_embed(message)
            await channel.send(embed=embed)

        await ctx.okay()

    @commands.command(aliases=['fwa', 'weekly', 'force_weekly'])
    @commands.has_permissions(manage_guild=True)
    async def force_weekly_announcement(self, ctx: vbu.Context, channel: TextChannel = None):
        """
        Forces the bot to send the weekly email announcement message
        """
        channel = channel or ctx.channel

        embed = self.get_weekly_embed()
        await channel.send(embed=embed)
        await ctx.okay()

    @commands.command(aliases=['nfwa', 'nweekly', 'force_no_weekly'])
    @commands.has_permissions(manage_guild=True)
    async def force_no_weekly_announcement(self, ctx: vbu.Context, channel: TextChannel = None):
        """
        Forces the bot to send the "there is no" weekly email announcement message
        """
        channel = channel or ctx.channel

        embed = self.get_no_weekly_embed()
        await channel.send(embed=embed)
        await ctx.okay()


    def cog_unload(self):
        self.send_new_emails.cancel()

def setup(bot: vbu.Bot):
    x = EmailNotifier(bot)
    bot.add_cog(x)
