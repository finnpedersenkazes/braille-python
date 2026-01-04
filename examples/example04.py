#!/usr/bin/env python3

"""
Example 04a - Keyboard Learning Game
Demonstrates advanced braille translation and text input
Interactive learning tool with Louis library integration, file logging, and internationalization
"""

import brlapi
import louis
import errno
import time
import datetime
import os


def format_time_stamp(date_time):
    return date_time.isoformat()[:16].replace(":", "-")


# Global values

CURRENT_DATE_TIME = datetime.datetime.now()
DIRECTORY = os.getcwd()
LOG_FILE_NAME = DIRECTORY + "/logs/"
if not os.path.exists(LOG_FILE_NAME):
    os.mkdir(LOG_FILE_NAME)
LOG_FILE_NAME = LOG_FILE_NAME + format_time_stamp(CURRENT_DATE_TIME) + "_log.txt"

# Helper functions to print debug information to the log


def print_property(name, value):
    text = name + ": " + value
    print(text)
    with open(LOG_FILE_NAME, "a") as f:
        f.write(text)
        f.write("\n")


def adjust_number(n):
    return n - 0x8000  # 32768 = 2^15


def adjust_dots(d):
    return d | 0x8000


def translation_list():
    return [b"fr-bfu-comp6.utb"]
    # return [b'fr-bfu-comp8.utb']
    # return [b'fr-bfu-g2.ctb']
    # return [b'da-dk-g16.ctb']
    # return [b'da-dk-g18.ctb']


def char_to_dots(char):
    louis_dots = louis.charToDots(translation_list(), char, len(char))
    ord_dots = ord(louis_dots)
    adjusted_dots = adjust_number(ord_dots)
    return adjusted_dots


def helper(dots):
    adjusted_number = adjust_dots(dots)
    chr_number = chr(adjusted_number)
    louis_chars = louis.dotsToChar(translation_list(), chr_number)
    return louis_chars


def dots_to_char(modifier, dots):
    if modifier > 0:
        louis_chars = helper(modifier) + helper(dots)
        text = louis.backTranslateString(translation_list(), louis_chars)
        chars = text[0]
        return chars
    else:
        louis_chars = helper(dots)
        text = louis.backTranslateString(translation_list(), louis_chars)
        chars = text[0]
        return chars


def handle_text_input(m):
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

        m["text"] = m["text"] + dots_to_char(m["textModifier"], m["dots"])
        m["textModifier"] = 0
    return m


def text_to_dots(text):
    translated_text = louis.translateString(translation_list(), text)
    # print_property('translatedText', translated_text)

    translated_text_array = list(translated_text)
    # print_property('translatedTextArray', str(translated_text_array))

    dots_array = list(map(char_to_dots, translated_text_array))
    # print_property('dotsArray', str(dots_array))

    return bytes(dots_array)


def dots_to_display_size(dots, size):
    dots_length = len(dots)
    cells = []
    for i in range(0, size):  # it must be the length of the display
        if i < dots_length:
            cells.append(dots[i])
        else:
            cells.append(0)
    return bytes(cells)


def place_cursor(dots, cursor_position):
    dots_length = len(dots)
    cells = []
    for i in range(0, dots_length):
        if i == cursor_position:
            cells.append(dots[i] | brlapi.DOT7 | brlapi.DOT8)
        else:
            cells.append(dots[i])
    return bytes(cells)


def message_to_display(m):
    text = m["message"]
    dots = text_to_dots(text)
    dots = dots_to_display_size(dots, m["displayWidth"])
    dots = place_cursor(dots, m["cursorPosition"])
    return dots


def print_diagnostics(brl):
    print_property("File Descriptor", str(brl.fileDescriptor))
    print_property("Server Host", str(brl.host))
    print_property("Authorization Schemes", str(brl.auth))
    print_property("Driver Name", str(brl.driverName))
    print_property("Model Identifier", str(brl.modelIdentifier))
    print_property("Display Width", str(brl.displaySize[0]))
    print_property("Display Height", str(brl.displaySize[1]))

    """
    print_property(".......", '.........................')
    print_property("DOT1", str(brlapi.DOT1))
    print_property("DOT2", str(brlapi.DOT2))
    print_property("DOT3", str(brlapi.DOT3))
    print_property("DOT4", str(brlapi.DOT4))
    print_property("DOT5", str(brlapi.DOT5))
    print_property("DOT6", str(brlapi.DOT6))
    print_property("DOT7", str(brlapi.DOT7))
    print_property("DOT8", str(brlapi.DOT8))
    """

    print_property(".......", ".........................")
    print_property("Louis version", str(louis.version()))
    print_property(".......", ".........................")


def print_log(m):
    if m["counter"] == 0:
        print_property("LOG", "Program Initialized")
        print_property("Counter", str(m["counter"]))
        print_property("Message", m["message"])
        print_property("Language", m["language"])
        print_property("Display Width", str(m["displayWidth"]))

    elif m["programStopped"]:
        print_property("LOG", "Program Stopped")
        print_property("Counter", str(m["counter"]))
        print_property("Message", m["message"])
        print_property("Text", m["text"])

    else:
        if m["stopProgram"]:
            print_property("LOG", "Program Stopping")
            print_property("Counter", str(m["counter"]))
        else:
            print_property("LOG", "Program Running")
            print_property("Counter", str(m["counter"]))

        if "code" in m:
            print_property("Code", hex(m["code"]))
            print_property("Type", str(hex(m["type"])))
            print_property("Command", str(hex(m["command"])))
            print_property("Argument", str(hex(m["argument"])))
            print_property("Flags", str(hex(m["flags"])))

        print_property("Message", m["message"])
        print_property("Text", m["text"])

    print_property("-------", "-------------------------")


# Message in local language
def get_message(display_width, language, code):
    if code == "start":
        if language == "fr":
            if display_width < 20:
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
    display_width = brl.displaySize[0]
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
        "displayWidth": display_width,
        "message": get_message(display_width, language, "start"),
    }


# Visualize the model on the braille displan
def view(brl, m):
    print_log(m)
    brl.writeDots(message_to_display(m))


# Update the model before leaving end
def update_before_leaving(m):
    m["modelChanged"] = True
    m["programStopped"] = True
    m["message"] = get_message(m["displayWidth"], m["language"], "end")
    return m


# Update the model based because time passed
def update_by_time(m):
    m["modelChanged"] = False
    return m


# Update the model based based on the key pressed
def update_by_key(brl, m, key_code):
    m["modelChanged"] = True
    m["counter"] = m["counter"] + 1

    # Keep information about the key pressed in the model
    k = brl.expandKeyCode(key_code)
    m["code"] = key_code
    m["type"] = k["type"]
    m["command"] = k["command"]
    m["argument"] = k["argument"]
    m["flags"] = k["flags"]

    m["brailleCommand"] = (key_code & brlapi.KEY_TYPE_MASK) == brlapi.KEY_TYPE_CMD
    m["keysym"] = (key_code & brlapi.KEY_TYPE_MASK) == brlapi.KEY_TYPE_SYM

    m["brailleRouteCommand"] = (
        key_code & brlapi.KEY_CMD_BLK_MASK
    ) == brlapi.KEY_CMD_ROUTE
    m["highlightedCell"] = key_code & brlapi.KEY_CMD_ARG_MASK
    m["commandFlags"] = key_code & brlapi.KEY_FLAGS_MASK
    # m['shiftModifier'] = (key_code & brlapi.KEY_FLAGS_MASK) == brlapi.KEY_FLG_SHIFT
    #  AttributeError: module 'brlapi' has no attribute 'KEY_FLG_SHIFT'

    m["tabKey"] = (key_code & brlapi.KEY_CODE_MASK) == brlapi.KEY_SYM_TAB
    m["unicodeKeysym"] = (key_code & brlapi.KEY_SYM_UNICODE) != 0
    m["unicodeKeysymValue"] = key_code & (brlapi.KEY_SYM_UNICODE - 1)

    # Type: brlapi.KEY_TYPE_CMD == 0x20000000

    if key_code == brlapi.KEY_TYPE_CMD:
        m["modelChanged"] = False

    elif key_code == brlapi.KEY_TYPE_CMD | brlapi.KEY_CMD_LNUP:
        m["message"] = "Line Up - Left panning button UP"
    elif key_code == brlapi.KEY_TYPE_CMD | brlapi.KEY_CMD_LNDN:
        m["message"] = "Line Down - Left panning button DOWN"

    elif key_code == brlapi.KEY_TYPE_CMD | brlapi.KEY_CMD_HOME:
        m["message"] = "Home Button - Selector button RIGHT"
    elif key_code == brlapi.KEY_TYPE_CMD | brlapi.KEY_CMD_BACK:
        m["message"] = "Go back after cursor tracking - Selector button LEFT"

    elif key_code == brlapi.KEY_TYPE_CMD | brlapi.KEY_CMD_LNBEG:
        m["message"] = "Go to beginning of line - mode button left"
    elif key_code == brlapi.KEY_TYPE_CMD | brlapi.KEY_CMD_LNEND:
        m["message"] = "Go to end of line - mode button right"

    elif key_code == brlapi.KEY_TYPE_CMD | brlapi.KEY_CMD_FWINLT:
        m["message"] = "Go backward one braille window - Panning button LEFT"
    elif key_code == brlapi.KEY_TYPE_CMD | brlapi.KEY_CMD_FWINRT:
        m["message"] = "Go forward one braille window - Panning button RIGHT"

    elif key_code == brlapi.KEY_TYPE_CMD | 0x220000:  # Space bar
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
        m = handle_text_input(m)
        m["message"] = m["text"]
        m["cursorPosition"] = len(m["text"])
        m["showCursor"] = True

    elif (m["type"] == brlapi.KEY_TYPE_CMD) and (m["command"] == 0x10000):
        m["cursorPosition"] = m["argument"]
        m["showCursor"] = True

    elif key_code == brlapi.KEY_SYM_UP:
        m["message"] = "KEY_SYM_UP - Left rocker bar UP"
    elif key_code == brlapi.KEY_SYM_DOWN:
        m["message"] = "KEY_SYM_DOWN - Left rocker bar DOWN"

    elif key_code == 0xFF0D:  # Enter
        m["text"] = m["text"] + "/n"
        m["message"] = m["text"]
        m["cursorPosition"] = len(m["text"])

    elif key_code == 0xFF08:  # Delete
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
        print_property("Initialization", "Before Connection")
        # Initialization
        b = brlapi.Connection()
        b.enterTtyModeWithPath()
        b.acceptKeys(brlapi.rangeType_all, [0])
        print_diagnostics(b)

        # The architecture
        model = init(b)
        view(b, model)
        wait_for_key_press = True
        while not model["stopProgram"]:
            key = b.readKey(not wait_for_key_press)
            if not key:
                model = update_by_time(model)
            else:
                model = update_by_key(b, model, key)

            if model["modelChanged"]:
                model["modelChanged"] = False
                view(b, model)

        model = update_before_leaving(model)
        view(b, model)
        key = b.readKey(wait_for_key_press)

        b.leaveTtyMode()
        b.closeConnection()

    # Error Handling
    except brlapi.ConnectionError as e:
        if e.brlerrno == brlapi.ERROR_CONNREFUSED:
            print_property(
                "Connection refused",
                "Connection to %s refused. BRLTTY is too busy..." % (e.host),
            )
        elif e.brlerrno == brlapi.ERROR_AUTHENTICATION:
            print_property(
                "Authentication failed.",
                "Authentication with %s failed. Please check the permissions of %s"
                % (e.host, e.auth),
            )
        elif e.brlerrno == brlapi.ERROR_LIBCERR and (
            e.libcerrno == errno.ECONNREFUSED or e.libcerrno == errno.ENOENT
        ):
            print_property(
                "Connection failed",
                "Connection to %s failed. Is BRLTTY really running?" % (e.host),
            )
        else:
            print_property(
                "Connection to BRLTTY failed",
                "Connection to BRLTTY at %s failed: " % (e.host),
            )
        print_property("error", str(e))
        print_property("error.brlerrno", str(e.brlerrno))
        print_property("error.libcerrno", str(e.libcerrno))


if __name__ == "__main__":
    main()
