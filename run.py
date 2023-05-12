import os
import sys
import requests
import json
import threading
import webbrowser
import time
import pyunpack
import shutil
from io import BytesIO

version = ''

#determine if running on linux, windows, or mac
if sys.platform.startswith('linux'):
    os.system('clear')
elif sys.platform.startswith('win32'):
    os.system('cls')
elif sys.platform.startswith('darwin'):
    os.system('clear')

def initalizer():
    global version
    if os.path.isfile('.storage') and os.path.isfile('.key'):
        print('Storage and key files found, skipping login')
    else:
        print('Storage and key files not found, logging in')
        login()
    if os.path.isfile('config.py'):
        print('Config file found, skipping config')
    else:
        print('Config file not found, creating')
        config()
    if os.path.isfile('auth_users.txt'):
        print('Auth users file found, skipping auth users')
    else:
        print('Auth users file not found, creating')
        with open('auth_users.txt', 'w') as f:
            f.write('')
            f.close()
    try:
        with open('version.txt', 'r') as f:
            version = f.read()
            f.close()
    except:
        print('Version file not found, instigating upgrade as a precaution')
        do_upgrade()  
    if os.path.isfile('.lockdown'):
        os.remove('.lockdown')
    if os.path.isfile('.session'):
        os.remove('.session')
    return version
    
def login():
    tlogin = threading.Thread(target=login_thread)
    tlogin.start()
    #wait for login to finish
    while tlogin.is_alive():
        pass
    if os.path.isfile('.storage') and os.isfile('.key'):
        print('Login successful')
    else:
        print('Login failed, please try again')
        login()

def login_thread():
    os.system('pythonw login.py')
    webbrowser.open('http://localhost:8080')

def config():
    print('Please enter the following information:')
    nick = input('Bot nickname: ')
    channel = input('Channel name: ')
    prefix = input('Command prefix: ')
    with open('config.py', 'w') as f:
        f.write(f'nick = "{nick}"\n')
        f.write(f'channel = "{channel}"\n')
        f.write(f'prefix = "{prefix}"\n')
        f.close()

def check_upgrade(version):
    #get latest release
    r = requests.get('https://api.github.com/repos/wolfeservices/soundbot/releases/latest')
    if r.status_code == 200:
        #get version number
        latest = json.loads(r.text)['tag_name']
        if latest != version:
            print(f'New version available: {latest}')
            do_upgrade()
        else:
            print('No new version available')
    else:
        print('Error checking for new version')

def do_upgrade():
    release = json.loads(requests.get('https://api.github.com/repos/wolfeservices/soundbot/releases/latest').text)
    for asset in release['assets']:
        if asset['name'] == 'soundbot.zip':
            url = asset['browser_download_url']
            break
    r = requests.get(url)
    if r.status_code == 200:
        pyunpack.Archive(BytesIO(r.content)).extractall('.')
        print('Upgrade complete')
        with open('version.txt', 'w') as f:
            f.write(release['tag_name'])
            f.close()
    else:
        print('Error downloading upgrade')

def main():
    #initialize
    version = initalizer()
    print(version)
    #thread bot
    tbot = threading.Thread(target=bot_thread)
    tbot.start()
    print('Bot started')
    while tbot.is_alive():
        if os.path.isfile('.control'):
            with open('.control', 'r') as f:
                command = f.read()
                f.close()
            if command == 'stop':
                os.remove('.control')
                os.remove('.session')
                os.remove('.lockdown')
                os._exit(0)
            elif command == 'restart':
                tbot.kill()
                os.remove('.control')
                os.remove('.session')
                os.remove('.lockdown')
                tbot = threading.Thread(target=bot_thread)
                tbot.start()
                print('Bot restarted')

        else:
            time.sleep(1)
            
def bot_thread():
    fullVenv = os.path.join(os.getcwd(), 'venv')
    if sys.platform.startswith('linux'):
        venv = os.path.join(fullVenv, 'bin', 'python')
    elif sys.platform.startswith('win32'):
        venv = os.path.join(fullVenv, 'Scripts', 'python.exe')
    elif sys.platform.startswith('darwin'):
        venv = os.path.join(fullVenv, 'bin', 'python')
    os.system(f'{venv} bot.py')

if __name__ == '__main__':
    main()

