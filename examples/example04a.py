#!/bin/python3

# Game: Learn the buttons on the keyboard

import brlapi
import louis
import errno
import time
import datetime
import os


def formatTimeStamp(dateTime):
    return dateTime.isoformat()[:16].replace(":", "-")


# Global values

currentDateTime = datetime.datetime.now()
directory = os.getcwd()
logFileName = directory + "/logs/"
if not os.path.exists(logFileName):
    os.mkdir(logFileName)
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
    return n - 0x8000  # 32768 = 2^15


def adjustDots(d):
    return d | 0x8000


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


def helper(dots):
    adjustedNumber = adjustDots(dots)
    chrNumber = chr(adjustedNumber)
    louisChars = louis.dotsToChar(translationList(), chrNumber)
    return louisChars


def dotsToChar(modifier, dots):
    if modifier > 0:
        louisChars = helper(modifier) + helper(dots)
        text = louis.backTranslateString(translationList(), louisChars)
        chars = text[0]
        return chars
    else:
        louisChars = helper(dots)
        text = louis.backTranslateString(translationList(), louisChars)
        chars = text[0]
        return chars


def handleTextInput(m):
    dots = m["dots"]
    if dots == 0x28:  # Uppercase
        m["textModifier"] = dots
        m["uppercaseModifier"] = True
    elif dots == 0x20:  # Number
        m["textModifier"] = dots
        m["numberModifier"] = True
    else:
        # I need to handle
        # if it is a continious list of digits or not
        # if it is a double uppercase sign and uppercase what follows.

        # what can I receive here?
        # modifier, double uppercase, single uppercase, number, italics, ...
        # letter a-z
        # letter special and w
        # digit 0-9
        # signs , . ; : ' ! ...
        # special characters # < > \ % & " / ...
        # math symbols / * - + =  ...

        m["text"] = m["text"] + dotsToChar(m["textModifier"], m["dots"])
        m["textModifier"] = 0
    return m


def textToDots(text):
    translatedText = louis.translateString(translationList(), text)
    # printProperty('translatedText', translatedText)

    translatedTextArray = list(translatedText)
    # printProperty('translatedTextArray', str(translatedTextArray))

    dotsArray = list(map(charToDots, translatedTextArray))
    # printProperty('dotsArray', str(dotsArray))

    return bytes(dotsArray)


def dotsToDisplaySize(dots, size):
    dotsLength = len(dots)
    cells = []
    for i in range(0, size):  # it must be the length of the display
        if i < dotsLength:
            cells.append(dots[i])
        else:
            cells.append(0)
    return bytes(cells)


def placeCursor(dots, cursorPosition):
    dotsLength = len(dots)
    cells = []
    for i in range(0, dotsLength):
        if i == cursorPosition:
            cells.append(dots[i] | brlapi.DOT7 | brlapi.DOT8)
        else:
            cells.append(dots[i])
    return bytes(cells)


def messageToDisplay(m):
    text = m["message"]
    dots = textToDots(text)
    dots = dotsToDisplaySize(dots, m["displayWidth"])
    dots = placeCursor(dots, m["cursorPosition"])
    return dots


def printDiagnostics(brl):
    printProperty("File Descriptor", str(brl.fileDescriptor))
    printProperty("Server Host", str(brl.host))
    printProperty("Authorization Schemes", str(brl.auth))
    printProperty("Driver Name", str(brl.driverName))
    printProperty("Model Identifier", str(brl.modelIdentifier))
    printProperty("Display Width", str(brl.displaySize[0]))
    printProperty("Display Height", str(brl.displaySize[1]))

    """
    printProperty(".......", '.........................')
    printProperty("DOT1", str(brlapi.DOT1))
    printProperty("DOT2", str(brlapi.DOT2))
    printProperty("DOT3", str(brlapi.DOT3))
    printProperty("DOT4", str(brlapi.DOT4))
    printProperty("DOT5", str(brlapi.DOT5))
    printProperty("DOT6", str(brlapi.DOT6))
    printProperty("DOT7", str(brlapi.DOT7))
    printProperty("DOT8", str(brlapi.DOT8))
    """

    printProperty(".......", ".........................")
    printProperty("Louis version", str(louis.version()))
    printProperty(".......", ".........................")


def printLog(m):
    if m["counter"] == 0:
        printProperty("LOG", "Program Initialized")
        printProperty("Counter", str(m["counter"]))
        printProperty("Message", m["message"])
        printProperty("Language", m["language"])
        printProperty("Display Width", str(m["displayWidth"]))

    elif m["programStopped"]:
        printProperty("LOG", "Program Stopped")
        printProperty("Counter", str(m["counter"]))
        printProperty("Message", m["message"])
        printProperty("Text", m["text"])

    else:
        if m["stopProgram"]:
            printProperty("LOG", "Program Stopping")
            printProperty("Counter", str(m["counter"]))
        else:
            printProperty("LOG", "Program Running")
            printProperty("Counter", str(m["counter"]))

        if "code" in m:
            printProperty("Code", hex(m["code"]))
            printProperty("Type", str(hex(m["type"])))
            printProperty("Command", str(hex(m["command"])))
            printProperty("Argument", str(hex(m["argument"])))
            printProperty("Flags", str(hex(m["flags"])))

        printProperty("Message", m["message"])
        printProperty("Text", m["text"])

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
    elif code == "end":
        if language == "fr":
            message = "Au revoir"
        else:
            message = "Goodbye"
    else:
        message = code
    return message


# Initialize the model.
# This should define all possible states.
def init(brl):
    displayWidth = brl.displaySize[0]
    language = "en"  # or 'fr'

    return {
        "stopProgram": False,
        "programStopped": False,
        "modelChanged": False,
        "counter": 0,
        "showCursor": False,
        "cursorPosition": 0,
        "textModifier": 0,
        "uppercaseModifier": False,
        "numberModifier": False,
        "numberString": "",  # I might have to keep special track of an onging number.
        "text": "",  # the line to display
        "textArray": [],  # Note taking app, array of text line
        "currentLine": 0,  # to allow to move up and down
        "numberArray": [],  # to make a calculator polish notation STACK
        "language": language,
        "displayWidth": displayWidth,
        "message": getMessage(displayWidth, language, "start"),
    }


# Visualize the model on the braille displan
def view(brl, m):
    printLog(m)
    brl.writeDots(messageToDisplay(m))


# Update the model before leaving end
def updateBeforeLeaving(m):
    m["modelChanged"] = True
    m["programStopped"] = True
    m["message"] = getMessage(m["displayWidth"], m["language"], "end")
    return m


# Update the model based because time passed
def updateByTime(m):
    m["modelChanged"] = False
    return m


# Update the model based based on the key pressed
def updateByKey(brl, m, keyCode):
    m["modelChanged"] = True
    m["counter"] = m["counter"] + 1

    # Keep information about the key pressed in the model
    k = brl.expandKeyCode(keyCode)
    m["code"] = keyCode
    m["type"] = k["type"]
    m["command"] = k["command"]
    m["argument"] = k["argument"]
    m["flags"] = k["flags"]

    m["brailleCommand"] = (keyCode & brlapi.KEY_TYPE_MASK) == brlapi.KEY_TYPE_CMD
    m["keysym"] = (keyCode & brlapi.KEY_TYPE_MASK) == brlapi.KEY_TYPE_SYM

    m["brailleRouteCommand"] = (
        keyCode & brlapi.KEY_CMD_BLK_MASK
    ) == brlapi.KEY_CMD_ROUTE
    m["highlightedCell"] = keyCode & brlapi.KEY_CMD_ARG_MASK
    m["commandFlags"] = keyCode & brlapi.KEY_FLAGS_MASK
    # m['shiftModifier'] = (keyCode & brlapi.KEY_FLAGS_MASK) == brlapi.KEY_FLG_SHIFT
    #  AttributeError: module 'brlapi' has no attribute 'KEY_FLG_SHIFT'

    m["tabKey"] = (keyCode & brlapi.KEY_CODE_MASK) == brlapi.KEY_SYM_TAB
    m["unicodeKeysym"] = (keyCode & brlapi.KEY_SYM_UNICODE) != 0
    m["unicodeKeysymValue"] = keyCode & (brlapi.KEY_SYM_UNICODE - 1)

    # Type: brlapi.KEY_TYPE_CMD == 0x20000000

    if keyCode == brlapi.KEY_TYPE_CMD:
        m["modelChanged"] = False

    elif keyCode == brlapi.KEY_TYPE_CMD | brlapi.KEY_CMD_LNUP:
        m["message"] = "Line Up - Left panning button UP"
    elif keyCode == brlapi.KEY_TYPE_CMD | brlapi.KEY_CMD_LNDN:
        m["message"] = "Line Down - Left panning button DOWN"

    elif keyCode == brlapi.KEY_TYPE_CMD | brlapi.KEY_CMD_HOME:
        m["message"] = "Home Button - Selector button RIGHT"
    elif keyCode == brlapi.KEY_TYPE_CMD | brlapi.KEY_CMD_BACK:
        m["message"] = "Go back after cursor tracking - Selector button LEFT"

    elif keyCode == brlapi.KEY_TYPE_CMD | brlapi.KEY_CMD_LNBEG:
        m["message"] = "Go to beginning of line - mode button left"
    elif keyCode == brlapi.KEY_TYPE_CMD | brlapi.KEY_CMD_LNEND:
        m["message"] = "Go to end of line - mode button right"

    elif keyCode == brlapi.KEY_TYPE_CMD | brlapi.KEY_CMD_FWINLT:
        m["message"] = "Go backward one braille window - Panning button LEFT"
    elif keyCode == brlapi.KEY_TYPE_CMD | brlapi.KEY_CMD_FWINRT:
        m["message"] = "Go forward one braille window - Panning button RIGHT"

    elif keyCode == brlapi.KEY_TYPE_CMD | 0x220000:  # Space bar
        m["text"] = m["text"] + " "
        m["message"] = m["text"]
        m["cursorPosition"] = len(m["text"])
        m["showCursor"] = True

    elif (
        (m["type"] == brlapi.KEY_TYPE_CMD)
        and (m["command"] == 0x220000)
        and (m["argument"] != 0)
    ):
        m["dots"] = m["argument"]
        m = handleTextInput(m)
        m["message"] = m["text"]
        m["cursorPosition"] = len(m["text"])
        m["showCursor"] = True

    elif (m["type"] == brlapi.KEY_TYPE_CMD) and (m["command"] == 0x10000):
        m["cursorPosition"] = m["argument"]
        m["showCursor"] = True

    elif keyCode == brlapi.KEY_SYM_UP:
        m["message"] = "KEY_SYM_UP - Left rocker bar UP"
    elif keyCode == brlapi.KEY_SYM_DOWN:
        m["message"] = "KEY_SYM_DOWN - Left rocker bar DOWN"

    elif keyCode == 0xFF0D:  # Enter
        m["text"] = m["text"] + "/n"
        m["message"] = m["text"]
        m["cursorPosition"] = len(m["text"])

    elif keyCode == 0xFF08:  # Delete
        if len(m["text"]) > 0:
            m["text"] = m["text"][:-1]
        m["message"] = m["text"]
        m["cursorPosition"] = len(m["text"])

    else:
        m["message"] = "Unknown key"

    return m


# Main function
def main():
    try:
        printProperty("Initialization", "Before Connection")
        # Initialization
        b = brlapi.Connection()
        b.enterTtyModeWithPath()
        b.acceptKeys(brlapi.rangeType_all, [0])
        printDiagnostics(b)

        # The architecture
        model = init(b)
        view(b, model)
        waitForKeyPress = True
        while not model["stopProgram"]:
            key = b.readKey(not waitForKeyPress)
            if not key:
                model = updateByTime(model)
            else:
                model = updateByKey(b, model, key)

            if model["modelChanged"]:
                model["modelChanged"] = False
                view(b, model)

        model = updateBeforeLeaving(model)
        view(b, model)
        key = b.readKey(waitForKeyPress)

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


if __name__ == "__main__":
    main()
