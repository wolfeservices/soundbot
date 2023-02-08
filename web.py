from flask import Flask, request, render_template, redirect, url_for

from updater import check_for_update, update, get_latest_release

import subprocess

bot_toggle_text = "start"
bot_state = "stopped"


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
    else:
        print("error")
        return redirect(url_for('error'))
    return redirect(url_for('index'))

@app.route('/redir')
def redir():
    return redirect(url_for('index'))

@app.route('/error')
def error():
    return render_template('error.html')

@app.route('/alert/<message>')
def alert(message):
    return render_template('alert.html', message=message)

@app.route('/shutdown')
def shutdown():
    bot(False)
    #close the server
    shutdown_server()

if __name__ == '__main__':
    app.run(debug=True)