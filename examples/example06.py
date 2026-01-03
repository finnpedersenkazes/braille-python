#!/usr/bin/env python3

"""Example 06: Character Identification Game

An educational braille game that teaches character-to-braille mapping.
The game displays a random character (a-z) at a random position on the braille display.

Display format (20 cells example):
- Cells 0-14: Game area - all blank except one cell showing the target character
- Cells 15-19: Score display - \"p\" followed by score digits (e.g., \"p00\", \"p05\", \"p12\")

Players must:
1. Find the character by pressing the cursor routing button under it
2. Type the character using braille dots (Grade 1 Braille)

The terminal screen shows the target position and character for learning.
The game provides immediate feedback and tracks score and attempts.

Architecture:
- Model: Game state with target character, position, score, and phase
- Update: Handles cursor presses, dot inputs, and phase transitions  
- View: Renders challenge display with score counter

Learning objectives:
- Spatial awareness on braille display
- Character-to-braille dot pattern mapping
- Braille keyboard input practice
"""

import brlapi
import sys
import os
import time

# Add src to path to import libraries
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from library import (
    printProperty,
    printDiagnostics,
    handleConnectionError,
    digitDots,
    tens,
    units,
    charToBrailleDots,
    brailleDotsToChar,
    combineKeysToDots,
    randomChar,
    randomPosition,
    dotsToDisplaySize,
)


# ============================================================================
# Model - Game state initialization
# ============================================================================

def getMessage(code, **params):
    """Get message based on code and parameters"""
    if code == "start":
        return "Press any key to start"
    elif code == "find":
        char = params.get("char", "?")
        pos = params.get("position", 0)
        return f"Find character '{char}' at position {pos} (press cursor button under it)"
    elif code == "waiting_position":
        char = params.get("char", "?")
        pos = params.get("position", 0)
        return f"Target: '{char}' at position {pos}. Click cursor button under it."
    elif code == "position_selected":
        pos = params.get("position", 0)
        char = params.get("char", "?")
        return f"Position {pos} selected. Now press dots for '{char}'"
    elif code == "correct":
        char = params.get("char", "?")
        score = params.get("score", 0)
        return f"Correct! '{char}' found. Score: {score}"
    elif code == "incorrect_position":
        return "Wrong position. Try again!"
    elif code == "incorrect_dots":
        return "Wrong dots. Try again!"
    elif code == "game_over":
        score = params.get("score", 0)
        attempts = params.get("attempts", 0)
        return f"Game Over! Score: {score}/{attempts}"
    else:
        return ""


def generateChallenge(displayWidth):
    """Generate new random character and position for challenge"""
    # Pick random character (a-z)
    targetChar = randomChar()
    
    # Pick random position in game area (last 5 cells reserved for score)
    gameWidth = displayWidth - 5
    targetPosition = randomPosition(gameWidth)
    
    return targetChar, targetPosition


def init(brl):
    """Initialize the game model with all possible states"""
    displayWidth = brl.displaySize[0]
    
    return {
        "targetChar": "",
        "targetPosition": 0,
        "displayWidth": displayWidth,
        "score": 0,
        "attempts": 0,
        "currentPhase": "start",  # "start", "waiting", "position_selected", "complete"
        "selectedPosition": None,
        "selectedDots": [],
        "message": getMessage("start"),
        "gameStarted": False,
        "counter": 0,
    }


def printLog(m):
    """Print model state to log"""
    printProperty("LOG", f"Phase: {m['currentPhase']}")
    printProperty("Counter", str(m["counter"]))
    printProperty("Message", m["message"])
    
    if m["gameStarted"]:
        printProperty("Target Char", m["targetChar"])
        printProperty("Target Position", str(m["targetPosition"]))
        printProperty("Score", str(m["score"]))
        printProperty("Attempts", str(m["attempts"]))
        
        if m["selectedPosition"] is not None:
            printProperty("Selected Position", str(m["selectedPosition"]))
        if m["selectedDots"]:
            printProperty("Selected Dots", str(m["selectedDots"]))
    
    printProperty("-------", "-------------------------")


# ============================================================================
# Update - Game logic and state updates
# ============================================================================

def updateByGameStart(m):
    """Initialize game and generate first challenge"""
    m["gameStarted"] = True
    targetChar, targetPosition = generateChallenge(m["displayWidth"])
    m["targetChar"] = targetChar
    m["targetPosition"] = targetPosition
    m["currentPhase"] = "waiting"
    m["message"] = getMessage("find", char=targetChar, position=targetPosition)
    m["attempts"] = 0
    m["score"] = 0
    return m


def updateByNewChallenge(m):
    """Generate new challenge"""
    targetChar, targetPosition = generateChallenge(m["displayWidth"])
    m["targetChar"] = targetChar
    m["targetPosition"] = targetPosition
    m["currentPhase"] = "waiting"
    m["selectedPosition"] = None
    m["selectedDots"] = []
    m["message"] = getMessage("find", char=targetChar, position=targetPosition)
    return m


def updateByCursorPress(m, position):
    """Handle cursor routing button press"""
    if m["currentPhase"] == "waiting":
        m["selectedPosition"] = position
        m["currentPhase"] = "position_selected"
        m["message"] = getMessage("position_selected", position=position, char=m["targetChar"])
        m["selectedDots"] = []  # Reset dots for new attempt
    return m


def updateByDotKey(m, dotNumber):
    """Handle braille keyboard dot key press (1-6)"""
    if m["currentPhase"] == "position_selected":
        # Add dot if not already in list
        if dotNumber not in m["selectedDots"]:
            m["selectedDots"].append(dotNumber)
            m["selectedDots"].sort()  # Keep sorted for consistency
        # Auto-submit if user has entered dots (simple approach: wait for space/enter)
    return m


def updateBySubmit(m):
    """Validate answer and update score"""
    if m["currentPhase"] == "position_selected" and m["selectedDots"]:
        # Check position
        if m["selectedPosition"] != m["targetPosition"]:
            m["message"] = getMessage("incorrect_position")
            m["selectedPosition"] = None
            m["selectedDots"] = []
            m["currentPhase"] = "waiting"
            return m
        
        # Check dots
        userDots = combineKeysToDots(m["selectedDots"])
        targetDots = charToBrailleDots(m["targetChar"])
        
        m["attempts"] += 1
        
        if userDots == targetDots:
            m["score"] += 1
            m["currentPhase"] = "complete"
            m["message"] = getMessage("correct", char=m["targetChar"], score=m["score"])
        else:
            m["message"] = getMessage("incorrect_dots")
            m["selectedDots"] = []
            # Stay in position_selected phase to try dots again
    
    return m


def updateByQuit(m):
    """End game"""
    m["message"] = getMessage("game_over", score=m["score"], attempts=m["attempts"])
    m["gameStarted"] = False
    m["currentPhase"] = "start"
    return m


def updateByKey(brl, m, keyCode):
    """Update model based on key press"""
    k = brl.expandKeyCode(keyCode)
    m["counter"] += 1
    
    # Check for cursor routing key (position selection)
    if (k["type"] == brlapi.KEY_TYPE_CMD) and (k["command"] == brlapi.KEY_CMD_ROUTE):
        position = k["argument"]
        m = updateByCursorPress(m, position)
    
    # Check for braille keyboard dot keys (command 0x220000 with argument as dots)
    elif (k["type"] == brlapi.KEY_TYPE_CMD) and (k["command"] == 0x220000) and (k["argument"] != 0):
        # Convert dot pattern to list of dot numbers
        dots_arg = k["argument"]
        dot_list = []
        if dots_arg & brlapi.DOT1: dot_list.append(1)
        if dots_arg & brlapi.DOT2: dot_list.append(2)
        if dots_arg & brlapi.DOT3: dot_list.append(3)
        if dots_arg & brlapi.DOT4: dot_list.append(4)
        if dots_arg & brlapi.DOT5: dot_list.append(5)
        if dots_arg & brlapi.DOT6: dot_list.append(6)
        
        # Add each dot
        for dot in dot_list:
            m = updateByDotKey(m, dot)
        
        # Auto-submit after receiving dot combination
        m = updateBySubmit(m)
    
    # Space bar - submit answer or start game
    elif keyCode == brlapi.KEY_TYPE_CMD | 0x220000:
        if m["currentPhase"] == "start":
            m = updateByGameStart(m)
        elif m["currentPhase"] == "position_selected":
            m = updateBySubmit(m)
        elif m["currentPhase"] == "complete":
            m = updateByNewChallenge(m)
    
    # Line Down - quit game
    elif keyCode == brlapi.KEY_TYPE_CMD | brlapi.KEY_CMD_LNDN:
        m = updateByQuit(m)
    
    # Home button - quit game
    elif keyCode == brlapi.KEY_TYPE_CMD | brlapi.KEY_CMD_HOME:
        m = updateByQuit(m)
    
    return m


# ============================================================================
# View - Game rendering
# ============================================================================

def scoreToDisplay(score):
    """Render score as braille cells (5 cells for right side display)
    Format: blank, blank, p, tens_digit, units_digit
    """
    cells = []
    cells.append(0)  # blank
    cells.append(0)  # blank
    cells.append(brlapi.DOT1 | brlapi.DOT2 | brlapi.DOT3 | brlapi.DOT4)  # p
    cells.append(digitDots(tens(score)))
    cells.append(digitDots(units(score)))
    return cells


def challengeToDisplay(m):
    """Render challenge character and fill other positions with blanks"""
    cells = []
    
    # Fill game area (display width minus 5 cells for score)
    gameWidth = m["displayWidth"] - 5
    for i in range(gameWidth):
        if i == m["targetPosition"]:
            cells.append(charToBrailleDots(m["targetChar"]))
        else:
            # Fill with blank
            cells.append(0)
    
    # Add score display on the right side
    cells.extend(scoreToDisplay(m["score"]))
    
    # Add cursor at selected position
    if m["selectedPosition"] is not None:
        for i in range(len(cells)):
            if i == m["selectedPosition"]:
                cells[i] |= brlapi.DOT7 | brlapi.DOT8
    
    return bytes(cells)


def gameToDots(m):
    """Convert game state to braille dots for display"""
    if not m["gameStarted"]:
        # Show start message
        cells = [0] * m["displayWidth"]
        return bytes(cells)
    
    return challengeToDisplay(m)


def view(brl, m):
    """Visualize the model on the braille display"""
    printLog(m)
    
    if m["displayWidth"] == 0:
        print("Warning: No braille display detected. Skipping writeDots.")
        return
    
    dots = gameToDots(m)
    dots = dotsToDisplaySize(dots, m["displayWidth"])
    brl.writeDots(dots)


# ============================================================================
# Main - Application entry point
# ============================================================================

def main():
    """Main game loop"""
    try:
        printProperty("Initialization", "Before Connection")
        
        # Initialization
        b = brlapi.Connection()
        b.enterTtyModeWithPath()
        b.acceptKeys(brlapi.rangeType_all, [0])
        printDiagnostics(b)
        
        # The architecture
        model = init(b)
        view(b, model)
        
        waitForKeyPress = True
        while model["currentPhase"] != "quit":
            key = b.readKey(waitForKeyPress)
            
            if key:
                model = updateByKey(b, model, key)
                view(b, model)
                
                # Generate new challenge after completing one
                if model["currentPhase"] == "complete":
                    time.sleep(2)  # Show success message
                    model = updateByNewChallenge(model)
                    view(b, model)
        
        # Show final score
        view(b, model)
        time.sleep(3)
        
        b.leaveTtyMode()
        b.closeConnection()
    
    except brlapi.ConnectionError as e:
        handleConnectionError(e)


if __name__ == "__main__":
    main()
