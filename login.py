#!/usr/bin/python3
import tkinter as tk
import tkinter.ttk as ttk
import os
import subprocess
import time


class UiApp:
    def __init__(self, master=None):
        # build ui
        self.Login = tk.Tk() if master is None else tk.Toplevel(master)
        self.img_wolfebot = tk.PhotoImage(file=os.path.join(os.path.dirname(__file__), './static/wolfebot.png'))
        self.Login.configure(
            background="#4b4b4b",
            height=200,
            highlightbackground="#4b4b4b",
            takefocus=False,
            width=200)
        self.Login.geometry("352x288")
        self.Login.iconphoto(True, self.img_wolfebot)
        self.Login.resizable(False, False)
        self.version = open('version.txt', 'r').read().strip()
        self.Login.title("WolfeBot " + self.version)
        label2 = ttk.Label(self.Login)
        label2.configure(
            background="#4b4b4b",
            font="{Arial Black} 12 {}",
            foreground="#ffffff",
            text='Please Login')
        label2.pack(side="top")
        frame3 = ttk.Frame(self.Login)
        frame3.configure(height=220, width=352)
        self.tlog = ttk.Button(frame3)
        self.img_tlogin = tk.PhotoImage(file=os.path.join(os.path.dirname(__file__), './static/tlogin.png'))
        self.tlog.configure(image=self.img_tlogin, text='Twitch Login')
        self.tlog.place(anchor="center", relx=0.5, rely=0.5, x=0, y=0)
        self.tlog.configure(command=self.tlogin)
        frame3.pack(side="top")
        frame3.pack_propagate(0)
        self.Tlog = ttk.Button(self.Login)
        self.Tlog.configure(text='Cancel')
        self.Tlog.place(anchor="se", x=344, y=280)
        self.Tlog.configure(command=self.canceltlog)

        # Main widget
        self.mainwindow = self.Login

    def run(self):
        self.mainwindow.mainloop()

    def tlogin(self):
        #if .key and .storage exist, then delete them 
        if os.path.isfile('./.key'):
            os.remove('./.key')
        if os.path.isfile('./.storage'):
            os.remove('./.storage')
        #run tlog.pyw, and wait for either .logsuccess or .logfail to be created
        tlog = subprocess.Popen(['python', 'tlog.pyw'])
        while not os.path.isfile('./.logsuccess') and not os.path.isfile('./.logfail'):
            time.sleep(1)
        #if .logsuccess exists, then close tlog.pyw and open main.pyw
        if os.path.isfile('./.logsuccess'):
            tlog.kill()
            os.remove('./.logsuccess')
            self.mainwindow.destroy()
            os.system('python main.py')
        #if .logfail exists, then close tlog.pyw and delete .logfail
        elif os.path.isfile('./.logfail'):
            tlog.kill()
            os.remove('./.logfail')
            tk.messagebox.showerror(title='Login Failed', message='Login failed, please try again in a few minutes.')
            self.mainwindow.destroy()
            os.system('python settings.py')




    def canceltlog(self):
        pass


if __name__ == "__main__":
    app = UiApp()
    app.run()
