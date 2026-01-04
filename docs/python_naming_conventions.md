# Python Naming Conventions (Project Guidelines)

This document defines **naming conventions** to be used consistently across this Python project.

These rules are based on **PEP 8** and common Python ecosystem practices. They are not enforced by the language but are assumed by tools, libraries, and experienced Python developers.

---

## 1. General Principles

- Naming is about **communicating intent**.
- Prefer **clarity over brevity**.
- Be consistent across the entire codebase.
- Follow community conventions so code looks *idiomatic Python*.

---

## 2. Variables

**Format:** `snake_case`

```python
counter_value = 42
braille_display_size = (40, 1)
is_connected = True
```

Rules:
- Lowercase letters
- Words separated by underscores
- Avoid unclear abbreviations

---

## 3. Functions

**Format:** `snake_case`

```python
def read_display():
    pass

def write_text_to_display(text):
    pass
```

Guidelines:
- Use **verbs** or verb phrases
- Boolean-returning functions should start with `is_`, `has_`, or `can_`

```python
def is_connected():
    pass
```

---

## 4. Classes

**Format:** `PascalCase` (CapWords)

```python
class BrailleDisplay:
    pass
```

Guidelines:
- Use **nouns**
- No underscores
- First letter capitalized

---

## 5. Constants

**Format:** `UPPER_SNAKE_CASE`

```python
MAX_RETRIES = 3
DEFAULT_TIMEOUT_SECONDS = 5
USB_VENDOR_ID = 0x1C71
```

Notes:
- Python does not enforce constants
- UPPERCASE signals *do not modify*
- Usually defined at module level

---

## 6. Modules & Packages

### Modules (files)

```text
braille_driver.py
usb_utils.py
display_config.py
```

### Packages (directories)

```text
braille/
braille/drivers/
braille/utils/
```

Rules:
- `snake_case`
- Short, descriptive names
- No hyphens, no PascalCase

---

## 7. Public vs Private Names

### Internal (non-public) names

Prefix with a single underscore:

```python
_internal_buffer = []

def _read_raw_bytes():
    pass
```

Meaning:
> Internal implementation detail. Not part of the public API.

### Name mangling (rare)

```python
class Device:
    def __reset(self):
        pass
```

This becomes `_Device__reset` internally.

Use sparingly.

---

## 8. Class Attributes & Instance Variables

```python
class BrailleDisplay:
    def __init__(self, driver_name):
        self.driver_name = driver_name
        self.display_size = None
        self._connection = None
```

Rules:
- Same conventions as variables
- Use leading underscore for internal state

---

## 9. Exceptions

**Format:** `PascalCase` + `Error`

```python
class BrailleError(Exception):
    pass

class DeviceNotFoundError(BrailleError):
    pass
```

Always end exception names with `Error`.

---

## 10. Type Variables (Typing / Generics)

```python
from typing import TypeVar

T = TypeVar("T")
```

Conventions:
- Single uppercase letter for generic use
- Descriptive name for domain-specific types

```python
DisplayType = TypeVar("DisplayType")
```

---

## 11. What to Avoid

Avoid:

```python
list = []        # shadows built-in
str = "abc"     # shadows built-in
```

Avoid unclear names:

```python
a = 10
x = device
```

Avoid non-Python styles:

```python
def WriteText():  # C#/Java style (wrong in Python)
    pass
```

---

## 12. Reference Example

```python
MAX_COUNTER_VALUE = 100

class BrailleDisplay:
    def __init__(self, driver_name):
        self.driver_name = driver_name
        self._connected = False

    def connect(self):
        self._connected = True

    def is_connected(self):
        return self._connected

    def write_counter(self, value):
        if not self.is_connected():
            raise DeviceNotFoundError("Display not connected")
        print(f"counter: {value}")


class DeviceNotFoundError(Exception):
    pass
```

---

## 13. Summary

- `snake_case` → variables, functions, modules
- `PascalCase` → classes, exceptions
- `UPPER_SNAKE_CASE` → constants
- `_leading_underscore` → internal/private
- Naming communicates **intent**, not enforcement

Follow these conventions consistently throughout the project.

