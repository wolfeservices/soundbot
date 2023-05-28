Wolfe Soundbot
==============
This is a simple bot that plays sounds in response to commands in a Twitch chat. It is written in Python and uses the [TwitchIO](https://twitchio.dev/en/latest/index.html) library.

Features
--------
- twitch API integration, this version does not handle any Affiliate or Partner only features yet. (#TODO add support for these features)
- plays sounds in response to commands in chat (e.g. !sound)
- queue sounds to play in order, for large volumes of usage (#TODO)
- GUI for managing the bot, including on-the-fly reloading of sounds and commands (#IN PROGRESS)
- chat logging (#TODO, simple logging is implemented but not saved to file yet)
- soundboard mode, where sounds can be played by clicking on buttons in the GUI (#TODO)

Installation
------------
1. Install Python 3.8 or higher
2. run setup.bat (or setup.sh on Linux) to configure the virtual environment and install dependencies
     - the script will prompt you for how you want to start the bot, either by a desktop shortcut or by run.py
3. run the bot using the shortcut or run.py
4. the first time you run the bot, it will request access to your Twitch account. If you want to have the bot use a different Twitch name, you can create a new Twitch account and log in with that instead.

Configuration
-------------
At the moment, the bot is configured by editing the config.py file. This will be replaced with a GUI in the future. here is an example of the config file:
`#config.py`
```python
#Bot Nickname (the name of the bot account), this MUST be the same as the account you logged in with
BOT_NICK = "wolfe_soundbot"
#prefix for commands, e.g. !sound
COMMAND_PREFIX = "!"
#twitch channel to join
CHANNEL = "GreatestWolfe"
```

Adding Sounds and Commands
--------------------------
at the moment you must manually add sounds and commands to the bot. This will be replaced with a GUI in the future. To add a sound, place the sound file in the sounds folder, and add a line to the commands.txt file in the format `command_name:Text Response:sound_name:vol`. For example, if you wanted to add a command called `!sound` that plays the sound `sound.mp3` at 50% volume, you would add the following line to commands.txt:
`#commands.txt`
```text
sound:Playing sound:sound.mp3:50
```
The text response is what the bot will say in chat when the command is used. The sound name is the name of the sound file in the sounds folder. Volume is a number between 0 and 100, where 0 is silent and 100 is full volume. The volume is optional, and if it is not specified, the bot will use the default volume of 50.

To add a command that does not play a sound, you would put null in the sound name field, like this:
`#commands.txt`
```text
hello:Hello, world!:null
```

__NOTE:__ the commands.txt file is parsed when the bot starts, so if you add a new command, you will need to restart the bot for it to take effect. Once the GUI is implemented, this will no longer be necessary.

for more information on how to use the bot, I will be adding a wiki soon.

Contributing
------------
While I would enjoy collaborating, I am not currently accepting pull requests. If you have a suggestion or bug report, please open an issue on the GitHub page. If you would like to contribute to the code, please contact me on Discord (GlassesWolfe#4599) and we can discuss it.

License
-------
This project is licensed under the MIT license. See the LICENSE file for more information.

Credits
-------
- [TwitchIO](https://twitchio.dev/en/latest/index.html) - the library used to connect to Twitch

