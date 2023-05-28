import requests
import os
import pyunpack

#check for new version on the repo
#repo github.com/wolfeservices/soundbot
def check_for_updates():
    if os.path.exists('version.txt'):
        with open('version.txt', 'r') as f:
            version = f.read()
            #if the version file begins with DEV, then it is a dev version, and should not be updated
            if version.startswith('DEV'):
                print('Dev version, not updating')
                exit(211)
    else:
        version = 'v.0.0.0' #force update

    #strip v from version
    version = version[1:]

    r = requests.get('https://api.github.com/repos/wolfeservices/soundbot/releases/latest')
    if r.status_code == 200:
        #strip the v from the version
        latest_version = r.json()['tag_name'][1:]
        #break the versions into lists
        version = version.split('.')
        latest_version = latest_version.split('.')
        #compare the versions
        #store the url for soundbot.zip
        url = r.json()['assets'][0]['browser_download_url']
        if latest_version[0] > version[0]:
            print('New major version available, Updating automatically')
            update(url)
        elif latest_version[1] > version[1]:
            print('New minor version available, Updating automatically')
            update(url)
        elif latest_version[2] > version[2]:
            print('New patch version available, Updating automatically')
            update(url)
        else:
            print('No update available')
            exit(0)

def update(url):
    #download the zip
    r = requests.get(url)
    if r.status_code == 200:
        with open('soundbot.zip', 'wb') as f:
            f.write(r.content)
    #unzip the zip
    pyunpack.Archive('soundbot.zip').extractall('.')
    #delete the zip
    os.remove('soundbot.zip')
    #exit with code 214 to indicate that the update was successful
    exit(214)
    
