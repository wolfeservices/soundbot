from twitchio.ext import commands

class AGen(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

##COMMANDS##

def prepare(bot):
    bot.add_cog(AGen(bot))
