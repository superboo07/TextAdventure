# Quick and dirty multiple choice thing. Acts kind of like an text adventure.
# You can modify or add rooms in the Game/ folder. The room you want the player to start in must be named 'StartingRoom.TA'
# Style Guide:
# def Example():
#   [List Globals first]
#   [List Defaults]
#
#   [Now do logic]

import os
import TAUtilities
from dataclasses import dataclass

# List all global variables here
global gameName
global gameInfoList
global worldItems
worldItems = dict()
debug = True

def openDoor(roomName, command: list):
    items = getAllItemsInRoom(roomName)
    itemsDictionary = dict()
    for item in items:
        itemsDictionary[item.name] = item
    if (len(command) > 1):
        if ( itemsDictionary.__contains__( command[1].strip() )):
            for description in itemsDictionary[ command[1].strip() ].descriptions["open "]: print(description)
            return True
        else: print("I don't know what you are trying to look at")
    else: print("I don't know what you are trying to open")
    return False

commands = {"open": openDoor}

@dataclass
class worldItem:
    name: str
    ID: str
    descriptions: dict
    type: str
    currentRoom: str

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
        if (aboutFileVar.__contains__(": ")):
            aboutFileVarSplit = aboutFileVar.split(": ")
            gameInfoList[aboutFileVarSplit[0].lower()] = aboutFileVarSplit[1]
    goToRoom(gameInfoList['startingroom'])
    
def goToRoom(roomName):
    items = list()

    os.system('cls||clear')
    os.system("title " + roomName)

    items = findItemsInRoomFile(roomName)
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
        if (len(commandSplit) > 1): 
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
        if (len(commandSplit) > 1):
            if (commandSplit[1].strip() == "around"):
                # look around
                directions = getRoomDirections(roomName, False)
                print("You can go:")

                for direction in directions: 
                    if (not direction.__contains__("!")): print(direction.capitalize())

                items = getAllItemsInRoom(roomName)

                if (len(items) > 0):
                    print("\nYou can look at:")

                    for item in worldItems: 
                        if (worldItems[item].currentRoom == roomName): print(worldItems[item].name.capitalize())
            else:
                # look [item]
                items = getAllItemsInRoom(roomName)
                itemsDictionary = dict()
                for item in items:
                    itemsDictionary[item.name] = item
                if ( itemsDictionary.__contains__( commandSplit[1].strip() )):
                    for description in itemsDictionary[ commandSplit[1].strip() ].descriptions["lookat "]: print(description)
                else: print("I don't know what you are trying to look at")
        else: print("I don't know what to look at")
        directionsLoop(roomName)
        return
    elif (commands.__contains__(commandSplit[0])):
        commands[commandSplit[0]](roomName, commandSplit)
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
    descriptionArray = TAUtilities.getBlock(
        [
            TAUtilities.block("description", '{', '}')
        ],
        roomFileArray
    )
    return descriptionArray

def getRoomDirections(roomName, excludeHideMarker):
    directionsArray = list()
    directionsList = dict()
    foundDirections = False

    roomFileArray = getRoomFileArray(roomName)
    directionsArray = TAUtilities.getBlock(
        [TAUtilities.block("directions", '{', '}')],
        roomFileArray
    )
    for direction in directionsArray:
        directionSplit = direction.split(": ")
        if (excludeHideMarker):
            directionSplit[0] = directionSplit[0].replace("!", "")
        directionsList[directionSplit[0].lower()] = directionSplit[1]

    return directionsList

def findItemsInRoomFile(roomName):
    debugPrint("Searching for items in " + roomName)
    itemClassList = list()
    multiDictVars = list()
    multiLineVars = dict()
    oneLineVars = dict()
    gameFileArray = getRoomFileArray(roomName)
    itemsList = TAUtilities.getBlock(
        [
            TAUtilities.block("items", '{', '}')
        ],
        gameFileArray
    )
    for item in itemsList:
        if (item.__contains__(" [")): 
            multiLineVars.clear()
            oneLineVars.clear()
            itemVars = getStringInbetween(itemsList, item.split(" [")[0].lower() + " ", '[', ']')
            for itemVar in itemVars:
                if (itemVar.__contains__(" |{")):
                    itemVarSplit = itemVar.split("|{")
                    multiDictVars = getStringInbetween(itemVars, itemVarSplit[0].lower(), '|{', '}|')
                    for description in multiDictVars:
                        if ( description.__contains__(" {") ):
                            dictVarSplit = description.split("{")
                            if (multiLineVars.__contains__(itemVarSplit[0].lower())):
                                multiLineVars[itemVarSplit[0].lower()][dictVarSplit[0].lower()] = getStringInbetween(multiDictVars, dictVarSplit[0].lower(), '{', '}')
                            else: multiLineVars[itemVarSplit[0].lower()] = { dictVarSplit[0].lower(): getStringInbetween(multiDictVars, dictVarSplit[0].lower(), '{', '}') }

                elif (itemVar.__contains__(" <{")):
                    itemVarSplit = itemVar.split("<{")
                    multiDictVars = getStringInbetween(itemVars, itemVarSplit[0].lower(), '<{', '}>')
                    for description in multiDictVars:
                        if ( description.__contains__(": ") ):
                            dictVarSplit = description.split(": ")
                            multiLineVars[itemVarSplit[0].lower()] = { dictVarSplit[0].lower(): dictVarSplit[1] }
                
                elif (itemVar.__contains__(": ")):
                    itemVarSplit = itemVar.split(": ")
                    oneLineVars[itemVarSplit[0].lower()] = itemVarSplit[1]
            if (multiLineVars.__contains__("description ") and oneLineVars.__contains__("id")):
                itemClass = worldItem(item.split(" [")[0].lower(), oneLineVars["id"], multiLineVars["description "], 'scenery', roomName)
                itemClassList.append(itemClass)
                debugPrint("Found " + item.split(" [")[0] + "[" + oneLineVars["id"] + "]")
            else:
                if (not multiLineVars.__contains__("description ")):
                    debugPrint("Item " + item.split(" [")[0] + " is missing it's description")
                if (not oneLineVars.__contains__('id')):
                    debugPrint("Item " + item.split(" [")[0] + " is missing it's id")
    return itemClassList

def getAllItemsInRoom(roomName):
    items = list()
    for item in worldItems:
        if ( worldItems[item].currentRoom == roomName ): items.append(worldItems[item])
    return items


def loadItem(item):
    global worldItems

    if (worldItems.__contains__(item.ID) ): 
        debugPrint("Tried to load already loaded item: " + item.name + "[" + item.ID + "]")
        return False
    else: 
        worldItems[item.ID] = item
        debugPrint("Succesfully loaded item: " + item.name + "[" + item.ID + "]")
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