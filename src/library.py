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

def format_time_stamp(date_time):
    """Format datetime for use in filenames"""
    return date_time.isoformat()[:16].replace(":", "-")


# Global values for logging
CURRENT_DATE_TIME = datetime.datetime.now()
LOG_DIR = os.path.join(os.path.expanduser("~"), "Documents")
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE_NAME = os.path.join(LOG_DIR, format_time_stamp(CURRENT_DATE_TIME) + "_log.txt")


def print_property(name, value):
    """Helper function to print debug information to the log"""
    text = name + ": " + value
    print(text)
    with open(LOG_FILE_NAME, "a", encoding="utf-8") as f:
        f.write(text)
        f.write("\n")


def print_diagnostics(brl):
    """Print BrlAPI diagnostics information"""
    print_property("File Descriptor", str(brl.fileDescriptor))
    print_property("Server Host", str(brl.host))
    print_property("Authorization Schemes", str(brl.auth))
    print_property("Driver Name", str(brl.driverName))
    print_property("Model Identifier", str(brl.modelIdentifier))
    print_property("Display Width", str(brl.displaySize[0]))
    print_property("Display Height", str(brl.displaySize[1]))
    print_property(".......", ".........................")
    print_property("DOT1", str(brlapi.DOT1))
    print_property("DOT2", str(brlapi.DOT2))
    print_property("DOT3", str(brlapi.DOT3))
    print_property("DOT4", str(brlapi.DOT4))
    print_property("DOT5", str(brlapi.DOT5))
    print_property("DOT6", str(brlapi.DOT6))
    print_property("DOT7", str(brlapi.DOT7))
    print_property("DOT8", str(brlapi.DOT8))
    print_property(".......", ".........................")
    print_property("Louis version", str(louis.version()))
    print_property(".......", ".........................")


# ============================================================================
# Braille conversion utilities
# ============================================================================

def translation_list():
    """Get braille translation table list"""
    return [b"fr-bfu-comp6.utb"]
    # return [b'fr-bfu-comp8.utb']
    # return [b'fr-bfu-g2.ctb']
    # return [b'da-dk-g16.ctb']
    # return [b'da-dk-g18.ctb']


def adjust_number(n):
    """Adjust number for braille translation"""
    return n - 32768  # = 2^15


def char_to_dots(char):
    """Convert character to braille dots"""
    louis_dots = louis.charToDots(translation_list(), char, len(char))
    ord_dots = ord(louis_dots)
    adjusted_dots = adjust_number(ord_dots)
    return adjusted_dots


def text_to_dots(text):
    """Convert text to braille dots array"""
    translated_text = louis.translateString(translation_list(), text)
    print_property("translatedText", translated_text)

    translated_text_array = list(translated_text)
    print_property("translatedTextArray", str(translated_text_array))

    dots_array = list(map(char_to_dots, translated_text_array))
    print_property("dotsArray", str(dots_array))

    return bytes(dots_array)


def dots_to_display_size(dots, size):
    """Adjust dots array to display size"""
    dots_length = len(dots)
    cells = []
    for i in range(0, size):  # it must be the length of the display
        if i < dots_length:
            cells.append(dots[i])
        else:
            cells.append(0)
    return bytes(cells)


def digit_dots(i):
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

def full_cell():
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


def underline_cell():
    """Get underline character for braille display"""
    return chr(brlapi.DOT7 + brlapi.DOT8)


def place_cursor(dots, cursor_position):
    """Place cursor at specified position in dots array"""
    dots_length = len(dots)
    cells = []
    for i in range(0, dots_length):
        if i == cursor_position:
            cells.append(dots[i] | brlapi.DOT7 | brlapi.DOT8)
        else:
            cells.append(dots[i])
    return bytes(cells)


def adjust_dots(d):
    """Adjust dots by adding offset (inverse of adjust_number)"""
    return d | 0x8000


def dots_to_char(modifier, dots):
    """Convert braille dots back to character with optional modifier"""
    def helper(dots):
        adjusted_number = adjust_dots(dots)
        chr_number = chr(adjusted_number)
        louis_chars = louis.dotsToChar(translation_list(), chr_number)
        return louis_chars

    if modifier > 0:
        louis_chars = helper(modifier) + helper(dots)
        text = louis.backTranslateString(translation_list(), louis_chars)
        chars = text[0]
        return chars

    louis_chars = helper(dots)
    text = louis.backTranslateString(translation_list(), louis_chars)
    chars = text[0]
    return chars


# ============================================================================
# Connection and error handling utilities
# ============================================================================

def handle_connection_error(e):
    """Handle BrlAPI connection errors with appropriate messages"""
    if e.brlerrno == brlapi.ERROR_CONNREFUSED:
        print_property(
            "Connection refused",
            f"Connection to {e.host} refused. BRLTTY is too busy...",
        )
    elif e.brlerrno == brlapi.ERROR_AUTHENTICATION:
        print_property(
            "Authentication failed.",
            f"Authentication with {e.host} failed. Please check the permissions of {e.auth}",
        )
    elif e.brlerrno == brlapi.ERROR_LIBCERR:
        import errno as err
        if e.libcerrno in (err.ECONNREFUSED, err.ENOENT):
            print_property(
                "Connection failed",
                f"Connection to {e.host} failed. Is BRLTTY really running?",
            )
    else:
        print_property(
            "Connection to BRLTTY failed",
            f"Connection to BRLTTY at {e.host} failed: ",
        )
    print_property("error", str(e))
    print_property("error.brlerrno", str(e.brlerrno))
    print_property("error.libcerrno", str(e.libcerrno))


def check_display_connected(brl):
    """Check if a braille display is actually connected"""
    if brl.displaySize[0] == 0 or brl.displaySize[1] == 0:
        print_property("WARNING", "No braille display detected! (displaySize is 0)")
        print_property(
            "Info",
            "The driver name may show a configured driver, but no physical device is connected.",
        )
        return False
    return True


# ============================================================================
# Key handling utilities
# ============================================================================

def write_property(name, value):
    """Alternative name for print_property (used in some examples)"""
    print_property(name, value)


# ============================================================================
# Braille character utilities
# ============================================================================

def char_to_braille_dots(char):
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
        'é': brlapi.DOT1 | brlapi.DOT2 | brlapi.DOT3 | brlapi.DOT4 | brlapi.DOT5 | brlapi.DOT6,  # Full cell
    }
    
    return braille_map.get(char, 0)


def braille_dots_to_char(dots):
    """
    Convert braille dot pattern back to character (inverse of char_to_braille_dots)
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


def combine_keys_to_dots(dot_list):
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

def random_char():
    """Get a random lowercase letter a-z"""
    import random
    return random.choice('abcdefghijklmnopqrstuvwxyz')


def random_position(max_position):
    """Get a random position from 0 to max_position-1"""
    import random
    return random.randint(0, max_position - 1)

