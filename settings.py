#!/usr/bin/python3
import tkinter as tk
import tkinter.ttk as ttk
import os
import subprocess
import time


class UiApp:
    def __init__(self, master=None):
        # build ui
        self.Settings = tk.Tk() if master is None else tk.Toplevel(master)
        #imagepath  ../static/wolfebot.png
        self.img_wolfebot = tk.PhotoImage(file=os.path.join(os.path.dirname(__file__), './static/wolfebot.png'))
        self.Settings.configure(
            background="#4b4b4b",
            height=200,
            highlightbackground="#4b4b4b",
            takefocus=False,
            width=200)
        self.Settings.geometry("352x288")
        self.Settings.iconphoto(True, self.img_wolfebot)
        self.Settings.resizable(False, False)
        self.version = open('version.txt', 'r').read().strip()
        self.Settings.title("WolfeBot " + self.version)
        label9 = ttk.Label(self.Settings)
        label9.configure(
            background="#4b4b4b",
            font="{Arial Black} 12 {}",
            foreground="#ffffff",
            text='Settings')
        label9.pack(side="top")
        frame1 = ttk.Frame(self.Settings)
        frame1.configure(height=220, width=352)
        label10 = ttk.Label(frame1)
        label10.configure(font="{Arial} 12 {}", text='Bot Nickname')
        label10.grid(column=0, row=0)
        entry4 = ttk.Entry(frame1)
        self.nick = tk.StringVar()
        entry4.configure(textvariable=self.nick, width=35)
        entry4.grid(column=1, row=0)
        label11 = ttk.Label(frame1)
        label11.configure(font="{Arial} 12 {}", text='Prefix')
        label11.grid(column=0, row=1)
        entry5 = ttk.Entry(frame1)
        self.prefix = tk.StringVar()
        entry5.configure(textvariable=self.prefix, width=35)
        entry5.grid(column=1, row=1)
        label12 = ttk.Label(frame1)
        label12.configure(font="{Arial} 12 {}", text='Channel')
        label12.grid(column=0, row=2)
        entry6 = ttk.Entry(frame1)
        self.channel = tk.StringVar()
        entry6.configure(textvariable=self.channel, width=35)
        entry6.grid(column=1, row=2)
        label13 = ttk.Label(frame1)
        label13.configure(font="{Arial} 12 {}", text='Twitch Login')
        label13.grid(column=0, row=3)
        button20 = ttk.Button(frame1)
        self.tlog_status = tk.StringVar(value='Login')
        button20.configure(text='Login', textvariable=self.tlog_status)
        button20.grid(column=1, row=3)
        button20.configure(command=self.tloggi)
        frame1.pack(anchor="center", expand="true", side="top")
        frame1.grid_propagate(0)
        frame1.grid_anchor("center")
        frame1.rowconfigure(0, pad=10)
        frame1.rowconfigure("all", pad=10)
        frame1.columnconfigure(0, pad=10)
        frame1.columnconfigure("all", pad=10)
        self.SettingSave = ttk.Button(self.Settings)
        self.SettingSave.configure(text='Save & Close')
        self.SettingSave.pack(anchor="se", padx=10, pady=10, side="bottom")
        self.SettingSave.configure(command=self.save_settings)

        if os.path.isfile('.storage'):
            self.tlog_status.set('Re-Login')
        else:
            self.tlog_status.set('Login')

        #prefill the settings with the current settings
        if os.path.isfile('config.py'):
            with open('config.py', 'r') as config:
                for line in config.readlines():
                    if 'nick' in line:
                        self.nick.set(line.split('=')[1].strip().strip("'"))
                    elif 'prefix' in line:
                        self.prefix.set(line.split('=')[1].strip().strip("'"))
                    elif 'channel' in line:
                        self.channel.set(line.split('=')[1].strip().strip("'"))


        # Main widget
        self.mainwindow = self.Settings

    def run(self):
        self.mainwindow.mainloop()

    def tloggi(self):
        #close current window and open the login window
        self.mainwindow.destroy()
        subprocess.Popen(['python', 'login.py'])


    def save_settings(self):
        #check if the settings changed, and if so, update the config file
        if os.path.isfile('config.py'):
            os.remove('config.py')
        with open('config.py', 'w') as config:
            config.write(f"nick = '{self.nick.get()}'\n")
            config.write(f"prefix = '{self.prefix.get()}'\n")
            config.write(f"channel = '{self.channel.get()}'\n")
        self.mainwindow.destroy()
        subprocess.Popen(['python3', 'main.py'])


            


if __name__ == "__main__":
    app = UiApp()
    app.run()

