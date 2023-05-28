import os
import time
import random
from flask import Flask, render_template, request, redirect
from cryptography.fernet import Fernet
import urllib.parse
import webbrowser

clientid = "83dnr5c7wspcobvhegzd0029gr9apq"
callback = "http://localhost:8080/callback?"
scope = "chat%3Aread+chat%3Aedit"

if os.path.exists('.key'):
    #check if .key is hidden, if so, unhide it
    if os.system('attrib .key') == 0:
        os.system('attrib -h .key')

if os.path.exists('.storage'):
    #check if .storage is hidden, if so, unhide it
    if os.system('attrib .storage') == 0:
        os.system('attrib -h .storage')

try:
    with open('.key', 'r') as key:
        enc_key = key.read()
except FileNotFoundError:
    enc_key = Fernet.generate_key()
    with open('.key', 'wb') as key:
        key.write(enc_key)
    #make .key hidden
    os.system('attrib +h .key')

fern = Fernet(enc_key)


def oauth():
    return f'https://id.twitch.tv/oauth2/authorize?client_id=83dnr5c7wspcobvhegzd0029gr9apq&force_verify=true&redirect_uri=http://localhost:8080/callback?&response_type=token&scope=chat%3Aread+chat%3Aedit'

app = Flask(__name__)

@app.route('/')
def index():
    #use random string for state to prevent CSRF
    rgen = random.getrandbits(256) + int(time.time())
    #encode state as hex
    state = str(hex(rgen))
    print(state)
    #save state to file
    with open('.state', 'w') as f:
        f.write(state)
    #redirect to twitch oauth page
    return redirect (oauth() + f'&state={state}')


@app.route('/callback')
def callback():
    return render_template('callback.html')

@app.route('/auth')
def auth():
    
    args = request.args.get('fragment')
    urllib.parse.unquote(args)
    print(args)
    args = args.split('&')
    for arg in args:
        arg = arg.split('=')
        if arg[0] == 'access_token':
            access_token = arg[1]
        elif arg[0] == 'state':
            state = arg[1]
        else:
            pass
    if state == open('.state', 'r').read():
        print('state is valid')
        with open('.storage', 'wb') as storage:
            storage.write(fern.encrypt(access_token.encode('utf-8')))
            storage.close()
        with open('.storage', 'r') as storage:
            encrypted = storage.read()
            decrypted = fern.decrypt(encrypted.encode('utf-8')).decode('utf-8')
            if decrypted == access_token:
                print('token is valid')
            else:
                print('token is invalid')
        os.remove('.state')
        os.system('attrib +h .storage')
        with open('.logsuccess', 'w') as f:
            f.write('1')
        return "Logged in successfully, you can close this window now."
    else:
        print('state is invalid')
        with open('.logfail', 'w') as f:
            f.write('1')
        return "State is invalid, please try again in a few minutes."




if __name__ == '__main__':
    webbrowser.open('http://localhost:8080')
    app.run(port=8080)


    
