import discord
import os
from discord.ext import commands
from discord.utils import get
import youtube_dl

class music_system(commands.Cog):

    def __init__(self,bot):
        self.client = bot




    @commands.command(pass_context = True, aliases = ['J', 'jo'])
    async def join(self,ctx):
        global voice
        channel = ctx.message.author.voice.channel
        voice = get(self.client.voice_clients, guild=ctx.guild)

        if voice and voice.is_connected():
            await voice.move_to(channel)

        else:
            voice = await channel.connect()

        await voice.disconnect()


        if voice and voice.is_connected():
            await voice.move_to(channel)

        else:
            voice = await channel.connect()
            print(f"The bot has connected to {channel}\n")
            await ctx.send(f"Joined {channel}")

    @commands.command(pass_context = True, aliases = ['L', 'le'])
    async def leave(self,ctx):
        channel = ctx.message.author.voice.channel
        voice = get(self.client.voice_clients, guild=ctx.guild)

        if voice and voice.is_connected():
            await voice.disconnect()
            print(f"The bot has left {channel}")
            await ctx.send(f"Disconnect {channel}")


        else:
            print("Bot was told to leave voice channel, yet was not in one")
            await ctx.send("Not in a current voice channel")

    @commands.command(pass_context = True, aliases = ['p', 'pl'])
    async def play(self,ctx, url: str):
        song_there = os.path.isfile("song.mp3")
        try:
            if song_there:
                os.remove("song.mp3")
                print("Removed old song file")

        except PermissionError:
                print("Trying to remove song file but it is being played")
                await ctx.send("Error")
                return
        await ctx.send("Ready Time")

        # voice = get(bot.voice_clients, guild=ctx.guild)
        # ydl_opts = (
        #     "format":"bestaudio/"
        #
        # )





def setup(bot):
    bot.add_cog(music_system(bot))
