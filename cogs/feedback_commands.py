from discord.ext import commands, vbu
import discord

import asyncio

class FeedbackCommands(vbu.Cog):

    CHANNEL_ID = 979492290991099984

    @vbu.Cog.listener()
    async def on_message(self, message: discord.Message):

        # If we're not in dms, ignore the message
        if message.guild:
            return

        # If the author is a bot, ignore the message
        if message.author.bot:
            return

        # If the author is not able to see the feedback channel
        try:
            feedback_channel = self.bot.get_channel(self.CHANNEL_ID)
            self.bot.logger.info("Got Feedback Channel (on_message)  " + str(feedback_channel))
            if message.author not in feedback_channel.members:
                return
        except:
            feedback_channel = None
            self.bot.logger.info("Could not find feedback channel")

        # Deal with various message lengths
        if not message or not message.content or len(message.content) <= 1:
            return

        # If it's a presumed command
        if message.content.startswith("c!") or message.content.startswith("/"):
            return

        # Send the user a confirmation message
        yes_button = discord.ui.Button(label = f"Yes", custom_id = "yes",  style=discord.ui.ButtonStyle.success)
        no_button = discord.ui.Button(label = f"No", custom_id = "no",  style=discord.ui.ButtonStyle.danger)
        feedback_components = discord.ui.MessageComponents(discord.ui.ActionRow(yes_button, no_button))
        feedback_message = await message.channel.send(
            "Did you want to send that to the feedback channel?", components=feedback_components
            )

        # Wait for a response
        try:
            check = lambda p: p.message.id == feedback_message.id and p.user.id == message.author.id
            payload = await self.bot.wait_for("component_interaction", check=check, timeout=60)
            await payload.response.defer_update()
            await payload.message.edit(components=feedback_components.disable_components())

            # If they don't want to send the feedback, we cancel
            if payload.component.custom_id.lower() == "no":
                return await message.channel.send("Cancelling feedback...")

        except asyncio.TimeoutError:
            # If we time out from waiting for the response, we cancel
            return await message.channel.send("Timed out waiting for response. Cancelling feedback...")

        # Ask if the user wants to send feedback anonymously
        anon_button = discord.ui.Button(label = f"Yes", custom_id = "yes",  style=discord.ui.ButtonStyle.success)
        nonanon_button = discord.ui.Button(label = f"No", custom_id = "no",  style=discord.ui.ButtonStyle.danger)
        anon_components = discord.ui.MessageComponents(
            discord.ui.ActionRow(anon_button, nonanon_button)
        )
        anon_message = await message.channel.send("Would you like to send the feedback anonymously?", components=anon_components)

        # Wait for a response
        anonymous = True
        try:
            check = lambda p: p.message.id == anon_message.id and p.user.id == message.author.id
            payload = await self.bot.wait_for("component_interaction", check=check, timeout=60)
            await payload.response.defer_update()
            await payload.message.edit(components=anon_components.disable_components())

            # If they want to be anonymous
            anonymous = payload.component.custom_id.lower() == "yes"
            await message.channel.send("Continuing " + ("anonymously..." if anonymous else "non-anonymously..."))

        except asyncio.TimeoutError:
            # If we time out from waiting for the response, we set it to be anonymous
            await message.channel.send("Timed out waiting for response. Continuing anonymously...")

        self.bot.logger.info("Entering Give Feedback")
        await self.give_feedback(message, anonymous, feedback_channel = None)

    async def give_feedback(self, message: discord.Message, anonymous: bool = True, feedback_channel: discord.TextChannel = None):
        """
        The helper method for dealing with feedback when it's sent to the bot.
        This is where we create an embed and send it to the feedback channel anonymously or not
        """
        self.bot.logger.info("Entered Give Feedback")

        # Get the feedback channel
        if not feedback_channel:
            feedback_channel = self.bot.get_channel(self.CHANNEL_ID)
            self.bot.logger.info("Got Feedback Channel (give_feedback)  " + str(feedback_channel))

        # Create a new embed
        embed = vbu.Embed(use_random_colour=True)
        embed.title = "New Feedback!"
        embed.description = message.content

        # Set the anonymity of the embed
        if not anonymous:
            embed.set_author_to_user(message.author)
        else:
            embed.set_author(name="Anonymous")

        # Send the embed to the feedback channel
        feedback = await feedback_channel.send(embed=embed)
        self.bot.logger.info("Send feedback")

        await feedback.add_reaction("\U00002b50")

        # Send a message to the user
        await message.channel.send("Your feedback has been sent!")


def setup(bot: vbu.Bot):
    x = FeedbackCommands(bot)
    bot.add_cog(x)
