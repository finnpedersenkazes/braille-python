#!/bin/python

import brlapi
import time

brl = brlapi.Connection()
brl.enterTtyModeWithPath()
print("display size: " + str(brl.displaySize))
print("driver name: " + str(brl.driverName))

try:
    brl.writeText("This is a 5 sec test")
    print("writing text for 5 seconds...")

except Exception as e:
    print(e)

time.sleep(5)
print("Stop...")

brl.leaveTtyMode()
brl.closeConnection()
