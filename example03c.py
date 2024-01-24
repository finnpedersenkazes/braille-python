#!/bin/python3

# Game: Jump over the obstacles

import brlapi
import errno
import time
import datetime
import louis


def formatTimeStamp(dateTime):
    return dateTime.isoformat()[:16].replace(":", "-")


# Global values

currentDateTime = datetime.datetime.now()
logFileName = "/home/pi/Documents/"
logFileName = logFileName + formatTimeStamp(currentDateTime) + "_log.txt"

# Helper functions to print debug information to the log


def printProperty(name, value):
    text = name + ": " + value
    print(text)
    f = open(logFileName, "a")
    f.write(text)
    f.write("\n")
    f.close()


def adjustNumber(n):
    return n - 32768  # = 2^15


def translationList():
    return [b"fr-bfu-comp6.utb"]
    # return [b'fr-bfu-comp8.utb']
    # return [b'fr-bfu-g2.ctb']
    # return [b'da-dk-g16.ctb']
    # return [b'da-dk-g18.ctb']


def charToDots(char):
    louisDots = louis.charToDots(translationList(), char, len(char))
    ordDots = ord(louisDots)
    adjustedDots = adjustNumber(ordDots)
    return adjustedDots


def textToDots(text):
    translatedText = louis.translateString(translationList(), text)
    printProperty("translatedText", translatedText)

    translatedTextArray = list(translatedText)
    printProperty("translatedTextArray", str(translatedTextArray))

    dotsArray = list(map(charToDots, translatedTextArray))
    printProperty("dotsArray", str(dotsArray))

    return bytes(dotsArray)


def dotsToDisplaySize(dots, size):
    cells = []
    for i in range(0, size):  # it must be the length of the display
        if i < size:
            cells.append(dots[i])
        else:
            cells.append(0)
    return cells


def messageToDisplay(m):
    text = m["message"]
    dots = textToDots(text)
    dots = dotsToDisplaySize(dots, m["displayWidth"])
    return dots


def printDiagnostics(brl):
    printProperty("File Descriptor", str(brl.fileDescriptor))
    printProperty("Server Host", str(brl.host))
    printProperty("Authorization Schemes", str(brl.auth))
    printProperty("Driver Name", str(brl.driverName))
    printProperty("Model Identifier", str(brl.modelIdentifier))
    printProperty("Display Width", str(brl.displaySize[0]))
    printProperty("Display Height", str(brl.displaySize[1]))
    printProperty(".......", ".........................")
    printProperty("DOT1", str(brlapi.DOT1))
    printProperty("DOT2", str(brlapi.DOT2))
    printProperty("DOT3", str(brlapi.DOT3))
    printProperty("DOT4", str(brlapi.DOT4))
    printProperty("DOT5", str(brlapi.DOT5))
    printProperty("DOT6", str(brlapi.DOT6))
    printProperty("DOT7", str(brlapi.DOT7))
    printProperty("DOT8", str(brlapi.DOT8))
    printProperty(".......", ".........................")
    printProperty("Louis version", str(louis.version()))
    printProperty(".......", ".........................")


def printLog(m):
    # os.system('clear')

    if m["counter"] == 0:
        printProperty("LOG", "Program Initialized")
        printProperty("Counter", str(m["counter"]))
        printProperty("Message", m["message"])
        printProperty("Language", m["language"])
        printProperty("Display Width", str(m["displayWidth"]))
        printProperty("Point Blocks", str(m["pointBlocks"]))
        printProperty("Game Blocks", str(m["gameBlocks"]))
        printProperty("Game Duration", str(m["gameDuration"]))

    else:
        printProperty("LOG", "Program Started")
        if "code" in m:
            printProperty("Code", str(m["code"]))
            printProperty("Type", str(m["type"]))
            printProperty("Command", str(m["command"]))
            printProperty("Argument", str(m["argument"]))
            printProperty("Flags", str(m["flags"]))
            printProperty("Counter", str(m["counter"]))
        printProperty("Message", m["message"])
        printProperty("Text", m["text"])

        printProperty("Cursor Position", str(m["cursorPos"]))
        printProperty("Obstacle Posistion", str(m["obstaclePos"]))
        printProperty("Points", str(m["points"]))
        printProperty("Game Counter", str(m["gameCounter"]))
        printProperty("High Score", str(m["highScore"]))

    printProperty("-------", "-------------------------")


# Message in local language
def getMessage(displayWidth, language, code):
    if code == "start":
        if language == "fr":
            if displayWidth < 20:
                message = "Touche éspace"
            else:
                message = "Appuyez sur une touche"
        else:
            message = "Press any key"
    elif code == "highscore":
        if language == "fr":
            message = "Max points :"
        else:
            message = "Max score:"
    elif code == "points":
        if language == "fr":
            message = "Points :"
        else:
            message = "Points:"
    elif code == "birthday":
        if language == "fr":
            if displayWidth > 19:
                message = "Joyeux anniversaire"
            else:
                message = "Bon anniversaire"
        else:
            message = "Happy birthday"
    else:
        message = ""
    return message


# Initialize the model.
# This should define all possible states.
def init(brl):
    displayWidth = brl.displaySize[0]
    numberOfBlocks = displayWidth // 5
    if numberOfBlocks >= 6:
        pointBlocks = 2
    else:
        pointBlocks = 1
    language = "en"  # or 'fr'

    return {
        "cursorPos": 0,  # 0..3
        "obstaclePos": 9,  # 0..4
        "points": 0,  # 0..999
        "collision": False,
        "stop": False,
        "gameCounter": 0,
        "highScore": 0,
        "counter": 0,
        "text": "",
        "language": language,
        "displayWidth": displayWidth,
        "message": getMessage(displayWidth, language, "start"),
        "pointBlocks": pointBlocks,
        "gameBlocks": numberOfBlocks - pointBlocks,
        "gameDuration": 30,  # seconds
    }


def collisionDetection(m):
    if ("cursorPos" in m) and ("obstaclePos" in m):
        m["collision"] = (m["cursorPos"] in [0, 1]) and (m["obstaclePos"] in [2, 3, 4])
    else:
        m["collision"] = False
    return m


def pointsCalculation(m):
    if m["obstaclePos"] == 4:
        if m["collision"]:
            m["points"] = m["points"] - 1
        else:
            m["points"] = m["points"] + 1
    if m["points"] < 0:
        m["points"] = 0
    if m["points"] > 99:
        m["points"] = 99
    return m


def timeUpDetection(m):
    if time.time() - m["gameStartedAt"] > m["gameDuration"]:
        m["stop"] = True
    return m


def tens(i):
    i = i % 100
    if i > 9:
        i = int(str(i)[0])
    else:
        i = 0
    return i


def units(i):
    return i % 10


def digitDots(i):
    if i == 0:
        dots = brlapi.DOT3 | brlapi.DOT4 | brlapi.DOT5 | brlapi.DOT6
    elif i == 1:
        dots = brlapi.DOT1 | brlapi.DOT6
    elif i == 2:
        dots = brlapi.DOT1 | brlapi.DOT2 | brlapi.DOT6
    elif i == 3:
        dots = brlapi.DOT1 | brlapi.DOT4 | brlapi.DOT6
    elif i == 4:
        dots = brlapi.DOT1 | brlapi.DOT4 | brlapi.DOT5 | brlapi.DOT6
    elif i == 5:
        dots = brlapi.DOT1 | brlapi.DOT5 | brlapi.DOT6
    elif i == 6:
        dots = brlapi.DOT1 | brlapi.DOT2 | brlapi.DOT4 | brlapi.DOT6
    elif i == 7:
        dots = brlapi.DOT1 | brlapi.DOT2 | brlapi.DOT4 | brlapi.DOT5 | brlapi.DOT6

    elif i == 8:
        dots = brlapi.DOT1 | brlapi.DOT2 | brlapi.DOT5 | brlapi.DOT6
    elif i == 9:
        dots = brlapi.DOT2 | brlapi.DOT4 | brlapi.DOT5 | brlapi.DOT6
    else:
        dots = 0

    return dots


def gameToDots(m):
    """
    fullCell = brlapi.DOT1 | brlapi.DOT2 | brlapi.DOT3 | brlapi.DOT4 |
        brlapi.DOT5 | brlapi.DOT6 | brlapi.DOT7 | brlapi.DOT8
    """
    cells = []

    # Calculated cursor dots
    cursorDots = 0
    if m["cursorPos"] == 0:
        cursorDots = brlapi.DOT7 | brlapi.DOT8
    elif m["cursorPos"] == 1:
        cursorDots = brlapi.DOT3 | brlapi.DOT6
    elif m["cursorPos"] == 2:
        cursorDots = brlapi.DOT2 | brlapi.DOT5
    elif m["cursorPos"] == 3:
        cursorDots = brlapi.DOT1 | brlapi.DOT4

    # Calculate moving obstacles
    # for cells in range(0, 30) 40 cells display
    # for cells in range(0, 15) 20 cells display

    for i in range(0, m["gameBlocks"]):
        cell00 = 0
        cell01 = 0
        cell02 = 0
        cell03 = 0
        cell04 = 0

        if i == 0:
            cell01 = cursorDots

        if m["obstaclePos"] == 0:
            cell00 = brlapi.DOT3 | brlapi.DOT7
            cell04 = brlapi.DOT6 | brlapi.DOT8
        elif m["obstaclePos"] == 1:
            cell00 = brlapi.DOT3 | brlapi.DOT7 | brlapi.DOT6 | brlapi.DOT8
        elif m["obstaclePos"] == 2:
            cell00 = brlapi.DOT6 | brlapi.DOT8
            cell01 = cell01 | brlapi.DOT3 | brlapi.DOT7
        elif m["obstaclePos"] == 3:
            cell01 = cell01 | brlapi.DOT3 | brlapi.DOT7 | brlapi.DOT6 | brlapi.DOT8
        elif m["obstaclePos"] == 4:
            cell01 = cell01 | brlapi.DOT6 | brlapi.DOT8
            cell02 = brlapi.DOT3 | brlapi.DOT7
        elif m["obstaclePos"] == 5:
            cell02 = brlapi.DOT3 | brlapi.DOT7 | brlapi.DOT6 | brlapi.DOT8
        elif m["obstaclePos"] == 6:
            cell02 = brlapi.DOT6 | brlapi.DOT8
            cell03 = brlapi.DOT3 | brlapi.DOT7
        elif m["obstaclePos"] == 7:
            cell03 = brlapi.DOT3 | brlapi.DOT7 | brlapi.DOT6 | brlapi.DOT8
        elif m["obstaclePos"] == 8:
            cell03 = brlapi.DOT6 | brlapi.DOT8
            cell04 = brlapi.DOT3 | brlapi.DOT7
        elif m["obstaclePos"] == 9:
            cell04 = brlapi.DOT3 | brlapi.DOT7 | brlapi.DOT6 | brlapi.DOT8

        if (i == 0) and m["collision"]:
            if m["counter"] % 2 == 0:
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
    cells.append(brlapi.DOT1 | brlapi.DOT2 | brlapi.DOT3 | brlapi.DOT4)  # p
    if m["pointBlocks"] > 1:
        cells.append(brlapi.DOT1 | brlapi.DOT3 | brlapi.DOT5)  # o
        cells.append(brlapi.DOT2 | brlapi.DOT4)  # i
        cells.append(brlapi.DOT1 | brlapi.DOT3 | brlapi.DOT4 | brlapi.DOT5)  # n
        cells.append(brlapi.DOT2 | brlapi.DOT3 | brlapi.DOT4 | brlapi.DOT5)  # t
        cells.append(brlapi.DOT2 | brlapi.DOT3 | brlapi.DOT4)  # s
    cells.append(brlapi.DOT2 | brlapi.DOT5)  # :

    # Display number of points. French system
    cells.append(brlapi.DOT6)  # Number coming
    cells.append(digitDots(tens(m["points"])))  # 0
    cells.append(digitDots(units(m["points"])))  # 0

    cells = dotsToDisplaySize(cells, m["displayWidth"])
    printProperty("cells", str(cells))

    return bytes(cells)


# Visualize the model on the braille displan
def view(brl, m):
    printLog(m)
    if (m["counter"] == 0) or m["stop"]:
        brl.writeDots(messageToDisplay(m))
        # brl.writeText()
    else:
        brl.writeDots(gameToDots(m))


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


# Update the model at game start
def updateByGameStart(m):
    m["gameStartedAt"] = time.time()
    m["stop"] = False
    m["points"] = 0
    return m


# Update the model at game end
def updateByGameEnd(m):
    if m["points"] > m["highScore"]:
        m["highScore"] = m["points"]
    m["gameCounter"] = m["gameCounter"] + 1
    m["message"] = (
        getMessage(m["displayWidth"], m["language"], "points") + " " + str(m["points"])
    )
    return m


# Update the High score message
def updateHighScoreMessage(m):
    m["message"] = (
        getMessage(m["displayWidth"], m["language"], "highscore")
        + " "
        + str(m["highScore"])
    )
    return m


# Update the model based because time passed
def updateByTime(m):
    m["message"] = "Time flies when you are having fun"

    m["counter"] = m["counter"] + 1
    if m["counter"] % 2 == 0:
        m["obstaclePos"] = obstacleAdvance(m["obstaclePos"])
        m = collisionDetection(m)
        m = pointsCalculation(m)
    if m["obstaclePos"] == 1:
        m["cursorPos"] = 0

    m = timeUpDetection(m)
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
        m["text"] = m["text"] + chr(m["argument"])

    # Update the model
    m["counter"] = m["counter"] + 1
    if keyCode == brlapi.KEY_TYPE_CMD | brlapi.KEY_CMD_HOME:
        m["message"] = "Home Button"
        m["stop"] = True
    elif keyCode == brlapi.KEY_TYPE_CMD | brlapi.KEY_CMD_LNUP:
        m["message"] = "Line Up"
        m["cursorPos"] = cursorUp(m["cursorPos"])
    elif keyCode == brlapi.KEY_TYPE_CMD | brlapi.KEY_CMD_LNDN:
        m["stop"] = True
    elif (
        (m["type"] == 536870912) and (m["command"] == 2228224) and (m["argument"] == 0)
    ):
        m["message"] = "Space bar"
        if m["cursorPos"] == 3:
            m["cursorPos"] = 0
        else:
            m["cursorPos"] = cursorUp(m["cursorPos"])
    else:
        m["message"] = "Unknown key"

    m = collisionDetection(m)
    m = timeUpDetection(m)
    return m


try:
    printProperty("Initialization", "Before Connection")
    # Initialization
    b = brlapi.Connection()
    b.enterTtyModeWithPath()
    b.acceptKeys(brlapi.rangeType_all, [0])
    printDiagnostics(b)

    # Supprise
    if currentDateTime.month == 5:
        # Happy birthday
        model = init(b)
        model["message"] = getMessage(
            model["displayWidth"], model["language"], "birthday"
        )
        view(b, model)
        time.sleep(10)

    # The architecture
    model = init(b)
    view(b, model)
    delay = 0.1  # seconds
    waitForKeyPress = True
    for _ in range(0, 1):  # TODO change to 3
        key = b.readKey(waitForKeyPress)
        model = updateByGameStart(model)
        while not model["stop"]:
            key = b.readKey(not waitForKeyPress)
            if not key:
                time.sleep(delay)
                model = updateByTime(model)
            else:
                model = updateByKey(b, model, key)

            view(b, model)

        model = updateByGameEnd(model)
        view(b, model)
        time.sleep(10)

    model = updateHighScoreMessage(model)
    view(b, model)
    time.sleep(10)

    b.leaveTtyMode()
    b.closeConnection()

# Error Handling
except brlapi.ConnectionError as e:
    if e.brlerrno == brlapi.ERROR_CONNREFUSED:
        printProperty(
            "Connection refused",
            "Connection to %s refused. BRLTTY is too busy..." % (e.host),
        )
    elif e.brlerrno == brlapi.ERROR_AUTHENTICATION:
        printProperty(
            "Authentication failed.",
            "Authentication with %s failed. Please check the permissions of %s"
            % (e.host, e.auth),
        )
    elif e.brlerrno == brlapi.ERROR_LIBCERR and (
        e.libcerrno == errno.ECONNREFUSED or e.libcerrno == errno.ENOENT
    ):
        printProperty(
            "Connection failed",
            "Connection to %s failed. Is BRLTTY really running?" % (e.host),
        )
    else:
        printProperty(
            "Connection to BRLTTY failed",
            "Connection to BRLTTY at %s failed: " % (e.host),
        )
    printProperty("error", str(e))
    printProperty("error.brlerrno", str(e.brlerrno))
    printProperty("error.libcerrno", str(e.libcerrno))
