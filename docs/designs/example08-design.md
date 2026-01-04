# Example 08 - Panning left and right and discover patterns

## Overview
This app is an educational braille navigation trainer that teaches students to feel different dot patterns while scrolling left and right through a long tactile line. The line features a "rail" pattern (dots 1,3,4,6) that is periodically interrupted by different pattern variations.

**Display format** (20 cells example):
- Cells 0-19: Pattern area showing current 20-character window of the long line

**Educational purpose:**
- Practice tactile discrimination of different braille dot patterns
- Learn horizontal panning controls (Left/Right panning keys)
- Build muscle memory for recognizing pattern interruptions in a baseline
- Develop spatial awareness along a horizontal line
- Train finger tracking along a tactile rail

## Content Structure

The app presents a single long static line (240 characters total) divided into 4 sections of 60 characters each. Each section features a "rail" pattern (character 'x' = dots 1,3,4,6) that serves as a baseline, with periodic interruptions by other patterns.

### Pattern Design Philosophy

**Rail Pattern** (dots 1,3,4,6 = character 'x'):
- Serves as tactile baseline for students to follow with their fingers
- Creates consistent reference point throughout the line
- Appears in runs of 3-6 consecutive characters

**Interruption Patterns**:
- Always appear in pairs (two identical characters)
- Preceded by rail pattern of 3-6 characters
- Different sections feature different interruption patterns

### Section Content Table

| Section | Length | Rail Char | Interruption Patterns       | Interruption Dots        | Purpose                                                 |
| ------- | ------ | --------- | --------------------------- | ------------------------ | ------------------------------------------------------- |
| 1       | 60     | x         | l (lowercase L)             | 1, 2, 3                  | Detect subtle pattern change - similar to rail         |
| 2       | 60     | x         | c AND dots 3,6              | (1, 4) AND (3, 6)        | Detect complementary patterns - left vs right side     |
| 3       | 60     | x         | g AND dots 2,3,5,6          | (1, 2, 4, 5) AND (2,3,5,6) | Detect shifted patterns - different vertical positions |
| 4       | 60     | x         | Random mix of all 4 patterns| Mixed                    | Practice recognizing all patterns in mixed sequence    |

**Pattern Structure**:
- Each interruption: [rail × 3-6] + [interruption × 2] + repeat
- Section 1 (0-59): Pure 'l' (dots 1,2,3) interruptions throughout 60 characters
- Section 2 (60-119): Random mix of 'c' (dots 1,4) and dots 3,6 interruptions
- Section 3 (120-179): Random mix of 'g' (dots 1,2,4,5) and dots 2,3,5,6 interruptions
- Section 4 (180-239): Random mix of all 4 interruption patterns

**Example pattern from Section 1**:
```
xxxxx  ll  xxxx  ll  xxxxxx  ll  xxx  ll  xxxxx  ll  (etc.)
(rail) (interrupt) (rail) (interrupt)...
```

## Learning Objectives
- **Concepts taught**: 
  - Tactile discrimination between similar braille patterns
  - Horizontal panning navigation using Left/Right keys
  - Following a tactile baseline (rail pattern)
  - Detecting pattern interruptions through touch
  - Spatial orientation along a long horizontal line
- **Patterns demonstrated**: 
  - Viewport/window navigation (20-cell window on 240-character line)
  - Panning with boundary limits (stop at edges)
  - Static content with dynamic viewport positioning
  - Elm architecture (Model-Update-View) pattern
- **Builds on previous examples**:
  - Similar to example07 (static content navigation) but horizontal instead of vertical
  - Display techniques from example06
  - Elm architecture foundation from all previous examples

## Requirements

### Functional
- Display a 20-cell window into a 240-character line
- Pan left/right through the line using Left/Right panning keys
- Stop at line boundaries (cannot pan beyond start or end)
- Show position indicator in display
- Quit program with Home button
- Generate consistent static line with rail and interruption patterns
- Log panning activity to terminal

### Technical
- **Libraries needed from src/library.py**:
  - `print_property` - logging panning events
  - `print_diagnostics` - display info
  - `handle_connection_error` - error handling
  - `char_to_braille_dots(char)` - convert characters to dot patterns
  - `random_char` - generate random interruption patterns for section 4
  - `random_position` - random rail lengths and interruption placement

- **Display requirements**: 
  - Any width (typically 20-40 cells)
  - 8-dot braille cells
  - Left/Right panning buttons (FWINLT/FWINRT or thumb buttons)

- **Input requirements**:
  - Left panning key (FWINLT or Left thumb) - pan viewport left
  - Right panning key (FWINRT or Right thumb) - pan viewport right
  - Home button - quit program

## Architecture

### Model
```python
{
    "line_content": [],          # Full 240-character line as list of braille dot values
    "viewport_start": 0,         # Starting position of 20-cell viewport (0-220)
    "display_width": 20,         # Width of braille display (viewport size)
    "line_length": 240,          # Total length of the line
    "counter": 0,                # Key press counter for logging
    "quit": False,               # Quit flag
}
```

### Update

**Events/Messages:**
- `PAN_LEFT` - Move viewport left one character (FWINLT or CHRLT)
- `PAN_RIGHT` - Move viewport right one character (FWINRT or CHRRT)
- `JUMP_PREVIOUS` - Jump left by display width (Previous thumb key/LNUP)
- `JUMP_NEXT` - Jump right by display width (Next thumb key/LNDN)
- `QUIT` - Exit program (Home button)

**State Transitions:**

1. **Pan Left** (viewport_start → viewport_start - 1):
   - Decrement `viewport_start` by 1 (move left one character)
   - If `viewport_start < 0`, clamp to 0 (cannot go before start of line)
   - Increment `counter`
   - Update display with new viewport window

2. **Pan Right** (viewport_start → viewport_start + 1):
   - Increment `viewport_start` by 1 (move right one character)
   - If `viewport_start > (line_length - display_width)`, clamp to max position
   - Maximum viewport_start = 220 (for 240 line with 20 display: 240 - 20 = 220)
   - Increment `counter`
   - Update display with new viewport window

3. **Jump Previous** (viewport_start → viewport_start - display_width):
   - Decrement `viewport_start` by display_width (e.g., 20 for 20-cell display)
   - Simulates moving to "previous line" in multi-line view
   - If `viewport_start < 0`, clamp to 0
   - Increment `counter`
   - Update display with new viewport window

4. **Jump Next** (viewport_start → viewport_start + display_width):
   - Increment `viewport_start` by display_width (e.g., 20 for 20-cell display)
   - Simulates moving to "next line" in multi-line view
   - If `viewport_start > (line_length - display_width)`, clamp to max position
   - Increment `counter`
   - Update display with new viewport window

5. **Quit**:
   - Set `quit = True`
   - Log final state
   - Exit main loop
   - Clean up BrlAPI connection

### View

**Display Layout:**
```
[20-character viewport window showing portion of 240-character line]
[Pattern cells based on current viewport position]
Position 0-19 when viewport_start = 0
Position 10-29 when viewport_start = 10
Position 220-239 when viewport_start = 220 (max)
```

**Elements:**
- All cells (0 to display_width-1): Current viewport window of the line
- Content extracted from `line_content[viewport_start : viewport_start + display_width]`

**Line Generation Algorithm:**

For each section:
1. **Section 1** (60 chars, indices 0-59): Rail + 'l' (dots 1,2,3) interruptions
2. **Section 2** (60 chars, indices 60-119): Rail + random mix of 'c' (dots 1,4) and dots 3,6
3. **Section 3** (60 chars, indices 120-179): Rail + random mix of 'g' (dots 1,2,4,5) and dots 2,3,5,6
4. **Section 4** (60 chars, indices 180-239): Rail + random mix of all 4 patterns

**Pattern Generation Logic**:
```python
def generate_section(section_length, rail_char, interrupt_patterns):
    pattern = []
    while len(pattern) < section_length:
        # Add rail segment (3-6 chars)
        rail_length = min(random.randint(3, 6), section_length - len(pattern))
        pattern.extend([rail_char] * rail_length)

        # Add interruption pair (2 chars)
        if len(pattern) < section_length - 1:
            interrupt_dots = random.choice(interrupt_patterns)
            pattern.extend([interrupt_dots] * 2)

    return pattern
```

**Feedback Messages (printed to terminal):**
```
"Viewport at position 0 (start)"
"Panning right to position 10"
"Panning left to position 9"
"Viewport at position 220 (end)"
"At left edge - cannot pan further left"
"At right edge - cannot pan further right"
"Program stopped by user"
```

**Braille Patterns Used:**
- Rail: 'x' (dots 1,3,4,6) - baseline pattern
- Interruption 'l': (dots 1,2,3) - letter L lowercase
- Interruption 'c': (dots 1,4) - letter c
- Interruption dots 3,6: (dots 3,6) - no letter, just dots pattern
- Interruption 'g': (dots 1,2,4,5) - letter g
- Interruption dots 2,3,5,6: (dots 2,3,5,6) - no letter, just dots pattern
| Key or Button         | BrlAPI Key Code                | Action                                                      |
| --------------------- | ------------------------------ | ----------------------------------------------------------- |
| Left panning key      | KEY_TYPE_CMD \| KEY_CMD_FWINLT | Pan viewport left by 1 character (with boundary check)      |
| Right panning key     | KEY_TYPE_CMD \| KEY_CMD_FWINRT | Pan viewport right by 1 character (with boundary check)     |
| Character left key    | KEY_TYPE_CMD \| KEY_CMD_CHRLT  | Pan viewport left by 1 character (alternative)              |
| Character right key   | KEY_TYPE_CMD \| KEY_CMD_CHRRT  | Pan viewport right by 1 character (alternative)             |
| Previous thumb key    | KEY_TYPE_CMD \| KEY_CMD_LNUP   | Jump left by display_width (simulates previous line)        |
| Next thumb key        | KEY_TYPE_CMD \| KEY_CMD_LNDN   | Jump right by display_width (simulates next line)           |
| Home button           | KEY_TYPE_CMD \| KEY_CMD_HOME   | Quit program                                                |
| Other keys            | Any other key code             | No effect (logged but ignored)                              |

## Implementation Plan

1. **[ ] Step 1: Model implementation**
   - Create `init(brl)` function with initial state
   - Implement `generate_line()` to create full 240-character pattern
   - Implement `generate_section(length, rail_char, interrupt_chars)` helper
   - Initialize `viewport_start = 0`

2. **[ ] Step 2: Update functions**
   - `update_by_pan_left(m)` - decrement viewport_start by 1 with boundary check
   - `update_by_pan_right(m)` - increment viewport_start by 1 with boundary check
   - `update_by_jump_previous(m)` - decrement viewport_start by display_width with boundary check
   - `update_by_jump_next(m)` - increment viewport_start by display_width with boundary check
   - `update_by_quit(m)` - set quit flag
   - `update_by_key(brl, m, key_code)` - main key dispatcher
   - `print_log(m)` - log current viewport position

3. **[ ] Step 3: View rendering**
   - `view(brl, m)` - main rendering function
   - `viewport_to_dots(m)` - extract current viewport window from line_content
   - Convert characters to braille dots using `char_to_braille_dots()`

4. **[ ] Step 4: Main loop**
   - Setup BrlAPI connection
   - Enter TTY mode
   - Accept all keys with `acceptKeys(brlapi.rangeType_all, [0])`
   - Main panning loop until quit
   - Proper cleanup and error handling

5. **[ ] Step 5: Testing**
   - Unit tests for line generation (verify sections and patterns)
   - Test viewport extraction at various positions (0, 110, 220)
   - Test boundary conditions (panning at edges)
   - Test rail length randomization (3-6 characters)
   - Integration test for panning flow
   - Manual testing on actual braille display

6. **[ ] Step 6: Documentation**
   - Add comprehensive docstring to example08.py
   - Document pattern structure and sections
   - Update examples/README.md with example08 entry

## Testing Strategy

**Unit Tests:**
- Test `generate_section()` produces correct length
- Test rail characters appear in runs of 3-6
- Test interruptions always appear in pairs (2 consecutive)
- Test full line is exactly 240 characters
- Test viewport extraction at boundaries (start, middle, end)
- Test boundary clamping for viewport_start

**Integration Tests:**
- Test complete panning from start to end
- Test panning stops at left boundary (viewport_start = 0)
- Test panning stops at right boundary (viewport_start = 220 for 20-cell display)
- Test quit functionality
- Test display rendering for different viewport positions

**Manual Testing:**
- Verify rail pattern feels consistent tactilely
- Verify interruptions are noticeable by touch
- Verify panning is smooth and responsive
- Verify cannot pan beyond line boundaries
- Verify different sections have different interruption patterns
- Test with various display widths (20, 40 cells)

## Implementation Notes

**Pattern Design Rationale:**
- **Rail pattern (x)**: Strong tactile baseline with dots on both sides (1,4) and middle (3,6)
- **Interruption 'l' (dots 1,2,3)**: Adds dot 2 to left side, creates subtle change from rail
- **Interruption 'c' (dots 1,4)**: Left side dots only - missing middle dots 3,6 from rail
- **Interruption dots 3,6**: Right side dots only - missing left dots 1,4 from rail (complementary to 'c')
- **Interruption 'g' (dots 1,2,4,5)**: Shifts middle dots vertically (3→2, 6→5)
- **Interruption dots 2,3,5,6**: All non-rail dots (no 1 or 4) - completely different tactile feel
- **Progressive difficulty**: Section 1 isolates one pattern, sections 2-3 mix complementary pairs, section 4 mixes all

**Viewport Navigation:**
- **Window size**: Always equals display_width (typically 20 cells)
- **Boundary handling**: Clamp viewport_start to valid range [0, line_length - display_width]
- **Smooth panning**: One character at a time for precise control
- **No wrapping**: Unlike vertical line navigation, horizontal panning stops at edges

**Line Generation:**
- **Deterministic sections 1-3**: Consistent patterns for initial learning
- **Random section 4**: Unpredictable mix for pattern recognition practice
- **Rail consistency**: 'x' appears throughout all sections as baseline reference
- **Interruption pairs**: Always two consecutive characters for clear tactile signal

**Key BrlAPI Integration:**
- Left panning: `KEY_TYPE_CMD | KEY_CMD_FWINLT` (forward window left)
- Right panning: `KEY_TYPE_CMD | KEY_CMD_FWINRT` (forward window right)
- Alternative: Character left/right (`KEY_CMD_CHRLT`/`KEY_CMD_CHRRT`)
- Home: `KEY_TYPE_CMD | KEY_CMD_HOME`
- Accept all keys to log unhandled input for debugging

**Extensibility:**
- Line length easily adjustable (change 240 to any value)
- Number of sections can be increased or decreased
- Interruption characters easily modified
- Viewport size adapts to any display width
- Pattern generation algorithm can be enhanced with more sophisticated rules

## References
- **example07**: Similar navigation concept but vertical (line up/down) vs horizontal (pan left/right)
- **example04**: Panning and navigation foundations
- **src/library.py**: `char_to_braille_dots()`, `random_char()`, `random_position()` utilities
- **Elm Architecture**: Model-Update-View pattern used throughout examples 