from twitchio.ext import commands

import datetime
Time = datetime.datetime.now(tz=datetime.timezone.utc)
TimeMST = Time - datetime.timedelta(hours=7)
TimeMST = TimeMST.strftime("%I:%M %p")
TimePST = Time - datetime.timedelta(hours=8)
TimePST = TimePST.strftime("%I:%M %p")
Time = Time.strftime("%I:%M %p")


#read from file ../version.txt
with open('version.txt', 'r') as f:
    version = f.read()


class wolf(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx: commands.Context):
        await ctx.send('Pong!')

    @commands.command()
    async def version(self, ctx: commands.Context):
        await ctx.send(f'My Version is {version}')

    @commands.command()
    async def time(self, ctx: commands.Context):
        await ctx.send(f'The time is {Time} UTC. {TimeMST} MST. {TimePST} PST.')

def prepare(bot):
    bot.add_cog(wolf(bot))
