from datetime import datetime

from discord import Intents
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from discord import Embed, File
from discord.ext.commands import Bot as BotBase
from discord.ext.commands import CommandNotFound

PREFIX = "*" # the key used to control the bot.
OWNER_IDS = [396766040182358017] # the server owner's ID.


class Bot(BotBase):
	def __init__(self):
		self.PREFIX = PREFIX
		self.ready = False
		self.guild = None
		self.scheduler = AsyncIOScheduler()

		super().__init__(
			command_prefix=PREFIX, 
			owner_ids=OWNER_IDS,
			intents=Intents.all(),
		)

	def run(self, version): # when the bot is running.
		self.VERSION = version

		with open("./lib/bot/token.token", "r", encoding="utf-8") as tf: # the token of the bot. this must be manually added.
			self.TOKEN = tf.read()

		print("running bot...") # this message displays in the terminal when the bot is running.
		super().run(self.TOKEN, reconnect=True)

	async def on_connect(self): # when the bot is connecting.
		print("bot connecting...") # this message displays in the terminal when the bot is connecting.

	async def on_disconnect(self): # when the bot is disconnecting.
		print ("bot disconnecting...") # this message displays in the terminal when the bot is disconnecting.

	async def on_error(self, err, *args, **kwargs): # when the bot has encountered an error.
		if err == "on_command_error":
			await args[0].send("something went wrong...") # this message displays in the terminal when the bot has encountered an error.

		channel = self.get_channel(824271658877059092) # the ID of the channel to receive the error message.
		await channel.send("An error has occured.") # this message will appear in the server when the bot has encountered an error.
		raise

	async def on_command_error(self, ctx, exc):
		if isinstance(exc, CommandNotFound):
			pass

		elif hasattr(exc, "original"):
			raise exc.original

		else:
			raise exc

	async def on_ready(self): # when the bot is ready.
		if not self.ready:
			self.ready = True
			self.guild = self.get_guild(752575907012673569) # the server's ID.
			print("bot ready") # this message displays in the terminal when the bot is ready and online.

			channel = self.get_channel(824271658877059092) # the ID of the channel to receive the ready message.
			await channel.send("MOGGY is now online!") # this message will appear in the server when the bot is ready and online.

			embed = Embed(title="Title 1", description="Description 1", # this line will appear on the top row by itself.
						  colour=0xFF0000, timestamp=datetime.utcnow()) # the colour of the post and the timestamp.
			fields = [("Title 2", "Description 2", True), # this line will appear below Title 1.
					  ("Title 3", "Description 3", True), # this line will appear beside Title 2 because of True.
					  ("Title 4", "Description 4", False)] # this line will appear by itself below Title 3 because of False.
			for name, value, inline in fields:
				embed.add_field(name=name, value=value, inline=inline)
			embed.set_author(name="AUTHOR", icon_url=self.guild.icon_url) # this is the author of the post and the user icon.
			embed.set_footer(text="FOOTER") # this is the footer. 
			embed.set_thumbnail(url=self.guild.icon_url) # this is the thumbnail in the top right corner.
			embed.set_image(url=self.guild.icon_url) # this image will be sent after the initial post has been sent.
			await channel.send(embed=embed)

			await channel.send(file=File("./data/images/example.png")) # the location of the image to be sent after the initial post has been sent.

		else:
			print("bot reconnecting...") # this message displays in the terminal when the bot is reconnecting.

	async def on_message(self, message):
		pass


bot = Bot()