import discord
from discord.ext import commands

class Events(commands.Cog):

    def __init__(self,bot):
        self.bot = bot




    async def on_message1(self,message):
        if message.author == self.bot.user:
            return

            user = message.author
            msg = message.content
            print(f"{user} said {msg}")

            await self.bot.process_commands(message)

    async def on_message_delete(self, message):
        await message.channel.send("A message was deleted here")


def setup(bot):
    bot.add_cog(Events(bot))
