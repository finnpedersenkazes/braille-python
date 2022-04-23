#!/bin/python3

# This example counts to 100 on the display. No key input.

import brlapi
import time

brl = brlapi.Connection()
brl.enterTtyModeWithPath()

(displayLength, displayHeight) = brl.displaySize 

print('display size: %i x %i' %(displayLength, displayHeight))
print('driver name: '+str(brl.driverName))

start = time.time()
c = 0
dot = brlapi.DOT1
cells = []
for i in range(40):
    cells.append(dot)

try:
    while(c < 320):
        t = time.time()
        timepassed = round(t - start)
        time.sleep(0.1)
        if c % 8 == 0:
            dot = brlapi.DOT1
        elif c % 8 == 1:
            dot = brlapi.DOT2
        elif c % 8 == 2:
            dot = brlapi.DOT3
        elif c % 8 == 3:
            dot = brlapi.DOT7
        elif c % 8 == 4:
            dot = brlapi.DOT8
        elif c % 8 == 5:
            dot = brlapi.DOT6
        elif c % 8 == 6:
            dot = brlapi.DOT5
        else: # c % 8 == 7:
            dot = brlapi.DOT4

        cells = []
        for i in range(40):
            if c // 8 == i:
                cells.append(dot)
            else:
                cells.append(0)
                
        print('c: %s, dot: %s, time: %s' %(str(c), str(dot), str(timepassed)))

        brl.writeDots(bytes(cells))

        c = c + 1

except Exception as e:
    print(e)

brl.leaveTtyMode()
brl.closeConnection()