import os

from flake8.api import legacy as flake8

import pytest


@pytest.fixture
def function_calls_file_path(dummy_file_path):
    return f'{dummy_file_path}/callable/function_call.py'


def test_js101_function_calls(function_calls_file_path):
    style_guide = flake8.get_style_guide(
        select=['JS101'],
    )

    p = os.path.abspath(function_calls_file_path)
    r = style_guide.check_files([p])

    assert 9 == r.total_errors


def test_js102_function_calls(function_calls_file_path):
    style_guide = flake8.get_style_guide(
        select=['JS102'],
    )

    p = os.path.abspath(function_calls_file_path)
    r = style_guide.check_files([p])

    assert 2 == r.total_errors
