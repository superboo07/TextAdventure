# Quick and dirty multiple choice thing. Acts kind of like an text adventure.
# You can modify or add rooms in the Game/ folder. The room you want the player to start in must be named 'StartingRoom.TA'
# Style Guide:
# def Example():
#   [List Globals first]
#   [List Defaults]
#
#   [Now do logic]


import os

# List all global variables here
global gameName

def main():
    global gameName
    foundGame = False

    games = os.listdir('Games/')
    print("Please choose a game from the list below: ")
    for game in games:
        print(game)
    while ( not foundGame ):
        gameName = input("> ")
        if (games.__contains__(gameName)): 
            goToRoom('StartingRoom')
            foundGame = True
        else:
            print("Please choose a valid game")

    
def goToRoom(roomName):
    os.system('cls||clear')
    os.system("title " + roomName)
    descriptions = getRoomDescription(roomName)
    for description in descriptions: print(description)
    directionsLoop(roomName)
    return

def directionsLoop(roomName):
    directions = getRoomDirections(roomName, False)
    command = input("> ").lower()

    commandSplit = []
    
    commandSplit = command.split(" ", 1)

    if (commandSplit[0] == "go"):
        # Check if the commandSplit array has more then one string in it, if it doesn't the next if statements would error out.
        if (commandSplit.__len__() > 1): 
            directions = getRoomDirections(roomName, True)
            if (directions.__contains__(commandSplit[1])):
                nextRoom = directions.get(commandSplit[1])
                goToRoom(nextRoom)
                return
        print("I don't understand where you are trying to go. For a list of directions type 'look' into the terminal.")
        directionsLoop(roomName)
    elif (commandSplit[0] == "help"):
        print("In order to move around you must type 'Go [Direction]'.\nif you need the list of directions you can go to, type 'look' into the terminal.\nIf you wish to exit the program then type 'Exit' into the terminal." )
        directionsLoop(roomName)
        return
    elif (commandSplit[0] == "look"):
        if (commandSplit.__len__() > 1):
            if (commandSplit[1].strip() == "around"):
                print("You can go:")
                for direction in directions: 
                    if (not direction.__contains__("!")): print(direction.capitalize())
            else: print("I don't know what you are trying to look at")
        else: print("I don't know what to look at")
        directionsLoop(roomName)
        return
    elif (commandSplit[0] == "exit"):
        exit()    
    print("I don't understand what you are trying to do. If you need help type 'help' into the terminal.")
    directionsLoop(roomName)
    return

# Function for embedding variables into a string
# This function is based on an function I wrote in C++.
def customString(string, stringVariables: list):
    for key in stringVariables.keys(): string = string.replace(str("^" + key), stringVariables.get(key))
    return string

# Opens the file with the name of the room and splits it up into an array
def getRoomFileArray(roomName):
    with open('Games/' + gameName + "/" + roomName + '.TA') as gameFile: roomFileArray = [roomFileLine.strip() for roomFileLine in gameFile]
    return roomFileArray
    
def getRoomDescription(roomName):
    roomFileArray = getRoomFileArray(roomName)
    descriptionArray = []
    foundDiscription = False
    for roomVar in roomFileArray:
        if (foundDiscription == False):
            roomVarSplit = roomVar.split("{")
            if (roomVarSplit[0].lower() == 'description '): 
                foundDiscription = True 
                if (roomVarSplit[1].__len__() > 0): descriptionArray.append(roomVarSplit[1])
        else:
            if (not roomVar.__contains__("}")):
                descriptionArray.append(roomVar)
            else: 
                foundDiscription = False
                roomVarSplit = roomVar.split("}")
                if (roomVarSplit[0].__len__() > 0): descriptionArray.append(roomVarSplit[0])
    return descriptionArray

def getRoomDirections(roomName, excludeHideMarker):
    roomFileArray = getRoomFileArray(roomName)
    foundDirections = False
    # There must be something in the list for it to allow adding to the list.
    directionsList = {"": ''}
    for roomVar in roomFileArray:
        if (foundDirections == False):
            roomVarSplit = roomVar.split("{")
            if (roomVarSplit[0].lower() == 'directions '): foundDirections = True
        else:
            roomVarSplit = roomVar.split(": ")
            # Make sure this line doesn't contain an }, this will technically flag all directions
            # with one in their name, but that won't matter since this symbol shouldn't even be put in one.
            if (not roomVarSplit[0].__contains__("}")):
                # Try adding the direction to the list, this method should no longer fail. Though I still have exception handling just in case.
                try: 
                    if (excludeHideMarker):
                        roomVarSplit[0] = roomVarSplit[0].replace("!", "")
                    directionsList[roomVarSplit[0].lower()] = roomVarSplit[1]
                except: print("Tried to add invalid command to directions list")
            else: foundDirections = False
    return directionsList

main()