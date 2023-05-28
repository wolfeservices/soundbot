#imports
from twitchio.ext import commands, sounds
from config import nick, prefix, channel
import os
from cryptography.fernet import Fernet as fernet
import atexit
import signal

#handle SIGTERM and SIGINT
def sigterm_handler(signum, frame):
    print('SIGTERM received, exiting...')
    if os.path.exists('.session'):
        os.remove('.session')
    exit()
signal.signal(signal.SIGTERM, sigterm_handler)
signal.signal(signal.SIGINT, sigterm_handler)



try:
    with open('.key', 'r') as f: fern_key = f.read()
    f.close()
    fern = fernet(fern_key)
    with open('.storage', 'r') as f: token = fern.decrypt(f.read().encode()).decode()
    f.close()
except:  
    if os.path.exists('.key') and os.path.exists('.storage'):
        #unhide .key and .token
        os.system('attrib -h .key')
        os.system('attrib -h .storage')
        with open('.key', 'r') as f: fern_key = f.read()
        f.close()
        fern = fernet(fern_key)
        with open('.storage', 'r') as f: token = fern.decrypt(f.read().encode()).decode()
        f.close()
    else:
        print ('No token found, or .key is invalid/missing. Please run tlog.pyw regenrate.')
        exit()

if os.path.exists('.loaded_cogs'):
    os.remove('.loaded_cogs')
    print('Removed .loaded_cogs file from previous session')

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
                with open('.loaded_cogs', 'a') as f: f.write(f'{name}\n')

    async def playback_finished(self):
        print('Playback finished')    

    async def event_ready(self):
        print(f'logged in as | {self.nick}')
        print(f'Version: {version}')
        print(f'User ID: {self.user_id}')
        print(f'Channel: {channel}')
        print(f'Prefix: {prefix}')

    #make the bot say something in chat when it joins
    async def event_channel_joined(self, channel):
        await channel.send(f'WolfeBot {version} has started.')

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

    async def reload_cog(self, name: str):
        if name == 'all':
            #unload all cogs
            for line in open('.loaded_cogs', 'r').readlines():
                print(f'Unloading cog: {line}')
                self.unload_module(f'cogs.{line.strip()}')
            os.remove('.loaded_cogs')
            #load all cogs
            for file in sorted(os.listdir('./cogs')):
                if file.endswith('.py'):
                    name = file[:-3]
                    print(f'Loading cog: {name}')
                    self.load_module(f'cogs.{name}')
                    with open('.loaded_cogs', 'a') as f: f.write(f'{name}\n')
        else:
            print(f'Reloading cog: {name}')
            self.reload_module(f'cogs.{name}')

    async def event_message(self, message):
        if message.echo:
            return
        if os.path.isfile('.lockdown'):
            print(f'{message.author.name}: {message.content}')
            if message.author.is_broadcaster or message.author.name in auth_users:
                if message.content.startswith(prefix):
                    print(f'{message.author.name} bypassed lockdown.')
                    await self.handle_commands(message)
            else:
                print(f'{message.author.name} tried to use a command while in lockdown.')
                await message.channel.send('Lockdown enabled, only broadcaster and auth users can use commands.')
        else:
            print(f'{message.author.name}: {message.content}')
            await self.handle_commands(message)


    @commands.command()
    async def reloadCommands(self, ctx: commands.Context):
        if self.perm_check(4, ctx):
            await self.reload_cog('all')
            await ctx.send('Reloaded all commands.')
        else:
            await ctx.send('You do not have permission to use this command.')


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

@atexit.register
def cleanup():
    print('Cleaning up...')
    if os.path.exists('.session'):
        os.remove('.session')
    if os.path.exists('.lockdown'):
        os.remove('.lockdown')
    if os.path.exists('.loaded_cogs'):
        os.remove('.loaded_cogs')
    print('Done.')
