from discord.ext.commands import Cog


class Fun(Cog):
	def __init__(self, bot):
		self.bot = bot

	@Cog.listener()
	async def on_ready(self):
		if not self.bot.ready:
			self.bot.cogs_ready.ready_up("fun")
		# print("fun cog ready") # this message displays in the terminal when the Fun Cog is ready.


def setup(bot):
	bot.add_cog(Fun(bot))