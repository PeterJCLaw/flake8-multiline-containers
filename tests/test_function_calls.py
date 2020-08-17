import os

from flake8.api import legacy as flake8

import pytest


@pytest.fixture
def function_calls_file_path(dummy_file_path):
    return f'{dummy_file_path}/callable/function_call.py'


def test_pl101_function_calls(function_calls_file_path):
    style_guide = flake8.get_style_guide(
        select=['PL101'],
    )

    p = os.path.abspath(function_calls_file_path)
    r = style_guide.check_files([p])

    assert 6 == r.total_errors


def test_pl102_function_calls(function_calls_file_path):
    style_guide = flake8.get_style_guide(
        select=['PL102'],
    )

    p = os.path.abspath(function_calls_file_path)
    r = style_guide.check_files([p])

    assert 5 == r.total_errors


def test_pl110_function_calls(function_calls_file_path):
    style_guide = flake8.get_style_guide(
        select=['PL110'],
    )

    p = os.path.abspath(function_calls_file_path)
    r = style_guide.check_files([p])

    assert 1 == r.total_errors
