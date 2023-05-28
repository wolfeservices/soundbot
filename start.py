import subprocess
import os

def check_for_updates():
    #run c4ud.py in a subprocess, and read the exit code
    subprocess.Popen(["python", "c4ud.py"])
    exit_code = 0
    if exit_code == 214:
        print('Update successful')
    elif exit_code == 0:
        print('No update available')
    elif exit_code == 1:
        print('Update failed')
    elif exit_code == 211:
        print('Dev version, not updating')
    else:
        print('Unknown exit code')

def main():
    check_for_updates()
    #run mainuiapp.py in a new window
    os.system('python main.py')

if __name__ == '__main__':
    main()


