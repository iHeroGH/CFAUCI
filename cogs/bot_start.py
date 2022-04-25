from discord.ext import commands, vbu

from cogs.GmailConnection.requester import Requester
import asyncio

class BotStart(vbu.Cog):

    TIME_TO_WAIT = 3 # in hours
    CHANNEL_ID = 913280990145830922

    def get_messages(self):
        return self.bot.requester.get_messages()

    async def send_messages(self):
        messages = self.get_messages()
        channel = self.bot.get_channel(self.CHANNEL_ID)

        for message in messages:
            embed = self.create_embed(message)
            await channel.send(embed=embed)

    async def restart_task(self):
        await asyncio.sleep(self.TIME_TO_WAIT * 3600)
        await self.send_messages()

    def create_embed(self, message):
        embed = vbu.Embed()

        embed.title = "New Email!"
        embed.color = 0xFF00FF

        body = message['body']
        body = body.split('\n')[5:]
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
        requester = Requester()
        self.bot.requester = requester

        await self.send_messages()
        await self.restart_task()


def setup(bot: vbu.Bot):
    x = BotStart(bot)
    bot.add_cog(x)
