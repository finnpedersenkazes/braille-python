#!/bin/python

import brlapi
import time


def main():
    brl = brlapi.Connection()
    brl.enterTtyModeWithPath()
    print("display size: " + str(brl.displaySize))
    print("driver name: " + str(brl.driverName))

    try:
        brl.writeText("This is a 5 sec test")
        print("writing text for 5 seconds...")
        time.sleep(5)
        brl.writeText("Stop")

    except Exception as e:
        print(e)

    print("Stop...")

    brl.leaveTtyMode()
    brl.closeConnection()


if __name__ == "__main__":
    main()
