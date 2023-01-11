import discord
from discord.ext import commands, vbu

import requests

class MinecraftInfo(vbu.Cog):

    API_ENDPOINT = "https://api.mcsrvstat.us/2/"
    ICON_ENDPOINT = "https://api.mcsrvstat.us/icon/"

    def __init__(self, bot: vbu.Bot):
        super().__init__(bot)
        self.SERVER_ADDRESS = self.bot.config['cfa']['server_address']

        self.bot: vbu.Bot

    @commands.command(
        aliases=['mc', 'minecraft'], 
        application_command_meta=commands.ApplicationCommandMeta())
    async def server(self, ctx: vbu.Context):
        """
        Finds info on the CFA Minecraft server and sends an embed to chat
        """

        request = requests.get(self.API_ENDPOINT + self.SERVER_ADDRESS)
        server_data = request.json()

        embed = discord.Embed(title="Minecraft Server!")

        server_status = server_data['online']
        embed.color = 0x00FF00 if server_status else 0xFF0000
        embed.description = "*Refreshes every 5 minutes*"

        if not server_status:
            embed.description = "The server is currently offline! Check back later :(\n" + embed.description
            return await ctx.send(embed=embed)

        player_count = server_data['players']['online']
        max_players = server_data['players']['max']
        version = server_data['version']
        ip = f"{server_data['ip']}: {server_data['port']}"

        players = []
        player_string = "*Nobody is on :(*"
        if player_count:
            players = server_data['players']['list']
            player_string = "\n".join(players)

        embed.add_field(name = f"Players Online {player_count}/{max_players}", value = player_string)
        embed.add_field(name = "Connection Info", value = f"Version: **{version}**\nAddress: **{ip}**", inline=False)

        try:
            embed.set_thumbnail(url = self.ICON_ENDPOINT + self.SERVER_ADDRESS)
        except:
            pass

        await ctx.send(embed=embed)


def setup(bot: vbu.Bot):
    x = MinecraftInfo(bot)
    bot.add_cog(x)
