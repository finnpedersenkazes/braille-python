# Tests for Braille-Python Development Platform

This directory contains comprehensive tests for the braille-python development platform.

## Test Files

### Unit Tests

- **test_library.py** - Tests for `src/library.py` utility functions
  - Timestamp formatting
  - Braille conversion utilities
  - Display utilities (digitDots, tens, units)
  - Cursor placement
  - Display connection checking

- **test_model.py** - Tests for `src/model.py` module
  - Module structure
  - Template patterns
  - Diagnostics functions

- **test_update.py** - Tests for `src/update.py` module
  - Module structure
  - Update patterns

- **test_view.py** - Tests for `src/view.py` module
  - Module structure
  - View patterns

- **test_main.py** - Tests for `src/main.py` launcher
  - Default example loading
  - Command-line argument parsing
  - Shorthand notation (e.g., "01" → "example01")
  - Error handling for missing examples
  - Handling examples without main() function

### Integration Tests

- **test_examples.py** - Tests for all example files
  - Structure verification (all have main() function)
  - Import testing
  - Elm architecture component checking
  - Syntax validation

- **test_integration.py** - Integration tests for the platform
  - Directory structure verification
  - Elm architecture implementation testing
  - Launcher integration
  - Consistency checks across examples

## Running Tests

### All Tests (Local Development with Hardware)
```bash
pytest tests/
```

### CI/CD Tests (Skip Hardware-Dependent Tests)
```bash
pytest tests/ -m "not hardware"
```

### Only Hardware-Dependent Tests
```bash
pytest tests/ -m "hardware"
```

### Test Markers

**@pytest.mark.hardware** - Marks tests that require:
- brlapi Python module (braille display interface)
- Physical or virtual braille display hardware
- BrlTTY daemon running

These tests are automatically skipped in CI/CD environments where braille hardware is not available.

**Hardware-dependent tests:**
- `test_library.py::test_digit_dots` - Uses brlapi.DOT constants
- `test_library.py::test_full_cell` - Uses brlapi.DOT constants
- `test_library.py::test_underline_cell` - Uses brlapi.DOT constants
- `test_library.py::test_place_cursor` - Uses brlapi.DOT constants
- `test_library.py::test_char_to_braille_dots` - Uses brlapi.DOT constants
- `test_library.py::test_braille_dots_to_char` - Uses brlapi.DOT constants
- `test_library.py::test_combine_keys_to_dots` - Uses brlapi.DOT constants

### Run all tests:
```bash
python -m pytest tests/
```

### Run specific test file:
```bash
python -m pytest tests/test_library.py
```

### Run with unittest:
```bash
python -m unittest discover tests/
```

### Run specific test class:
```bash
python -m unittest tests.test_library.TestLibraryUtilities
```

### Run with coverage:
```bash
python -m pytest --cov=src --cov=examples tests/
```

## Test Coverage

The tests cover:

1. **Utility Functions** - All mathematical and conversion utilities in library.py
2. **Module Structure** - Proper import and structure of all modules
3. **Examples Consistency** - All examples follow the same patterns
4. **Elm Architecture** - Proper implementation of Model-Update-View pattern
5. **Launcher Functionality** - Main launcher works correctly with all examples
6. **Error Handling** - Proper error handling for missing examples and connection issues
7. **Syntax Validation** - All Python files compile without syntax errors

## Test Requirements

Tests use:
- `unittest` (Python standard library)
- `unittest.mock` for mocking BrlAPI connections
- No braille display hardware required for testing

## Notes

- Tests mock BrlAPI connections so they can run without physical braille hardware
- All examples are tested for structure but not full execution (to avoid requiring hardware)
- Integration tests verify the development platform patterns are correctly implemented
