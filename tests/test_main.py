"""Tests for src/main.py"""
import sys
import os
import pytest
from unittest.mock import patch, MagicMock

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import main


def test_main_default_example():
    """Test main launcher with default example"""
    with patch('builtins.__import__') as mock_import:
        mock_module = MagicMock()
        mock_module.main = MagicMock()
        mock_import.return_value = mock_module

        with patch.object(sys, 'argv', ['main.py']):
            main.main()

        mock_import.assert_called_once_with('example05')
        mock_module.main.assert_called_once()


def test_main_shorthand_example():
    """Test main launcher with shorthand example name (01 -> example01)"""
    with patch('builtins.__import__') as mock_import:
        mock_module = MagicMock()
        mock_module.main = MagicMock()
        mock_import.return_value = mock_module

        with patch.object(sys, 'argv', ['main.py', '01']):
            main.main()

        mock_import.assert_called_once_with('example01')
        mock_module.main.assert_called_once()


def test_main_full_example_name():
    """Test main launcher with full example name"""
    with patch('builtins.__import__') as mock_import:
        mock_module = MagicMock()
        mock_module.main = MagicMock()
        mock_import.return_value = mock_module

        with patch.object(sys, 'argv', ['main.py', 'example02']):
            main.main()

        mock_import.assert_called_once_with('example02')
        mock_module.main.assert_called_once()


def test_main_example_with_letter_suffix():
    """Test example with letter suffix (04 -> example04)"""
    with patch('builtins.__import__') as mock_import:
        mock_module = MagicMock()
        mock_module.main = MagicMock()
        mock_import.return_value = mock_module

        with patch.object(sys, 'argv', ['main.py', '04']):
            main.main()

        mock_import.assert_called_once_with('example04')
        mock_module.main.assert_called_once()


def test_main_invalid_example():
    """Test handling of invalid example name"""
    with patch('builtins.__import__', side_effect=ImportError("No module named 'example99'")):
        with patch.object(sys, 'argv', ['main.py', '99']):
            with pytest.raises(SystemExit) as exc_info:
                main.main()
            assert exc_info.value.code == 1


def test_main_example_without_main_function():
    """Test handling example without main() function"""
    with patch('builtins.__import__') as mock_import:
        mock_module = MagicMock(spec=[])  # No main attribute
        mock_import.return_value = mock_module

        with patch.object(sys, 'argv', ['main.py', '01']):
            # Should not raise an error
            main.main()

        mock_import.assert_called_once_with('example01')
