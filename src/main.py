#!/usr/bin/env python3

"""
Main entry point for the braille game
Following Elm-like architecture with Model-Update-View pattern
"""

import brlapi
import errno
import time

# Import from our Elm-like libraries
from model import init, getMessage
from library import (
    printProperty,
    printDiagnostics,
    currentDateTime,
    handleConnectionError,
)
from update import (
    updateByGameStart,
    updateByGameEnd,
    updateHighScoreMessage,
    updateByTime,
    updateByKey,
)
from view import view


def main():
    """Main game loop"""
    try:
        printProperty("Initialization", "Before Connection")
        # Initialization
        b = brlapi.Connection()
        b.enterTtyModeWithPath()
        b.acceptKeys(brlapi.rangeType_all, [0])
        printDiagnostics(b)

        # Surprise
        if currentDateTime.month == 5:
            # Happy birthday
            model = init(b)
            model["message"] = getMessage(
                model["displayWidth"], model["language"], "birthday"
            )
            view(b, model)
            time.sleep(10)

        # The architecture
        model = init(b)
        view(b, model)
        delay = 0.1  # seconds
        waitForKeyPress = True
        for _ in range(0, 1):  # TODO change to 3
            key = b.readKey(waitForKeyPress)
            model = updateByGameStart(model)
            while not model["stop"]:
                key = b.readKey(not waitForKeyPress)
                if not key:
                    time.sleep(delay)
                    model = updateByTime(model)
                else:
                    model = updateByKey(b, model, key)

                view(b, model)

            model = updateByGameEnd(model)
            view(b, model)
            time.sleep(10)

        model = updateHighScoreMessage(model)
        view(b, model)
        time.sleep(10)

        b.leaveTtyMode()
        b.closeConnection()

    # Error Handling
    except brlapi.ConnectionError as e:
        handleConnectionError(e)


if __name__ == "__main__":
    main()
