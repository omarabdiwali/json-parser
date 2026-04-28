from time import time
from sys import argv

objectOpen = '{'
objectClose = '}'
listOpen = '['
listClose = ']'
quotes = '"'
content = ""

if len(argv) < 2:
    print("Usage: python main.py <json-file-path>")
    exit()

def parseString(content, index):
    parsed = ""
    passedChars = []
    index += 1
    if index >= len(content):
        return [parsed, index]
    
    while True:
        nextChar = content[index]
        if nextChar == quotes:
            if len(passedChars) == 0:
                break
            elif passedChars[-1] != "\\":
                break
            elif len(passedChars) > 1 and passedChars[-2] == "\\":
                break

        parsed += nextChar
        passedChars.append(nextChar)
        index += 1
        if index >= len(content):
            break
    
    return [parsed, index]

def parseNumber(content, index):
    parsed = ""
    breakChars = [',' , objectClose, listClose, ' ']
    while True:
        nextChar = content[index]
        if nextChar in breakChars:
            break
        else:
            parsed += nextChar
            index += 1
            if index >= len(content):
                break
    
    if index < len(content) and content[index] in [objectClose, listClose]:
        index -= 1
    
    try:
        return [int(parsed), index]
    except:
        return [float(parsed), index]

def parseBoolOrNull(content, index):
    values = { 'false': False, 'true': True, 'null': None }
    parsed = ""
    
    while True:
        nextChar = content[index]
        if nextChar == ",":
            break
        else:
            parsed += nextChar
            index += 1
            if index >= len(content) or parsed.lower() in values:
                break
    
    if content[index] != ',':
        index -= 1
    
    return [values[parsed.lower()], index] if parsed.lower() in values else ["ERROR", index]

def parseList(content, index):
    parsedList = []
    index += 1
    if index >= len(content):
        return [parsedList, index]
    
    while True:
        nextChar = content[index]
        parsed = None

        if nextChar == listClose:
            break
        elif nextChar == "," or nextChar == " ":
            index += 1
        else:
            if nextChar == quotes:
                parsed, index = parseString(content, index)
            elif nextChar.isdigit() or nextChar == "-":
                parsed, index = parseNumber(content, index)
            elif nextChar.lower() in ['f', 't', 'n']:
                parsed, index = parseBoolOrNull(content, index)
            elif nextChar == listOpen:
                parsed, index = parseList(content, index)
            elif nextChar == objectOpen:
                parsed, index = parseObject(content, index)
            else:
                parsed = 'UNKNOWN'

            parsedList.append(parsed)
            index += 1

        if index >= len(content):
            break
    
    return [parsedList, index]            

def parseObject(content, index):
    keys = []
    values = []
    ident = "key"
    index += 1

    while True:
        curChar = content[index]
        parsed = None

        if curChar == ":" or curChar == ",":
            index += 1
        elif curChar == " ":
            index += 1
        elif curChar == objectClose:
            break
        else:
            if curChar == quotes:
                parsed, index = parseString(content, index)
            elif curChar.isdigit() or curChar == "-":
                parsed, index = parseNumber(content, index)
            elif curChar.lower() in ['f', 't', 'n']:
                parsed, index = parseBoolOrNull(content, index)
            elif curChar == listOpen:
                parsed, index = parseList(content, index)
            elif curChar == objectOpen:
                parsed, index = parseObject(content, index)
            else:
                print("UNKNOWN-OBJ:", curChar, "index:", index)
                parsed = "UNKNOWN"
            
            if ident == "key":
                keys.append(parsed)
                ident = "value"
            else:
                values.append(parsed)
                ident = "key"
            
            index += 1
        
        if index >= len(content):
            break

    assert len(keys) == len(values), f"Key-Value lengths don't match: {keys} to {values}"
    
    obj = {}
    for i in range(len(keys)):
        obj[keys[i]] = values[i]
    
    return [obj, index]

start = time()

with open(argv[1], "r") as f:
    content = f.read()
    f.close()

content = content.replace("\r\n", "").replace("\n", "")
jsonParsed = None

if content[0] == objectOpen:
    jsonParsed, _ = parseObject(content, 0)
elif content[0] == listOpen:
    jsonParsed, _ = parseList(content, 0)
else:
    print("Invalid JSON: File has to begin with '{' or '['.")
    exit()

endTime = time()
print(jsonParsed)
print("\nParsing took", (endTime - start), "seconds.")