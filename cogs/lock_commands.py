from discord.ext import commands, vbu
import discord

class LockCommands(vbu.Cog):

    # PERMISSIONS EDITOR
    async def edit_work_perms(self, ctx: vbu.Context, perms: discord.PermissionOverwrite = None):
        """
        Edits the permissions of the work category
        """

        # We don't want to set the perm to True, just None or False
        if perms:
            perms = None

        # Set up our vars
        gen = self.bot.get_channel(914719765875019786) # The general-work channel
        cat = gen.category # The entire work category
        def_role = ctx.guild.default_role # The 'everyone' role

        # Set our perm overwrite
        overwrite = discord.PermissionOverwrite()
        overwrite.read_messages = perms
        await cat.set_permissions(def_role, overwrite = overwrite)

        # Rename the channel
        if perms is None:
            await cat.edit(name = "Work (Sunday Mode)")
        else:
            await cat.edit(name = "Work")

    # DELEGATOR METHODS
    async def lock_work_channels(self, ctx):
        """
        Locks the work channels
        """
        await self.edit_work_perms(ctx, False)

    async def unlock_work_channels(self, ctx):
        """
        Unlocks the work channels
        """
        await self.edit_work_perms(ctx)

    # COMMANDS
    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def lock(self, ctx: vbu.Context):
        """
        Locks all the channels in the work category.
        """

        await self.lock_work_channels(ctx)
        await ctx.okay()

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def unlock(self, ctx: vbu.Context):
        """
        Unlocks all the channels in the work category.
        """

        await self.unlock_work_channels(ctx)
        await ctx.okay()


def setup(bot: vbu.Bot):
    x = LockCommands(bot)
    bot.add_cog(x)
