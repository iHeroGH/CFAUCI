from discord.ext import commands, vbu, tasks
from discord import TextChannel, AllowedMentions

from cogs.GmailConnection.requester import Requester
from cogs.bot_start import BotStart
from bs4 import BeautifulSoup
import re

class HotSchedulesNotifier(vbu.Cog):

    TIME_TO_WAIT = 0.1 # in hours
    ANNOUNCEMENTS_CHANNEL_ID = 913280556169592893 # Announcements
    HS_CHANNEL_ID = 913255703651684372 # HotSchedules Channel

    def __init__(self, bot: vbu.Bot):
        super().__init__(bot)
        self.send_hotschedules_email.start()

        self.bot: vbu.Bot

    @tasks.loop(seconds=TIME_TO_WAIT * 3600)
    async def send_hotschedules_email(self):
        """
        The email check task that checks if any HotSchedules emails were sent
        """
        await self.bot.wait_until_ready()
        self.bot.logger.info("Restarting HS Task!")

        try:
            messages = self.bot.requester.get_hs_emails()
        except Exception as e:
            self.bot.requester.__login__()
            self.send_hotschedules_email.restart()
            return

        announcement_channel = self.bot.get_channel(self.ANNOUNCEMENTS_CHANNEL_ID)
        hs_channel = self.bot.get_channel(self.HS_CHANNEL_ID)

        for message in messages:
            sender = message['from']
            subject = message['subject']
            match = re.match(r"Your schedule for (?P<start_date>\d+/\d+/\d+) to (?P<end_date>\d+/\d+/\d+) has been posted\.", subject)

            if match:
                embed = self.get_schedule_embed(match.group("start_date"), match.group("end_date"))
                await announcement_channel.send(embed=embed)
            else:
                if sender.lower().replace(" ", "") == "helenkim":
                    continue

                embed = self.create_embed(sender)
                await hs_channel.send(embed=embed)

    @staticmethod
    def create_embed(sender):
        """
        Makes a nice lookin' embed given the HS email sender
        """
        embed = vbu.Embed(use_random_colour=True)

        embed.title = "New HotSchedules Message!"
        embed.description = f"New message found from {sender}! Check the HS app for timing details."
        embed.color = 0x0EA3D1 # HS Blue

        return embed
        
    @staticmethod
    def get_schedule_embed(start_date = None, end_date = None):
        """
        Creates the nice lookin embed for the "schedule has been released" email - this doesn't change based on any parameters
        It's the same embed every time (with different dates and the HS Blue color)
        """
        embed = vbu.Embed()

        embed.title = "Schedule Posted!" + (f" ({start_date} to {end_date})" if start_date and end_date else "")
        embed.description = "Make sure to check your inbox for your schedule!"
        embed.color = 0x0EA3D1 # HS Blue

        return embed

    @staticmethod
    def get_no_schedule_embed():
        """
        Creates the nice lookin embed for when the schedule has not yet been released - this doesn't change based on any parameters
        This embed will usually be run by a command manually    
        It's the same embed every time (with a red color)
        """
        embed = vbu.Embed()

        embed.title = "No Schedule Yet!"
        embed.description = "The schedule has not yet been released (or the HotSchedules website/app is down). Check your HS app to get the most up-to-date information."
        embed.color = 0xFF0000 # Red

        return embed

    @commands.command(aliases=['fshe', 'send__hotschedules_emails'])
    @commands.has_permissions(manage_guild=True)
    async def force_send_hs_emails(self, ctx: vbu.Context, channel: TextChannel = None):
        """
        Forces the bot to read all HotSchedules messages from the inbox
        """
        messages = self.bot.requester.get_hs_emails()
        channel = channel or ctx.channel

        for message in messages:
            sender = message['from']
            subject = message['subject']
            match = re.match(r"Your schedule for (?P<start_date>\d+/\d+/\d+) to (?P<end_date>\d+/\d+/\d+) has been posted\.", subject)

            if match:
                embed = self.get_schedule_embed(match.group("start_date"), match.group("end_date"))
                await channel.send(embed=embed)
            else:
                if sender.lower().replace(" ", "") == "helenkim":
                    continue

                embed = self.create_embed(sender)
                await channel.send(embed=embed)

    @commands.command(aliases=['fsa', 'schedule', 'force_schedule'])
    @commands.has_permissions(manage_guild=True)
    async def force_schedule_announcement(self, ctx: vbu.Context, channel: TextChannel = None, start_time = None, end_time = None):
        """
        Forces the bot to send the "schedule has been posted" embed
        """
        channel = channel or ctx.channel

        embed = self.get_schedule_embed(start_time, end_time)
        await channel.send(embed=embed)
        await ctx.okay()

    @commands.command(aliases=['nfsa', 'nschedule', 'force_no_schedule'])
    @commands.has_permissions(manage_guild=True)
    async def force_no_schedule_announcement(self, ctx: vbu.Context, channel: TextChannel = None):
        """
            Forces the bot to send the "there is no" schedule announcement message
        """
        channel = channel or ctx.channel

        embed = self.get_no_schedule_embed()
        await channel.send(embed=embed)
        await ctx.okay()


    def cog_unload(self):
        self.send_new_emails.cancel()

def setup(bot: vbu.Bot):
    x = HotSchedulesNotifier(bot)
    bot.add_cog(x)
