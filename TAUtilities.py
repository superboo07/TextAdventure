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

    for string in input:
        if (index == len(blocks)):
            if (string.__contains__(blocks[index - 1].seperatorStart)):
                offsetindex += 1
            elif (string.__contains__(blocks[index - 1].seperatorEnd)):
                if (offsetindex == 0): break
                else: offsetindex -= 1
            strings.append(string)
        else:
            if (string.__contains__(blocks[index].seperatorStart)):
                stringSplit = string.split(blocks[index].seperatorStart, 1)
                if (stringSplit[0].strip().lower() == blocks[index].name and offsetindex == 0):
                    if (len(stringSplit[1].strip()) > 0):
                        strings.append(stringSplit[1].strip())
                    index += 1
                else:
                    offsetindex += 1
            elif (string.__contains__(blocks[index].seperatorEnd)):
                if (offsetindex > 0): 
                    offsetindex -= 1

                else: index -= 1
    return strings

