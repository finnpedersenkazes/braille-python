#!/usr/bin/env python3

"""
Example 02b - Traveling Dot Animation
Demonstrates animated dot moving across braille display
Shows all 8 dot positions in each cell
"""

import time

import brlapi


def main():
    brl = brlapi.Connection()
    brl.enterTtyModeWithPath()

    (display_length, display_height) = brl.displaySize

    print(f"display size: {display_length} x {display_height}")
    print("driver name: " + str(brl.driverName))

    start = time.time()
    c = 0
    dot = brlapi.DOT1
    cells = []
    for _i in range(display_length):
        cells.append(dot)

    try:
        while c < display_length * 8:
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
            else:  # c % 8 == 7:
                dot = brlapi.DOT4

            cells = []
            for i in range(display_length):
                if c // 8 == i:
                    cells.append(dot)
                else:
                    cells.append(0)

            print(f"c: {c}, dot: {dot}, time: {timepassed}")

            brl.writeDots(bytes(cells))

            c = c + 1

    except Exception as e:
        print(e)

    brl.leaveTtyMode()
    brl.closeConnection()


if __name__ == "__main__":
    main()
