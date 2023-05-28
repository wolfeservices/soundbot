#!/usr/bin/python3
import tkinter as tk
import tkinter.ttk as ttk
import subprocess
import os
import time
import signal
i=0

class UiApp:
    def __init__(self, master=None):
        # build ui
        self.Main = tk.Tk() if master is None else tk.Toplevel(master)
        self.img_wolfebot = tk.PhotoImage(file=os.path.join(os.path.dirname(__file__), './static/wolfebot.png'))
        self.Main.configure(
            background="#4b4b4b",
            height=200,
            highlightbackground="#4b4b4b",
            takefocus=False,
            width=200)
        self.Main.iconphoto(True, self.img_wolfebot)
        self.Main.resizable(False, False)
        self.version = open('version.txt', 'r').read().strip()
        self.Main.title("WolfeBot " + self.version)
        label1 = ttk.Label(self.Main)
        self.botState = tk.StringVar(value='Please set up bot.')
        label1.configure(
            background="#4b4b4b",
            font="{Arial Black} 12 {}",
            foreground="#ffffff",
            text='Please set up bot.',
            textvariable=self.botState)
        label1.grid(column=0, columnspan=4, row=0)
        self.start = ttk.Button(self.Main)
        self.start.configure(state="disabled", text='Start')
        self.start.grid(column=0, padx=10, pady=10, row=1)
        self.start.configure(command=self.startbot)
        self.restart = ttk.Button(self.Main)
        self.restart.configure(state="disabled", text='Restart')
        self.restart.grid(column=2, padx=10, pady=10, row=1)
        self.restart.configure(command=self.restartbot)
        self.stop = ttk.Button(self.Main)
        self.stop.configure(state="disabled", text='Stop')
        self.stop.grid(column=3, padx=10, pady=10, row=1)
        self.stop.configure(command=self.stopbot)
        self.sett = ttk.Button(self.Main)
        self.sett.configure(text='Settings')
        self.sett.grid(column=0, columnspan=3, padx=10, pady=10, row=2)
        self.sett.configure(command=self.settings)
        self.safeexit = ttk.Button(self.Main)
        self.safeexit.configure(text='Exit')
        self.safeexit.grid(column=2, columnspan=2, padx=10, pady=10, row=2)
        self.safeexit.configure(command=self.exitsafe)
        self.Main.grid_anchor("n")

        self.bot_thread = None
        # Main widget
        self.mainwindow = self.Main

    def run(self):
        if os.path.exists('./.key') and os.path.exists('./.storage'):
            self.start.configure(state="normal")
            self.restart.configure(state="disabled")
            self.stop.configure(state="disabled")
            self.botState.set("Bot is ready to start.")
        else:
            subprocess.Popen(["python", "login.py"])
            self.mainwindow.destroy()
        if os.path.exists('./.session'):
            self.botState.set("Bot may be running. please exit and restart.")
            self.start.configure(state="disabled")
            self.restart.configure(state="disabled")
            self.stop.configure(state="disabled")
        self.mainwindow.mainloop()

    def startbot(self):
        subprocess.Popen(["python", "commandwrapper.py"])
        time.sleep(2)
        self.botState.set("Bot is running.")
        self.start.configure(state="disabled")
        self.restart.configure(state="normal")
        self.stop.configure(state="normal")
        self.bot_thread = subprocess.Popen(["python", "bot.py"])
        return


    def restartbot(self):
        self.bot_thread.send_signal(signal.SIGTERM)
        time.sleep(2)
        self.botState.set("Bot is running.")
        self.bot_thread = subprocess.Popen(["python", "bot.py"])
        return

    def stopbot(self):
        if self.bot_thread is not None:
            self.bot_thread.send_signal(signal.SIGTERM)
            self.start.configure(state="normal")
            self.restart.configure(state="disabled")
            self.stop.configure(state="disabled")
            self.botState.set("Bot is stopped.")
            if os.path.exists('./.session'):
                os.remove('./.session')
        return

    def settings(self):
        #close main window
        self.mainwindow.destroy()
        #open settings window
        subprocess.Popen(["python", "settings.py"])

    def exitsafe(self):
        self.stopbot()
        self.mainwindow.destroy()
        exit()


if __name__ == "__main__":
    app = UiApp()
    app.run()
