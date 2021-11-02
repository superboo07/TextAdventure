# Quick and dirty multiple choice thing. Acts kind of like an text adventure.
# You can modify or add rooms in the Game/ folder. The room you want the player to start in must be named 'StartingRoom.TA'
# Style Guide:
# def Example():
#   [List Globals first]
#   [List Defaults]
#
#   [Now do logic]

import os

from dataclasses import dataclass

# List all global variables here
global gameName
global gameInfoList
global worldItems
worldItems = dict()
debug = False

@dataclass
class worldItem:
    description: list
    currentRoom: str
    id: str
    name: str

def debugPrint(string):
    if (debug):
        print("Debug: ", string)

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
            startGame()
            foundGame = True
        else:
            print("Please choose a valid game")

def startGame():
    global gameInfoList
    gameInfoList = dict()

    with open('Games/' + gameName + "/GameInfo.TA") as aboutFile: aboutFileArray = [aboutFileLine.strip() for aboutFileLine in aboutFile]
    for aboutFileVar in aboutFileArray:
        aboutFileVarSplit = aboutFileVar.split(": ")
        gameInfoList[aboutFileVarSplit[0].lower()] = aboutFileVarSplit[1]
    goToRoom(gameInfoList['startingroom'])
    
def goToRoom(roomName):
    items = list()

    os.system('cls||clear')
    os.system("title " + roomName)

    items = getItemsInRoom(roomName)
    for item in items:
        loadItem(item)
    descriptions = getRoomDescription(roomName)
    for description in descriptions: print(description)
    directionsLoop(roomName)
    return

def directionsLoop(roomName):
    commandSplit = list()

    command = input("> ").lower()
    
    commandSplit = command.split(" ", 1)

    if (commandSplit[0] == "go"):
        # Check if the commandSplit array has more then one string in it, if it doesn't the next if statements would error out.
        if (commandSplit.__len__() > 1): 
            directions = getRoomDirections(roomName, True)
            if (directions.__contains__(commandSplit[1])):
                nextRoom = directions.get(commandSplit[1])
                goToRoom(nextRoom)
                return
        print("I don't understand where you are trying to go. For a list of directions type 'look around' into the terminal.")
        directionsLoop(roomName)
    elif (commandSplit[0] == "help"):
        print("In order to move around you must type 'Go [Direction]'.\nif you need the list of directions you can go to, type 'look around' into the terminal.\nIf you wish to exit the program then type 'Exit' into the terminal." )
        directionsLoop(roomName)
        return
    elif (commandSplit[0] == "look"):
        if (commandSplit.__len__() > 1):
            if (commandSplit[1].strip() == "around"):
                directions = getRoomDirections(roomName, False)
                print("You can go:")
                for direction in directions: 
                    if (not direction.__contains__("!")): print(direction.capitalize())
            else:
                items = dict()
                for itemID in worldItems:
                    itemName = worldItems[itemID].name
                    items[itemName] = itemID
                if items.__contains__(commandSplit[1].strip()):
                    for description in worldItems.get(items.get(commandSplit[1].strip())).description: print(description)
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
    with open('Games/' + gameName + "/Rooms/" + roomName + '.TA') as gameFile: roomFileArray = [roomFileLine.strip() for roomFileLine in gameFile]
    return roomFileArray
    
def getRoomDescription(roomName):
    descriptionArray = []
    foundDescription = False

    roomFileArray = getRoomFileArray(roomName)
    descriptionArray = getStringInbetween(roomFileArray, 'description ', '{', '}')
    return descriptionArray

def getRoomDirections(roomName, excludeHideMarker):
    directionsArray = list()
    directionsList = dict()
    foundDirections = False

    roomFileArray = getRoomFileArray(roomName)
    directionsArray = getStringInbetween(roomFileArray, 'directions ', '{', '}')
    for direction in directionsArray:
        directionSplit = direction.split(": ")
        if (excludeHideMarker):
            directionSplit[0] = directionSplit[0].replace("!", "")
        directionsList[directionSplit[0].lower()] = directionSplit[1]

    return directionsList

def getItemsInRoom(roomName):
    itemClassList = list()

    gameFileArray = getRoomFileArray(roomName)
    itemsList = getStringInbetween(gameFileArray, 'items ', ':{', '}:')
    for item in itemsList:
        if (item.__contains__(" [")): 
            # Ensure variables aren't already filled so the interpter ALWAYS errors out if the user forgets to input them
            description = None
            ID = None
            # del id
            # del description
            itemVars = getStringInbetween(itemsList, item.split(" [")[0].lower() + " ", '[', ']')
            for itemVar in itemVars:
                if (itemVar.__contains__(" {")):
                    itemVarSplit = itemVar.split(" {")
                    if (itemVarSplit[0].lower() == "description"): 
                        description = getStringInbetween(itemVars, "description ", '{', '}')
                elif (itemVar.__contains__(": ")):
                    itemVarSplit = itemVar.split(": ")
                    if (itemVarSplit[0].lower() == "id"): 
                        ID = itemVarSplit[1]
            if (description != None and ID != None):
                itemClass = worldItem(description, roomName, ID, item.split(" [")[0].lower())
                itemClassList.append(itemClass)
                debugPrint("Found " + item.split(" [")[0] + "[" + ID + "]")
            else:
                if (description == None):
                    debugPrint("Item " + item.split(" [")[0] + " is missing it's description")
                if (ID == None):
                    debugPrint("Item " + item.split(" [")[0] + " is missing it's id")
    return itemClassList


def loadItem(item):
    global worldItems

    if (worldItems.__contains__(item.id) ): 
        debugPrint("Tried to load already loaded item: " + item.name)
        return False
    else: worldItems[item.id] = item
    return True

def getStringInbetween(stringArray, name, start, end):
    outputArray = list()
    index = -1
    savedIndex = 0
    foundName = False
    foundValidVariable = False

    for string in stringArray:
        index += 1
        if (foundName == False):
            foundValidVariable = False
            foundEndOfBlock = False
            stringSplit = string.split(start)
            if (stringSplit[0].lower() == name):
                if (index > 0):
                    savedIndex = index
                    # Make sure this block isn't in another block
                    while (foundValidVariable == False):
                        savedIndex -= 1
                        if ( stringArray[savedIndex].strip().__len__() > 0):
                            # Check for start of block
                            if (stringArray[savedIndex].__contains__(end)): foundEndOfBlock=True
                            if ( stringArray[savedIndex].__contains__(start) ): 
                                if (foundEndOfBlock): foundEndOfBlock = False
                                else: break
                            # If it has reached this point without breaking it should mean the block isn't embedded in another block
                            if (savedIndex == 0): foundValidVariable = True
                else: foundValidVariable = True

                if (foundValidVariable == True):
                    foundName = True
                    if (stringSplit[1].__len__() > 0): outputArray.append(stringSplit[1])
        else:
            if (not string.__contains__(end)):
                outputArray.append(string)
            else: 
                foundName = False
                stringSplit = string.split(end)
                if (stringSplit[0].__len__() > 0): outputArray.append(stringSplit[0])
    return outputArray

main()