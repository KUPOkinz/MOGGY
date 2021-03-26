from asyncio import sleep
from datetime import datetime
from glob import glob

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from discord import Embed, File, Intents
from discord.errors import HTTPException, Forbidden
from discord.ext.commands import Bot as BotBase
from discord.ext.commands import Context
from discord.ext.commands import (CommandNotFound, BadArgument, MissingRequiredArgument)

from ..db import db

PREFIX = "*" # the key used to control the bot.
OWNER_IDS = [396766040182358017] # the server owner's ID.
COGS = [path.split("\\")[-1][:-3] for path in glob("./lib/cogs/*.py")] # the location of the Cogs folder.
IGNORE_EXCEPTIONS = (CommandNotFound, BadArgument)


class Ready(object):
	def __init__(self):
		for cog in COGS:
			setattr(self, cog, False)

	def ready_up(self,cog):
		setattr(self,cog, True)
		print(f"{cog} cog ready") # displays in the terminal when a specific Cog is ready.

	def all_ready(self):
		return all([getattr(self, cog) for cog in COGS])


class Bot(BotBase):
	def __init__(self):
		self.PREFIX = PREFIX
		self.ready = False
		self.cogs_ready = Ready()

		self.guild = None
		self.scheduler = AsyncIOScheduler()

		db.autosave(self.scheduler)
		super().__init__(
			command_prefix=PREFIX, 
			owner_ids=OWNER_IDS,
			intents=Intents.all(),
		)

	def setup(self):
		for cog in COGS:
			self.load_extension(f"lib.cogs.{cog}")
			print(f"{cog} cog loading...") # displays in the terminal when a specific Cog is loading.

		print("setup complete...") # displays in the terminal when the start-up process has completed.

	def run(self, version): # when the bot is running.
		self.VERSION = version

		print("running setup...") # displays in the terminal when the start-up process begins.
		self.setup()

		with open("./lib/bot/token.token", "r", encoding="utf-8") as tf: # the location of the bot token. this must be added and saved as "token.token".
			self.TOKEN = tf.read()

		print("running bot...") # displays in the terminal when the bot is running.
		super().run(self.TOKEN, reconnect=True)

	async def process_commands(self, message):
		ctx =await self.get_context(message, cls=Context)
			
		if self.ready:	
			if ctx.command is not None and ctx.guild is not None:
					await self.invoke(ctx)

		else:
			await ctx.send("I'm not ready to receive commands.") # appears in the server when an action is performed and the bot is not fully ready or online.

	async def timed_message(self): # this is a timed message. timing can be adjusted using the "on_ready" function.
		await self.stdout.send("I am a timed notification.") # appears in the server when the timed message is sent.

	async def on_connect(self): # when the bot is connecting.
		print("bot connecting...") # displays in the terminal when the bot is connecting.

	async def on_disconnect(self): # when the bot is disconnecting.
		print ("bot disconnecting...") # displays in the terminal when the bot is disconnecting.

	async def on_error(self, err, *args, **kwargs): # when the bot has encountered an error.
		if err == "on_command_error":
			await args[0].send("Something went wrong...") # appears in the server when the bot has encountered an error.

		await self.stdout.send("An error has occured.") # appears in the server when the bot has encountered an error.
		raise

	async def on_command_error(self, ctx, exc):
		if any([isinstance(exc, error) for error in IGNORE_EXCEPTIONS]):
			pass

		elif isinstance(exc, MissingRequiredArgument):
			await ctx.send("One or more required arguments are missing.") # appears in the server when missing a required argument for a command.

		elif isinstance(exc.original, HTTPException):
			await ctx.send("Unable to send message.") # appears in the server when the bot cannot send a message.

		elif isinstance(exc.original, Forbidden):
			await ctx.send("I do not have permission to do that.") # appears in the server when the bot does not have permissions to perform the task.
		
		elif hasattr(exc, "original"):
			raise exc.original

		else:
			raise exc.original

	async def on_ready(self): # when the bot is ready and online.
		if not self.ready:
			self.guild = self.get_guild(752575907012673569) # the server's ID.
			self.stdout = self.get_channel(824271658877059092) # the ID of the standard output channel (usually general chat).
			# self.scheduler.add_job(self.timed_message, CronTrigger(second="0,15,30,45")) # this line controls the timing of timed messages.
			self.scheduler.start()

			# embed = Embed(title="Title 1", description="Description 1", # this line appears on the top row by itself.
			# 			  colour=0xFF0000, timestamp=datetime.utcnow()) # the colour of the post and the timestamp.
			# fields = [("Title 2", "Description 2", True), # this line appears below Title 1.
			# 		  ("Title 3", "Description 3", True), # this line appears beside Title 2 because of True.
			# 		  ("Title 4", "Description 4", False)] # this line appears by itself below Title 3 because of False.
			# for name, value, inline in fields:
			# 	embed.add_field(name=name, value=value, inline=inline)
			# embed.set_author(name="AUTHOR", icon_url=self.guild.icon_url) # the author of the post and the user icon.
			# embed.set_footer(text="FOOTER") # the footer. 
			# embed.set_thumbnail(url=self.guild.icon_url) # the thumbnail in the top right corner.
			# embed.set_image(url=self.guild.icon_url) # this image will be sent after the initial post has been sent.
			# await channel.send(embed=embed)

			# await channel.send(file=File("./data/images/example.png")) # the location of the image to be sent after the initial post has been sent.
		
			while not self.cogs_ready.all_ready():
				await sleep(0.5)

			await self.stdout.send("MOGGY is now online!") # appears in the server when the bot is ready and online.
			self.ready = True
			print("bot ready") # displays in the terminal when the bot is ready and online.

		else:
			print("bot reconnecting...") # displays in the terminal when the bot is reconnecting.

	async def on_message(self, message):
		if not message.author.bot:
			await self.process_commands(message)


bot = Bot()