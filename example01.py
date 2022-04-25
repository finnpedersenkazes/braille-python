import brlapi
import errno
import Xlib.keysymdef.miscellany
try:
  b = brlapi.Connection()
  b.enterTtyMode(1)
  b.ignoreKeys(brlapi.rangeType_all,[0])

  # Accept the home, window up and window down braille commands
  b.acceptKeys(brlapi.rangeType_command,[brlapi.KEY_TYPE_CMD|brlapi.KEY_CMD_HOME, brlapi.KEY_TYPE_CMD|brlapi.KEY_CMD_WINUP, brlapi.KEY_TYPE_CMD|brlapi.KEY_CMD_WINDN])

  # Accept the tab key
  b.acceptKeys(brlapi.rangeType_key,[brlapi.KEY_TYPE_SYM|Xlib.keysymdef.miscellany.XK_Tab])

  b.writeText("Press home, winup/dn or tab to continue ...")
  key = b.readKey()

  k = b.expandKeyCode(key)
  b.writeText("Key %ld (%x %x %x %x) !" % (key, k["type"], k["command"], k["argument"], k["flags"]))
  b.writeText(None,1)
  b.readKey()

  underline = chr(brlapi.DOT7 + brlapi.DOT8)
  # Note: center() can take two arguments only starting from python 2.4
  b.write(
      regionBegin = 1,
      regionSize = 40,
      text = "Press any key to exit                 ",
      orMask = "".center(21,underline) + "".center(19,chr(0)))

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
