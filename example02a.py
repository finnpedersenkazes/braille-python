#!/bin/python3

# This example counts to 100 on the display. No key input.

import brlapi
import time

brl = brlapi.Connection()
brl.enterTtyModeWithPath()
print("display size: " + str(brl.displaySize))
print("driver name: " + str(brl.driverName))

t = time.time()
c = 0
try:
    while c <= 100:
        c = c + 1
        time.sleep(0.1)
        brl.writeText("counter: %c" % (c))

except Exception as e:
    print(e)

time.sleep(5)
brl.leaveTtyMode()
brl.closeConnection()
