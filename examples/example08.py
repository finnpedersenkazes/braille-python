#!/usr/bin/env python3

"""Example 08: Panning Left and Right to Discover Patterns

An educational braille navigation trainer that teaches tactile discrimination
through horizontal panning navigation along a long line with pattern interruptions.

Display format (20 cells example):
- Cells 0-19: Viewport window showing 20 characters of the 240-character line

The app presents a single 240-character line divided into sections:
- Section 1 (0-59): Rail pattern 'x' interrupted by 'l' (dots 1,2,3) pairs
- Section 2 (60-119): Rail pattern 'x' interrupted by 'c' (dots 1,4) and dots 3,6 pairs
- Section 3 (120-179): Rail pattern 'x' interrupted by 'g' (dots 1,2,4,5) and dots 2,3,5,6 pairs
- Section 4 (180-239): Rail pattern 'x' interrupted by random mix of all 4 patterns

Students pan left/right through the line to practice feeling the rail pattern
(dots 1,3,4,6) and detecting interruptions.

Architecture:
- Model: Full 240-character line with viewport tracking
- Update: Handles panning left/right with boundary clamping
- View: Renders current viewport window

Learning objectives:
- Tactile discrimination between similar patterns
- Horizontal panning navigation using Left/Right keys
- Following a tactile baseline (rail pattern)
- Detecting pattern interruptions through touch
"""

import sys
import os
import random

import brlapi

# Add src to path to import libraries
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

# pylint: disable=wrong-import-position,import-error
from library import (
    print_property,
    print_diagnostics,
    handle_connection_error,
    char_to_braille_dots,
)


# ============================================================================
# Model - Line generation and state
# ============================================================================

def generate_section(section_length, rail_dots, interrupt_patterns):
    """Generate a section with rail pattern interrupted by dot patterns

    Args:
        section_length: Total length of section in characters
        rail_dots: Braille dot value for rail pattern (typically char_to_braille_dots('x'))
        interrupt_patterns: List of braille dot values to use for interruptions

    Returns:
        List of braille dot values for the section
    """
    pattern = []

    while len(pattern) < section_length:
        # Calculate remaining space
        remaining = section_length - len(pattern)

        # Add rail segment (3-6 characters, or less if near end)
        rail_length = min(random.randint(3, 6), remaining)
        pattern.extend([rail_dots] * rail_length)

        # Add interruption pair (2 characters) if there's room for both
        remaining = section_length - len(pattern)
        if remaining >= 2:
            interrupt_dots = random.choice(interrupt_patterns)
            pattern.extend([interrupt_dots] * 2)

    return pattern


def generate_line():
    """Generate the full 240-character line with all sections

    Returns:
        List of 240 braille dot values representing the full line
    """
    rail_dots = char_to_braille_dots('x')  # dots 1,3,4,6
    l_dots = char_to_braille_dots('l')     # dots 1,2,3
    c_dots = char_to_braille_dots('c')     # dots 1,4
    dots_36 = brlapi.DOT3 | brlapi.DOT6    # dots 3,6 (no letter)
    g_dots = char_to_braille_dots('g')     # dots 1,2,4,5
    dots_2356 = brlapi.DOT2 | brlapi.DOT3 | brlapi.DOT5 | brlapi.DOT6  # dots 2,3,5,6 (no letter)

    line = []

    # Section 1 (60 chars): Rail + 'l' interruptions only
    line.extend(generate_section(60, rail_dots, [l_dots]))

    # Section 2 (60 chars): Rail + mix of 'c' and dots 3,6 interruptions
    line.extend(generate_section(60, rail_dots, [c_dots, dots_36]))

    # Section 3 (60 chars): Rail + mix of 'g' and dots 2,3,5,6 interruptions
    line.extend(generate_section(60, rail_dots, [g_dots, dots_2356]))

    # Section 4 (60 chars): Rail + random mix of all 4 interruptions
    line.extend(generate_section(60, rail_dots, [l_dots, c_dots, dots_36, g_dots, dots_2356]))

    return line


def init(brl):
    """Initialize the model with generated line and viewport state"""
    display_width = brl.displaySize[0]
    line_content = generate_line()

    return {
        "line_content": line_content,
        "viewport_start": 0,
        "display_width": display_width,
        "line_length": len(line_content),
        "counter": 0,
        "quit": False,
    }


def print_log(m):
    """Print model state to log"""
    max_viewport = m["line_length"] - m["display_width"]
    at_start = m["viewport_start"] == 0
    at_end = m["viewport_start"] >= max_viewport

    position_desc = ""
    if at_start:
        position_desc = " (start)"
    elif at_end:
        position_desc = " (end)"

    print_property("LOG", f"Viewport at position {m['viewport_start']}{position_desc}")
    print_property("Counter", str(m["counter"]))
    print_property("Display Width", str(m["display_width"]))
    print_property("Line Length", str(m["line_length"]))
    print_property("-------", "-------------------------")


# ============================================================================
# Update - Panning logic
# ============================================================================

def update_by_pan_left(m):
    """Pan viewport left by 1 character (decrease viewport_start)"""
    if m["viewport_start"] > 0:
        m["viewport_start"] -= 1
        print_property("Action", f"Panned left to position {m['viewport_start']}")
    else:
        print_property("Action", "At left edge - cannot pan further left")

    return m


def update_by_pan_right(m):
    """Pan viewport right by 1 character (increase viewport_start)"""
    max_viewport = m["line_length"] - m["display_width"]

    if m["viewport_start"] < max_viewport:
        m["viewport_start"] += 1
        print_property("Action", f"Panned right to position {m['viewport_start']}")
    else:
        print_property("Action", "At right edge - cannot pan further right")

    return m


def update_by_jump_previous(m):
    """Jump viewport left by display_width (simulates previous line)"""
    old_position = m["viewport_start"]
    m["viewport_start"] = max(0, m["viewport_start"] - m["display_width"])

    if m["viewport_start"] == 0 and old_position == 0:
        print_property("Action", "At start - cannot jump to previous line")
    else:
        print_property("Action", f"Jumped to previous line at position {m['viewport_start']}")

    return m


def update_by_jump_next(m):
    """Jump viewport right by display_width (simulates next line)"""
    max_viewport = m["line_length"] - m["display_width"]
    old_position = m["viewport_start"]
    m["viewport_start"] = min(max_viewport, m["viewport_start"] + m["display_width"])

    if m["viewport_start"] == max_viewport and old_position == max_viewport:
        print_property("Action", "At end - cannot jump to next line")
    else:
        print_property("Action", f"Jumped to next line at position {m['viewport_start']}")

    return m


def update_by_quit(m):
    """Set quit flag"""
    m["quit"] = True
    print_property("Action", "Program stopped by user")
    return m


def update_by_key(_brl, m, key_code):
    """Handle key press and update model

    Args:
        _brl: BrlAPI connection (unused but kept for consistency)
        m: Model dictionary
        key_code: Key code from readKey()

    Returns:
        Updated model
    """
    m["counter"] += 1

    print_property("Key Code", hex(key_code))

    # Left panning key or left thumb key
    if key_code in (brlapi.KEY_TYPE_CMD | brlapi.KEY_CMD_FWINLT,
                     brlapi.KEY_TYPE_CMD | brlapi.KEY_CMD_CHRLT):
        return update_by_pan_left(m)

    # Right panning key or right thumb key
    if key_code in (brlapi.KEY_TYPE_CMD | brlapi.KEY_CMD_FWINRT,
                     brlapi.KEY_TYPE_CMD | brlapi.KEY_CMD_CHRRT):
        return update_by_pan_right(m)

    # Previous (up) thumb key - jump left by display width
    if key_code == brlapi.KEY_TYPE_CMD | brlapi.KEY_CMD_LNUP:
        return update_by_jump_previous(m)

    # Next (down) thumb key - jump right by display width
    if key_code == brlapi.KEY_TYPE_CMD | brlapi.KEY_CMD_LNDN:
        return update_by_jump_next(m)

    # Home button - quit
    if key_code == brlapi.KEY_TYPE_CMD | brlapi.KEY_CMD_HOME:
        return update_by_quit(m)

    # Log unhandled keys for debugging
    print_property("Info", f"Unhandled key: {hex(key_code)}")

    return m


# ============================================================================
# View - Viewport rendering
# ============================================================================

def viewport_to_dots(m):
    """Extract current viewport window from line content

    Args:
        m: Model dictionary

    Returns:
        Bytes array of braille dots for current viewport window
    """
    start = m["viewport_start"]
    end = start + m["display_width"]
    viewport_content = m["line_content"][start:end]

    # Pad if necessary (shouldn't happen if boundaries are correct)
    while len(viewport_content) < m["display_width"]:
        viewport_content.append(0)

    return bytes(viewport_content)


def view(brl, m):
    """Render current viewport to braille display

    Args:
        brl: BrlAPI connection
        m: Model dictionary
    """
    print_log(m)

    if m["display_width"] == 0:
        print("Warning: No braille display detected. Skipping writeDots.")
        return

    dots = viewport_to_dots(m)
    brl.writeDots(dots)


# ============================================================================
# Main - Application entry point
# ============================================================================

def main():
    """Main panning navigation loop"""
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

        # Main navigation loop
        while not model["quit"]:
            key = b.readKey()
            model = update_by_key(b, model, key)

            if not model["quit"]:
                view(b, model)

        # Cleanup - skip if quit flag is set (display might be disconnected)
        if not model["quit"]:
            b.leaveTtyMode()
            b.closeConnection()

    except brlapi.ConnectionError as e:
        handle_connection_error(e)
    except (brlapi.OperationError, EOFError):
        # Handle disconnection gracefully
        print_property("Info", "Display disconnected")
    except KeyboardInterrupt:
        print_property("Info", "Program interrupted by user (Ctrl+C)")


if __name__ == "__main__":
    main()
