from flask import Flask, request, render_template, redirect, url_for

from updater import check_for_update, update, get_latest_release

import subprocess
import os

bot_toggle_text = "start"
bot_state = "stopped"

try:    
    last_added = open("last_added.txt", "r").read()
except:
    #if file does not exist create it and write "none"
    open("last_added.txt", "w").write("none")
    last_added = open ("last_added.txt", "r").read()

def commandwrapper(bool, command, response, responsefile, volume):
    #bool is True if command is to be added to commandlist, False if command is to be removed
    if bool == False:
        if os.system("python commandwrapper.py -R -c " + command) == 0:
            return url_for ('alert', message="Command removed", destinationID="2")
        else:
            return url_for ('alert', message="Command not found", destinationID="2")
    elif bool == True:
        if os.system("python commandwrapper.py -A -c " + command + " -r " + response + " -f " + responsefile + "-v "+ volume) == 0:
            return url_for ('alert', message="Command added", destinationID="2")
        else:
            return url_for ('alert', message="Command already exists", destinationID="2")
    else:
        return url_for ('alert', message="Error", destinationID="2")

def start_bot():
    global bot_state
    bot_state = "running"
    global bot
    bot = subprocess.Popen("python bot.py", shell=True)


app = Flask(__name__)

@app.route('/')
def index():
    if bot_state == "stopped":
        return render_template('indexu.html', bot_toggle_text="Start Bot", bot_state="offline")
    elif bot_state == "running":
        return render_template('index.html', bot_toggle_text="Running", bot_state="online")

@app.route('/command', methods=['POST'])
def command():
    post = request.form
    #strip"ImmutableMultiDict([(" and ")])"
    post = str(post)[21:-3]
    #remove '
    post = post.replace("'", "")
    #remove whitespace
    post = post.replace(" ", "")
    #discard everything after the first comma
    post = post.split(",")[0]
    print(post)
    if post == "U1":
        #run check_for_update() if reurn is True print "update complete" else print "no update"
        if check_for_update() == True:
            return redirect(url_for('alert', message="Update complete"))
        else:
            return redirect(url_for('alert', message="No update"))
    elif post == "S1":
        if bot_state == "stopped":
            start_bot()
        elif bot_state == "running":
            return redirect(url_for('alert', message="Bot is already running"))
        else:
            print("error")
            return redirect(url_for('error'))
    elif post == "AC":
        return redirect(url_for('ac'))
    else:
        print("error")
        return redirect(url_for('error'))
    return redirect(url_for('index'))

@app.route('/redir')
def redir():
    return redirect(url_for('index'))

@app.route('/error/<int:destinationID>')
def error(destinationID):
    if destinationID == "1":
        destination = url_for('index')
    elif destinationID == "2":
        destination = url_for('ac')
    else:
        destination = url_for('errorFinal')

@app.route('/alert/<message>/<int:destinationID>')
def alert(message, destinationID):
    if destinationID == "1":
        destination = url_for('index')
    elif destinationID == "2":
        destination = url_for('ac')
    else:
        destination = url_for('error')

    return render_template('alert.html', message=message, destination=destination)
    

@app.route('/ac')
def ac():
    return render_template('ac.html')

@app.route('/ac/add', methods=['POST'])
def acadd():
    post = request.form
    print(post)
    #trim "ImmutableMultiDict([*])"
    post = str(post)[20:-2]
    print(post)
    #break  into clusters cluster ex: ('name', 'value')
    post = post.split("), (")
    for i in range(len(post)):
        #remove '
        post[i] = post[i].replace("'", "")
        #remove whitespace
        post[i] = post[i].replace(" ", "")
        #remove ( and )
        post[i] = post[i].replace("(", "")
        post[i] = post[i].replace(")", "")
        #split into name and value
        post[i] = post[i].split(",")
    print(post)
    #break post into known structure
    command = post[0][1]
    response = post[1][1]
    responsefile = post[2][1]
    volume = post[3][1]
    #check if responsefile is empty
    if responsefile == "":
        responsefile = "0"
    #pass to commandwrapper
    commandwrapper(True, command, response, responsefile, volume)

@app.route('/ac/delete', methods=['POST'])
def acdelete():
    post = request.form
    print(post)
    #trim "ImmutableMultiDict([*])"
    post = str(post)[20:-2]
    print(post)
    #break  into clusters cluster ex: ('name', 'value')
    post = post.split("), (")
    for i in range(len(post)):
        #remove '
        post[i] = post[i].replace("'", "")
        #remove whitespace
        post[i] = post[i].replace(" ", "")
        #remove ( and )
        post[i] = post[i].replace("(", "")
        post[i] = post[i].replace(")", "")
        #split into name and value
        post[i] = post[i].split(",")
    print(post)
    #break post into known structure
    command = post[0][1]
    #pass to commandwrapper
    commandwrapper(False, command, "", "", "")
    
    

if __name__ == '__main__':
    app.run(debug=True)