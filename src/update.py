"""
Update module - Elm-like architecture for braille game
Contains state update logic and game mechanics
"""

import time
import brlapi
from model import getMessage


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
