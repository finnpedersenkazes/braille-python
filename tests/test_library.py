"""Tests for src/library.py"""
import os
import sys
from datetime import datetime

import pytest

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from library import (
    adjust_dots,
    adjust_number,
    braille_dots_to_char,
    char_to_braille_dots,
    check_display_connected,
    combine_keys_to_dots,
    digit_dots,
    dots_to_display_size,
    format_time_stamp,
    full_cell,
    place_cursor,
    random_char,
    random_position,
    tens,
    underline_cell,
    units,
)


def test_format_timestamp():
    """Test timestamp formatting for filenames"""
    dt = datetime(2024, 1, 15, 14, 30, 45)
    result = format_time_stamp(dt)
    assert result == "2024-01-15T14-30"
def test_adjust_number():
    """Test number adjustment for braille translation"""
    assert adjust_number(32768) == 0
    assert adjust_number(32769) == 1
    assert adjust_number(32800) == 32


def test_dots_to_display_size():
    """Test padding dots array to display size"""
    dots = bytes([1, 2, 3])
    result = dots_to_display_size(dots, 5)
    assert result == bytes([1, 2, 3, 0, 0])

    # Test when dots longer than size
    dots = bytes([1, 2, 3, 4, 5])
    result = dots_to_display_size(dots, 3)
    assert result == bytes([1, 2, 3])


@pytest.mark.hardware
def test_digit_dots():
    """Test digit to braille dots conversion"""
    import brlapi

    # Test digit 0
    result = digit_dots(0)
    expected = brlapi.DOT3 | brlapi.DOT4 | brlapi.DOT5 | brlapi.DOT6
    assert result == expected

    # Test digit 1
    result = digit_dots(1)
    expected = brlapi.DOT1 | brlapi.DOT6
    assert result == expected

    # Test invalid digit
    result = digit_dots(10)
    assert result == 0

    # Test negative
    result = digit_dots(-1)
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


@pytest.mark.hardware
def test_full_cell():
    """Test full braille cell generation"""
    import brlapi
    result = full_cell()
    expected = (
        brlapi.DOT1 | brlapi.DOT2 | brlapi.DOT3 | brlapi.DOT4 |
        brlapi.DOT5 | brlapi.DOT6 | brlapi.DOT7 | brlapi.DOT8
    )
    assert result == expected


@pytest.mark.hardware
def test_underline_cell():
    """Test underline cell generation"""
    import brlapi
    result = underline_cell()
    expected = chr(brlapi.DOT7 + brlapi.DOT8)
    assert result == expected


@pytest.mark.hardware
def test_place_cursor():
    """Test cursor placement in dots array"""
    import brlapi
    dots = bytes([10, 20, 30, 40])
    result = place_cursor(dots, 2)

    # Third element should have DOT7 and DOT8 added
    expected = bytes([
        10,
        20,
        30 | brlapi.DOT7 | brlapi.DOT8,
        40
    ])
    assert result == expected


def test_adjust_dots():
    """Test dots adjustment (inverse of adjust_number)"""
    assert adjust_dots(0) == 0x8000
    assert adjust_dots(1) == 0x8001


def test_check_display_connected():
    """Test display connection check"""
    from unittest.mock import Mock

    # Mock connected display
    brl = Mock()
    brl.displaySize = (20, 1)
    assert check_display_connected(brl) is True

    # Mock disconnected display (width = 0)
    brl.displaySize = (0, 0)
    assert check_display_connected(brl) is False

    # Mock disconnected display (height = 0)
    brl.displaySize = (20, 0)
    assert check_display_connected(brl) is False


@pytest.mark.hardware
def test_char_to_braille_dots():
    """Test character to braille dots conversion"""
    import brlapi

    # Test lowercase letters
    assert char_to_braille_dots('a') == brlapi.DOT1
    assert char_to_braille_dots('b') == brlapi.DOT1 | brlapi.DOT2
    assert char_to_braille_dots('x') == brlapi.DOT1 | brlapi.DOT3 | brlapi.DOT4 | brlapi.DOT6
    assert char_to_braille_dots('z') == brlapi.DOT1 | brlapi.DOT3 | brlapi.DOT5 | brlapi.DOT6

    # Test uppercase (should convert to lowercase)
    assert char_to_braille_dots('A') == brlapi.DOT1
    assert char_to_braille_dots('Z') == brlapi.DOT1 | brlapi.DOT3 | brlapi.DOT5 | brlapi.DOT6

    # Test non-alphabet characters (should return 0)
    assert char_to_braille_dots('1') == 0
    assert char_to_braille_dots('?') == 0


@pytest.mark.hardware
def test_braille_dots_to_char():
    """Test braille dots to character conversion"""
    import brlapi

    # Test basic conversions
    assert braille_dots_to_char(brlapi.DOT1) == 'a'
    assert braille_dots_to_char(brlapi.DOT1 | brlapi.DOT2) == 'b'
    assert braille_dots_to_char(brlapi.DOT1 | brlapi.DOT3 | brlapi.DOT4 | brlapi.DOT6) == 'x'

    # Test invalid dots
    assert braille_dots_to_char(0) == '?'
    assert braille_dots_to_char(brlapi.DOT7 | brlapi.DOT8) == '?'


@pytest.mark.hardware
def test_combine_keys_to_dots():
    """Test combining dot numbers to braille pattern"""
    import brlapi

    # Test single dot
    assert combine_keys_to_dots([1]) == brlapi.DOT1

    # Test multiple dots
    result = combine_keys_to_dots([1, 3, 4, 6])
    expected = brlapi.DOT1 | brlapi.DOT3 | brlapi.DOT4 | brlapi.DOT6
    assert result == expected

    # Test all dots 1-6
    result = combine_keys_to_dots([1, 2, 3, 4, 5, 6])
    expected = brlapi.DOT1 | brlapi.DOT2 | brlapi.DOT3 | brlapi.DOT4 | brlapi.DOT5 | brlapi.DOT6
    assert result == expected

    # Test empty list
    assert combine_keys_to_dots([]) == 0

    # Test invalid dot numbers (should be ignored)
    assert combine_keys_to_dots([1, 7, 8]) == brlapi.DOT1


def test_random_char():
    """Test random character generation"""
    # Test it returns a lowercase letter
    for _ in range(10):
        char = random_char()
        assert len(char) == 1
        assert char.islower()
        assert char.isalpha()
        assert 'a' <= char <= 'z'


def test_random_position():
    """Test random position generation"""
    # Test it returns position in range
    for _ in range(10):
        pos = random_position(20)
        assert 0 <= pos < 20
        assert isinstance(pos, int)

    # Test with small max
    pos = random_position(1)
    assert pos == 0
