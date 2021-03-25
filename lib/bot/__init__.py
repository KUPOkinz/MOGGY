from discord import Intents
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from discord.ext.commands import Bot as BotBase

PREFIX = "*" # the key used to control the bot.
OWNER_IDS = [396766040182358017] # the server owner's ID.


class Bot(BotBase):
	def __init__(self):
		self.PREFIX = PREFIX
		self.ready = False
		self.guild = None
		self.scheduler = AsyncIOScheduler

		super().__init__(
			command_prefix=PREFIX, 
			owner_ids=OWNER_IDS,
			intents=Intents.all(),
		)

	def run(self, version): # when the bot is running.
		self.VERSION = version

		with open("./lib/bot/token.token", "r", encoding="utf-8") as tf:
			self.TOKEN = tf.read()

		print("running bot...") # this message displays in the terminal when the bot is running.
		super().run(self.TOKEN, reconnect=True)

	async def on_connect(self): # when the bot is connecting.
		print("bot connecting...") # this message displays in the terminal when the bot is connecting.

	async def on_disconnect(self): # when the bot is disconnecting.
		print ("bot disconnecting...") # this message displays in the terminal when the bot is disconnecting.

	async def on_ready(self): # when the bot is ready.
		if not self.ready:
			self.ready = True
			self.guild = self.get_guild(752575907012673569) # the server's ID.
			print("bot ready") # this message displays in the terminal when the bot is ready.

		else:
			print("bot reconnecting...") # this message displays in the terminal when the bot is reconnecting.

	async def on_message(self, message):
		pass


bot = Bot()