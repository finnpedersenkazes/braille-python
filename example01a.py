import brlapi
import errno
import Xlib.keysymdef.miscellany

# Helper functions to print debug information to the log
def print_diagnostics():
    k = b.expandKeyCode(brlapi.KEY_CMD_HOME)
    print("Key (Type %x, Command %x, Argument %x, Flags %x) !" %(k["type"], k["command"], k["argument"], k["flags"]))
    print('display size' + str(b.displaySize))
    print('driver name'+str(b.driverName))
    print()

def print_log(m):
    if m['counter'] == 0:
        print_diagnostics()
        print(m['message'])
        print()
    else:
        print("Key (Type %x, Command %x, Argument %x, Flags %x) !" %(m["type"], m["command"], m["argument"], m["flags"]))
        print("Counter: %s" %(m['counter']))
        print(m['message'][0:40])
        print()

# Initialize the model.
# This should define all possible states.
def init():
    return {
        'counter': 0,
        'message': "Press home, winup/dn or tab to continue ..."
    }

# Visualize the model on the braille displan
def view(m):
    print_log(m)
    if m['counter'] == 0:
        b.writeText(m['message'])
    else:
        b.writeText("Count: %s, %s" %(m['counter'],m['message']))

# Update the model based based on the key pressed
def update(m, keyCode):

    # Keep information about the key pressed in the model
    k = b.expandKeyCode(keyCode)
    m["type"] = k["type"]
    m["command"] = k["command"]
    m["argument"] = k["argument"]
    m["flags"] = k["flags"]

    # Update the model
    # if key == brlapi.KEY_CMD_HOME:
    m['counter'] = m['counter'] + 1
    m['message'] = "Home Button"
    return m

try:
    # Connection and Initialization
    b = brlapi.Connection()
    b.enterTtyMode(1)
    b.acceptKeys(brlapi.rangeType_all,[0])

    # The architecture
    model = init()
    while model['counter'] < 20:
        view(model)
        key = b.readKey()
        model = update(model, key)

    # Close the connection
    b.leaveTtyMode()
    b.closeConnection()

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

