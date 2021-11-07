from dataclasses import dataclass

@dataclass
class block:
    name: str
    seperatorStart: str
    seperatorEnd: str

def getBlock(blocks: list, input: list):
    strings = list()
    index = 0
    offsetindex = 0
    foundBlock = False
    dontAppend = False

    for string in input:
        dontAppend = False
        if (foundBlock and blocks[index].name == "*"):
            if (type(strings) == list): strings = dict()

            if (string.__contains__(blocks[index].seperatorStart)):
                if (offsetindex == 0): 
                    foundBlockName = string.split(blocks[index].seperatorStart)[0].strip()
                    dontAppend = True
                offsetindex += 1
            elif (string.__contains__(blocks[index].seperatorEnd)):
                if (offsetindex == 0): break
                else: offsetindex -= 1

            if (dontAppend == False and offsetindex > 0):
                if (strings.__contains__(foundBlockName)): 
                    strings[foundBlockName].append(string)
                else: 
                    strings[foundBlockName] = [string]

        elif (foundBlock == True):
            if (string.__contains__(blocks[index].seperatorStart)):
                offsetindex += 1
            elif (string.__contains__(blocks[index].seperatorEnd)):
                if (offsetindex == 0): break
                else: offsetindex -= 1
            strings.append(string)
        else:
            if (string.__contains__(blocks[index].seperatorStart)):
                stringSplit = string.split(blocks[index].seperatorStart, 1)
                if (stringSplit[0].strip().lower() == blocks[index].name.lower().strip() and offsetindex == 0):
                    if (len(stringSplit[1].strip()) > 0):
                        strings.append(stringSplit[1].strip())
                    if (index + 1 <= len(blocks) - 1 ): index += 1
                    if (index == len(blocks) - 1): foundBlock = True
                else:
                    offsetindex += 1
            elif (string.__contains__(blocks[index].seperatorEnd)):
                if (offsetindex > 0): 
                    offsetindex -= 1

                else: index -= 1
    return strings

def getVariable(name: str, blocks: list, seperator: str, input: list):
    if (len(blocks) > 0): block = getBlock(blocks, input)
    else: block = input
    if (name == "*"):
        output = dict()
        for string in block:
            if (string.__contains__(seperator)):
                stringSplit = [ stringSplit.strip() for stringSplit in string.split(seperator)]
                output[stringSplit[0].lower()] = stringSplit[1]
    else: 
        for string in block:
            if (string.__contains__(seperator)):
                stringSplit = [ stringSplit.strip() for stringSplit in string.split(seperator)]
                if (stringSplit[0].lower() == name.lower()): 
                    output = stringSplit[1]
                    break
    
    return output