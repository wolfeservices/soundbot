from twitchio.ext import commands, sounds
import asyncio


def refresh_auth_users():
    with open('auth_users.txt', 'r') as f:
        auth_users = []
        for line in f.readlines():
            auth_users.append(line.strip())
        f.close()
    return auth_users

class AGen(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.player = sounds.AudioPlayer(callback=self.playback_finished)

    def perm_check(self, lev, ctx):
        auth_users = refresh_auth_users()
        if lev == 0:
            return True
        if lev == 1: 
            if ctx.author.is_mod or ctx.author.is_subscriber or ctx.author.is_vip or ctx.author.is_broadcaster or ctx.author.name in auth_users: return True
            else: return False
        if lev == 2:
            if ctx.author.is_mod or ctx.author.is_vip or ctx.author.is_broadcaster or ctx.author.name in auth_users: return True
            else: return False
        if lev == 3:
            if ctx.author.is_mod or ctx.author.is_broadcaster or ctx.author.name in auth_users: return True
            else: return False
        if lev == 4:
            if ctx.author.is_broadcaster or ctx.author.name in auth_users: return True
            else: return False
        return False

    async def playback_finished(self):
        print('Playback finished')


##COMMANDS##

def prepare(bot):
    bot.add_cog(AGen(bot))
