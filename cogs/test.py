import discord
from discord.ext import commands

class Test1(commands.Cog):

    def __init__(self,client):
        self.client = client

    @commands.command()
    async def test1(self,ctx):
        await ctx.send('test')

def setup(client):
    client.add_cog(Test1(client))
