#imports
from twitchio.ext import commands, sounds
from config import nick, prefix, channel
import os
from cryptography.fernet import Fernet as fernet

try:
    with open('.key', 'r') as f: fern_key = f.read()
    f.close()
    fern = fernet(fern_key)
    with open('.token', 'r') as f: token = fern.decrypt(f.read().encode()).decode()
    f.close()
except:  
    print ('No token found, or .key is invalid/missing. Please run tlog.pyw regenrate.')
    exit()


version = open('version.txt', 'r').read()
auth_users = []

def refresh_auth_users():
    with open('auth_users.txt', 'r') as f:
        auth_users = []
        for line in f:
            auth_users.append(line.strip())
        f.close()




class Bot(commands.Bot):
    def __init__(self):
        super().__init__(token=token, nick=nick, prefix=prefix, initial_channels=[channel])
        
        self.player = sounds.AudioPlayer(callback=self.playback_finished)

        #load cogs
        for file in sorted(os.listdir('./cogs')):
            if file.endswith('.py'):
                name = file[:-3]
                print(f'Loading cog: {name}')
                self.load_module(f'cogs.{name}')

    async def playback_finished(self):
        print('Playback finished')    

    async def event_ready(self):
        print(f'logged in as | {self.nick}')
        print(f'Version: {version}')
        print(f'User ID: {self.user_id}')
        print(f'Channel: {channel}')
        print(f'Prefix: {prefix}')

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

    async def event_message(self, message):
        if message.echo:
            return
        if os.path.isfile('.lockdown'):
            if message.author.is_broadcaster or message.author.name in auth_users:\
                await self.handle_commands(message)
            else:
                await message.channel.send('Lockdown enabled, only broadcaster and auth users can use commands.')
        else:
            await self.handle_commands(message)


def main():
    #write session file
    with open('.session', 'w') as f:
        f.write('')
    #load listfiles
    #auth_users
    with open('auth_users.txt', 'r') as f:
        auth_users = []
        for line in f.readlines():
            auth_users.append(line.strip())
        f.close()
    bot = Bot()
    bot.run()

if __name__ == "__main__":
    main()

else:
    main()