from discord.ext import commands, vbu, tasks

from cogs.GmailConnection.requester import Requester
import asyncio
from bs4 import BeautifulSoup

class BotStart(vbu.Cog):

    TIME_TO_WAIT = 0.5 # in hours
    CHANNEL_ID = 913280556169592893

    def __init__(self, bot: vbu.Bot):
        super().__init__(bot)
        self.bot.requester = Requester()
        self.send_messages.start()

    @tasks.loop(seconds=TIME_TO_WAIT * 3600)
    async def send_messages(self):
        bot_owner = self.bot.get_user(322542134546661388)
        if bot_owner:
            await bot_owner.send("Restarting task")
        try:
            messages = self.get_messages()
        except Exception as e:
            if bot_owner:
                await bot_owner.send(e)
            self.bot.requester.__login__()
            self.send_messages.restart()
            return

        channel = self.bot.get_channel(self.CHANNEL_ID)

        for message in messages:
            embed = self.create_embed(message)
            await channel.send(content="@everyone", embed=embed, allowed_mentions=discord.AllowedMentions.all())

    def get_messages(self):
        return self.bot.requester.get_messages()

    def create_embed(self, message):
        embed = vbu.Embed()

        embed.title = "New Email!"
        embed.color = 0xFF00FF

        body = message['body']
        if 'html_body' in message.keys():
            body = BeautifulSoup(message['html_body']).get_text()
        body = body.split('\n')
        if body[0] == "---------- Forwarded message ---------":
            body = body[5:]
        body = '\n'.join(body)
        body = "No Body Found" if body == "" else body[0:500] + ("\n*...\n Content Cropped*" if len(body) > 500 else "")
        subject = "No Subject Found" if message["subject"] == "" else message["subject"]

        embed.add_field(name = subject , value = body, inline=False)

        embed.description = "*Make sure to check the email through your inbox! Messages displayed here may be incorrect or incomplete*\n.\n.\n.\n"

        return embed

    @vbu.Cog.listener()
    async def on_ready(self):
        """
        Create a new requester object when the bot starts
        """
        if not self.bot.requester:
            requester = Requester()
            self.bot.requester = requester

    def cog_unload(self):
        self.send_messages.cancel()

def setup(bot: vbu.Bot):
    x = BotStart(bot)
    bot.add_cog(x)
