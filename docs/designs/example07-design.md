# Example 07 - Navigate lines and feel the dots

## Overview
This app is an educational braille navigation trainer that teaches students to feel different dot patterns and navigate between lines using line up/down buttons on the braille display.

**Display format** (20 cells example):
- Cells 0-14: Pattern area - repeated character pattern for tactile learning
- Cells 15-19: Line indicator - blank, blank, "L", line number (max 2 digits)

**Educational purpose:**
- Practice tactile discrimination of different braille dot patterns
- Learn line navigation controls (Previous/Next thumb keys)
- Build muscle memory for common braille patterns
- Understand spatial navigation on braille display

## Content Structure

The app presents a static set of 9 lines, each featuring a different braille pattern. Students navigate through these lines to practice feeling and recognizing patterns.

### Line Content Table

| Line | Dots             | Character | Pattern Type          | Description                    |
| ---- | ---------------- | --------- | --------------------- | ------------------------------ |
| 1    | 1, 3, 4, 6       | x         | Filled (repeated)     | All cells show 'x'             |
| 2    | 1, 4             | c         | Filled (repeated)     | All cells show 'c'             |
| 3    | 1                | a         | Filled (repeated)     | All cells show 'a'             |
| 4    | 1, 2, 4, 5       | g         | Filled (repeated)     | All cells show 'g'             |
| 5    | 1, 2, 3, 4, 5, 6 | é (full)  | Filled (repeated)     | All cells show full cell (⠿)   |
| 6    | 1, 4             | c         | Alternating (c/space) | Pattern: c, space, c, space... |
| 7    | 1                | a         | Alternating (a/space) | Pattern: a, space, a, space... |
| 8    | 1, 2, 4, 5       | g         | Alternating (g/space) | Pattern: g, space, g, space... |
| 9    | 1, 2, 3, 4, 5, 6 | é (full)  | Alternating (⠿/space) | Pattern: ⠿, space, ⠿, space... |

**Pattern progression:**
- Lines 1-5: Continuous patterns (easier - all cells same character)
- Lines 6-9: Alternating patterns (harder - pattern/space alternation)
- Variety of dot densities from simple (dot 1 only) to complex (all 6 dots)

## Learning Objectives
- **Concepts taught**: 
  - Tactile discrimination of braille dot patterns
  - Line navigation using Previous/Next buttons
  - Spatial orientation on braille display
  - Pattern recognition and consistency
- **Patterns demonstrated**: 
  - Line-based navigation interface
  - Static content model (no dynamic state changes)
  - Line indicator display (L + line number)
  - Elm architecture (Model-Update-View) pattern
- **Builds on previous examples**:
  - Line navigation similar to example04 concepts
  - Display formatting from example06
  - Elm architecture foundation from all previous examples

## Requirements

### Functional
- Display static content across 9 predefined lines
- Show current line number as "L#" in rightmost 5 cells
- Navigate up/down through lines using Previous/Next buttons
- Wrap navigation (line 1 ← line 9 wraps, line 9 → line 1 wraps)
- Quit program with Home button
- Display appropriate pattern based on line number
- Log navigation activity to terminal

### Technical
- **Libraries needed from src/library.py**:
  - `print_property` - logging navigation events
  - `print_diagnostics` - display info
  - `handle_connection_error` - error handling
  - `char_to_braille_dots(char)` - convert characters to dot patterns
  - `digit_dots` - line number display
  - `tens`, `units` - line number formatting (for 2-digit support)
  - `dots_to_display_size` - ensure display array is correct size

- **Display requirements**: 
  - Minimum 20 cells width recommended
  - 8-dot braille cells
  - Previous/Next navigation buttons (thumb keys or LNUP/LNDN)

- **Input requirements**:
  - Previous thumb key or Line Up (LNUP) - navigate to previous line
  - Next thumb key or Line Down (LNDN) - navigate to next line
  - Home button - quit program

## Architecture

### Model
```python
{
    "current_line": 1,           # Current line number (1-9)
    "display_width": 20,         # Width of braille display
    "total_lines": 9,            # Total number of lines in content
    "lines": [                   # Static line definitions
        {"char": "x", "pattern": "filled"},
        {"char": "c", "pattern": "filled"},
        {"char": "a", "pattern": "filled"},
        {"char": "g", "pattern": "filled"},
        {"char": "é", "pattern": "filled"},
        {"char": "c", "pattern": "alternating"},
        {"char": "a", "pattern": "alternating"},
        {"char": "g", "pattern": "alternating"},
        {"char": "é", "pattern": "alternating"},
    ],
    "counter": 0,                # Key press counter for logging
}
```

### Update

**Events/Messages:**
- `LINE_UP` - Navigate to previous line (Previous thumb key or LNUP)
- `LINE_DOWN` - Navigate to next line (Next thumb key or LNDN)
- `QUIT` - Exit program (Home button)

**State Transitions:**

1. **Line Up** (current_line → current_line - 1):
   - Decrement `current_line` by 1
   - If `current_line < 1`, wrap to `total_lines` (9)
   - Increment `counter`
   - Update display with new line content

2. **Line Down** (current_line → current_line + 1):
   - Increment `current_line` by 1
   - If `current_line > total_lines`, wrap to 1
   - Increment `counter`
   - Update display with new line content

3. **Quit**:
   - Log final state
   - Exit main loop
   - Clean up BrlAPI connection

### View

**Display Layout:**
```
[Pattern Area (15 cells)                    ][Line Indicator (5 cells)]
[x][x][x][x][x][x][x][x][x][x][x][x][x][x][x][_][_][L][0][1]
Position: 0  1  2  3  4  5  6  7  8  9  10 11 12 13 14 15 16 17 18 19
```

**Elements:**
- Cells 0-14: Pattern area
  - **Filled pattern**: All cells show the same character (lines 1-5)
  - **Alternating pattern**: Character, space, character, space... (lines 6-9)
- Cells 15-19: Line indicator
  - Cell 15-16: Blank (0)
  - Cell 17: "L" (dots 1,2,3)
  - Cell 18: Tens digit (0 for lines 1-9)
  - Cell 19: Units digit (1-9)

**Pattern Rendering:**
- **Filled**: `char_to_braille_dots(char)` repeated for all pattern cells
- **Alternating**: Alternates between `char_to_braille_dots(char)` and 0 (blank)

**Feedback Messages (printed to terminal):**
```
"Line 1: x (filled)"
"Line 2: c (filled)"
"Line 6: c (alternating)"
"Navigated up to line 9 (wrapped)"
"Navigated down to line 1 (wrapped)"
"Program stopped by user"
```

**Braille Patterns Used:**
- Letter "x" (dots 1,3,4,6) - medium complexity
- Letter "c" (dots 1,4) - simple pattern
- Letter "a" (dot 1) - simplest pattern
- Letter "g" (dots 1,2,4,5) - medium-high complexity
- Letter "é" / full cell (dots 1,2,3,4,5,6) - most complex
- Letter "L" (dots 1,2,3) for line indicator
- Digit dots for line number

## Navigation

| Key or Button      | BrlAPI Key Code            | Action                                    |
| ------------------ | -------------------------- | ----------------------------------------- |
| Previous thumb key | KEY_TYPE_CMD \| KEY_CMD_LNUP | Navigate to previous line (with wrap)     |
| Next thumb key     | KEY_TYPE_CMD \| KEY_CMD_LNDN | Navigate to next line (with wrap)         |
| Home button        | KEY_TYPE_CMD \| KEY_CMD_HOME | Quit program                              |
| Other keys         | Any other key code         | No effect (logged but ignored)            |

## Implementation Plan

1. **[✅] Step 1: Model implementation**
   - Created `init(brl)` function with initial state
   - Defined static `lines` array with 9 line definitions
   - Created `get_line_content(m)` helper to retrieve current line data
   - Initialized `current_line = 1`

2. **[✅] Step 2: Update functions**
   - `update_by_line_up(m)` - decrement line with wrap to 9
   - `update_by_line_down(m)` - increment line with wrap to 1
   - `update_by_quit(m)` - set quit flag
   - `update_by_key(brl, m, key_code)` - main key dispatcher
   - `print_log(m)` - log current line and navigation

3. **[✅] Step 3: View rendering**
   - `view(brl, m)` - main rendering function
   - `line_to_dots(m)` - convert current line to braille array
   - `line_indicator_to_display(line_number)` - render "L" + line number (5 cells)
   - `pattern_to_display(char, pattern_type, width)` - render filled or alternating pattern
   - Helper: `create_filled_pattern(char, width)` - repeat character
   - Helper: `create_alternating_pattern(char, width)` - alternate char/space

4. **[✅] Step 4: Main loop**
   - Setup BrlAPI connection
   - Enter TTY mode
   - Accept all keys with `acceptKeys(brlapi.rangeType_all, [0])`
   - Main navigation loop until quit
   - Proper cleanup and error handling

5. **[ ] Step 5: Testing**
   - Unit tests for pattern generation (filled vs alternating)
   - Test line wrapping (1 → 9 and 9 → 1)
   - Test line indicator display for all lines 1-9
   - Integration test for navigation flow
   - Manual testing on actual braille display

6. **[ ] Step 6: Documentation**
   - Add comprehensive docstring to example07.py
   - Document pattern types and line content
   - Update examples/README.md with example07 entry

## Testing Strategy

**Unit Tests:**
- Test `create_filled_pattern()` for correct repetition
- Test `create_alternating_pattern()` for char/space alternation
- Test `line_indicator_to_display()` for lines 1-9
- Test line wrapping logic (boundary conditions)
- Test model initialization and structure

**Integration Tests:**
- Test complete navigation cycle (1 → 9 → 1)
- Test Previous button wrapping (line 1 → line 9)
- Test Next button wrapping (line 9 → line 1)
- Test quit functionality
- Test display rendering for each line type

**Manual Testing:**
- Verify filled patterns feel consistent tactilely
- Verify alternating patterns create clear rhythm
- Verify line indicator updates correctly
- Verify navigation is smooth and responsive
- Verify wrapping behavior is intuitive
- Test with various display widths

## Implementation Notes

**Pattern Design Rationale:**
- **Lines 1-5 (filled)**: Easier for beginners - consistent tactile feedback
- **Lines 6-9 (alternating)**: More challenging - requires pattern recognition
- **Dot progression**: From simple (dot 1) to complex (all 6 dots) for progressive difficulty
- **Character choice**: Common braille patterns that students will encounter frequently

**Display Layout:**
- Pattern area width calculated as `display_width - 5` to accommodate various displays
- Line indicator always in rightmost 5 cells for consistency
- Format matches example06 score display style (prefix + number)

**Navigation Behavior:**
- **Circular navigation**: Prevents "dead ends" at top/bottom of content
- **Immediate feedback**: Display updates instantly on key press
- **No confirmation**: Direct navigation for fluid practice

**Key BrlAPI Integration:**
- Line Up: `KEY_TYPE_CMD | KEY_CMD_LNUP`
- Line Down: `KEY_TYPE_CMD | KEY_CMD_LNDN`
- Home: `KEY_TYPE_CMD | KEY_CMD_HOME`
- Accept all keys to log unhandled input for debugging

**Extensibility:**
- Easy to add more lines by extending `lines` array
- Pattern types easily extendable (could add "random", "sequence", etc.)
- Line indicator format supports up to 99 lines (2-digit display)

## References
- **example04**: Line navigation concepts (LNUP/LNDN keys)
- **example06**: Display layout with indicator area (score/line number)
- **src/library.py**: `char_to_braille_dots()`, `digit_dots()`, formatting utilities
- **Elm Architecture**: Model-Update-View pattern used throughout examples

