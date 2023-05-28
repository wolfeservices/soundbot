import os


cogfile = 'cogs/commands.py'
emptycog = 'templates/emptycog.py'

#copy emptycog to cogfile
with open(emptycog, 'r') as f:
    with open(cogfile, 'w') as f2:
        f2.write(f.read())

#open cogfile locate ##COMMANDS## and get index for writing
with open(cogfile, 'r') as f:
    lines = f.readlines()
    for i, line in enumerate(lines):
        if '##COMMANDS##' in line:
            index = i
            break

#initalize .temp file so we can determine if there are any commands to add
with open('.temp', 'w') as f:
    f.write('')

#check if commands.txt does not contain any commands
if open('commands.txt', 'r').read() == '':
    print ('No commands to add')
    exit()

#write commands to cogfile
with open(cogfile, 'w') as f:
    with open('commands.txt', 'r') as f2:
        for line in f2.readlines():
            #parse command by reading line and splitting into list on :
            line = line.strip()
            if line == '': continue
            command, resp, sound, volume, perm = line.split(':')
            print (command, resp, sound, volume, perm)
            text = resp
            volume = int(volume)

            if perm != 0 and perm != 1 and perm != 2 and perm != 3 and perm != 4:
                perm = 0

            if volume > 100:
                volume = 100
            elif volume < 0:
                volume = 0
            elif volume == '':
                volume = 100
            
            #write command to temoprary file
            if sound != 'nil' and text == 'nil':
                with open('.temp', 'a') as t:
                    t.write(f'   @commands.command(name=\'{command}\')\n    async def {command}(self, ctx: commands.Context):\n        if not self.perm_check({perm}, ctx):\n            await ctx.send(\'You do not have permission to use this command.\')\n        else:\n            noise = sounds.Sound(source=\'sounds/{sound}.mp3\')\n            self.player.volume = {volume}\n            self.player.play(noise)\n')
                            
            elif sound == 'nil' and text != 'nil':
                with open('.temp', 'a') as t:
                    t.write(f'    @commands.command(name=\'{command}\')\n    async def {command}(self, ctx: commands.Context):\n        if not self.perm_check({perm}, ctx):\n            await ctx.send(\'You do not have permission to use this command.\')\n        else:\n            await ctx.send(\'{text}\')\n')
            
            elif sound != 'nil' and text != 'nil':
                with open('.temp', 'a') as t:
                    t.write(f'    @commands.command(name=\'{command}\')\n    async def {command}(self, ctx: commands.Context):\n        if not self.perm_check({perm}, ctx):\n            await ctx.send(\'You do not have permission to use this command.\')\n        else:\n            noise = sounds.Sound(source=\'sounds/{sound}.mp3\')\n            self.player.volume = {volume}\n            self.player.play(noise)\n            await ctx.send(\'{text}\')\n')
            else:
                raise Exception('Invalid command format')
            
    #write temporary file to cogfile at index
    if not os.path.exists('.temp'):
        print ('No commands to add')
    elif open('.temp', 'r').read() == '':
        print ('No commands to add')
        #remove empty cogfile
        os.remove(cogfile)
    else:
        with open('.temp', 'r') as t:
            lines[index:index] = t.readlines()
            f.writelines(lines)
        os.remove('.temp')




            
            
                        










#EXAMPLE COMMAND FORMAT
#    @commands(command)
#    async def {command}(self, ctx: commands.Context):
#        if not self.perm_check({perm}, ctx):
#            await ctx.send('You do not have permission to use this command.')
#        else:
#        noise= sounds.Sound(source-'sounds/{sound}.mp3')
#        self.player.volume = {volume}
#        self.player.play(noise)
#        await ctx.send('{text}')

