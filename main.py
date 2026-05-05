from time import time
from sys import argv
import re

objectOpen = '{'
objectClose = '}'
listOpen = '['
listClose = ']'
quotes = '"'
content = ""
breakPattern = re.compile(r'[,\s}\]]')

if len(argv) < 2:
    print("Usage: python main.py <json-file-path>")
    exit()

def parseString(content, index):
    lastChar = content[index]
    index += 1
    startIndex = index
    
    while index < len(content):
        char = content[index]
        if char == quotes and lastChar != "\\":
            break
        
        lastChar = char if lastChar != "\\" else None   
        index += 1
    
    parsed = content[startIndex:index]
    return tuple([parsed, index])

def parseNumber(content, index):
    breakMatch = breakPattern.search(content, index)
    lastIndex = len(content) if breakMatch is None else breakMatch.start()
    parsed = content[index:lastIndex]

    if lastIndex < len(content) and (content[lastIndex] == objectClose or content[lastIndex] == listClose):
        lastIndex -= 1
    
    try:
        return tuple([int(parsed), lastIndex])
    except:
        return tuple([float(parsed), lastIndex])

def parseBoolAndNull(content, index):
    values = { 'false': False, 'true': True, 'null': None }
    breakMatch = breakPattern.search(content, index)
    endIndex = len(content) if breakMatch is None else breakMatch.start()
    parsed = content[index:endIndex]
    
    if endIndex != len(content) and content[endIndex] != ',':
        endIndex -= 1
    
    translated = values.get(parsed, -1)
    if translated == -1:
        erMes = f"Invalid value while parsing bool/null value: End Index: {endIndex} - Total Substring: {content[index:endIndex]}"
        raise KeyError(erMes)
    
    return tuple([translated, endIndex])

def parseArray(content, index):
    parsedList = []
    index += 1
    
    while index < len(content):
        char = content[index]
        parsed = None

        if char == listClose:
            break
        elif char == "," or char == " ":
            index += 1
        else:
            if char == quotes:
                parsed, index = parseString(content, index)
            elif char.isdigit() or char == "-":
                parsed, index = parseNumber(content, index)
            elif char in set(['f', 't', 'n']):
                parsed, index = parseBoolAndNull(content, index)
            elif char == listOpen:
                parsed, index = parseArray(content, index)
            elif char == objectOpen:
                parsed, index = parseObject(content, index)
            else:
                erMes = f"Unknown character while parsing list: {char}. Index: {index} - Substring: {content[max(0, index-20):index+1]}"
                raise KeyError(erMes)

            parsedList.append(parsed)
            index += 1
    
    return tuple([parsedList, index])

def parseObject(content, index):
    obj = {}
    prevKey = None
    isKey = True
    index += 1

    while index < len(content):
        char = content[index]
        parsed = None

        if char == ":" or char == "," or char == " ":
            index += 1
        elif char == objectClose:
            break
        else:
            if char == quotes:
                parsed, index = parseString(content, index)
            elif char.isdigit() or char == "-":
                parsed, index = parseNumber(content, index)
            elif char in set(['f', 't', 'n']):
                parsed, index = parseBoolAndNull(content, index)
            elif char == listOpen:
                parsed, index = parseArray(content, index)
            elif char == objectOpen:
                parsed, index = parseObject(content, index)
            else:
                erMes = f"Unknown character while parsing obj: {char}. Index: {index} - Substring: {content[max(0, index-20):index+1]}"
                raise KeyError(erMes)
            
            if isKey:
                prevKey = parsed
            else:
                obj[prevKey] = parsed
                prevKey = None

            isKey = not isKey            
            index += 1

    assert isKey and None not in obj and prevKey == None, f"Key-Value lengths don't match. {obj}"
    return tuple([obj, index])

def parse(content):
    startChar = content[0]
    
    if startChar == '{':
        return parseObject(content, 0)[0]
    elif startChar == '[':
        return parseArray(content, 0)[0]
    elif startChar == 'f' or startChar == 't' or startChar == 'n':
        return parseBoolAndNull(content, 0)[0]
    elif startChar == '"':
        return parseString(content, 0)[0]
    elif startChar.isdigit() or startChar == '-':
        return parseNumber(content, 0)[0]
    else:
        raise KeyError("Invalid JSON file.")

def stringifyDict(obj):
    string = []
    string.append("{")
    for key, val in obj.items():
        string.append(f'"{key}":')
        valType = type(val)
        
        if valType == dict:
            string.append(stringifyDict(val))
        elif valType == list:
            string.append(stringifyList(val, 1))
        elif valType == str:
            string.append(f'"{val}"')
        elif valType == int or valType == float:
            string.append(f"{val}")
        elif val == None or valType == bool:
            replacement = { True: 'true', False: 'false', None: 'null' }
            string.append(f"{replacement[val]}")
        else:
            raise KeyError(f"Encountered unknown type: {valType} - Item: {val}")

        string.append(",")

    if string[-1] == ',':
        string.pop()
    
    string.append("}")
    return "".join(string)

def stringifyList(array, depth=0):
    string = []
    string.append("[")
    for val in array:
        valType = type(val)

        if valType == dict:
            string.append(stringifyDict(val))
        elif valType == list:
            string.append(stringifyList(val, depth + 1))
        elif valType == str:
            string.append(f'"{val}"')
        elif valType == int or valType == float:
            string.append(f"{val}")
        elif val == None or valType == bool:
            replacement = { True: 'true', False: 'false', None: 'null' }
            string.append(f"{replacement[val]}")
        else:
            raise KeyError(f"Encountered unknown type: {valType} - Item: {val}")

        if depth == 0:
            string.append("\n")
        string.append(",")
    
    if string[-1] == ',':
        string.pop()

    string.append(']')
    return "".join(string)

def stringify(json):
    jsonType = type(json)
    
    if jsonType == dict:
        return stringifyDict(json)
    elif jsonType == list:
        return stringifyList(json)
    elif jsonType == str:
        return f'"{json}"'
    elif jsonType == int or jsonType == float:
        return f"{json}"
    elif json == None or jsonType == bool:
        replacement = { True: 'true', False: 'false', None: 'null' }
        return f"{replacement[json]}"
    else:
        raise KeyError(f"Encountered unknown type: {jsonType} - Item: {json}")

start = time()

with open(argv[1], "r", encoding="utf-8") as f:
    content = f.read()
    f.close()

content = content.strip().replace("\n", "")
jsonParsed = parse(content)
duration = time() - start
print(jsonParsed)
print(f"\nParsing took {duration} seconds.")