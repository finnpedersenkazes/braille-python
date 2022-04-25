#!/bin/python3

# This example read the keypress'

import brlapi
import errno
import Xlib.keysymdef.miscellany




# Helper functions to print debug information to the log

def writeProperty (name, value):
    #try:
    #    value = value.decode("utf-8")
    #except AttributeError:
    #    pass

    # sys.stdout.write(name + ": " + value + "\n")
    print(name + ": " + value)

    # source
    # https://github.com/brltty/brltty/blob/f72a1f8ce45436365523ab29ce8eaf2429caf4a8/Bindings/Python/apitest.py

def print_diagnostics(b):
    writeProperty("File Descriptor", str(b.fileDescriptor))
    writeProperty("Server Host", str(b.host))
    writeProperty("Authorization Schemes", str(b.auth))
    writeProperty("Driver Name", str(b.driverName))
    writeProperty("Model Identifier", str(b.modelIdentifier))
    writeProperty("Display Width", str(b.displaySize[0]))
    writeProperty("Display Height", str(b.displaySize[1]))
    writeProperty(".......", '.........................')

def print_log(m):
    if m['counter'] == 0:
        writeProperty("LOG", 'Program Initialized')
        writeProperty("Counter", str(m['counter']))
        writeProperty("Message", m['message'])
    else:
        writeProperty("LOG", 'Program Started')
        writeProperty("Type", str(m["type"]))
        writeProperty("Command", str(m["command"]))
        writeProperty("Argument", str(m["argument"]))
        writeProperty("Flags", str(m["flags"]))
        writeProperty("Counter", str(m['counter']))
        writeProperty("Message", m['message'])

    writeProperty("-------", '-------------------------')

# Template functions
def establishConnection(b):
    # Connection and Initialization
    print_diagnostics(b)
    b.enterTtyMode(1)
    b.acceptKeys(brlapi.rangeType_all,[0])

def closeConnection(b):
   # Close the connection
    b.leaveTtyMode()
    b.closeConnection()

# Initialize the model.
# This should define all possible states.
def init():
    return {
        'counter': 0,
        'message': "Press home, winup/dn or tab to continue ..."
    }

# Visualize the model on the braille displan
def view(b, m):
    print_log(m)
    if m['counter'] == 0:
        b.writeText(m['message'])
    else:
        b.writeText("Count: %s, %s" %(m['counter'],m['message']))

# Update the model based based on the key pressed
def update(b, m, keyCode):
    # Keep information about the key pressed in the model
    k = b.expandKeyCode(keyCode)
    m["code"] = "0X%X" % keyCode
    m["type"] = k["type"]
    m["command"] = k["command"]
    m["argument"] = k["argument"]
    m["flags"] = k["flags"]

    # Update the model
    m['counter'] = m['counter'] + 1
    if keyCode == brlapi.KEY_TYPE_CMD|brlapi.KEY_CMD_HOME:
        m['message'] = "Home Button"
    elif keyCode == brlapi.KEY_TYPE_CMD|brlapi.KEY_CMD_LNUP:
        m['message'] = "Line Up"
    elif keyCode == brlapi.KEY_TYPE_CMD|brlapi.KEY_CMD_LNDN:
        m['message'] = "Line Up"
    elif keyCode == brlapi.KEY_TYPE_SYM|Xlib.keysymdef.miscellany.XK_Tab:
        m['message'] = "Tab"
    else:
        m['message'] = "x-x-x-x-x-x"
    return m

try:
    # Initialization
    b = brlapi.Connection()
    establishConnection(b)
    timeout = 10 #seconds

    # The architecture
    model = init()
    while model['counter'] < 20:
        view(b, model)
        key = b.readKey()
        #key = b.readKeyWithTimeout(timeout * 1000)
        #if not key: break
        
        model = update(b, model, key)

    closeConnection(b)

# Error Handling
except brlapi.ConnectionError as e:
    if e.brlerrno == brlapi.ERROR_CONNREFUSED:
        print("Connection to %s refused. BRLTTY is too busy..." %(e.host))
    elif e.brlerrno == brlapi.ERROR_AUTHENTICATION:
        print("Authentication with %s failed. Please check the permissions of %s" %(e.host,e.auth))
    elif e.brlerrno == brlapi.ERROR_LIBCERR and (e.libcerrno == errno.ECONNREFUSED or e.libcerrno == errno.ENOENT):
        print("Connection to %s failed. Is BRLTTY really running?" %(e.host))
    else:
        print("Connection to BRLTTY at %s failed: " %(e.host))
    print(e)
    print(e.brlerrno)
    print(e.libcerrno)

