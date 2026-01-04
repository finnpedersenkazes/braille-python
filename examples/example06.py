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

import sys
import os
import time

import brlapi

# Add src to path to import libraries
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

# pylint: disable=wrong-import-position,import-error
from library import (
    print_property,
    print_diagnostics,
    handle_connection_error,
    digit_dots,
    tens,
    units,
    char_to_braille_dots,
    combine_keys_to_dots,
    random_char,
    random_position,
    dots_to_display_size,
)


# ============================================================================
# Model - Game state initialization
# ============================================================================

def get_message(code, **params):
    """Get message based on code and parameters"""
    messages = {
        "start": lambda p: "Press any key to start",
        "find": lambda p: (
            f"Find character '{p.get('char', '?')}' at position {p.get('position', 0)} "
            f"(press cursor button under it)"
        ),
        "waiting_position": lambda p: (
            f"Target: '{p.get('char', '?')}' at position {p.get('position', 0)}. "
            f"Click cursor button under it."
        ),
        "position_selected": lambda p: (
            f"Position {p.get('position', 0)} selected. "
            f"Now press dots for '{p.get('char', '?')}'"
        ),
        "correct": lambda p: f"Correct! '{p.get('char', '?')}' found. Score: {p.get('score', 0)}",
        "incorrect_position": lambda p: "Wrong position. Try again!",
        "incorrect_dots": lambda p: "Wrong dots. Try again!",
        "game_over": lambda p: f"Game Over! Score: {p.get('score', 0)}/{p.get('attempts', 0)}",
    }
    return messages.get(code, lambda p: "")(params)


def generate_challenge(display_width):
    """Generate new random character and position for challenge"""
    # Pick random character (a-z)
    target_char = random_char()

    # Pick random position in game area (last 5 cells reserved for score)
    game_width = display_width - 5
    target_position = random_position(game_width)

    return target_char, target_position


def init(brl):
    """Initialize the game model with all possible states"""
    display_width = brl.displaySize[0]

    return {
        "targetChar": "",
        "targetPosition": 0,
        "displayWidth": display_width,
        "score": 0,
        "attempts": 0,
        "currentPhase": "start",  # "start", "waiting", "position_selected", "complete"
        "selectedPosition": None,
        "selectedDots": [],
        "message": get_message("start"),
        "gameStarted": False,
        "counter": 0,
    }


def print_log(m):
    """Print model state to log"""
    print_property("LOG", f"Phase: {m['currentPhase']}")
    print_property("Counter", str(m["counter"]))
    print_property("Message", m["message"])

    if m["gameStarted"]:
        print_property("Target Char", m["targetChar"])
        print_property("Target Position", str(m["targetPosition"]))
        print_property("Score", str(m["score"]))
        print_property("Attempts", str(m["attempts"]))

        if m["selectedPosition"] is not None:
            print_property("Selected Position", str(m["selectedPosition"]))
        if m["selectedDots"]:
            print_property("Selected Dots", str(m["selectedDots"]))

    print_property("-------", "-------------------------")


# ============================================================================
# Update - Game logic and state updates
# ============================================================================

def convert_dots_arg_to_list(dots_arg):
    """Convert braille dot argument bitmask to list of dot numbers (1-6)"""
    dot_list = []
    if dots_arg & brlapi.DOT1:
        dot_list.append(1)
    if dots_arg & brlapi.DOT2:
        dot_list.append(2)
    if dots_arg & brlapi.DOT3:
        dot_list.append(3)
    if dots_arg & brlapi.DOT4:
        dot_list.append(4)
    if dots_arg & brlapi.DOT5:
        dot_list.append(5)
    if dots_arg & brlapi.DOT6:
        dot_list.append(6)
    return dot_list


def handle_dot_input(m, dots_arg):
    """Handle braille keyboard dot input"""
    dot_list = convert_dots_arg_to_list(dots_arg)
    for dot in dot_list:
        m = update_by_dot_key(m, dot)
    return update_by_submit(m)


def handle_space_key(m):
    """Handle space bar key based on current game phase"""
    if m["currentPhase"] == "start":
        return update_by_game_start(m)
    if m["currentPhase"] == "position_selected":
        return update_by_submit(m)
    if m["currentPhase"] == "complete":
        return update_by_new_challenge(m)
    return m

def update_by_game_start(m):
    """Initialize game and generate first challenge"""
    m["gameStarted"] = True
    target_char, target_position = generate_challenge(m["displayWidth"])
    m["targetChar"] = target_char
    m["targetPosition"] = target_position
    m["currentPhase"] = "waiting"
    m["message"] = get_message("find", char=target_char, position=target_position)
    m["attempts"] = 0
    m["score"] = 0
    return m


def update_by_new_challenge(m):
    """Generate new challenge"""
    target_char, target_position = generate_challenge(m["displayWidth"])
    m["targetChar"] = target_char
    m["targetPosition"] = target_position
    m["currentPhase"] = "waiting"
    m["selectedPosition"] = None
    m["selectedDots"] = []
    m["message"] = get_message("find", char=target_char, position=target_position)
    return m


def update_by_cursor_press(m, position):
    """Handle cursor routing button press"""
    if m["currentPhase"] == "waiting":
        m["selectedPosition"] = position
        m["currentPhase"] = "position_selected"
        m["message"] = get_message("position_selected", position=position, char=m["targetChar"])
        m["selectedDots"] = []  # Reset dots for new attempt
    return m


def update_by_dot_key(m, dot_number):
    """Handle braille keyboard dot key press (1-6)"""
    if m["currentPhase"] == "position_selected":
        # Add dot if not already in list
        if dot_number not in m["selectedDots"]:
            m["selectedDots"].append(dot_number)
            m["selectedDots"].sort()  # Keep sorted for consistency
        # Auto-submit if user has entered dots (simple approach: wait for space/enter)
    return m


def update_by_submit(m):
    """Validate answer and update score"""
    if m["currentPhase"] == "position_selected" and m["selectedDots"]:
        # Check position
        if m["selectedPosition"] != m["targetPosition"]:
            m["message"] = get_message("incorrect_position")
            m["selectedPosition"] = None
            m["selectedDots"] = []
            m["currentPhase"] = "waiting"
            return m

        # Check dots
        user_dots = combine_keys_to_dots(m["selectedDots"])
        target_dots = char_to_braille_dots(m["targetChar"])

        m["attempts"] += 1

        if user_dots == target_dots:
            m["score"] += 1
            m["currentPhase"] = "complete"
            m["message"] = get_message("correct", char=m["targetChar"], score=m["score"])
        else:
            m["message"] = get_message("incorrect_dots")
            m["selectedDots"] = []
            # Stay in position_selected phase to try dots again

    return m


def update_by_quit(m):
    """End game"""
    m["message"] = get_message("game_over", score=m["score"], attempts=m["attempts"])
    m["gameStarted"] = False
    m["currentPhase"] = "start"
    return m


def update_by_key(brl, m, key_code):
    """Update model based on key press"""
    k = brl.expandKeyCode(key_code)
    m["counter"] += 1

    # Check for cursor routing key (position selection)
    if (k["type"] == brlapi.KEY_TYPE_CMD) and (k["command"] == brlapi.KEY_CMD_ROUTE):
        position = k["argument"]
        return update_by_cursor_press(m, position)

    # Check for braille keyboard dot keys (command 0x220000 with argument as dots)
    if (k["type"] == brlapi.KEY_TYPE_CMD) and (k["command"] == 0x220000) and (k["argument"] != 0):
        return handle_dot_input(m, k["argument"])

    # Space bar - submit answer or start game
    if key_code == brlapi.KEY_TYPE_CMD | 0x220000:
        return handle_space_key(m)

    # Line Down - quit game
    if key_code == brlapi.KEY_TYPE_CMD | brlapi.KEY_CMD_LNDN:
        return update_by_quit(m)

    # Home button - quit game
    if key_code == brlapi.KEY_TYPE_CMD | brlapi.KEY_CMD_HOME:
        return update_by_quit(m)

    return m


# ============================================================================
# View - Game rendering
# ============================================================================

def score_to_display(score):
    """Render score as braille cells (5 cells for right side display)
    Format: blank, blank, p, tens_digit, units_digit
    """
    cells = []
    cells.append(0)  # blank
    cells.append(0)  # blank
    cells.append(brlapi.DOT1 | brlapi.DOT2 | brlapi.DOT3 | brlapi.DOT4)  # p
    cells.append(digit_dots(tens(score)))
    cells.append(digit_dots(units(score)))
    return cells


def challenge_to_display(m):
    """Render challenge character and fill other positions with blanks"""
    cells = []

    # Fill game area (display width minus 5 cells for score)
    game_width = m["displayWidth"] - 5
    for i in range(game_width):
        if i == m["targetPosition"]:
            cells.append(char_to_braille_dots(m["targetChar"]))
        else:
            # Fill with blank
            cells.append(0)

    # Add score display on the right side
    cells.extend(score_to_display(m["score"]))

    # Add cursor at selected position
    if m["selectedPosition"] is not None:
        for i, _ in enumerate(cells):
            if i == m["selectedPosition"]:
                cells[i] |= brlapi.DOT7 | brlapi.DOT8

    return bytes(cells)


def game_to_dots(m):
    """Convert game state to braille dots for display"""
    if not m["gameStarted"]:
        # Show start message
        cells = [0] * m["displayWidth"]
        return bytes(cells)

    return challenge_to_display(m)


def view(brl, m):
    """Visualize the model on the braille display"""
    print_log(m)

    if m["displayWidth"] == 0:
        print("Warning: No braille display detected. Skipping writeDots.")
        return

    dots = game_to_dots(m)
    dots = dots_to_display_size(dots, m["displayWidth"])
    brl.writeDots(dots)


# ============================================================================
# Main - Application entry point
# ============================================================================

def main():
    """Main game loop"""
    try:
        print_property("Initialization", "Before Connection")

        # Initialization
        b = brlapi.Connection()
        b.enterTtyModeWithPath()
        b.acceptKeys(brlapi.rangeType_all, [0])
        print_diagnostics(b)

        # The architecture
        model = init(b)
        view(b, model)

        wait_for_key_press = True
        while model["currentPhase"] != "quit":
            key = b.readKey(wait_for_key_press)

            if key:
                model = update_by_key(b, model, key)
                view(b, model)

                # Generate new challenge after completing one
                if model["currentPhase"] == "complete":
                    time.sleep(2)  # Show success message
                    model = update_by_new_challenge(model)
                    view(b, model)

        # Show final score
        view(b, model)
        time.sleep(3)

        b.leaveTtyMode()
        b.closeConnection()

    except brlapi.ConnectionError as e:
        handle_connection_error(e)


if __name__ == "__main__":
    main()
