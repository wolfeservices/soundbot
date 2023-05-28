from flask import Flask, url_for, render_template, request
import base64
import requests

#example request : https://commands.wolfebot.info/?commandListID=cG90YXRvLCFwaW5nLCF2ZXJzaW9uLCF0aW1lLCFXQkNvbW1hbmRzLCFsb2NrZG93biwhdW5sb2NrfmdyZWF0ZXN0d29sZmU=

client_id = open('./.client_id', 'r').read()
client_secret = open('./.client_secret', 'r').read()
client_auth = ""
client_tokenType = ""
try_count = 0

debug = True

def get_twitch(channel):
    global client_auth, client_id, client_tokenType, try_count
    if client_auth == "":
        try:
            client_auth = open('./.client_auth', 'r').read()
            client_tokenType = open('./.tokenType', 'r').read()
        except:
            print('client_auth not found, getting new auth token')
            get_tauth()
            get_twitch(channel)
    if client_auth != "":
        auth = client_tokenType + " " + client_auth
        url = 'https://api.twitch.tv/helix/users?login='+channel
        headers = {'Authorization': auth, 'Client-Id': client_id}
        r = requests.get(url, headers=headers)
        if r.status_code == 401:
            print('Received 401, getting new auth token')
            if try_count == 1:
                print('Error getting twitch info, returning "Error"')
                return "Error"
            get_tauth()
            try_count += 1
            get_twitch(channel)
        elif r.status_code != 200:
            print('Received '+str(r.status_code)+' from twitch, returning "Error"')
            return "Error"
        else:
            result = r.json()
            return result
        

def get_tauth():
    #we need to get the access token from twitch
    global client_auth, client_id, client_secret, client_tokenType
    url = 'https://id.twitch.tv/oauth2/token'
    params = "client_id="+client_id+"&client_secret="+client_secret+"&grant_type=client_credentials"
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    r = requests.post(url, data=params, headers=headers)
    #print all the info we got back from twitch for debugging
    result = r.json()
    print(result)
    #capitalise the first letter of the token type
    #FUCK TWITCH DEV, WHY THE FUCK IS THIS CASE SENSITIVE
    result['token_type'] = result['token_type'].capitalize()
    #set the global variable client_auth to the access token
    client_auth = result['access_token']
    client_tokenType = result['token_type']
    with open('./.client_auth', 'w') as f:
        f.write(client_auth)
    with open(".tokenType", "w") as f:
        f.write(client_tokenType)




app = Flask(__name__)

@app.route('/')
def index():
    payload = request.args.get('commandListID')
    print(payload)
    if payload == None:
        return render_template('indexError.html')
    else:
        content = base64.urlsafe_b64decode(payload).decode()
        content = content.split('~')
        command_list = content[0]
        channel = content[1]
        command_list = command_list.split(',')
        wrapped_command_list = []
        for command in command_list:
            #wrap each command in a <li> tag
            wrapped_command_list.append('<li>'+command+'</li>')
        #join the list into a string
        wrapped_command_list = ''.join(wrapped_command_list)
        tjson = get_twitch(channel)
        if tjson == "Error":
            channel_display = channel
            channel_logo= "https://static-cdn.jtvnw.net/jtv_user_pictures/xarth/404_user_150x150.png"
        else:
            print(tjson)
            channel_display = tjson['data'][0]['display_name']
            channel_logo = tjson['data'][0]['profile_image_url']
        return render_template('index.html', command_list=wrapped_command_list, channel=channel_display, channel_logo=channel_logo)

if __name__ == '__main__':
    if debug:
        app.run(debug=True, host='localhost', port=5000)
    else:
        app.run(port=8081)