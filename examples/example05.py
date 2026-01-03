#!/usr/bin/env python3

"""
Example 05 - Jump over the obstacles game
Demonstrates Elm-like architecture with Model-Update-View pattern
Based on example03c.py
"""

import brlapi
import time
import sys
import os

# Add src to path to import libraries
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from library import (
    printProperty,
    printDiagnostics,
    currentDateTime,
    handleConnectionError,
    textToDots,
    dotsToDisplaySize,
    tens,
    units,
    digitDots,
)


# ============================================================================
# Model - Game state initialization and messages
# ============================================================================

def getMessage(displayWidth, language, code):
    """Get localized message based on language and code"""
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


def init(brl):
    """Initialize the game model with all possible states"""
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


def printLog(m):
    """Print model state to log"""
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


# ============================================================================
# Update - Game logic and state updates
# ============================================================================

def cursorUp(position):
    """Move cursor up, legal positions: 0..3, blocked"""
    if position > 2:
        position = 2
    if position < 0:
        position = 0
    return position + 1


def cursorDown(position):
    """Move cursor down, legal positions: 0..3, blocked"""
    if position > 3:
        position = 3
    if position < 1:
        position = 1
    return position - 1


def obstacleAdvance(position):
    """Advance obstacle position, legal positions: 0..9, revolving"""
    if position > 9:
        position = 9
    if position <= 0:
        position = 10
    return position - 1


def collisionDetection(m):
    """Detect collision between cursor and obstacle"""
    if ("cursorPos" in m) and ("obstaclePos" in m):
        m["collision"] = (m["cursorPos"] in [0, 1]) and (m["obstaclePos"] in [2, 3, 4])
    else:
        m["collision"] = False
    return m


def pointsCalculation(m):
    """Calculate points based on collision and obstacle position"""
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
    """Check if game time is up"""
    if time.time() - m["gameStartedAt"] > m["gameDuration"]:
        m["stop"] = True
    return m


def updateByGameStart(m):
    """Update the model at game start"""
    m["gameStartedAt"] = time.time()
    m["stop"] = False
    m["points"] = 0
    return m


def updateByGameEnd(m):
    """Update the model at game end"""
    if m["points"] > m["highScore"]:
        m["highScore"] = m["points"]
    m["gameCounter"] = m["gameCounter"] + 1
    m["message"] = (
        getMessage(m["displayWidth"], m["language"], "points") + " " + str(m["points"])
    )
    return m


def updateHighScoreMessage(m):
    """Update the High score message"""
    m["message"] = (
        getMessage(m["displayWidth"], m["language"], "highscore")
        + " "
        + str(m["highScore"])
    )
    return m


def updateByTime(m):
    """Update the model because time passed"""
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


def updateByKey(brl, m, keyCode):
    """Update the model based on the key pressed"""
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


# ============================================================================
# View - Game rendering
# ============================================================================

def messageToDisplay(m):
    """Convert message to display format"""
    text = m["message"]
    dots = textToDots(text)
    dots = dotsToDisplaySize(dots, m["displayWidth"])
    return dots


def gameToDots(m):
    """Convert game state to braille dots for display"""
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


def view(brl, m):
    """Visualize the model on the braille display"""
    printLog(m)
    if m["displayWidth"] == 0:
        print("Warning: No braille display detected. Skipping writeDots.")
        return
    if (m["counter"] == 0) or m["stop"]:
        brl.writeDots(messageToDisplay(m))
    else:
        brl.writeDots(gameToDots(m))


# ============================================================================
# Main - Application entry point
# ============================================================================

def main():
    """Main game loop"""
    try:
        printProperty("Initialization", "Before Connection")
        # Initialization
        b = brlapi.Connection()
        b.enterTtyModeWithPath()
        b.acceptKeys(brlapi.rangeType_all, [0])
        printDiagnostics(b)

        # Surprise
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
        handleConnectionError(e)


if __name__ == "__main__":
    main()
