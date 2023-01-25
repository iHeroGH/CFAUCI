import discord
from discord.ext import commands, vbu


class WeeklyEmailReminder(vbu.Cog):

    @commands.command(application_command_meta=commands.ApplicationCommandMeta(
        options = [discord.ApplicationCommandOption(
            name = "name",
            description = "The name you want to add",
            type = discord.ApplicationCommandOptionType.string
            )
        ]
    )
    )
    @commands.has_role(913265779363942452)
    async def set_name(self, ctx: vbu.Context, name: str):
        """
        Sets or changes the name of the user who wants to be notified of weekly email existence
        """
        async with self.bot.database() as db:
            await db("""INSERT INTO user_settings (user_id, user_name)
            VALUES ($1, $2)
            ON CONFLICT (user_id) DO UPDATE SET user_name = $2""", ctx.author.id, name)

        await ctx.okay()
    
    @commands.command(application_command_meta=commands.ApplicationCommandMeta())
    @commands.has_role(913265779363942452)
    async def remove_name(self, ctx: vbu.Context):
        """
        Removes a user from the database
        """
        async with self.bot.database() as db:
            await db("""REMOVE FROM user_settings WHERE user_id = $1""", ctx.author.id)

        await ctx.okay()

    @commands.command(application_command_meta=commands.ApplicationCommandMeta())
    @commands.has_role(913265779363942452)
    async def get_name(self, ctx: vbu.Context):
        """
        Gets a user's name from the database
        """
        async with self.bot.database() as db:
            user_rows = await db("""SELECT * FROM user_settings WHERE user_id = $1""", ctx.author.id)

        if not user_rows or not user_rows[0]['user_name']:   
            return await ctx.send("There was no name found in the database. Run /set_name to set a name")

        await ctx.send(f"The name found in the database was **{user_rows[0]['user_name']}**")

    @commands.command(application_command_meta=commands.ApplicationCommandMeta(
        options = [discord.ApplicationCommandOption(
            name = "cooldown",
            description = "The cooldown you want to set",
            type = discord.ApplicationCommandOptionType.integer
            )
        ]
    )
    )
    @commands.has_role(913265779363942452)
    async def set_cooldown(self, ctx: vbu.Context, cooldown: int):
        """
        Sets or changes the cooldown (in hours) of the user
        """
        async with self.bot.database() as db:
            await db("""INSERT INTO user_settings (user_id, duration)
            VALUES ($1, $2)
            ON CONFLICT (user_id) DO UPDATE SET duration = $2""", ctx.author.id, cooldown)

        await ctx.okay()

    @commands.command(application_command_meta=commands.ApplicationCommandMeta())
    @commands.has_role(913265779363942452)
    async def get_cooldown(self, ctx: vbu.Context):
        """
        Gets a user's cooldown from the database
        """
        async with self.bot.database() as db:
            user_rows = await db("""SELECT * FROM user_settings WHERE user_id = $1""", ctx.author.id)

        if not user_rows or not user_rows[0]['duration']:   
            return await ctx.send("There was no cooldown found in the database. Run /set_cooldown to set a cooldown")

        await ctx.send(f"The cooldown found in the database was **{user_rows[0]['duration']} hours**")    

def setup(bot: vbu.Bot):
    x = WeeklyEmailReminder(bot)
    bot.add_cog(x)
