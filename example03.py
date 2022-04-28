#!/bin/python3

# Game: Jump over the obstacles

import brlapi
import errno
#import Xlib.keysymdef.miscellany
import time

# Helper functions to print debug information to the log

def printProperty (name, value):
    print(name + ": " + value)

def printDiagnostics(brl):
    printProperty("File Descriptor", str(brl.fileDescriptor))
    printProperty("Server Host", str(brl.host))
    printProperty("Authorization Schemes", str(brl.auth))
    printProperty("Driver Name", str(brl.driverName))
    printProperty("Model Identifier", str(brl.modelIdentifier))
    printProperty("Display Width", str(brl.displaySize[0]))
    printProperty("Display Height", str(brl.displaySize[1]))
    printProperty(".......", '.........................')

def printLog(m):
    if m['counter'] == 0:
        printProperty("LOG", 'Program Initialized')
        printProperty("Counter", str(m['counter']))
        printProperty("Message", m['message'])
    else:
        printProperty("LOG", 'Program Started')
        if "code" in m:
            printProperty("Code", str(m["code"]))
            printProperty("Type", str(m["type"]))
            printProperty("Command", str(m["command"]))
            printProperty("Argument", str(m["argument"]))
            printProperty("Flags", str(m["flags"]))
            printProperty("Counter", str(m['counter']))
        printProperty("Message", m['message'])
        printProperty("Text", m['text'])

        printProperty("Cursor Position", str(m['cursorPos']))
        printProperty("Obstacle Posistion", str(m['obstaclePos']))
        printProperty("Points", str(m['points']))

    printProperty("-------", '-------------------------')

# Initialize the model.
# This should define all possible states.
def init():
    return {
        'counter': 0,
        'text': '',
        'message': "Press the spacebar to start",
        'cursorPos': 0, # 0..3
        'obstaclePos': 9, # 0..4
        'points': 0 # 0..999
    }

def helper(m):
    # fullCell = brlapi.DOT1 | brlapi.DOT2 | brlapi.DOT3 | brlapi.DOT4 | brlapi.DOT5 | brlapi.DOT6 | brlapi.DOT7 | brlapi.DOT8
    cells = []

    # Calculated cursor dots    
    cursorDots = 0
    if m['cursorPos'] == 0:
        cursorDots = brlapi.DOT7 | brlapi.DOT8
    elif m['cursorPos'] == 1:
        cursorDots = brlapi.DOT3 | brlapi.DOT6
    elif m['cursorPos'] == 2:
        cursorDots = brlapi.DOT2 | brlapi.DOT5
    elif m['cursorPos'] == 3:
        cursorDots = brlapi.DOT1 | brlapi.DOT4

    cursorObstacleColition = (m['cursorPos'] in [0, 1]) and (m['obstaclePos'] in [2, 3, 4])

    # Calculate moving obstacles
    # for cells in range(0, 30)
    for i in range(0, 6):
        cell00 = 0
        cell01 = 0
        cell02 = 0
        cell03 = 0
        cell04 = 0
        
        if i == 0:
            cell01 = cursorDots
        
        if m['obstaclePos'] == 0:
            cell00 = brlapi.DOT3 | brlapi.DOT7
            cell04 = brlapi.DOT6 | brlapi.DOT8
        elif m['obstaclePos'] == 1:
            cell00 = brlapi.DOT3 | brlapi.DOT7 | brlapi.DOT6 | brlapi.DOT8
        elif m['obstaclePos'] == 2:
            cell00 = brlapi.DOT6 | brlapi.DOT8
            cell01 = cell01 | brlapi.DOT3 | brlapi.DOT7
        elif m['obstaclePos'] == 3:
            cell01 = cell01 | brlapi.DOT3 | brlapi.DOT7 | brlapi.DOT6 | brlapi.DOT8
        elif m['obstaclePos'] == 4:
            cell01 = cell01 | brlapi.DOT6 | brlapi.DOT8
            cell02 = brlapi.DOT3 | brlapi.DOT7
        elif m['obstaclePos'] == 5:
            cell02 = brlapi.DOT3 | brlapi.DOT7 | brlapi.DOT6 | brlapi.DOT8
        elif m['obstaclePos'] == 6:
            cell02 = brlapi.DOT6 | brlapi.DOT8
            cell03 = brlapi.DOT3 | brlapi.DOT7
        elif m['obstaclePos'] == 7:
            cell03 = brlapi.DOT3 | brlapi.DOT7 | brlapi.DOT6 | brlapi.DOT8
        elif m['obstaclePos'] == 8:
            cell03 = brlapi.DOT6 | brlapi.DOT8
            cell04 = brlapi.DOT3 | brlapi.DOT7
        elif m['obstaclePos'] == 9:
            cell04 = brlapi.DOT3 | brlapi.DOT7 | brlapi.DOT6 | brlapi.DOT8

        if (i == 0) and cursorObstacleColition:
            if (m['counter'] % 2 == 0):
                cell00 = brlapi.DOT1 | brlapi.DOT3 | brlapi.DOT5 | brlapi.DOT8
            else:            
                cell00 = brlapi.DOT2 | brlapi.DOT7 | brlapi.DOT4 | brlapi.DOT6
            cell01 = cell00
            cell02 = cell00
            cell03 = cell00
            cell04 = cell00

        # Display moving obstacles and player in position 1 
        cells.append(cell00)
        cells.append(cell01)
        cells.append(cell02)
        cells.append(cell03)
        cells.append(cell04)

    # Display score
    # for cells in range(30, 40): 
    cells.append(brlapi.DOT1 | brlapi.DOT2 | brlapi.DOT3 | brlapi.DOT4) # p
    cells.append(brlapi.DOT1 | brlapi.DOT3 | brlapi.DOT5 ) # o
    cells.append(brlapi.DOT2 | brlapi.DOT4) # i
    cells.append(brlapi.DOT1 | brlapi.DOT3 | brlapi.DOT4 | brlapi.DOT5) # n
    cells.append(brlapi.DOT2 | brlapi.DOT3 | brlapi.DOT4 | brlapi.DOT5) # t
    cells.append(brlapi.DOT2 | brlapi.DOT3 | brlapi.DOT4) # s
    cells.append(brlapi.DOT2 | brlapi.DOT5) # :
    cells.append(brlapi.DOT1 | brlapi.DOT2 | brlapi.DOT3 | brlapi.DOT6) # 0
    cells.append(brlapi.DOT1 | brlapi.DOT2 | brlapi.DOT3 | brlapi.DOT6) # 0
    cells.append(brlapi.DOT1 | brlapi.DOT2 | brlapi.DOT3 | brlapi.DOT6) # 0
    
    print(str(cells))

    return bytes(cells)

# Visualize the model on the braille displan
def view(brl, m):
    printLog(m)
    if m['counter'] == 0:
        brl.writeText(m['message'])
    else:
        brl.writeDots(helper(m))

def cursorUp(position):
    # Legal positions: 0..3, blocked
    if position > 2:
        position = 2
    if position < 0:
        position = 0
    return position + 1

def cursorDown(position):
    # Legal positions: 0..3, blocked
    if position > 3:
        position = 3
    if position < 1:
        position = 1
    return position - 1

def obstacleAdvance(position):
    # Legal positions: 0..9, revolving
    if position > 9:
        position = 9
    if position <= 0:
        position = 10
    return position - 1

# Update the model based because time passed
def updateByTime(m):
    m['counter'] = m['counter'] + 1
    if m['counter'] % 2 == 0:
        m['obstaclePos'] = obstacleAdvance(m['obstaclePos'])
    return m

# Update the model based based on the key pressed
def updateByKey(brl, m, keyCode):
    # Keep information about the key pressed in the model
    k = brl.expandKeyCode(keyCode)
    m["code"] = "0X%X" % keyCode
    m["type"] = k["type"]
    m["command"] = k["command"]
    m["argument"] = k["argument"]
    m["flags"] = k["flags"]

    if m["type"] == 0:
        m["text"] = m["text"] + chr(m['argument'])

    # Update the model
    m['counter'] = m['counter'] + 1
    if keyCode == brlapi.KEY_TYPE_CMD|brlapi.KEY_CMD_HOME:
        m['message'] = "Home Button"
    elif keyCode == brlapi.KEY_TYPE_CMD|brlapi.KEY_CMD_LNUP:
        m['message'] = "Line Up"
        m['cursorPos'] = cursorUp(m['cursorPos'])
    elif keyCode == brlapi.KEY_TYPE_CMD|brlapi.KEY_CMD_LNDN:
        m['message'] = "Line Down"
        m['cursorPos'] = cursorDown(m['cursorPos'])
    return m

try:
    # Initialization
    b = brlapi.Connection()
    printDiagnostics(b)
    b.enterTtyModeWithPath()
    b.acceptKeys(brlapi.rangeType_all,[0])

    # The architecture
    model = init()
    view(b, model)
    key = b.readKey(1)
    while model['counter'] < 200:
        view(b, model)
        
        key = b.readKey(0)
        if not key:
            time.sleep(0.2)            
            model = updateByTime(model)
        else:
            model = updateByKey(b, model, key)

    b.leaveTtyMode()
    b.closeConnection()

# Error Handling
except brlapi.ConnectionError as e:
    if e.brlerrno == brlapi.ERROR_CONNREFUSED:
        print("Connection to %s refused. BRLTTY is too busy..." %(e.host))
    elif e.brlerrno == brlapi.ERROR_AUTHENTICATION:
        print("Authentication with %s failed. Please check the permissions of %s" %(e.host,e.auth))
    elif e.brlerrno == brlapi.ERROR_LIBCERR and (e.libcerrno == errno.ECONNREFUSED or e.libcerrno == errno.ENOENT):
        print("Connection to %s failed. Is BRLTTY really running?" %(e.host))
    else:
        print("Connection to BRLTTY at %s failed: " %(e.host))
    print(e)
    print(e.brlerrno)
    print(e.libcerrno)
