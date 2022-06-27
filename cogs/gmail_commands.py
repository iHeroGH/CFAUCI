from discord.ext import commands, vbu
import discord

from cogs.GmailConnection.requester import Requester
from cogs.bot_start import BotStart

class GmailCommands(vbu.Cog):

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def force_get_messages(self, ctx: vbu.Context, channel: discord.TextChannel = None):
        """
        Forces the bot to read all messages from the inbox
        """
        messages = self.bot.requester.get_messages()
        channel = channel or ctx.channel

        for message in messages:
            embed = BotStart.create_embed(message)
            await channel.send(embed=embed)

        await ctx.okay()

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def force_weekly_announcement(self, ctx: vbu.Context, channel: discord.TextChannel = None):
        """
        Forces the bot to send the weekly email announcement message
        """
        channel = channel or ctx.channel

        embed = BotStart.get_weekly_embed()
        await channel.send(embed=embed)
        await ctx.okay()

def setup(bot: vbu.Bot):
    x = GmailCommands(bot)
    bot.add_cog(x)
