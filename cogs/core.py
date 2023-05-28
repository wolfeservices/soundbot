from twitchio.ext import commands
import os
import datetime
import base64

Time = datetime.datetime.now(tz=datetime.timezone.utc)
TimeMST = Time - datetime.timedelta(hours=7)
TimeMST = TimeMST.strftime("%I:%M %p")
TimePST = Time - datetime.timedelta(hours=8)
TimePST = TimePST.strftime("%I:%M %p")
Time = Time.strftime("%I:%M %p")

def URL_service(command_list, channel):
    #append default command list to command_list
    command_list = command_list + ',!ping,!version,!time,!WBCommands,!lockdown,!unlock'
    prepID = command_list + '~' + channel
    command_list_id = base64.urlsafe_b64encode(prepID.encode()).decode()
    url = 'https://commands.wolfebot.info/?commandListID=' + command_list_id
    return url

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

    @commands.command()
    async def WBCommands(self, ctx: commands.Context):
        command_list = []
        with open('commands.txt', 'r') as f:
            for line in f:
                command = line.split(':')[0]
                command = "!"+command
                command_list.append(command)
            f.close()
            command_list = ','.join(command_list)
            channel = ctx.channel.name
        response = URL_service(command_list, channel)
        await ctx.send('Command List: '+response)


def prepare(bot):
    bot.add_cog(wolf(bot))
