import os

from flake8.api import legacy as flake8

import pytest


@pytest.fixture
def class_def_file_path(dummy_file_path):
    return f'{dummy_file_path}/callable/class_def.py'


def test_pl101_class_def(class_def_file_path):
    style_guide = flake8.get_style_guide(
        select=['PL101'],
    )

    p = os.path.abspath(class_def_file_path)
    r = style_guide.check_files([p])

    assert 1 == r.total_errors


def test_pl110_class_def(class_def_file_path):
    style_guide = flake8.get_style_guide(
        select=['PL110'],
    )

    p = os.path.abspath(class_def_file_path)
    r = style_guide.check_files([p])

    assert 1 == r.total_errors
