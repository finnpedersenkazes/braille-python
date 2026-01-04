#!/usr/bin/env python3

"""
Example 02a - Counter Display Animation
Demonstrates animated counting from 0 to 100 on braille display
No keyboard input required
"""

import time

import brlapi


def main():
    brl = brlapi.Connection()
    brl.enterTtyModeWithPath()
    print("display size: " + str(brl.displaySize))
    print("driver name: " + str(brl.driverName))

    # Check if a braille display is actually connected
    if brl.displaySize[0] == 0 or brl.displaySize[1] == 0:
        print("WARNING: No braille display detected! (displaySize is 0)")
        print("The driver name may show a configured driver, but no physical device is connected.")
        return

    c = 0
    try:
        while c <= 100:
            c = c + 1
            time.sleep(0.1)
            brl.writeText(f"counter: {c}")

    except Exception as e:
        print(e)

    time.sleep(5)
    brl.leaveTtyMode()
    brl.closeConnection()


if __name__ == "__main__":
    main()
