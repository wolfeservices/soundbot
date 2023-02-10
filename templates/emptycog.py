from twitchio.ext import commands, sounds

class AGen(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.player = sounds.AudioPlayer(callback=self.playback_finished)

    async def playback_finished(self):
        print('Playback finished')

##COMMANDS##

def prepare(bot):
    bot.add_cog(AGen(bot))
