# Examples

This directory contains educational example scripts demonstrating braille display programming using the Elm Architecture pattern (Model-Update-View).

## Elm Architecture Pattern

All examples follow the Elm architecture for consistency and educational value:

```python
#!/usr/bin/env python3

import brlapi
from library import handle_connection_error

def init(brl):
    """Initialize the model (state)"""
    return {
        "key": "value",
        "stop": False,
        # ... other state
    }

def update(model, key_code, brl):
    """Update model based on input (pure function)"""
    # Process key_code and return updated model
    return model

def view(model, brl):
    """Render the model to braille display"""
    brl.writeText(str(model["value"]))

def main():
    """Main loop: init → readKey → update → view"""
    try:
        brl = brlapi.Connection()
        brl.enterTtyMode()
        
        model = init(brl)
        while not model.get("stop", False):
            key = brl.readKey(False)
            if key:
                model = update(model, key, brl)
                view(model, brl)
                
    except brlapi.ConnectionError as e:
        handle_connection_error(e)

if __name__ == "__main__":
    main()
```

## Example Files

| File | Description | Architecture | Status |
|------|-------------|--------------|--------|
| example01.py | Keyboard input with diagnostics | Elm (Model-Update-View) | ✓ Ready |
| example02.py | Basic text display | Simple loop | ✓ Ready |
| example02a.py | Counter animation | Simple loop | ✓ Ready |
| example02b.py | Traveling dot display | Simple loop | ✓ Ready |
| example02c.py | Filling display animation | Simple loop | ✓ Ready |
| example04.py | Keyboard learning game | Elm (with time updates) | ✓ Ready |
| example05.py | Obstacle jump game | Elm (with time updates) | ✓ Ready |
| example06.py | Character identification game | Elm | ✓ Ready |
| example07.py | Line navigation trainer | Elm | ✓ Ready |
| example08.py | Horizontal panning trainer | Elm | ✓ Ready |

## Running Examples

### Via launcher (recommended):
```bash
python src/main.py 01    # Runs example01
python src/main.py 02a   # Runs example02a
python src/main.py 04    # Runs example04
python src/main.py 05    # Runs example05 (default)
python src/main.py 08    # Runs example08
```

### Direct execution:
```bash
python examples/example01.py
./examples/example01.py  # If executable
```

## Example Details

### Example 01 - Keyboard Input
**File:** example01.py  
**Architecture:** Full Elm (Model-Update-View)  
**Features:**
- Captures keyboard input from braille display
- Displays key code, type, command, and flags
- Accumulates typed text
- Demonstrates basic Elm pattern

### Example 02 Series - Display Animations

**Example 02 - Basic Text Display**  
Simple text display demonstration

**Example 02a - Counter**  
Animated counter from 1 to 100

**Example 02b - Traveling Dot**  
Single dot traveling across display

**Example 02c - Progressive Fill**  
Cells filling progressively from left to right

### Example 04 - Keyboard Learning Game
**File:** example04.py  
**Architecture:** Elm with time-based updates  
**Features:**
- Teaches braille keyboard dot combinations
- Displays target character and dot pattern
- Validates user input
- Tracks score and progress
- Time-based challenges

### Example 05 - Obstacle Jump Game
**File:** example05.py  
**Architecture:** Full Elm with dual updates (key + time)  
**Features:**
- Character must jump over moving obstacles
- 4 vertical positions (cursor control)
- Moving obstacles (time-based animation)
- Score tracking
- Game duration timer
- Collision detection

### Example 06 - Character Identification Game
**File:** example06.py  
**Architecture:** Elm  
**Features:**
- Random character challenges
- User identifies character by feeling braille pattern
- Score tracking
- Configurable difficulty

### Example 07 - Line Navigation Trainer
**File:** example07.py  
**Architecture:** Elm  
**Features:**
- Navigate through 9 lines of patterns
- Different patterns per line (filled, alternating, gradient)
- Wrapping navigation (line 1 ↔ line 9)
- LNUP/LNDN key navigation

### Example 08 - Horizontal Panning Trainer
**File:** example08.py  
**Architecture:** Elm  
**Features:**
- 240-character horizontal line (12× display width)
- 4 pattern sections: filled, alternating, gradient, random
- Character-by-character panning (FWINLT/FWINRT, CHRLT/CHRRT)
- Jump navigation by display width (LNUP/LNDN)
- Visual position indicator

## Requirements

Make sure you have:
1. BRLTTY installed and running
2. A braille display connected and configured
3. Python 3.8 or higher
4. Required packages installed (see main README)

See the main [README](../README.md) and [Installation Guide](../docs/Installation.md) for setup instructions.

## Notes

- All examples use the `main()` function pattern for consistency
- The launcher (`src/main.py`) automatically detects and calls the `main()` function
- All examples handle braille connection errors gracefully
- Display size bugs have been fixed - examples now use actual display dimensions
