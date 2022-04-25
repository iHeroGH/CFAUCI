from discord.ext import commands, vbu

from cogs.GmailConnection.requester import Requester
import asyncio

class BotStart(vbu.Cog):

    TIME_TO_WAIT = 3 # in hours
    CHANNEL_ID = 913280990145830922

    async def send_messages(self):
        messages = self.bot.requester.get_messages()
        channel = self.bot.get_channel(self.CHANNEL_ID)

        for message in messages:
            embed = self.create_embed(message)
            await channel.send(embed=embed)

    async def restart_task(self):
        await asyncio.sleep(self.TIME_TO_WAIT * 3600)
        await self.send_messages()

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
