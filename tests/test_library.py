"""Tests for src/library.py"""
import sys
import os
import pytest
from datetime import datetime

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from library import (
    formatTimeStamp,
    adjustNumber,
    dotsToDisplaySize,
    digitDots,
    tens,
    units,
    fullCell,
    underlineCell,
    placeCursor,
    adjustDots,
    checkDisplayConnected,
)


def test_format_timestamp():
    """Test timestamp formatting for filenames"""
    dt = datetime(2024, 1, 15, 14, 30, 45)
    result = formatTimeStamp(dt)
    assert result == "2024-01-15T14-30"
def test_adjust_number():
    """Test number adjustment for braille translation"""
    assert adjustNumber(32768) == 0
    assert adjustNumber(32769) == 1
    assert adjustNumber(32800) == 32


def test_dots_to_display_size():
    """Test padding dots array to display size"""
    dots = bytes([1, 2, 3])
    result = dotsToDisplaySize(dots, 5)
    assert result == bytes([1, 2, 3, 0, 0])
    
    # Test when dots longer than size
    dots = bytes([1, 2, 3, 4, 5])
    result = dotsToDisplaySize(dots, 3)
    assert result == bytes([1, 2, 3])


def test_digit_dots():
    """Test digit to braille dots conversion"""
    import brlapi
    
    # Test digit 0
    result = digitDots(0)
    expected = brlapi.DOT3 | brlapi.DOT4 | brlapi.DOT5 | brlapi.DOT6
    assert result == expected
    
    # Test digit 1
    result = digitDots(1)
    expected = brlapi.DOT1 | brlapi.DOT6
    assert result == expected
    
    # Test invalid digit
    result = digitDots(10)
    assert result == 0
    
    # Test negative
    result = digitDots(-1)
    assert result == 0


def test_tens():
    """Test extracting tens digit"""
    assert tens(0) == 0
    assert tens(5) == 0
    assert tens(15) == 1
    assert tens(99) == 9
    assert tens(100) == 0
    assert tens(156) == 5


def test_units():
    """Test extracting units digit"""
    assert units(0) == 0
    assert units(5) == 5
    assert units(15) == 5
    assert units(99) == 9
    assert units(156) == 6


def test_full_cell():
    """Test full braille cell generation"""
    import brlapi
    result = fullCell()
    expected = (
        brlapi.DOT1 | brlapi.DOT2 | brlapi.DOT3 | brlapi.DOT4 |
        brlapi.DOT5 | brlapi.DOT6 | brlapi.DOT7 | brlapi.DOT8
    )
    assert result == expected


def test_underline_cell():
    """Test underline cell generation"""
    import brlapi
    result = underlineCell()
    expected = chr(brlapi.DOT7 + brlapi.DOT8)
    assert result == expected


def test_place_cursor():
    """Test cursor placement in dots array"""
    import brlapi
    dots = bytes([10, 20, 30, 40])
    result = placeCursor(dots, 2)
    
    # Third element should have DOT7 and DOT8 added
    expected = bytes([
        10,
        20,
        30 | brlapi.DOT7 | brlapi.DOT8,
        40
    ])
    assert result == expected


def test_adjust_dots():
    """Test dots adjustment (inverse of adjustNumber)"""
    assert adjustDots(0) == 0x8000
    assert adjustDots(1) == 0x8001


def test_check_display_connected():
    """Test display connection check"""
    from unittest.mock import Mock
    
    # Mock connected display
    brl = Mock()
    brl.displaySize = (20, 1)
    assert checkDisplayConnected(brl) is True
    
    # Mock disconnected display (width = 0)
    brl.displaySize = (0, 0)
    assert checkDisplayConnected(brl) is False
    
    # Mock disconnected display (height = 0)
    brl.displaySize = (20, 0)
    assert checkDisplayConnected(brl) is False
