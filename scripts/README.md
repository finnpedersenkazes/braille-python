# Scripts

Utility scripts for setting up and diagnosing braille display configurations.

## Available Scripts

### diagnostics.py

Python script for diagnosing braille display setup and configuration.

**Usage:**
```bash
python scripts/diagnostics.py
```

### setup_braille_display.sh

Shell script for setting up a braille display on Linux systems.

**Usage:**
```bash
bash scripts/setup_braille_display.sh
```

### fix_brltty_installation.sh

Shell script for fixing common BRLTTY installation issues.

**Usage:**
```bash
bash scripts/fix_brltty_installation.sh
```

## Requirements

- BRLTTY installed
- Appropriate system permissions (may require sudo)
- For Python scripts: Python 3.8+ with python3-brlapi and python3-louis installed
