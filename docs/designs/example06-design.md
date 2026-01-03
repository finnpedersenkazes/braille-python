# Example 06 - Identify the character

## Overview
This app is an educational app with the purpose of introducing braille characters to the student. 
The student has to find the character that we present, find it on the braille display, then click the corresponding cursor button to identify the position and press the keys representing the character on the braille keyboard. That is, the keys 1, 2, 3, 4, 5 and 6. 

## Examples

### Example A
Place an 'a' (dot 1) in position 5. 
The user clicks the cursor at position 5 and presses the key 1. 

### Example X
Place an 'x' (dot 1, 3, 4, 6) in position 7. 
The user clicks the cursor at position 7 and presses the keys 1, 3, 4, and 6 simultaneously. 

## Learning Objectives
- **Concepts taught**: Finding and identifying braille characters from the normal alphabet
- **Patterns demonstrated**: 
  - Navigating the braille display with cursor routing keys
  - Pattern recognition of dot combinations
  - Multi-key simultaneous input
- **Builds on previous examples**:
  - Points system from example05
  - Key recognition and display from example04
  - Elm architecture (Model-Update-View) pattern

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
- **Libraries needed from src/library.py**:
  - `printProperty` - logging
  - `printDiagnostics` - display info
  - `formatTimeStamp` - log filename
  - `currentDateTime` - timestamps
  - `handleConnectionError` - error handling
  - `digitDots` - score display
  - `tens`, `units` - score formatting

- **New functions to add to library**:
  - `charToBrailleDots(char)` - convert a-z to dot pattern (1-6 only)
  - `dotsToChar(dotPattern)` - convert dot pattern back to character
  - `randomChar()` - get random letter a-z
  - `randomPosition(displayWidth)` - get random position on display
  - `keyCodeToDotNumber(keyCode)` - map BrlAPI key codes to dots 1-6
  - `combineKeysToDots(keyList)` - combine multiple simultaneous key presses into dot pattern

- **Display requirements**: 
  - Minimum 20 cells width
  - 8-dot braille cells
  - Cursor routing buttons

- **Input requirements**:
  - Cursor routing keys (position selection)
  - Braille keyboard dots 1-6 (character identification)
  - Space or Enter key (skip/next)
  - Escape key (quit game)

## Architecture

### Model
```python
{
    "targetChar": "x",           # Character to find (a-z)
    "targetPosition": 7,         # Position where character is displayed (0-based)
    "displayWidth": 20,          # Width of braille display
    "score": 0,                  # Current score
    "attempts": 0,               # Number of attempts made
    "currentPhase": "waiting",   # "waiting", "position_selected", "complete", "incorrect"
    "selectedPosition": None,    # User's position selection
    "selectedDots": [],          # User's dot selections (1-6)
    "message": "Find: x",        # Current instruction/feedback
    "gameStarted": False,        # Has game started
    "displayArray": [],          # Braille dots array for display
}
```

### Update

**Events/Messages:**
- `GAME_START` - Initialize new game
- `NEW_CHALLENGE` - Generate new character and position
- `CURSOR_PRESS(position)` - User pressed cursor routing button
- `DOT_KEY(dotNumber)` - User pressed braille keyboard key (1-6)
- `SUBMIT_ANSWER` - User finished entering dots (timeout or explicit submit)
- `SKIP` - Skip current challenge
- `QUIT` - Exit game

**State Transitions:**
1. **Game Start**: 
   - Set `gameStarted = True`
   - Generate first challenge (targetChar, targetPosition)
   - Set `currentPhase = "waiting"`
   - Display character on braille display

2. **Cursor Press** (waiting phase):
   - Record `selectedPosition`
   - Set `currentPhase = "position_selected"`
   - Show feedback on selected position
   - Wait for dot input

3. **Dot Key Press** (position_selected phase):
   - Add dot to `selectedDots` list
   - Update display to show entered dots
   - Auto-submit after timeout (1 second) or all 6 dots entered

4. **Submit Answer**:
   - Check if `selectedPosition == targetPosition` AND `selectedDots match targetChar`
   - If correct:
     - `score += 1`
     - `message = "Correct! [char] at position [pos]"`
     - `currentPhase = "complete"`
     - Generate new challenge after delay
   - If incorrect:
     - `message = "Try again"`
     - `currentPhase = "incorrect"`
     - Reset selectedPosition and selectedDots
     - Keep same challenge

5. **New Challenge**:
   - Generate new random character (a-z)
   - Generate new random position
   - Clear selections
   - Update display
   - Increment attempts

### View

**Display Layout:**
```
[Score][.][.][Target Char][.][.][.][Other Chars][.][.][.][.][.][.][.][.][.][.]
Position: 0  1  2     3      4  5  6      7       8  9  10 11 12 13 14 15 16 17...
```

**Elements:**
- First 2 cells: Score (tens and units)
- Remaining cells: Challenge character at target position, random fill characters at other positions
- Cursor (DOT7+DOT8) shown at selected position when user clicks

**Feedback Messages (shown via print):**
```
"Find the character 'x' and press its dots"
"You selected position 7"
"Press dots: 1, 3, 4, 6 for 'x'"
"Correct! +1 point. Score: 5"
"Incorrect position. Try again."
"Incorrect dots. Try again."
"Game Over! Final score: 15/20"
```

**Braille Patterns Used:**
- Standard braille alphabet (a-z using dots 1-6)
- Digit dots for score display
- Cursor markers (DOT7+DOT8)

## Implementation Plan

1. **[ ] Step 1: Library enhancements**
   - Add `charToBrailleDots(char)` - map a-z to braille patterns
   - Add `keyCodeToDotNumber(keyCode)` - map BrlAPI keys to dots 1-6
   - Add `combineKeysToDots(dotsList)` - merge dot numbers into single pattern
   - Add `randomChar()` - select random letter
   - Add `randomPosition(max)` - select random position

2. **[ ] Step 2: Model implementation**
   - Create `init()` function with initial state
   - Create `getMessage(code, params)` for localized messages
   - Create `generateChallenge(displayWidth)` for new random challenge

3. **[ ] Step 3: Update functions**
   - `updateByGameStart(m)` - initialize game
   - `updateByNewChallenge(m)` - generate new character/position
   - `updateByCursorPress(m, position)` - handle position selection
   - `updateByDotKey(m, dotNumber)` - handle dot key input
   - `updateBySubmit(m)` - validate answer and update score
   - `updateBySkip(m)` - skip current challenge
   - `updateByQuit(m)` - end game

4. **[ ] Step 4: View rendering**
   - `view(brl, m)` - main rendering function
   - `gameToDots(m)` - convert game state to braille array
   - `scoreToDisplay(score, displayWidth)` - render score in first cells
   - `challengeToDisplay(char, position, displayWidth)` - place character and fill
   - `cursorToDisplay(dots, position)` - add cursor marker

5. **[ ] Step 5: Main loop**
   - Setup BrlAPI connection
   - Enter TTY mode
   - Main game loop handling all key events
   - Proper cleanup and error handling

6. **[ ] Step 6: Testing**
   - Unit tests for new library functions
   - Integration test for game flow
   - Manual testing on actual braille display

7. **[ ] Step 7: Documentation**
   - Update examples/README.md with example06 entry
   - Add inline code comments
   - Update test files

## Testing Strategy

**Unit Tests:**
- Test `charToBrailleDots()` for all letters a-z
- Test `keyCodeToDotNumber()` for dots 1-6
- Test `combineKeysToDots()` for various combinations
- Test answer validation logic

**Integration Tests:**
- Test complete game flow (start → challenge → answer → score → new challenge)
- Test incorrect answer handling
- Test score accumulation
- Test quit functionality

**Manual Testing:**
- Verify display shows character at correct position
- Verify cursor routing buttons work
- Verify braille keyboard input recognized correctly
- Verify simultaneous key press detection
- Verify score updates correctly
- Verify messages display properly

## Open Questions

1. **Difficulty progression**: Should later challenges use more complex characters or multiple characters?
2. **Time limit**: Should there be a time limit per challenge?
3. **Hint system**: Should we provide hints if user struggles (e.g., highlight correct position)?
4. **Character set**: Start with just lowercase a-z, or include numbers/punctuation?
5. **Answer input**: 
   - Should user press all dots simultaneously (harder, more realistic)?
   - Or sequentially (easier for learning)?
   - Or support both modes?
6. **Wrong position handling**: If position is wrong, should we:
   - Let them try again immediately?
   - Or show correct position and ask for dots only?
7. **Scoring**: 
   - Simple +1 per correct?
   - Or bonus points for speed/accuracy?
   - Penalty for wrong attempts?

## Notes

**Key BrlAPI Constants for Braille Keyboard:**
- Need to identify key codes for dots 1-6 on braille keyboard
- May vary by device model
- Use example04 key detection code to map keys during development

**Character-to-Dots Mapping (Grade 1 Braille):**
```
a=1, b=12, c=14, d=145, e=15, f=124, g=1245, h=125, i=24, j=245
k=13, l=123, m=134, n=1345, o=135, p=1234, q=12345, r=1235, s=234, t=2345
u=136, v=1236, w=2456, x=1346, y=13456, z=1356
```
(Where numbers represent dot positions)

**References:**
- example04: Key handling and diagnostics
- example05: Score display and game loop
- src/library.py: Existing utilities to build upon