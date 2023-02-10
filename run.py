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

import webbrowser


#check if config.py exists, else create it then exit
if not os.path.exists('config.py'):
    print('config.txt not found, creating it now')
    f=open('config.py','w')
    f.write('#config file for bot.py\ntoken=\'your token\'\nnick=\'your bot\'s \'\nchannel=\'channel to join\'\nprefix=\'command prefix\'')
    f.close()
    exit()

#get timestamp for log file
from datetime import datetime
now = datetime.now()

#logfile is in the format log_YYYY_MM_DD_HH_MM_SS.txt (e.g. log_2020_01_01_00_00_00.txt) and is stored in the logs folder
# if the logs folder does not exist, create it
if not os.path.exists('logs'):
    os.makedirs('logs')
logfile = 'logs/log_' + now.strftime("%Y_%m_%d_%H_%M_%S") + '.txt' 

print(f'bot has started, use the web interface at http://localhost:5000 to control it')
webbrowser.open('http://localhost:5000')
#start flask server
#simultaneously display the output of the terminal as well as store it in a file called log.txt
os.system('python ./web.py > ' + logfile + ' 2>&1')


