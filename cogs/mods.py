import discord
from discord.ext import commands
class Mod(commands.Cog):

    def __init__(self,bot):
        self.client = bot

     #events
    # @commands.Cog.listener()
    # async def on_ready(self):
    #     print("Bot is Online")
    #commands
    #
    # @commands.command()
    # async def ping(self,ctx):
    #     await ctx.send(f'Pong! + {client.latency} MS')
    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self,ctx, member:discord.Member, *, reason="None"):
        await member.kick(reason=reason)
        await ctx.send(f"{member.mention} was kicked by {ctx.author.mention}.[{reason}]")

    


def setup(bot):
    bot.add_cog(Mod(bot))
