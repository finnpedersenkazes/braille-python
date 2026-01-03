"""
Library module - Generic utility functions for braille applications
Contains reusable functions for logging, braille conversion, and utilities
"""

import datetime
import os
import brlapi
import louis


# ============================================================================
# Logging utilities
# ============================================================================

def formatTimeStamp(dateTime):
    """Format datetime for use in filenames"""
    return dateTime.isoformat()[:16].replace(":", "-")


# Global values for logging
currentDateTime = datetime.datetime.now()
logDir = os.path.join(os.path.expanduser("~"), "Documents")
os.makedirs(logDir, exist_ok=True)
logFileName = os.path.join(logDir, formatTimeStamp(currentDateTime) + "_log.txt")


def printProperty(name, value):
    """Helper function to print debug information to the log"""
    text = name + ": " + value
    print(text)
    f = open(logFileName, "a")
    f.write(text)
    f.write("\n")
    f.close()


def printDiagnostics(brl):
    """Print BrlAPI diagnostics information"""
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


# ============================================================================
# Braille conversion utilities
# ============================================================================

def translationList():
    """Get braille translation table list"""
    return [b"fr-bfu-comp6.utb"]
    # return [b'fr-bfu-comp8.utb']
    # return [b'fr-bfu-g2.ctb']
    # return [b'da-dk-g16.ctb']
    # return [b'da-dk-g18.ctb']


def adjustNumber(n):
    """Adjust number for braille translation"""
    return n - 32768  # = 2^15


def charToDots(char):
    """Convert character to braille dots"""
    louisDots = louis.charToDots(translationList(), char, len(char))
    ordDots = ord(louisDots)
    adjustedDots = adjustNumber(ordDots)
    return adjustedDots


def textToDots(text):
    """Convert text to braille dots array"""
    translatedText = louis.translateString(translationList(), text)
    printProperty("translatedText", translatedText)

    translatedTextArray = list(translatedText)
    printProperty("translatedTextArray", str(translatedTextArray))

    dotsArray = list(map(charToDots, translatedTextArray))
    printProperty("dotsArray", str(dotsArray))

    return bytes(dotsArray)


def dotsToDisplaySize(dots, size):
    """Adjust dots array to display size"""
    dotsLength = len(dots)
    cells = []
    for i in range(0, size):  # it must be the length of the display
        if i < dotsLength:
            cells.append(dots[i])
        else:
            cells.append(0)
    return bytes(cells)


def digitDots(i):
    """Convert digit (0-9) to braille dots"""
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


# ============================================================================
# Math utilities
# ============================================================================

def tens(i):
    """Get tens digit from a number"""
    i = i % 100
    if i > 9:
        i = int(str(i)[0])
    else:
        i = 0
    return i


def units(i):
    """Get units digit from a number"""
    return i % 10


# ============================================================================
# Display utilities
# ============================================================================

def fullCell():
    """Get a full braille cell with all dots"""
    return (
        brlapi.DOT1
        | brlapi.DOT2
        | brlapi.DOT3
        | brlapi.DOT4
        | brlapi.DOT5
        | brlapi.DOT6
        | brlapi.DOT7
        | brlapi.DOT8
    )


def underlineCell():
    """Get underline character for braille display"""
    return chr(brlapi.DOT7 + brlapi.DOT8)


def placeCursor(dots, cursorPosition):
    """Place cursor at specified position in dots array"""
    dotsLength = len(dots)
    cells = []
    for i in range(0, dotsLength):
        if i == cursorPosition:
            cells.append(dots[i] | brlapi.DOT7 | brlapi.DOT8)
        else:
            cells.append(dots[i])
    return bytes(cells)


def adjustDots(d):
    """Adjust dots by adding offset (inverse of adjustNumber)"""
    return d | 0x8000


def dotsToChar(modifier, dots):
    """Convert braille dots back to character with optional modifier"""
    def helper(dots):
        adjustedNumber = adjustDots(dots)
        chrNumber = chr(adjustedNumber)
        louisChars = louis.dotsToChar(translationList(), chrNumber)
        return louisChars

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


# ============================================================================
# Connection and error handling utilities
# ============================================================================

def handleConnectionError(e):
    """Handle BrlAPI connection errors with appropriate messages"""
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
    elif e.brlerrno == brlapi.ERROR_LIBCERR:
        import errno as err
        if e.libcerrno == err.ECONNREFUSED or e.libcerrno == err.ENOENT:
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


def checkDisplayConnected(brl):
    """Check if a braille display is actually connected"""
    if brl.displaySize[0] == 0 or brl.displaySize[1] == 0:
        printProperty("WARNING", "No braille display detected! (displaySize is 0)")
        printProperty(
            "Info",
            "The driver name may show a configured driver, but no physical device is connected.",
        )
        return False
    return True


# ============================================================================
# Key handling utilities
# ============================================================================

def writeProperty(name, value):
    """Alternative name for printProperty (used in some examples)"""
    printProperty(name, value)
