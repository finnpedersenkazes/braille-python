"""
Model module - Elm-like architecture for braille game
Contains data structures and state initialization
"""

from library import printProperty, printDiagnostics, currentDateTime


def getMessage(displayWidth, language, code):
    """Get localized message based on language and code"""
    if code == "start":
        if language == "fr":
            if displayWidth < 20:
                message = "Touche éspace"
            else:
                message = "Appuyez sur une touche"
        else:
            message = "Press any key"
    elif code == "highscore":
        if language == "fr":
            message = "Max points :"
        else:
            message = "Max score:"
    elif code == "points":
        if language == "fr":
            message = "Points :"
        else:
            message = "Points:"
    elif code == "birthday":
        if language == "fr":
            if displayWidth > 19:
                message = "Joyeux anniversaire"
            else:
                message = "Bon anniversaire"
        else:
            message = "Happy birthday"
    else:
        message = ""
    return message


def init(brl):
    """
    Initialize the model.
    This should define all possible states.
    """
    displayWidth = brl.displaySize[0]
    numberOfBlocks = displayWidth // 5
    if numberOfBlocks >= 6:
        pointBlocks = 2
    else:
        pointBlocks = 1
    language = "en"  # or 'fr'

    return {
        "cursorPos": 0,  # 0..3
        "obstaclePos": 9,  # 0..4
        "points": 0,  # 0..999
        "collision": False,
        "stop": False,
        "gameCounter": 0,
        "highScore": 0,
        "counter": 0,
        "text": "",
        "language": language,
        "displayWidth": displayWidth,
        "message": getMessage(displayWidth, language, "start"),
        "pointBlocks": pointBlocks,
        "gameBlocks": numberOfBlocks - pointBlocks,
        "gameDuration": 30,  # seconds
    }


def printLog(m):
    """Print model state to log"""
    if m["counter"] == 0:
        printProperty("LOG", "Program Initialized")
        printProperty("Counter", str(m["counter"]))
        printProperty("Message", m["message"])
        printProperty("Language", m["language"])
        printProperty("Display Width", str(m["displayWidth"]))
        printProperty("Point Blocks", str(m["pointBlocks"]))
        printProperty("Game Blocks", str(m["gameBlocks"]))
        printProperty("Game Duration", str(m["gameDuration"]))
    else:
        printProperty("LOG", "Program Started")
        if "code" in m:
            printProperty("Code", str(m["code"]))
            printProperty("Type", str(m["type"]))
            printProperty("Command", str(m["command"]))
            printProperty("Argument", str(m["argument"]))
            printProperty("Flags", str(m["flags"]))
            printProperty("Counter", str(m["counter"]))
        printProperty("Message", m["message"])
        printProperty("Text", m["text"])
        printProperty("Cursor Position", str(m["cursorPos"]))
        printProperty("Obstacle Posistion", str(m["obstaclePos"]))
        printProperty("Points", str(m["points"]))
        printProperty("Game Counter", str(m["gameCounter"]))
        printProperty("High Score", str(m["highScore"]))

    printProperty("-------", "-------------------------")


def printDiagnostics(brl):
    """Print BrlAPI diagnostics information"""
    import brlapi
    import louis

    printProperty("File Descriptor", str(brl.fileDescriptor))
    printProperty("Server Host", str(brl.host))
    printProperty("Authorization Schemes", str(brl.auth))
    printProperty("Driver Name", str(brl.driverName))
    printProperty("Model Identifier", str(brl.modelIdentifier))
    printProperty("Display Width", str(brl.displaySize[0]))
    printProperty("Display Height", str(brl.displaySize[1]))
    printProperty(".......", ".........................")
    printProperty("DOT1", str(brlapi.DOT1))
    printProperty("DOT2", str(brlapi.DOT2))