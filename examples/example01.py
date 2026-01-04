#!/usr/bin/env python3

"""
Example 01 - Keyboard Input with Diagnostics
Demonstrates Elm architecture pattern (Model-Update-View)
Reads keyboard input, displays key information, and captures typed text
"""

import brlapi
import errno
import Xlib.keysymdef.miscellany


def write_property(name, value):
    """Print a property in a structured format"""
    print(f"{name}: {value}")


def print_diagnostics(brl):
    """Display braille display connection information"""
    write_property("File Descriptor", str(brl.fileDescriptor))
    write_property("Server Host", str(brl.host))
    write_property("Authorization Schemes", str(brl.auth))
    write_property("Driver Name", str(brl.driverName))
    write_property("Model Identifier", str(brl.modelIdentifier))
    write_property("Display Width", str(brl.displaySize[0]))
    write_property("Display Height", str(brl.displaySize[1]))
    write_property("-------", "-------------------------")


def print_log(m):
    """Log current model state"""
    if m["counter"] == 0:
        write_property("LOG", "Program Initialized")
        write_property("Message", m["message"])
    else:
        write_property("LOG", f"Key Press #{m['counter']}")
        write_property("Code", m["code"])
        write_property("Type", hex(m["type"]))
        write_property("Command", hex(m["command"]))
        write_property("Argument", hex(m["argument"]))
        write_property("Flags", hex(m["flags"]))
        write_property("Message", m["message"])
        write_property("Text", m["text"])
    write_property("-------", "-------------------------")


def init():
    """Initialize the model (Elm architecture)"""
    return {
        "counter": 0,
        "text": "",
        "code": "",
        "type": 0,
        "command": 0,
        "argument": 0,
        "flags": 0,
        "message": "Press a key (max 20 keypresses)..."
    }


def view(brl, m):
    """Display the model on braille display (Elm architecture)"""
    print_log(m)
    if m["counter"] == 0:
        brl.writeText(m["message"])
    else:
        brl.writeText(f"Count: {m['counter']}, {m['message']}, {m['text']}")


def update(brl, m, keyCode):
    """Update model based on key press (Elm architecture)"""
    # Keep information about the key pressed in the model
    k = brl.expandKeyCode(keyCode)
    m["code"] = f"0x{keyCode:X}"
    m["type"] = k["type"]
    m["command"] = k["command"]
    m["argument"] = k["argument"]
    m["flags"] = k["flags"]
    
    # Capture text input
    if m["type"] == 0:
        m["text"] = m["text"] + chr(m["argument"])
    
    # Update counter and message
    m["counter"] = m["counter"] + 1
    
    # Identify specific keys
    if keyCode == brlapi.KEY_TYPE_CMD | brlapi.KEY_CMD_HOME:
        m["message"] = "Home Button"
    elif keyCode == brlapi.KEY_TYPE_CMD | brlapi.KEY_CMD_LNUP:
        m["message"] = "Line Up"
    elif keyCode == brlapi.KEY_TYPE_CMD | brlapi.KEY_CMD_LNDN:
        m["message"] = "Line Down"
    elif keyCode == brlapi.KEY_TYPE_SYM | Xlib.keysymdef.miscellany.XK_Tab:
        m["message"] = "Tab"
    else:
        m["message"] = "Key pressed"
    
    return m


def main():
    try:
        # Connection and Initialization
        b = brlapi.Connection()
        print_diagnostics(b)
        b.enterTtyModeWithPath()

        # Elm Architecture: Model-Update-View loop
        model = init()
        while model["counter"] < 20:
            view(b, model)
            key = b.readKey()
            if not key:
                print("No key received")
                continue
            model = update(b, model, key)

        # Cleanup
        b.leaveTtyMode()
        b.closeConnection()

    except brlapi.ConnectionError as e:
        if e.brlerrno == brlapi.ERROR_CONNREFUSED:
            print(f"Connection to {e.host} refused. BRLTTY is too busy...")
        elif e.brlerrno == brlapi.ERROR_AUTHENTICATION:
            print(f"Authentication with {e.host} failed. Please check the permissions of {e.auth}")
        elif e.brlerrno == brlapi.ERROR_LIBCERR and (
            e.libcerrno == errno.ECONNREFUSED or e.libcerrno == errno.ENOENT
        ):
            print(f"Connection to {e.host} failed. Is BRLTTY really running?")
        else:
            print(f"Connection to BRLTTY at {e.host} failed: ")
        print(e)
        print(f"Error number: {e.brlerrno}")
        print(f"Lib error: {e.libcerrno}")


if __name__ == "__main__":
    main()
