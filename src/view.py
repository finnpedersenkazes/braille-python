"""
View module - Elm-like architecture for braille game
Contains display and rendering functions
"""

import brlapi
from model import printLog
from library import (
    printProperty,
    textToDots,
    dotsToDisplaySize,
    tens,
    units,
    digitDots,
)


def messageToDisplay(m):
    """Convert message to display format"""
    text = m["message"]
    dots = textToDots(text)
    dots = dotsToDisplaySize(dots, m["displayWidth"])
    return dots


def gameToDots(m):
    """
    Convert game state to braille dots for display
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


def view(brl, m):
    """Visualize the model on the braille display"""
    printLog(m)
    if m["displayWidth"] == 0:
        print("Warning: No braille display detected. Skipping writeDots.")
        return
    if (m["counter"] == 0) or m["stop"]:
        brl.writeDots(messageToDisplay(m))
        # brl.writeText()
    else:
        brl.writeDots(gameToDots(m))
