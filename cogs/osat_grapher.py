from discord.ext import commands, vbu
import discord

import matplotlib.pyplot as plt
import numpy as np

class OSATGrapher(vbu.Cog):

    @commands.command()
    async def graph(self, ctx: vbu.Context):
        """
        Graphs all the available OSAT scores
        """
        # Get the days and the scores lists from the database
        days, scores = self.get_db_info()

        if not days or not scores or (len(days) != len(scores)):
            return await ctx.send("Something has gone catastrophically wrong with the database. No scores were found.")

        # PLOT DATA
        # Plot the days vs scores line
        plt.plot(days, scores)
        # Plot the predicted region score
        plt.axhline(y=70, color='r', linestyle=":")

        # FORMATTING
        # Cut off the y-axis to between 50-80%
        plt.ylim(50, 80)
        # Create the labels for the x-axis data
        x_tick_labels = [f"{i.month}/{i.day}" for i in days]
        plt.xticks(days, x_tick_labels)

        # Save the graph and send it
        plt.savefig("osat.png")
        plt.close()
        await ctx.send(file=discord.File("osat.png"))

    async def get_db_info(self):

        # Call the database and get our info
        async with self.bot.database() as db:
            osat_rows = await db("SELECT * FROM osat_over_time")

        # Return it for unpacking
        return osat_rows[0]['osat_date'], osat_rows[0]['osat_score']


def setup(bot: vbu.Bot):
    x = OSATGrapher(bot)
    bot.add_cog(x)
