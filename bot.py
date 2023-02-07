# bot.py

#audio bot for twitch
#twitchio docs: https://twitchio.readthedocs.io/en/latest/api.html

#imports
from twitchio.ext import commands, sounds
import sys


#VARS and ARGS
version = "0.0.3"
token = sys.argv[1]
nick = sys.argv[2]
channel = sys.argv[3]
prefix = sys.argv[4]

#check if all args are there
if len(sys.argv) < 5:
	print("Not enough args")
	exit()

class Bot(commands.Bot):
	def __init__(self):
		super().__init__(token=token, nick=nick, prefix=prefix, initial_channels=[channel])
		
		self.player = sounds.AudioPlayer(callback=self.playback_finished)

	async def playback_finished(self):
		print('Playback finished')	

	async def event_ready(self):
		print(f'logged in as | {self.nick}')
		print(f'Version: {version}')
		print(f'User ID: {self.user_id}')
		print(f'Channel: {channel}')
		print(f'Prefix: {prefix}')

	async def event_message(self, message):
		if message.echo:
			return
		else:
			print(message.content)
			await self.handle_commands(message)

	@commands.command()
	async def ping(self, ctx: commands.Context):
		await ctx.send('Pong!')

	@commands.command()
	async def version(self, ctx: commands.Context):
		await ctx.send(f'My Version is {version}')

	
#<commands>
	@commands.command()
	async def slap(self, ctx: commands.Context):
		self.player.volume = 100
		sound = sounds.Sound(source='./sounds/slap.mp3')
		self.player.play(sound)

	@commands.command()
	async def ed(self, ctx: commands.Context):
		self.player.volume = 25
		sound = sounds.Sound(source='./sounds/emotional-damage-meme.mp3')
		self.player.play(sound)
		await ctx.send('Emotional Damage!')

	@commands.command()
	async def bruh(self, ctx: commands.Context):
		self.player.volume = 100
		sound = sounds.Sound(source='./sounds/bruh.mp3')
		self.player.play(sound)
		await ctx.send('bruh')


#</commands>

bot = Bot()
bot.run()