#!/usr/bin/env python3

"""Example 07: Navigate Lines and Feel the Dots

An educational braille navigation trainer that teaches tactile discrimination
of different dot patterns through line-based navigation.

Display format (20 cells example):
- Cells 0-14: Pattern area - repeated or alternating character pattern
- Cells 15-19: Line indicator - blank, blank, "L", tens digit, units digit

The app presents 9 static lines with different braille patterns:
- Lines 1-5: Filled patterns (character repeated in all cells)
- Lines 6-9: Alternating patterns (character/space/character/space...)

Students navigate through lines using Previous/Next buttons to practice
feeling and recognizing different braille dot patterns.

Architecture:
- Model: Static line definitions with current line tracking
- Update: Handles line navigation (up/down) with circular wrapping
- View: Renders pattern area and line indicator

Learning objectives:
- Tactile discrimination of braille dot patterns
- Line navigation using Previous/Next buttons
- Spatial orientation on braille display
- Pattern recognition and consistency
"""

import os
import sys

import brlapi

# Add src to path to import libraries
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

# ruff: noqa: E402
from library import (
    char_to_braille_dots,
    digit_dots,
    dots_to_display_size,
    handle_connection_error,
    print_diagnostics,
    print_property,
    tens,
    units,
)

# ============================================================================
# Model - Static line definitions and state
# ============================================================================

def init(brl):
    """Initialize the model with static line definitions"""
    display_width = brl.displaySize[0]

    # Static line definitions
    lines = [
        {"char": "x", "pattern": "filled"},      # Line 1: dots 1,3,4,6
        {"char": "c", "pattern": "filled"},      # Line 2: dots 1,4
        {"char": "a", "pattern": "filled"},      # Line 3: dot 1
        {"char": "g", "pattern": "filled"},      # Line 4: dots 1,2,4,5
        {"char": "\u00e9", "pattern": "filled"}, # Line 5: dots 1,2,3,4,5,6 (full cell)
        {"char": "c", "pattern": "alternating"}, # Line 6: c/space/c/space...
        {"char": "a", "pattern": "alternating"}, # Line 7: a/space/a/space...
        {"char": "g", "pattern": "alternating"}, # Line 8: g/space/g/space...
        {"char": "\u00e9", "pattern": "alternating"}, # Line 9: full/space/full/space...
    ]

    return {
        "current_line": 1,
        "display_width": display_width,
        "total_lines": len(lines),
        "lines": lines,
        "counter": 0,
        "quit": False,
    }


def get_line_content(m):
    """Get current line content (0-indexed internally)"""
    line_index = m["current_line"] - 1  # Convert 1-based to 0-based
    return m["lines"][line_index]


def print_log(m):
    """Print model state to log"""
    line_content = get_line_content(m)
    print_property("LOG", f"Line {m['current_line']}")
    print_property("Counter", str(m["counter"]))
    print_property("Character", line_content["char"])
    print_property("Pattern", line_content["pattern"])
    print_property("-------", "-------------------------")


# ============================================================================
# Update - Navigation logic
# ============================================================================

def update_by_line_up(m):
    """Navigate to previous line (with circular wrap)"""
    m["current_line"] -= 1
    if m["current_line"] < 1:
        m["current_line"] = m["total_lines"]  # Wrap to last line
    return m


def update_by_line_down(m):
    """Navigate to next line (with circular wrap)"""
    m["current_line"] += 1
    if m["current_line"] > m["total_lines"]:
        m["current_line"] = 1  # Wrap to first line
    return m


def update_by_quit(m):
    """Set quit flag to exit program"""
    m["quit"] = True
    print_property("Action", "Program stopped by user")
    return m


def update_by_key(brl, m, key_code):
    """Update model based on key press"""
    m["counter"] += 1

    # Line Up (Previous)
    if key_code == brlapi.KEY_TYPE_CMD | brlapi.KEY_CMD_LNUP:
        return update_by_line_up(m)

    # Line Down (Next)
    if key_code == brlapi.KEY_TYPE_CMD | brlapi.KEY_CMD_LNDN:
        return update_by_line_down(m)

    # Home button - quit
    if key_code == brlapi.KEY_TYPE_CMD | brlapi.KEY_CMD_HOME:
        return update_by_quit(m)

    # Log unhandled keys for debugging
    k = brl.expandKeyCode(key_code)
    print_property("Unhandled Key", f"Type: {hex(k['type'])}, Command: {hex(k['command'])}")

    return m


# ============================================================================
# View - Pattern rendering
# ============================================================================

def create_filled_pattern(char, width):
    """Create filled pattern (character repeated)"""
    char_dots = char_to_braille_dots(char)
    return [char_dots] * width


def create_alternating_pattern(char, width):
    """Create alternating pattern (character/space/character/space...)"""
    char_dots = char_to_braille_dots(char)
    pattern = []
    for i in range(width):
        if i % 2 == 0:
            pattern.append(char_dots)  # Character
        else:
            pattern.append(0)  # Space (no dots)
    return pattern


def pattern_to_display(char, pattern_type, width):
    """Render pattern based on type"""
    if pattern_type == "filled":
        return create_filled_pattern(char, width)
    if pattern_type == "alternating":
        return create_alternating_pattern(char, width)
    # Default to filled if unknown pattern type
    return create_filled_pattern(char, width)


def line_indicator_to_display(line_number):
    """Render line indicator as 5 cells: [blank][blank][L][tens][units]"""
    cells = []
    cells.append(0)  # blank
    cells.append(0)  # blank
    cells.append(brlapi.DOT1 | brlapi.DOT2 | brlapi.DOT3)  # L
    cells.append(digit_dots(tens(line_number)))
    cells.append(digit_dots(units(line_number)))
    return cells


def line_to_dots(m):
    """Convert current line to braille dots for display"""
    # Get pattern area width (display width minus 5 for line indicator)
    pattern_width = m["display_width"] - 5

    # Get current line content
    line_content = get_line_content(m)

    # Generate pattern cells
    pattern_cells = pattern_to_display(
        line_content["char"],
        line_content["pattern"],
        pattern_width
    )

    # Generate line indicator cells
    indicator_cells = line_indicator_to_display(m["current_line"])

    # Combine pattern and indicator
    all_cells = pattern_cells + indicator_cells

    return bytes(all_cells)


def view(brl, m):
    """Visualize the model on the braille display"""
    print_log(m)

    if m["display_width"] == 0:
        print("Warning: No braille display detected. Skipping writeDots.")
        return

    dots = line_to_dots(m)
    dots = dots_to_display_size(dots, m["display_width"])
    brl.writeDots(dots)


# ============================================================================
# Main - Application entry point
# ============================================================================

def main():
    """Main navigation loop"""
    try:
        print_property("Initialization", "Starting Example 07")

        # Initialization
        b = brlapi.Connection()
        b.enterTtyModeWithPath()
        b.acceptKeys(brlapi.rangeType_all, [0])
        print_diagnostics(b)

        # Elm Architecture: Model-Update-View
        model = init(b)
        view(b, model)

        # Navigation loop
        wait_for_key_press = True
        while not model["quit"]:
            try:
                key = b.readKey(wait_for_key_press)

                if key:
                    model = update_by_key(b, model, key)
                    if not model["quit"]:
                        view(b, model)
            except (brlapi.OperationError, EOFError):
                # Connection lost or display disconnected
                print_property("Info", "Braille display disconnected")
                break

        # Cleanup
        print_property("Status", "Exiting program")
        if not model["quit"]:
            # Only try cleanup if we didn't quit via Home button
            # (Home button disconnects the display automatically)
            try:
                b.leaveTtyMode()
                b.closeConnection()
            except (brlapi.OperationError, brlapi.ConnectionError):
                # Connection already closed
                pass

    except brlapi.ConnectionError as e:
        handle_connection_error(e)


if __name__ == "__main__":
    main()
