import os

from flake8.api import legacy as flake8

import pytest


@pytest.fixture
def string_file_path(dummy_file_path):
    return f'{dummy_file_path}/string/string.py'


@pytest.fixture
def string_brackets_file_path(dummy_file_path):
    return f'{dummy_file_path}/string/string_brackets.py'


def test_pl101_string_ignore(string_file_path):
    """When opening and closing characters are in a string
    Then the linter should not detect them.
    """
    style_guide = flake8.get_style_guide(
        select=['PL101'],
    )

    p = os.path.abspath(string_file_path)
    r = style_guide.check_files([p])

    assert 0 == r.total_errors


def test_pl110_string_ignore(string_file_path):
    """When opening and closing characters are in a string
    Then the linter should not detect them.
    """
    style_guide = flake8.get_style_guide(
        select=['PL110'],
    )

    p = os.path.abspath(string_file_path)
    r = style_guide.check_files([p])

    assert 0 == r.total_errors


def test_pl101_string_brackets_ignore(string_brackets_file_path):
    """When opening and closing characters are in a string
    Then the linter should not detect them.
    """
    style_guide = flake8.get_style_guide(
        select=['PL101'],
    )

    p = os.path.abspath(string_brackets_file_path)
    r = style_guide.check_files([p])

    assert 0 == r.total_errors


def test_pl102_string_brackets_ignore(string_brackets_file_path):
    """When opening and closing characters are in a string
    Then the linter should not detect them.
    """
    style_guide = flake8.get_style_guide(
        select=['PL102'],
    )

    p = os.path.abspath(string_brackets_file_path)
    r = style_guide.check_files([p])

    assert 1 == r.total_errors


def test_pl110_string_brackets_ignore(string_brackets_file_path):
    """When opening and closing characters are in a string
    Then the linter should not detect them.
    """
    style_guide = flake8.get_style_guide(
        select=['PL110'],
    )

    p = os.path.abspath(string_brackets_file_path)
    r = style_guide.check_files([p])

    assert 0 == r.total_errors
