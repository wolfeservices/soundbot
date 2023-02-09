#expect commandwrapper.py to be in the same directory as bot.py
#expect flag arguments

import os
import sys
import getopt
cogfile = 'cogs/commands.py'
emptycog = 'templates/emptycog.py'

def buildcog():
    #build cog
    with open('commandlist.txt', 'r') as com:
        os.remove(cogfile)
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
                lines.insert(index, "@commands.command()\n")
                index += 1
                lines.insert(index, "    async def " + command + "(self, ctx: commands.Context):\n")
                index += 1
                if responsefile == "none":
                    lines.insert(index, "        await ctx.send('" + response + "')\n")
                    index += 1
                elif response == "none":
                    lines.insert(index, "        self.player.play(ctx, '" + responsefile + "', volume=" + volume + ")\n")
                    index += 1
                else:
                    lines.insert(index, "        self.player.play(ctx, '" + responsefile + "', volume=" + volume + ")\n")
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
opts, args = getopt.getopt(sys.argv[1:], "AR:c:r:f:v:")
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

#set flags
for opt, arg in opts:
    if opt == "-A":
        add = True
    elif opt == "-R":
        remove = True
    elif opt == "-c":
        command = arg
    elif opt == "-r":
        response = arg
    elif opt == "-f":
        responsefile = arg
    elif opt == "-v":
        volume = arg

#check if arguments are valid
if add == remove:
    print("Must specify -A or -R")
    exit(1)
if command == "none":
    print("Must specify command")
    exit(1)
if response == "none" and responsefile == "none":
    print("Must specify response or responsefile")
    exit(1)
if responsefile != "none" and not os.path.exists(responsefile):
    print("Responsefile not found, must be in sounds directory")
    exit(1)

#check if commandlist.txt exists, if not create it comands will be stored in commandlist.txt in the format "command:response:responsefile:volume"
if not os.path.exists('commandlist.txt'):
    open('commandlist.txt', 'w').close()

commands = []
#read existing commands
with open('commandlist.txt', 'r') as f:
    for line in f:
        splitline = line.split(':')
        commands.append(splitline[0])

#add command
if add == True:
    if command in commands:
        print("Command already exists")
        exit(1)
    else:
        with open('commandlist.txt', 'a') as f:
            f.write(command + ':' + response + ':' + responsefile + ':' + volume + '/n')
        if buildcog() == 0:
            print("Command added")
            exit(0)
        else:
            print("Error")
            exit(1)

#remove command
elif remove == True:
    if command in commands:
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


