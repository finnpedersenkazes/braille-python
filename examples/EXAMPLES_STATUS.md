# Examples Status

All examples have been updated for consistency and can be run from the launcher (`python src/main.py <example_number>`).

## Consistent Pattern

All examples now follow this pattern:
```python
#!/bin/python3

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

| File | Has main() | Description | Status |
|------|-----------|-------------|--------|
| example01.py | ✓ | Basic keyboard input | ✓ Ready |
| example01a.py | ✓ | Keyboard input with diagnostics | ✓ Ready |
| example01b.py | ✓ | Keyboard input with Elm architecture | ✓ Ready |
| example02.py | ✓ | Basic text display | ✓ Ready |
| example02a.py | ✓ | Counter display | ✓ Ready |
| example02b.py | ✓ | Traveling dot display | ✓ Ready |
| example02c.py | ✓ | Filling display animation | ✓ Ready |
| example04a.py | ✓ | Keyboard learning game | ✓ Ready |
| example05.py | ✓ | Obstacle jump game (Elm architecture) | ✓ Ready |

## Running Examples

### Direct execution:
```bash
python examples/example01.py
```

### Via launcher:
```bash
python src/main.py 01
python src/main.py 01a
python src/main.py 02
python src/main.py 04a
python src/main.py 05
# etc...
```

### Via VS Code:
Press `Ctrl+F5` to run the launcher with the currently configured example.

## Notes

- All examples use the `main()` function pattern for consistency
- The launcher (`src/main.py`) automatically detects and calls the `main()` function
- All examples handle braille connection errors gracefully
- Examples 02b and 02c were fixed to use actual display dimensions instead of hardcoded values
