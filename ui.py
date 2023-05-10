#imports
import os
import threading
import time
from tkinter import * 
from tkinter.ttk import *
import subprocess

#global variables
version = open('version.txt', 'r').read()
#token is stored in environment variable for security reasons
token = os.environ['TOKEN']

#if token is not set, start ui in login mode
if token == 'NTKN':
    login = True
else:
    login = False

#functions
def mainwindow():
    global mwin
    global status
    global login
    mwin = Tk()
    mwin.title('Wolfebot ' + version)
    mwin.geometry('300x300')
    mwin.resizable(False, False)
    if login:
        loginwindow()
    Canvas(mwin, width=300, height=300, bg='#1e1e1e').place(x=0, y=0)
    Label(mwin, text='Wolfebot ' + version, font=('Arial', 20), bg='#1e1e1e', fg='#ffffff').place(x=0, y=0)
    Label(mwin, text=status, font=('Arial', 10), bg='#1e1e1e', fg='#ffffff').place(x=0, y=40)
    Button(mwin, text='configure', command=configwin).place(x=0, y=50)
    Button(mwin, text='Start Bot', command=start_bot).place(x=0, y=100)
    Button(mwin, text='Stop Bot', command=stop_bot).place(x=0, y=150)
    Button(mwin, text='Restart Bot', command=restart_bot).place(x=0, y=200)
    Button(mwin, text='Exit', command=safe_exit).place(x=0, y=250)
    mwin.mainloop()

def loginwindow():
    global mwin
    global status
    global login
    #clear main window 
    for widget in mwin.winfo_children():
        widget.destroy()
    #create login buton
    Label(mwin, text='Please Log In with Twtch', font=('Arial', 10), bg='#1e1e1e', fg='#ffffff').place(x=0, y=40)
    Button(mwin, text='Login', command=tlog).place(x=150, y=150)
    while os.path.isfile('.storage') == False:
        time.sleep(0.25)
    #clear main window
    for widget in mwin.winfo_children():
        widget.destroy()
    login = False
    mainwindow()

def tlog():
    #run tlog.pyw in a subprocess, and wait for it to write .loginsuccess
    threading.Thread(target=subprocess.run, args=(['pythonw', 'tlog.pyw'],)).start()
    while os.path.isfile('.loginsuccess') == False:
        time.sleep(0.25)

def start_bot():
    with open('.control', 'w') as f:
        f.write('start')
    status = 'Bot starting...'
    while os.path.isfile('.session') == False:
        time.sleep(0.25)
    status = 'Bot started'

def stop_bot():
    with open('.control', 'w') as f:
        f.write('stop')
    status = 'Bot stopping...'
    while os.path.isfile('.session') == True:
        time.sleep(0.25)
    status = 'Bot stopped'
    mainwindow()

def restart_bot():
    with open('.control', 'w') as f:
        f.write('restart')
    status = 'Bot restarting...'
    time.sleep(2)
    while os.path.isfile('.session') == False:
        time.sleep(0.25)
    status = 'Bot started'

def safe_exit():
    with open('.control', 'w') as f:
        f.write('exit')
    status = 'Exiting...'
    time.sleep(2)
    mwin.destroy()

def configwin():
    conwin = Tk()
    conwin.title('Wolfebot ' + version + ' - Configure')
    conwin.geometry('300x300')
    conwin.resizable(False, False)
    Canvas(conwin, width=300, height=300, bg='#1e1e1e').place(x=0, y=0)
    Label(conwin, text='Bot Name', font=('Arial', 20), bg='#1e1e1e', fg='#ffffff').place(x=0, y=0)
    bn_entry = Entry(conwin)
    bn_entry.place(x=0, y=40)
    Label(conwin, text='Bot Prefix', font=('Arial', 20), bg='#1e1e1e', fg='#ffffff').place(x=0, y=80)
    bp_entry = Entry(conwin)
    bp_entry.place(x=0, y=120)
    Label(conwin, text='Channel to Join', font=('Arial', 20), bg='#1e1e1e', fg='#ffffff').place(x=0, y=160)
    cj_entry = Entry(conwin)
    cj_entry.place(x=0, y=200)
    Button(conwin, text='Save', command=save_config).place(x=0, y=250)
    conwin.mainloop()
    def save_config():
        with open('config.py') as conf:
            conf.write('bot_nickname = ' + bn_entry.get() + '\n')
            conf.write('bot_prefix = ' + bp_entry.get() + '\n')
            conf.write('channel_to_join = ' + cj_entry.get() + '\n')
        conwin.destroy()





if __name__ == '__main__':
    print('do not run this file directly, run control.py instead')
    exit()
else:
    mainwindow()
