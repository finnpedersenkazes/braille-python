"""pytest configuration and fixtures"""
import sys
import os

# Add src and examples to path for all tests
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'examples'))
