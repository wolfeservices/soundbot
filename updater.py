#this is a script to check if there is a new release of the bot and update it if there is
#https:/gihuib.com/wolfeservices/soundbot/releases/latest

#basic imports
import os

#test requirements
#zipfile is used to extract the archive
import zipfile
#requests
try:
    import requests
except ImportError:
    print('requests not installed, installing...')
    os.system('pip install requests')
    import requests


#the current version of the bot is stored in a file called version.txt

#release version is stored as a github tag, so we get the latest tag from the github api and compare it to the current version
#the api returns a json object, so we need to parse it, we only need the tag_name, so we get that

#parse the json object
def get_latest_release():
    url = 'https://api.github.com/repos/wolfeservices/soundbot/releases/latest'
    response = requests.get(url)
    json_data = response.json()
    return json_data['tag_name']    

#check if there is a new release
def check_for_update():
    local_version = open('version.txt', 'r').read()
    remote_version = get_latest_release()
    #strip the 'v.' from the version
    current_version = local_version[1:]
    latest_release = remote_version[1:]
    #split the version into an array
    current_version = current_version.split('.')
    latest_release = latest_release.split('.')
    #comare the versions major, minor and patch
    if current_version[0] < latest_release[0]:
        print('There is a new release, updating...')
        update()
    elif current_version[1] < latest_release[1]:
        print('There is a new release, updating...')
        update()
    elif current_version[2] < latest_release[2]:
        print('There is a new release, updating...')
        update()
    else:
        print('No new release')
        return False

#download the new release
def update():
    url = 'https://api.github.com/repos/wolfeservices/soundbot/releases/latest'
    response = requests.get(url)
    json_data = response.json()
    download_url = json_data['assets'][0]['browser_download_url'] #the download url is in the assets array, so we get the first item in the array
    print('Downloading new release...')
    r = requests.get(download_url, allow_redirects=True) #download the file from the url, allow_redirects is set to true so we can download the file from the github api
    open('soundbot.zip', 'wb').write(r.content) #write the file to disk as soundbot.zip
    print('Download complete, extracting...')
    zipfile.ZipFile('soundbot.zip').extractall() #extract the archive
    print('Extraction complete, deleting archive...')
    os.remove('soundbot.zip')
    print('Archive deleted, updating version.txt...')
    current_version = open('version.txt', 'w')
    current_version.write(get_latest_release())
    current_version.close()
    print('Update complete')
    return True


#
if __name__ == '__main__':
    check_for_update()

