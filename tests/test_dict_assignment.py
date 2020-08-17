import os

from flake8.api import legacy as flake8

import pytest


@pytest.fixture
def dict_file_path(dummy_file_path):
    return f'{dummy_file_path}/dict/dict_assignment.py'


def test_pl101_dict(dict_file_path):
    style_guide = flake8.get_style_guide(
        select=['PL101'],
    )

    p = os.path.abspath(dict_file_path)
    r = style_guide.check_files([p])

    assert 0 == r.total_errors


def test_pl110_dict(dict_file_path):
    style_guide = flake8.get_style_guide(
        select=['PL110'],
    )

    p = os.path.abspath(dict_file_path)
    r = style_guide.check_files([p])

    assert 0 == r.total_errors
