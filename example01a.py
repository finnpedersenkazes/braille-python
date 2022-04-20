import brlapi
import errno
# import Xlib.keysymdef.miscellany


def init():
    return {
        'counter': 0,
        'message': "Press home, winup/dn or tab to continue ..."
    }

def view(m):
    if m['counter'] == 0:
        k = b.expandKeyCode(brlapi.KEY_CMD_HOME)
        print("Key (Type %x, Command %x, Argument %x, Flags %x) !" %(k["type"], k["command"], k["argument"], k["flags"]))
        print('display size' + str(b.displaySize))
        print('driver name'+str(b.driverName))
        print(m['message'])
        b.writeText(m['message'])
        print()
    else:
        print("Key (Type %x, Command %x, Argument %x, Flags %x) !" %(m["type"], m["command"], m["argument"], m["flags"]))
        print("Counter: %s" %(m['counter']))
        print(m['message'][0:40])
        print()
        b.writeText("Count: %s, %s" %(m['counter'],m['message']))

def update(m, keyCode):
    k = b.expandKeyCode(keyCode)
    m["type"] = k["type"]
    m["command"] = k["command"]
    m["argument"] = k["argument"]
    m["flags"] = k["flags"]

#    if key == brlapi.KEY_CMD_HOME:
    m['counter'] = m['counter'] + 1
    m['message'] = "Home Button"

    return m


try:
    b = brlapi.Connection()
    b.enterTtyMode(1)
    b.acceptKeys(brlapi.rangeType_all,[0])

  # b.ignoreKeys(brlapi.rangeType_all,[0])

  # Accept the home, window up and window down braille commands
  # b.acceptKeys(brlapi.rangeType_command,[brlapi.KEY_TYPE_CMD|brlapi.KEY_CMD_HOME, brlapi.KEY_TYPE_CMD|brlapi.KEY_CMD_WINUP, brlapi.KEY_TYPE_CMD|brlapi.KEY_CMD_WINDN])

  # Accept the tab key
  # b.acceptKeys(brlapi.rangeType_key,[brlapi.KEY_TYPE_SYM|Xlib.keysymdef.miscellany.XK_Tab])


  # init model
    model = init()

  # loop

  #  for i in range(1, 5):
    while model['counter'] < 20:
    # view model
        view(model)

        key = b.readKey()

        model = update(model, key)

  # b.writeText(None,1)
  # b.readKey()

  # underline = chr(brlapi.DOT7 + brlapi.DOT8)
  # Note: center() can take two arguments only starting from python 2.4

  # https://brltty.app/doc/BrlAPIref/structbrlapi__writeArguments__t.html

  # b.write(
  #     regionBegin = 1,
  #     regionSize = 40,
  #     text = "Press any key to exit                 ",
  #     orMask = "".center(21,underline) + "".center(19,chr(0)))

    b.acceptKeys(brlapi.rangeType_all,[0])
    b.readKey()

    b.leaveTtyMode()
    b.closeConnection()

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

