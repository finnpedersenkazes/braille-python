#!/bin/python

import brlapi
import time

brl = brlapi.Connection()
brl.enterTtyModeWithPath()
print("display size: " + str(brl.displaySize))
print("driver name: " + str(brl.driverName))

try:
    brl.writeText("this is a 5 second test")

except Exception as e:
    print(e)

time.sleep(5)
brl.leaveTtyMode()
brl.closeConnection()
