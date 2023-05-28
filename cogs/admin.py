from twitchio.ext import commands, sounds
import os

def refresh_auth_users():
    with open('auth_users.txt', 'r') as f:
        auth_users = []
        for line in f.readlines():
            auth_users.append(line.strip())
        f.close()
    return auth_users

class lock(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

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

    @commands.command()
    async def lockdown(self, ctx: commands.Context):
        if self.perm_check(4, ctx):
            with open('.lockdown', 'w') as f:
                f.write('')
                f.close()
            await ctx.send('Lockdown enabled, only broadcaster and auth users can use commands.')
        else:
            await ctx.send('You do not have permission to use this command.')
    
    @commands.command()
    async def unlock(self, ctx: commands.Context):
        if self.perm_check(4, ctx):
            os.remove('.lockdown')
            await ctx.send('Lockdown disabled, all users can use commands.')
        else:
            await ctx.send('You do not have permission to use this command.')

def prepare(bot):
    bot.add_cog(lock(bot))
