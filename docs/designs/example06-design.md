# Example 06 - Identify the character

## Overview
This app is an educational braille game that teaches character-to-braille mapping. The game displays a random character (a-z) at a random position on the braille display.

**Display format** (20 cells example):
- Cells 0-14: Game area - all blank except one cell showing the target character
- Cells 15-19: Score display - blank, blank, "p", tens digit, units digit (e.g., "p00", "p05", "p12")

**Gameplay:**
The terminal screen shows the target position and character for learning. Players must:
1. Find the character by pressing the cursor routing button under it
2. Type the character using braille dots (Grade 1 Braille)
3. The game provides immediate feedback and tracks score and attempts

## Examples

### Example A
Target: 'a' (dot 1) at position 5
1. User clicks cursor routing button at position 5
2. User presses braille keyboard keys for dot 1
3. Game validates and awards point if correct

### Example X
Target: 'x' (dots 1, 3, 4, 6) at position 7
1. User clicks cursor routing button at position 7
2. User presses braille keyboard keys for dots 1, 3, 4, and 6
3. Game validates and awards point if correct 

## Learning Objectives
- **Concepts taught**: 
  - Spatial awareness on braille display
  - Character-to-braille dot pattern mapping (Grade 1 Braille, a-z)
  - Braille keyboard input practice
- **Patterns demonstrated**: 
  - Navigating the braille display with cursor routing keys
  - Pattern recognition of dot combinations
  - Sequential key input (not simultaneous - dots can be entered one at a time)
  - Elm architecture (Model-Update-View) pattern
- **Builds on previous examples**:
  - Points system similar to example05
  - Key recognition and display techniques from example04
  - Elm architecture foundation from all previous examples

## Requirements

### Functional
- Display a random character at a random position on the braille display
- Accept cursor routing button press to select position
- Accept braille keyboard input (dots 1-6) for character identification
- Validate both position and dot pattern are correct
- Award points for correct answers
- Display score and feedback
- Generate new challenges after correct/incorrect answers
- Option to quit the game
- Log activity for review

### Technical
### Technical
- **Libraries used from src/library.py**:
  - `printProperty` - logging and diagnostics
  - `printDiagnostics` - display connection info
  - `handleConnectionError` - error handling
  - `digitDots` - score display conversion
  - `tens`, `units` - score formatting helpers
  - `charToBrailleDots(char)` - convert a-z to dot pattern (1-6 only)
  - `combineKeysToDots(dotList)` - combine list of dot numbers into single pattern
  - `randomChar()` - get random letter a-z
  - `randomPosition(max)` - get random position in range
  - `dotsToDisplaySize` - ensure display array is correct size

- **Display requirements**: 
  - Minimum 20 cells width
  - 8-dot braille cells
  - Cursor routing buttons

- **Input requirements**:
  - Cursor routing keys (position selection)
  - Braille keyboard dots 1-6 (character identification via command 0x220000)
  - Space key (submit answer / start game / advance after correct answer)
  - Line Down or Home key (quit game)

## Architecture

### Model
```python
{
    "targetChar": "",            # Character to find (a-z)
    "targetPosition": 0,         # Position where character is displayed (0-based)
    "displayWidth": 20,          # Width of braille display
    "score": 0,                  # Current score
    "attempts": 0,               # Number of attempts made
    "currentPhase": "start",     # "start", "waiting", "position_selected", "complete"
    "selectedPosition": None,    # User's position selection
    "selectedDots": [],          # User's dot selections as list (1-6)
    "message": "Press any key to start",  # Current instruction/feedback
    "gameStarted": False,        # Has game started
    "counter": 0,                # Key press counter
}
```

### Update

### Update

**Events/Messages:**
- `GAME_START` - Initialize new game (triggered by space bar in "start" phase)
- `NEW_CHALLENGE` - Generate new character and position (triggered after correct answer)
- `CURSOR_PRESS(position)` - User pressed cursor routing button
- `DOT_KEY(dotNumber)` - User pressed braille keyboard key (1-6)
- `SUBMIT_ANSWER` - User finished entering dots (triggered by space bar)
- `QUIT` - Exit game (Line Down or Home button)

**State Transitions:**
1. **Game Start** (start → waiting): 
   - Set `gameStarted = True`
   - Generate first challenge (targetChar, targetPosition)
   - Set `currentPhase = "waiting"`
   - Initialize score and attempts to 0
   - Display character on braille display

2. **Cursor Press** (waiting → position_selected):
   - Record `selectedPosition`
   - Set `currentPhase = "position_selected"`
   - Reset `selectedDots = []`
   - Show feedback on selected position
   - Wait for dot input

3. **Dot Key Press** (position_selected):
   - Add dot to `selectedDots` list (if not already present)
   - Sort dots for consistency
   - Stay in position_selected phase
   - User presses space to submit

4. **Submit Answer**:
   - Check if `selectedPosition == targetPosition`
     - If wrong: message "Wrong position", reset to "waiting" phase
   - Check if `combineKeysToDots(selectedDots) == charToBrailleDots(targetChar)`
     - If correct:
       - `score += 1`, `attempts += 1`
       - `message = "Correct! [char] found. Score: [score]"`
       - `currentPhase = "complete"`
       - Wait 2 seconds, then generate new challenge
     - If wrong:
       - `message = "Wrong dots. Try again!"`
       - Reset `selectedDots = []`
       - Stay in "position_selected" phase to retry

5. **New Challenge** (complete → waiting):
   - Generate new random character (a-z)
   - Generate new random position in game area
   - Clear selectedPosition and selectedDots
   - Update display
   - Set `currentPhase = "waiting"`

6. **Quit**:
   - Show final score message
   - Set `currentPhase = "start"`, `gameStarted = False`
   - Loop exits when phase != "quit" (note: implementation uses currentPhase != "quit" but actual quit sets to "start")

### View

### View

**Display Layout:**
```
[Game Area (15 cells)                    ][Score (5 cells)]
[.][.][Target][.][.][...][.][.][.][.][.][_][_][p][tens][units]
Position: 0  1    2    3  4   5   6  7  8  9  10 11 12 13  14
```

**Elements:**
- Cells 0-14: Game area - all blank except target position shows target character
- Cells 15-19: Score display - blank, blank, "p" (dots 1,2,3,4), tens digit, units digit
- Cursor (DOT7+DOT8) shown at selected position when user clicks cursor routing button

**Feedback Messages (printed to terminal):**
```
"Press any key to start"
"Find character 'x' at position 7 (press cursor button under it)"
"Position 7 selected. Now press dots for 'x'"
"Correct! 'x' found. Score: 5"
"Wrong position. Try again!"
"Wrong dots. Try again!"
"Game Over! Score: 15/20"
```

**Braille Patterns Used:**
- Standard Grade 1 braille alphabet (a-z using dots 1-6)
- Digit dots for score display (0-9 using numeric braille)
- Letter "p" (dots 1,2,3,4) as score prefix
- Cursor markers (DOT7+DOT8) to show selected position

## Implementation Plan

1. **[✅] Step 1: Library enhancements**
   - Added `charToBrailleDots(char)` - map a-z to braille patterns (Grade 1)
   - Added `combineKeysToDots(dotsList)` - merge dot numbers into single bitmask
   - Added `randomChar()` - select random letter a-z
   - Added `randomPosition(max)` - select random position in range

2. **[✅] Step 2: Model implementation**
   - Created `init(brl)` function with initial state
   - Created `get_message(code, **params)` for message generation with lambda dispatch
   - Created `generate_challenge(display_width)` for new random challenge

3. **[✅] Step 3: Update functions**
   - `update_by_game_start(m)` - initialize game
   - `update_by_new_challenge(m)` - generate new character/position
   - `update_by_cursor_press(m, position)` - handle position selection
   - `update_by_dot_key(m, dot_number)` - handle dot key input (1-6)
   - `update_by_submit(m)` - validate answer and update score
   - `update_by_quit(m)` - end game
   - `update_by_key(brl, m, key_code)` - main key dispatcher
   - Helper functions:
     - `convert_dots_arg_to_list(dots_arg)` - convert bitmask to dot list
     - `handle_dot_input(m, dots_arg)` - process braille keyboard input
     - `handle_space_key(m)` - context-aware space key handler

4. **[✅] Step 4: View rendering**
   - `view(brl, m)` - main rendering function
   - `game_to_dots(m)` - convert game state to braille array
   - `score_to_display(score)` - render score as 5 cells (blank, blank, p, tens, units)
   - `challenge_to_display(m)` - place character and add cursor marker
   - `print_log(m)` - log game state to terminal

5. **[✅] Step 5: Main loop**
   - Setup BrlAPI connection with `acceptKeys(brlapi.rangeType_all, [0])`
   - Enter TTY mode
   - Main game loop handling all key events
   - Auto-advance after 2 second delay on correct answer
   - Proper cleanup and error handling with `handleConnectionError`

6. **[✅] Step 6: Testing**
   - Unit tests added to `tests/test_examples.py`
   - Integration test for game flow
   - Manual testing on actual braille display

7. **[✅] Step 7: Documentation**
   - Added comprehensive docstring to example06.py
   - Documented display layout, architecture, and learning objectives
   - This design document updated to match implementation

## Testing Strategy

**Unit Tests (in tests/test_examples.py):**
- Test `charToBrailleDots()` for letters a-z (Grade 1 braille)
- Test `combineKeysToDots()` for various dot combinations
- Test answer validation logic (position and dots)
- Test message generation for all game states
- Test model initialization and structure

**Integration Tests:**
- Test complete game flow (start → challenge → answer → score → new challenge)
- Test incorrect position handling (resets to waiting phase)
- Test incorrect dots handling (stays in position_selected, allows retry)
- Test score accumulation and attempts counter
- Test quit functionality

**Manual Testing:**
- ✅ Verify display shows character at correct position
- ✅ Verify cursor routing buttons work
- ✅ Verify braille keyboard input recognized correctly (dots 1-6)
- ✅ Verify score updates and displays correctly (p + tens + units)
- ✅ Verify messages print to terminal properly
- ✅ Verify game loop continues until quit
- ✅ Verify 2-second delay after correct answer before new challenge

## Implementation Notes

**Key BrlAPI Constants for Braille Keyboard:**
- Braille dot keys detected via command `0x220000` with argument as dot bitmask
- Individual dots mapped via `brlapi.DOT1` through `brlapi.DOT6`
- Cursor routing keys detected via `KEY_TYPE_CMD` and `KEY_CMD_ROUTE`
- Space bar detected as `KEY_TYPE_CMD | 0x220000` (with argument 0)

**Character-to-Dots Mapping (Grade 1 Braille):**
Implemented in library.py `charToBrailleDots()`:
```
a=1, b=12, c=14, d=145, e=15, f=124, g=1245, h=125, i=24, j=245
k=13, l=123, m=134, n=1345, o=135, p=1234, q=12345, r=1235, s=234, t=2345
u=136, v=1236, w=2456, x=1346, y=13456, z=1356
```
(Where numbers represent dot positions)

**Input Handling:**
- Dots can be entered **sequentially** (one at a time), not necessarily simultaneously
- Selected dots are stored in a sorted list
- Space bar submits the answer
- Wrong position resets to waiting phase (user must click cursor routing button again)
- Wrong dots resets dot list but keeps position selected (user can retry dots immediately)

**Score Display:**
- Score is displayed in last 5 cells of display
- Format: [blank][blank][p][tens digit][units digit]
- "p" uses dots 1,2,3,4
- Digits use standard numeric braille patterns via `digitDots()`

**Design Decisions:**
- Game area is dynamically calculated as `displayWidth - 5` to accommodate various display sizes
- Target position is randomly selected within game area only
- Terminal shows position and character for learning purposes (not just braille)
- 2-second delay after correct answer allows user to see success message
- No time limit per challenge (focus on learning, not speed)
- Attempts counter tracks all submission attempts, not just position selections