# Examples

This directory contains example scripts demonstrating how to work with braille displays using BrlAPI and BrlTTY.

## Consistent Pattern

All examples follow this pattern for consistency:
```python
#!/usr/bin/env python3

# Imports...

# Functions...

def main():
    try:
        # Main code here
        ...
    except brlapi.ConnectionError as e:
        # Error handling
        ...

if __name__ == "__main__":
    main()
```

## Example Files

| File | Description | Status |
|------|-------------|--------|
| example01.py | Basic keyboard input | ✓ Ready |
| example01a.py | Keyboard input with diagnostics | ✓ Ready |
| example01b.py | Keyboard input with Elm architecture | ✓ Ready |
| example02.py | Basic text display | ✓ Ready |
| example02a.py | Counter display | ✓ Ready |
| example02b.py | Traveling dot display | ✓ Ready |
| example02c.py | Filling display animation | ✓ Ready |
| example04a.py | Keyboard learning game (Elm architecture) | ✓ Ready |
| example05.py | Obstacle jump game (Elm architecture) | ✓ Ready |

## Running Examples

### Direct execution:
```bash
python examples/example01.py
./examples/example01.py  # If executable
```

### Via launcher (recommended):
```bash
python src/main.py 01    # Runs example01
python src/main.py 01a   # Runs example01a
python src/main.py 02    # Runs example02
python src/main.py 04a   # Runs example04a
python src/main.py 05    # Runs example05 (default)
```

### Via VS Code:
Press `Ctrl+F5` to run the launcher with the currently configured example.

## Example Series

### 01 Series - Keyboard Input
- **example01.py**: Basic keyboard event handling
- **example01a.py**: Adds diagnostic information display
- **example01b.py**: Implements Elm architecture (Model-Update-View)

### 02 Series - Display Output
- **example02.py**: Simple text display
- **example02a.py**: Counter animation
- **example02b.py**: Traveling dot pattern
- **example02c.py**: Progressive cell filling animation

### 04 Series - Learning Tools
- **example04a.py**: Keyboard learning game with braille translation

### 05 Series - Games
- **example05.py**: Obstacle jump game demonstrating full Elm architecture

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
