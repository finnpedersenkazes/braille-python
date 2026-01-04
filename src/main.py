#!/usr/bin/env python3

"""
Main launcher for braille application examples
Runs the selected example application

Usage:
    python src/main.py           # Runs example05 (default)
    python src/main.py example05 # Runs example05
    python src/main.py 03c       # Runs example03c
"""

import os
import sys


def main():
    """Launch the selected example"""
    # Add examples directory to path
    examples_dir = os.path.join(os.path.dirname(__file__), '..', 'examples')
    sys.path.insert(0, examples_dir)

    # Default example to run
    example_name = "example05"

    # Allow command line argument to specify which example to run
    if len(sys.argv) > 1:
        example_name = sys.argv[1]
        # Allow shorthand like "05" or "3c" instead of full "example05"
        if not example_name.startswith("example"):
            example_name = "example" + example_name

    try:
        # Import and run the selected example
        print(f"Running {example_name}...")
        example_module = __import__(example_name)

        # Check if the module has a main() function
        if hasattr(example_module, 'main'):
            example_module.main()
        else:
            # Old-style examples run on import, so just indicate completion
            print(f"{example_name} completed (no main() function, executed on import)")
    except ImportError as e:
        print(f"Error: Could not import {example_name}")
        print(f"Make sure the file examples/{example_name}.py exists")
        print(f"Details: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
