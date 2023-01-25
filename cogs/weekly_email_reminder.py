import discord
from discord.ext import commands, vbu, tasks

import datetime

class WeeklyEmailReminder(vbu.Cog):

    TIME_TO_WAIT = 0.01 # in hours
    
    def __init__(self, bot: vbu.Bot):
        super().__init__(bot)
        self.send_new_reminders.start()

        self.bot: vbu.Bot
    
    @tasks.loop(seconds=TIME_TO_WAIT * 3600)
    async def send_new_reminders(self):
        """
        The main email check task that checks for weekly emails and sends a reminder to available trainers
        """
        await self.bot.wait_until_ready()
        self.bot.logger.info("Restarting Weekly Reminder Task!")

        try:
            messages = self.bot.requester.get_training_emails()
        except Exception as e:
            self.bot.requester.__login__()
            self.send_new_reminders.restart()
            return

        async with self.bot.database() as db:
            
            for message in messages:
                # If there's a new weekly email from Dustin, reset the user_settings to not set 
                if "weeklyemail" in message["subject"].replace(" ", "").lower():
                    await db("UPDATE user_settings SET is_sent = $1", False)

            trainer_rows = await db("SELECT * FROM user_settings WHERE is_sent = $1", False)
        
            for trainer_record in trainer_rows:
                trainer_id = trainer_record['user_id']
            
                try:
                    trainer = self.bot.get_user(trainer_id) or await self.bot.fetch_user(trainer_id)
                except:
                    self.bot.logger.info(f"Could not find trainer of ID {trainer_id}")
                    continue
                
                last_sent = trainer_record['last_sent']
                offset = datetime.timedelta(seconds = trainer_record['duration'])
                future = last_sent + offset
                
                if datetime.datetime.now() > future:
                    await trainer.send("This is a reminder that you have not yet sent your weekly email! Run /force_stop_reminder to stop the reminders for this week.")
                    self.bot.logger.info(f"Sent {trainer_id} a reminder message")
                    
                    await db("""INSERT INTO user_settings (user_id, last_sent)
                    VALUES ($1, $2) 
                    ON CONFLICT (user_id) DO UPDATE SET last_sent = $2""", trainer_id, datetime.datetime.now()
                    )

                    self.bot.logger.info(f"Reset {trainer_id}'s last_sent")


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

    @commands.command(application_command_meta=commands.ApplicationCommandMeta())
    @commands.has_role(913265779363942452)
    async def force_stop_reminders(self, ctx: vbu.Context):
        """
        Forcibly stops a user from recieving hourly reminders for this week
        """
        async with self.bot.database() as db:
            user_rows = await db("""SELECT * FROM user_settings WHERE user_id = $1""", ctx.author.id)

            if not user_rows:   
                return await ctx.send("There was no record of you found in the database")

            await db("UPDATE user_settings SET is_sent = $1", True)

        await ctx.okay()

    def cog_unload(self):
        self.send_new_reminders.cancel()

def setup(bot: vbu.Bot):
    x = WeeklyEmailReminder(bot)
    bot.add_cog(x)
