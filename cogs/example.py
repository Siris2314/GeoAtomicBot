import discord
from discord.ext import commands


class Example(commands.Cog):

    def __init__(self, client):
        self.client = client

     #events
    # @commands.Cog.listener()
    # async def on_ready(self):
    #     print("Bot is Online")
    #commands
    #
    # @commands.command()
    # async def ping(self,ctx):
    #     await ctx.send(f'Pong! + {client.latency} MS')


def setup(client):
    client.add_cog(Example(client))