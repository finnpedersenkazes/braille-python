#!/bin/python3

# This example fills the display with dots
#

import brlapi
import time


def main():
    brl = brlapi.Connection()
    # brl.enterTtyMode(1)
    brl.enterTtyModeWithPath()

    (displayLength, displayHeight) = brl.displaySize

    print("display size: %i x %i" % (displayLength, displayHeight))
    print("driver name: " + str(brl.driverName))

    start = time.time()
    c = 0
    fullCell = (
        brlapi.DOT1
        | brlapi.DOT2
        | brlapi.DOT3
        | brlapi.DOT4
        | brlapi.DOT5
        | brlapi.DOT6
        | brlapi.DOT7
        | brlapi.DOT8
    )
    cells = []
    for i in range(displayLength):
        cells.append(fullCell)

    try:
        while c < displayLength * 8:
        t = time.time()
        timepassed = round(t - start)
        time.sleep(0.1)
        if c % 8 == 0:
            dot = brlapi.DOT1
        elif c % 8 == 1:
            dot = dot | brlapi.DOT2
        elif c % 8 == 2:
            dot = dot | brlapi.DOT3
        elif c % 8 == 3:
            dot = dot | brlapi.DOT7
        elif c % 8 == 4:
            dot = dot | brlapi.DOT8
        elif c % 8 == 5:
            dot = dot | brlapi.DOT6
        elif c % 8 == 6:
            dot = dot | brlapi.DOT5
        else:  # c % 8 == 7:
            dot = dot | brlapi.DOT4

        cells = []
        for i in range(displayLength):
            if c // 8 == i:
                cells.append(dot)
            else:
                if i * 8 < c:
                    cells.append(fullCell)
                else:
                    cells.append(0)

        print("c: %s, dot: %s, time: %s seconds" % (str(c), str(dot), str(timepassed)))

        brl.writeDots(bytes(cells))

        c = c + 1

    except Exception as e:
        print(e)

    brl.leaveTtyMode()
    brl.closeConnection()


if __name__ == "__main__":
    main()
