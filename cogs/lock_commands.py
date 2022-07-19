from discord.ext import commands, vbu, tasks
import discord

import datetime as dt
import pytz

class LockCommands(vbu.Cog):

    # TASK CALCULATOR
    TIME_TO_WAIT = 0.30 # in hours

    # Start task when cog is loaded
    def __init__(self, bot: vbu.Bot):
        super().__init__(bot)
        self.check_cat_lock.start()

    # The task itself
    @tasks.loop(seconds=TIME_TO_WAIT * 3600)
    async def check_cat_lock(self):
        """
        Check if it is a Sunday
        """
        if self.is_sunday():
            self.logger.info("Sunday detected")
            await self.lock_work_channels()
        else:
            self.logger.info("Sunday not detected")
            await self.unlock_work_channels()

    # Helpers
    def is_sunday(self):
        """
        Checks if it is a Sunday
        """
        pst = pytz.timezone("US/Pacific")
        now = dt.datetime.now(pst)

        return now.weekday() == 0 and now.hour >= 3

    # Stock task when cog is unloaded
    def cog_unload(self):
        self.check_cat_lock.cancel()

    # PERMISSIONS EDITOR
    async def edit_work_perms(self, perms: discord.PermissionOverwrite = None):
        """
        Edits the permissions of the work category
        """
        self.bot.logger.info("Editing work category permissions to: " + str(perms))
        # We don't want to set the perm to True, just None or False
        if perms:
            perms = None

        # Set up our vars
        chan = self.bot.get_channel(914719765875019786) # The general-work channel
        if not chan: # Fetch the channel if we can't just get it
            chan = await self.bot.fetch_channel(914719765875019786)
        cat = chan.category # The entire work category
        def_role = chan.guild.default_role # The 'everyone' role

        # Set our perm overwrite
        overwrite = discord.PermissionOverwrite()
        overwrite.read_messages = perms
        await cat.set_permissions(def_role, overwrite = overwrite)

        # Rename the channel
        if perms is None:
            await cat.edit(name = "Work")
        else:
            await cat.edit(name = "Work (Sunday Mode)")

        self.bot.logger.info("Edited work category permissions to: " + str(perms))

    # DELEGATOR METHODS
    async def lock_work_channels(self):
        """
        Locks the work channels
        """
        self.bot.logger.info("Locking work channels")
        await self.edit_work_perms(False)

    async def unlock_work_channels(self):
        """
        Unlocks the work channels
        """
        self.bot.logger.info("Unlocking work channels")
        await self.edit_work_perms()

    # COMMANDS
    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def lock(self, ctx: vbu.Context):
        """
        Locks all the channels in the work category.
        """

        self.bot.logger.info("Locking work channels manually")
        await self.lock_work_channels()
        await ctx.okay()

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def unlock(self, ctx: vbu.Context):
        """
        Unlocks all the channels in the work category.
        """

        self.bot.logger.info("Unlocking work channels manually")
        await self.unlock_work_channels()
        await ctx.okay()

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def check_locking(self, ctx: vbu.Context):
        """
        A command to run the checking task manually.
        """

        self.bot.logger.info("Checking work channels manually")
        await self.check_cat_lock()
        await ctx.okay()


def setup(bot: vbu.Bot):
    x = LockCommands(bot)
    bot.add_cog(x)
