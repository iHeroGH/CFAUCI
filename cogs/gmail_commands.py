from discord.ext import commands, vbu
import discord

from cogs.email_notifier import EmailNotifier

class GmailCommands(vbu.Cog):

    @commands.command(aliases=['fse', 'send_emails'])
    @commands.has_permissions(manage_guild=True)
    async def force_send_emails(self, ctx: vbu.Context, channel: discord.TextChannel = None):
        """
        Forces the bot to read all messages from the inbox
        """
        messages = self.bot.requester.get_new_emails()
        channel = channel or ctx.channel

        for message in messages:
            embed = EmailNotifier.create_embed(message)
            await channel.send(embed=embed)

        await ctx.okay()

    @commands.command(aliases=['fwa', 'weekly', 'force_weekly'])
    @commands.has_permissions(manage_guild=True)
    async def force_weekly_announcement(self, ctx: vbu.Context, channel: discord.TextChannel = None):
        """
        Forces the bot to send the weekly email announcement message
        """
        channel = channel or ctx.channel

        embed = EmailNotifier.get_weekly_embed()
        await channel.send(embed=embed)
        await ctx.okay()

    @commands.command(aliases=['nfwa', 'nweekly', 'force_no_weekly'])
    @commands.has_permissions(manage_guild=True)
    async def force_no_weekly_announcement(self, ctx: vbu.Context, channel: discord.TextChannel = None):
        """
        Forces the bot to send the "there is no" weekly email announcement message
        """
        channel = channel or ctx.channel

        embed = EmailNotifier.get_no_weekly_embed()
        await channel.send(embed=embed)
        await ctx.okay()


def setup(bot: vbu.Bot):
    x = GmailCommands(bot)
    bot.add_cog(x)
