#expect commandwrapper.py to be in the same directory as bot.py
#expect flag arguments

import os
import sys

cogfile = 'cogs/commands.py'
emptycog = 'templates/emptycog.py'

def buildcog():
    #build cog
    with open('commandlist.txt', 'r') as com:
        #check if cog file exists, is so delete it
        if os.path.isfile(cogfile) == True:
            os.remove(cogfile)
        #copy empty cog to cog file
        with open(cogfile, 'w') as f:
            with open(emptycog, 'r') as e:
                f.write(e.read())
        #get index of ##COMMANDS##
        with open(cogfile, 'r') as f:
            lines = f.readlines()
            for i, line in enumerate(lines):
                if line == "##COMMANDS##\n":
                    index = i

        #insert commands
            for line in com:
                #break line into command, response, responsefile, volume
                command, response, responsefile, volume = line.split(':')
                #insert command into cog file at index, increment index
                lines.insert(index, "    @commands.command()\n")
                index += 1
                lines.insert(index, "    async def " + command + "(self, ctx: commands.Context):\n")
                index += 1
                if responsefile == "none":
                    lines.insert(index, "        await ctx.send('" + response + "')\n")
                    index += 1
                elif response == "none":
                    lines.insert(index, "        self.player.volume = " + volume + "\n")
                    index += 1
                    lines.insert(index, "        psound = sounds.Sound(source='" + responsefilePath + responsefile +"')\n")
                    index += 1
                    lines.insert(index, "        self.player.play(psound)\n")
                    index += 1
                else:
                    lines.insert(index, "        self.player.volume = " + volume + "\n")
                    index += 1
                    lines.insert(index, "        psound = sounds.Sound(source='" + responsefilePath + responsefile +"')\n")
                    index += 1
                    lines.insert(index, "        self.player.play(psound)\n")
                    index += 1
                    lines.insert(index, "        await ctx.send('" + response + "')\n")
                    index += 1
                lines.insert(index, "\n")
                index += 1
        #write cog file
        with open(cogfile, 'w') as f:
            for line in lines:
                f.write(line)
    return 0

if os.path.isdir('sounds') == False:
    os.mkdir('sounds')
responsefilePath = 'sounds/'


#get arguments

#opts is a list of tuples, each tuple is of the form (flag, argument)
#args is a list of arguments that are not flags

# AR = add/remove command REQUIRED
# c = command REQUIRED
# r = response OPTIONAL (default none)
# f = responsefile OPTIONAL (default none)
# v = volume OTIONAL (default 100) (0-100) (int) (if f is none, v is ignored)

#set defaults
add = False
remove = False
command = "none"
response = "none"
responsefile = "none"
volume = "100"

#set flags,
if len(sys.argv) > 1:
    args = sys.argv[1:]
    print(args)
    #check if -A or -R is present
    if '-A' in args:
        add = True
    elif '-R' in args:
        remove = True
    else:
        print("Must specify -A or -R")
        exit(1)
    #check if -c is present
    if '-c' in args:
        command = args[args.index('-c') + 1]
    else:
        print("Must specify command")
        exit(1)
    #check if -r is present
    if '-r' in args:
        response = args[args.index('-r') + 1]
    #check if -f is present
    if '-f' in args:
        responsefile = args[args.index('-f') + 1]
    #check if -v is present
    if '-v' in args:
        volume = args[args.index('-v') + 1]




#check if arguments are valid
if add == remove:
    print("Must specify -A or -R")
    exit(1)
if command == "none":
    print("Must specify command")
    exit(1)
#oly check the following if adding a command
if add == True:
    if responsefile != "none":
        if os.path.isfile(responsefilePath + responsefile) == False:
            print("Response file not found")
            exit(1)
        elif responsefile[-4:] != ".mp3":
            print("Response file must be an mp3")
            exit(1)
    if response == "none" and responsefile == "none":
        print("Must specify response or responsefile")
        exit(1)
    if int(volume) < 0 or int(volume) > 100:
        print("Volume must be between 0 and 100")
        exit(1)

#check if commandlist.txt exists, if not create it comands will be stored in commandlist.txt in the format "command:response:responsefile:volume"
if not os.path.exists('commandlist.txt'):
    open('commandlist.txt', 'w').close()

exist = []
#read existing commands
with open('commandlist.txt', 'r') as f:
    for line in f:
        splitline = line.split(':')
        exist.append(splitline[0])

#add command
if add == True:
    if command in exist:
        print("Command already exists")
        exit(1)
    else:
        with open('commandlist.txt', 'a') as f:
            f.write(command + ':' + response + ':' + responsefile + ':' + volume +'\n')
        if buildcog() == 0:
            print("Command added")
            exit(0)
        else:
            print("Error")
            exit(1)

#remove command
elif remove == True:
    if command in exist:
        with open('commandlist.txt', 'r') as f:
            lines = f.readlines()
        with open('commandlist.txt', 'w') as f:
            for line in lines:
                if line.split(':')[0] != command:
                    f.write(line)
        if buildcog() == 0:
            print("Command removed")
            exit(0)
        else:
            print("Error")
            exit(1)
    else:
        print("Command not found")
        exit(1)


