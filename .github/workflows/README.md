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
- Tests require functional brlapi connection to actual braille displays
- Importing brlapi/louis at module level causes CI failures

**Hardware tests (35 total) are skipped in CI**, including:
- Tests in `test_library.py` using brlapi.DOT* constants (7 tests)
- Tests in `test_examples.py` that import example files (18 tests)
- Tests in `test_integration.py` that run Elm architecture validation (3 tests)
- Tests in `test_model.py` requiring hardware (1 test)
- Additional tests requiring brlapi functionality (6 tests)

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
- **CI tests:** 49 (non-hardware)
- **Hardware tests:** 35 (skipped in CI)

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
