# bot.py

#audio bot for twitch
#twitchio docs: https://twitchio.readthedocs.io/en/latest/api.html

#imports
from twitchio.ext import commands, sounds
from config import token, nick, prefix, channel
import os

version = open('version.txt', 'r').read()

class Bot(commands.Bot):
	def __init__(self):
		super().__init__(token=token, nick=nick, prefix=prefix, initial_channels=[channel])
		
		self.player = sounds.AudioPlayer(callback=self.playback_finished)

		#load cogs
		for file in sorted(os.listdir('./cogs')):
			if file.endswith('.py'):
				name = file[:-3]
				self.load_module(f'cogs.{name}')

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


bot = Bot()
bot.run()