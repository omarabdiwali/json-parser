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
    lastIndex = len(content) if breakMatch is None else breakMatch.start()
    parsed = content[index:lastIndex].lower()
    
    if lastIndex != len(content) and content[lastIndex] != ',':
        lastIndex -= 1
    
    return tuple([values[parsed], lastIndex]) if parsed in values else tuple(["ERROR", lastIndex])

def parseList(content, index):
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
            elif char.lower() in ['f', 't', 'n']:
                parsed, index = parseBoolAndNull(content, index)
            elif char == listOpen:
                parsed, index = parseList(content, index)
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
    ident = "key"
    index += 1

    while index < len(content):
        char = content[index]
        parsed = None

        if char == ":" or char == ",":
            index += 1
        elif char == " ":
            index += 1
        elif char == objectClose:
            break
        else:
            if char == quotes:
                parsed, index = parseString(content, index)
            elif char.isdigit() or char == "-":
                parsed, index = parseNumber(content, index)
            elif char.lower() in set(['f', 't', 'n']):
                parsed, index = parseBoolAndNull(content, index)
            elif char == listOpen:
                parsed, index = parseList(content, index)
            elif char == objectOpen:
                parsed, index = parseObject(content, index)
            else:
                erMes = f"Unknown character while parsing obj: {char}. Index: {index} - Substring: {content[max(0, index-20):index+1]}"
                raise KeyError(erMes)
            
            if ident == "key":
                prevKey = parsed
                ident = "value"
            else:
                obj[prevKey] = parsed
                prevKey = None
                ident = "key"
            
            index += 1

    assert None not in obj and prevKey == None, f"Key-Value lengths don't match. {obj}"
    return tuple([obj, index])

start = time()

with open(argv[1], "r", encoding="utf-8") as f:
    content = f.read()
    f.close()

content = content.strip().replace("\n", "")
jsonParsed = None

if content[0] == objectOpen:
    jsonParsed, _ = parseObject(content, 0)
elif content[0] == listOpen:
    jsonParsed, _ = parseList(content, 0)
else:
    print("Invalid JSON: File has to begin with '{' or '['.")
    exit()

duration = time() - start
print(jsonParsed)
print(f"\nParsing took {duration} seconds.")