
import discord
import random
import json
import os
from discord.ext import commands, tasks
from itertools import cycle
import asyncpg
import platform
import logging
from discord.utils import get
import youtube_dl





client = commands.Bot(command_prefix = '>')
status = cycle(['Game 1', 'Game 2'])
logging.basicConfig(level=logging.INFO)


with open('config.json', 'r') as f:
  key = json.loads(f.read())

token = key["token"]





async def create_db_pool():
	client.pg_con = await asyncpg.create_pool(database="LevelSystem", user = "postgres", password = "arry2314")
@client.event
async def on_ready():
	change_status.start()
	# await client.change_presence(status=discord.Status.idle,activity=discord.Game("Sup"))
	print("Bot is ready,")

@tasks.loop(seconds=10)
async def change_status():
	await client.change_presence(activity=discord.Game(next(status)))




@client.event
async def on_command_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.send("Please pass in all required arguments")

	if isinstance(error, commands.CommandNotFound):
		await ctx.send('Invalid command used')

	if isinstance(error, commands.TooManyArguments):
		await ctx.send("Too many arguments passed")

	if isinstance(error, commands.CheckFailure):
		await ctx.send("You do not have permission to use this command")

	if isinstance(error, commands.BadArgument):
		await ctx.send("Wrong Data Type Sent, Please only use integers")

def is_it_me(ctx):
	return ctx.author.id == 360135256155750421
@client.command()
@commands.check(is_it_me)
async def hi(ctx):
	await ctx.send(f'Hi im {ctx.author}')

@client.event
async def on_member_join(member):
	print(f'{member} has joined the server.')

@client.command()
async def testembed(ctx):

	embed = discord.Embed(title="Title", description="Description",color=discord.Color.red(), url="https//www.google.com")
	embed.set_author(name=client.user.name,icon_url=client.user.avatar_url)

	await ctx.send(embed=embed)





@client.command(aliases = ["whois"])
async def userinfo(ctx, member: discord.Member = None):

	member = ctx.author if not member else member
	roles = [role for role in member.roles]

	embed = discord.Embed(colour=member.color, timestamp=ctx.message.created_at)

	embed.set_author(name=f"User Info - {member}")
	embed.set_thumbnail(url=member.avatar_url)
	embed.set_footer(text=f"Requested by {ctx.author}", icon_url = ctx.author.avatar_url)
	embed.add_field(name="ID:", value=member.id)
	embed.add_field(name="Guild Name:", value=member.display_name)

	embed.add_field(name="Created at:", value=member.created_at.strftime("%a,%#d %B %Y, %I:%M %p UTC"))
	embed.add_field(name="Joined at:", value=member.joined_at.strftime("%a,%#d %B %Y, %I:%M %p UTC"))

	embed.add_field(name=f"Roles ({len(roles)})", value=" ".join([role.mention for role in roles]))
	embed.add_field(name="Top role: ", value=member.top_role.mention)

	embed.add_field(name="bot?", value=member.bot)

	await ctx.send(embed=embed)




@client.event
async def on_member_remove(member):
	print(f'{member} has left a server. ')

@client.command()
async def say(ctx,* ,words: commands.clean_content):
	await ctx.send(words)


@client.command()
@commands.has_permissions(manage_messages = True)
async def clear(ctx, amount : int):
	await ctx.channel.purge(limit = amount)

	@clear.error
	async def clear_error(self,ctx,error):
		if isinstance(error,commands.TooManyArguments):
			await ctx.send("Too many arguments sent")


		raise error


# @client.command(name = 'avatar', aliases = ['Avatar'])
# async def avatar(ctx,user: discord.Member):
#
# 	embed = discord.Embed(color = discord.Color(0xffff) , title = f"{user}")
#
# 	embed.set_image(url=f"{user.avatar_url}")
#
# 	await ctx.send(embed=embed)































# def is_it_me(ctx):
# 	return ctx.author.id ==

@client.command()
async def ping(ctx):
	await ctx.send(f'Pong! {round(client.latency * 1000)} MS')

@client.command(aliases = ['8Ball', 'test'])
async def _8Ball(ctx, *, question):
	responses = ["It is certain.","It is decidedly so.","Without a doubt.","Yes - definitely.","You may rely on it.","As I see it, yes.","Most likely.","Outlook good.","Yes.","Signs point to yes.","Reply hazy, try again.","Ask again later.","Better not tell you now.","Cannot predict now.","Concentrate and ask again.","Don't count on it.","My reply is no.","My sources say no.","Outlook not so good.","Very doubtful."]
	await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')


# @client.command()
# async def kick(ctx, member: discord.Member, reason=None):
# 	await member.kick(reason=reason)

@client.command()
async def ban(ctx, member: discord.Member, reason=None):
	await member.ban(reason=reason)
	await ctx.send(f'Banned {member.mention}')

@client.command()
async def unban(ctx,*, member):
	banned_users = await ctx.guild.bans()
	member_name, member_discriminator = member.split('#')

	for ban_entry in banned_users:
		user = ban_entry.user
		if(user.name, user.discriminator) == (member_name, member_discriminator):
			await ctx.guild.unban(user)
			await ctx.send(f'Unbanned {user.mention}')

@client.command()
async def load(ctx, extension):
	client.load_extension(f'cogs.{extension}')
	await ctx.send(f"{extension} has been loaded")


@client.command()
@commands.is_owner()
async def shutdown(ctx):
	await ctx.send("Bot has been shutdown")
	await client.logout()


@client.command()
async def unload(ctx, extension):
	client.unload_extension(f'cogs.{extension}')
	await ctx.send(f"{extension} has been unloaded")

# @client.command()
# async def reload(ctx, extension):
# 	client.unload_extension(f'cogs.{extension}')
# 	client.load_extension(f'cogs.{extension}')
@client.command()
@commands.is_owner()
async def reload(ctx, cog):
	try:
		bot.unload_extension(f"cogs.{cog}")
		bot.load_extension(f"cogs.{cog}")
		await ctx.send(f"{cog} got reloaded")
	except Exception as e:
		await ctx.send(f"{cog} can not be loaded")
		raise error

@client.command()
async def invite(ctx, channel:discord.TextChannel):
	invite = await channel.create_invite()
	await ctx.send(invite)




for filename in os.listdir('./cogs'):
	if filename.endswith('.py'):
		client.load_extension(f'cogs.{filename[:-3]}')






client.loop.run_until_complete(create_db_pool())
client.run(token)
