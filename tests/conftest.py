"""pytest configuration and fixtures"""
import os
import sys

# Add src and examples to path for all tests
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'examples'))


def pytest_configure(config):
    """Register custom markers"""
    config.addinivalue_line(
        "markers", "hardware: mark test as requiring braille display hardware"
    )
