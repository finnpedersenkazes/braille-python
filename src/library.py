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


# ============================================================================
# Braille character utilities
# ============================================================================

def charToBrailleDots(char):
    """
    Convert a-z character to braille dot pattern (Grade 1 Braille)
    Returns integer with bits set for dots 1-6
    """
    char = char.lower()
    
    # Braille alphabet mapping (dots 1-6)
    braille_map = {
        'a': brlapi.DOT1,
        'b': brlapi.DOT1 | brlapi.DOT2,
        'c': brlapi.DOT1 | brlapi.DOT4,
        'd': brlapi.DOT1 | brlapi.DOT4 | brlapi.DOT5,
        'e': brlapi.DOT1 | brlapi.DOT5,
        'f': brlapi.DOT1 | brlapi.DOT2 | brlapi.DOT4,
        'g': brlapi.DOT1 | brlapi.DOT2 | brlapi.DOT4 | brlapi.DOT5,
        'h': brlapi.DOT1 | brlapi.DOT2 | brlapi.DOT5,
        'i': brlapi.DOT2 | brlapi.DOT4,
        'j': brlapi.DOT2 | brlapi.DOT4 | brlapi.DOT5,
        'k': brlapi.DOT1 | brlapi.DOT3,
        'l': brlapi.DOT1 | brlapi.DOT2 | brlapi.DOT3,
        'm': brlapi.DOT1 | brlapi.DOT3 | brlapi.DOT4,
        'n': brlapi.DOT1 | brlapi.DOT3 | brlapi.DOT4 | brlapi.DOT5,
        'o': brlapi.DOT1 | brlapi.DOT3 | brlapi.DOT5,
        'p': brlapi.DOT1 | brlapi.DOT2 | brlapi.DOT3 | brlapi.DOT4,
        'q': brlapi.DOT1 | brlapi.DOT2 | brlapi.DOT3 | brlapi.DOT4 | brlapi.DOT5,
        'r': brlapi.DOT1 | brlapi.DOT2 | brlapi.DOT3 | brlapi.DOT5,
        's': brlapi.DOT2 | brlapi.DOT3 | brlapi.DOT4,
        't': brlapi.DOT2 | brlapi.DOT3 | brlapi.DOT4 | brlapi.DOT5,
        'u': brlapi.DOT1 | brlapi.DOT3 | brlapi.DOT6,
        'v': brlapi.DOT1 | brlapi.DOT2 | brlapi.DOT3 | brlapi.DOT6,
        'w': brlapi.DOT2 | brlapi.DOT4 | brlapi.DOT5 | brlapi.DOT6,
        'x': brlapi.DOT1 | brlapi.DOT3 | brlapi.DOT4 | brlapi.DOT6,
        'y': brlapi.DOT1 | brlapi.DOT3 | brlapi.DOT4 | brlapi.DOT5 | brlapi.DOT6,
        'z': brlapi.DOT1 | brlapi.DOT3 | brlapi.DOT5 | brlapi.DOT6,
    }
    
    return braille_map.get(char, 0)


def brailleDotsToChar(dots):
    """
    Convert braille dot pattern back to character (inverse of charToBrailleDots)
    Returns the character or '?' if not found
    """
    # Reverse mapping
    reverse_map = {
        brlapi.DOT1: 'a',
        brlapi.DOT1 | brlapi.DOT2: 'b',
        brlapi.DOT1 | brlapi.DOT4: 'c',
        brlapi.DOT1 | brlapi.DOT4 | brlapi.DOT5: 'd',
        brlapi.DOT1 | brlapi.DOT5: 'e',
        brlapi.DOT1 | brlapi.DOT2 | brlapi.DOT4: 'f',
        brlapi.DOT1 | brlapi.DOT2 | brlapi.DOT4 | brlapi.DOT5: 'g',
        brlapi.DOT1 | brlapi.DOT2 | brlapi.DOT5: 'h',
        brlapi.DOT2 | brlapi.DOT4: 'i',
        brlapi.DOT2 | brlapi.DOT4 | brlapi.DOT5: 'j',
        brlapi.DOT1 | brlapi.DOT3: 'k',
        brlapi.DOT1 | brlapi.DOT2 | brlapi.DOT3: 'l',
        brlapi.DOT1 | brlapi.DOT3 | brlapi.DOT4: 'm',
        brlapi.DOT1 | brlapi.DOT3 | brlapi.DOT4 | brlapi.DOT5: 'n',
        brlapi.DOT1 | brlapi.DOT3 | brlapi.DOT5: 'o',
        brlapi.DOT1 | brlapi.DOT2 | brlapi.DOT3 | brlapi.DOT4: 'p',
        brlapi.DOT1 | brlapi.DOT2 | brlapi.DOT3 | brlapi.DOT4 | brlapi.DOT5: 'q',
        brlapi.DOT1 | brlapi.DOT2 | brlapi.DOT3 | brlapi.DOT5: 'r',
        brlapi.DOT2 | brlapi.DOT3 | brlapi.DOT4: 's',
        brlapi.DOT2 | brlapi.DOT3 | brlapi.DOT4 | brlapi.DOT5: 't',
        brlapi.DOT1 | brlapi.DOT3 | brlapi.DOT6: 'u',
        brlapi.DOT1 | brlapi.DOT2 | brlapi.DOT3 | brlapi.DOT6: 'v',
        brlapi.DOT2 | brlapi.DOT4 | brlapi.DOT5 | brlapi.DOT6: 'w',
        brlapi.DOT1 | brlapi.DOT3 | brlapi.DOT4 | brlapi.DOT6: 'x',
        brlapi.DOT1 | brlapi.DOT3 | brlapi.DOT4 | brlapi.DOT5 | brlapi.DOT6: 'y',
        brlapi.DOT1 | brlapi.DOT3 | brlapi.DOT5 | brlapi.DOT6: 'z',
    }
    
    return reverse_map.get(dots, '?')


def combineKeysToDots(dot_list):
    """
    Combine list of dot numbers (1-6) into braille dot pattern
    Example: [1, 3, 4, 6] -> DOT1|DOT3|DOT4|DOT6
    """
    dots = 0
    dot_map = {
        1: brlapi.DOT1,
        2: brlapi.DOT2,
        3: brlapi.DOT3,
        4: brlapi.DOT4,
        5: brlapi.DOT5,
        6: brlapi.DOT6,
    }
    
    for dot_num in dot_list:
        if dot_num in dot_map:
            dots |= dot_map[dot_num]
    
    return dots


# ============================================================================
# Random utilities
# ============================================================================

def randomChar():
    """Get a random lowercase letter a-z"""
    import random
    return random.choice('abcdefghijklmnopqrstuvwxyz')


def randomPosition(max_position):
    """Get a random position from 0 to max_position-1"""
    import random
    return random.randint(0, max_position - 1)

