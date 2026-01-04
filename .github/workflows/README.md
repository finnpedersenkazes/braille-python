# GitHub Actions Workflows

## lint.yml - Lint and Test Workflow

This workflow runs on every push and performs code quality checks and testing.

### Configuration

- **Python Version:** 3.12
- **Runner:** ubuntu-latest
- **Linter:** ruff 0.14.10
- **Test Framework:** pytest

### Workflow Steps

1. **Checkout code** - Get repository contents
2. **Set up Python** - Install Python 3.12
3. **Install system dependencies** - Install braille library development headers
   - `liblouis-dev` - Braille translation library headers
   - `libbrlapi-dev` - BrlAPI development headers
   - `pkg-config` - Package configuration tool
4. **Install Python dependencies** - Install ruff, pytest, and project requirements
5. **Lint with ruff** - Check code quality (must pass with 0 issues)
6. **Run tests** - Execute test suite (skip hardware-dependent tests)

### Hardware-Dependent Tests

Tests requiring physical braille display hardware are marked with `@pytest.mark.hardware` and automatically skipped in CI/CD using:

```bash
pytest tests/ -m "not hardware"
```

**Why skip hardware tests?**
- CI runners don't have braille display hardware
- `brlapi` and `louis` Python modules require system-installed packages that are not available in pip
- System packages (`python3-brlapi`, `python3-louis`) are tied to system Python, not the workflow's Python version

**Hardware tests that are skipped in CI:**
- `test_library.py::test_digit_dots`
- `test_library.py::test_full_cell`
- `test_library.py::test_underline_cell`
- `test_library.py::test_place_cursor`
- `test_library.py::test_char_to_braille_dots`
- `test_library.py::test_braille_dots_to_char`
- `test_library.py::test_combine_keys_to_dots`

These tests use `brlapi.DOT*` constants which require the brlapi module.

### Local Testing

Run all tests including hardware-dependent ones:
```bash
pytest tests/
```

Run only non-hardware tests (simulate CI):
```bash
pytest tests/ -m "not hardware"
```

Run only hardware tests:
```bash
pytest tests/ -m "hardware"
```

### Test Results

- **Total tests:** 84
- **CI tests:** 77 (84 - 7 hardware-dependent)
- **Hardware tests:** 7

All non-hardware tests must pass for the workflow to succeed.

### Troubleshooting

**Issue:** `ModuleNotFoundError: No module named 'brlapi'`
- **Solution:** This is expected in CI. Hardware tests are automatically skipped.

**Issue:** Tests pass locally but fail in CI
- **Cause:** Test may be using brlapi but not marked with `@pytest.mark.hardware`
- **Solution:** Add `@pytest.mark.hardware` decorator to the test

**Issue:** Workflow fails at lint step
- **Cause:** Code doesn't meet ruff quality standards
- **Solution:** Run `ruff check .` locally and fix issues, or use `ruff check . --fix` for auto-fixes
