from random import choice, randint
from typing import Optional

from discord import Member
from discord.ext.commands import Cog
from discord.ext.commands import BadArgument
from discord.ext.commands import command


class Fun(Cog):
	def __init__(self, bot):
		self.bot = bot

	@command(name="hello", aliases=["hey", "hi"]) # [hello/hey/hi] replies with a welcome message.
	async def say_hello(self, ctx):
		await ctx.send(f"{choice(('Hello', 'Hey', 'Hi'))} {ctx.author.mention}!") # appears in the server as a response to the [hello/hey/hi] command. 

	@command(name="dice", aliases=["roll"]) # [dice/roll] [#] [d] [#] simulates dice rolling based on the values entered.  
	async def roll_dice(self, ctx, die_string: str):
		dice, value = (int(term) for term in die_string.split("d"))

		if dice <= 25:
			rolls = [randint(1, value) for i in range(dice)]

			await ctx.send(" + ".join([str(r) for r in rolls]) + f" = {sum(rolls)}") # appears in the server as a response to the [dice/roll] command.

		else:
			await ctx.send("I can't count that high. Try a lower number.") # appears when the [dice/roll] command encounters an error.

	@command(name="slap", aliases=["hit"]) # [slap/hit] [user] <reason> slaps the mentioned member with an optional reason.
	async def slap_member(self, ctx, member: Member, *, reason: Optional[str] = "for no reason"): # appears in the server as a respose to the [slap/hit] command when no reason is provided.
		await ctx.send(f"{ctx.author.mention} slapped {member.mention} {reason}!") # appears in the server as a response to the [slap/hit] command when given a reason.
	
	@slap_member.error
	async def slap_member_error(self, ctx, exc): # when the [slap/hit] command encounters an error.
		if isinstance(exc, BadArgument):
			await ctx.send(f"I cannot find that user.") # appears in the server when the [slap/hit] command encounters an error.

	@command(name="echo", aliases=["say", "mimic"]) # [echo/say/mimic] [message] repeats the sent message then deletes the user post.
	async def echo_message(self, ctx, *, message):
		await ctx.message.delete()
		await ctx.send(message)

	@Cog.listener()
	async def on_ready(self):
		if not self.bot.ready:
			self.bot.cogs_ready.ready_up("fun")


def setup(bot):
	bot.add_cog(Fun(bot))