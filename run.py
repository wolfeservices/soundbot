#this script edits bot.py to add the commands from the commands.txt file and then runs the bot

import os

#test for the required modules
try:
    import twitchio
except:
    print('twitchio not found, installing it now')
    os.system('pip install twitchio')
try:
    from twitchio.ext import sounds
except:
    print('twitchio.ext.sounds not found, installing it now')
    os.system('pip install twitchio[sounds]')
try:
    import pyaudio
except:
    print('pyaudio not found, installing it now')
    os.system('pip install pyaudio')



#variables
token=''
nick=''
channel=''
prefix=''

#check if config.py exists, else create it then exit
if not os.path.exists('config.py'):
    print('config.txt not found, creating it now')
    f=open('config.py','w')
    f.write('#config file for bot.py\ntoken=your token\nnick=your bot\'s nick\nchannel=channel to join\nprefix=command prefix')
    f.close()
    exit()

#import config.py
from config import *

#remove old commands by replacing everything between #<commands> and #</commands> with a single newline
f=open('bot.py','r')
lines=f.readlines()
f.close()
index=lines.index('#<commands>\n')
index2=lines.index('#</commands>\n')
lines=lines[:index+1]+['\n']+lines[index2:]
f=open('bot.py','w')
f.writelines(lines)
f.close()


#check if commands.txt exists, else create it then exit
if not os.path.exists('commands.txt'):
    print('commands.txt not found, creating it now')
    f=open('commands.txt','w')
    f.write('#commands go here, one per line in the format: command:response:sound.mp3:volume(0-100) Response and Sound.mp3 may be set to None (case sensitive) volume may be absent if sound isnt set, but one or both must be set')
    f.close()
    exit()

#read commands.txt to a list
commands=[]
f=open('commands.txt','r')
for line in f:
    commands.append(line.strip())

#remove comments
commands=[x for x in commands if not x.startswith('#')]

#convert commands to wrapped commands for bot.py command[3] is volume and is optional, default is 100 if not set
wrapped_commands=[]
for command in commands:
    print (command)
    #split command into parts and assign them to variables
    command=command.split(':')
    #if command does not have 3 or 4 parts, skip it
    if len(command) < 3 or len(command) > 4:
        print('invalid command, skipping')
        continue
    command_name=command[0]
    command_response=command[1]
    command_sound=command[2]
    if len(command) > 3:
        command_volume=command[3]
    else:
        command_volume=100
    #prepend the path to the sound file
    command_sound='./sounds/'+command_sound

    #print the calculated variables
    print(f'command_name: {command_name}')
    print(f'command_response: {command_response}')
    print(f'command_sound: {command_sound}')
    print(f'command_volume: {command_volume}')
    
    #wrap command
    if command_response != 'None' and command_sound != 'None':
        wrapped_commands.append(f"\t@commands.command()\n\tasync def {command_name}(self, ctx: commands.Context):\n\t\tself.player.volume = {command_volume}\n\t\tsound = sounds.Sound(source='{command_sound}')\n\t\tself.player.play(sound)\n\t\tawait ctx.send('{command_response}')\n\n")
    elif command_response != 'None':
        wrapped_commands.append(f"\t@commands.command()\n\tasync def {command_name}(self, ctx: commands.Context):\n\t\tawait ctx.send('{command_response}')\n\n")
    elif command_sound != 'None':
        wrapped_commands.append(f"\t@commands.command()\n\tasync def {command_name}(self, ctx: commands.Context):\n\t\tself.player.volume = {command_volume}\n\t\tsound = sounds.Sound(source='{command_sound}')\n\t\tself.player.play(sound)\n\n")
    else:
        print(f'Error: command {command_name} has no response or sound')
        continue
        
#add commands to bot.py
f=open('bot.py','r')
lines=f.readlines()
f.close()
index=lines.index('#<commands>\n')
lines=lines[:index+1]+wrapped_commands+lines[index+1:]


#write bot.py
f=open('bot.py','w')
f.writelines(lines)
f.close()

#start bot
print(f'Starting bot, press Ctrl+C to exit')
os.system('python bot.py '+token+' '+nick+' '+channel+' '+prefix)



