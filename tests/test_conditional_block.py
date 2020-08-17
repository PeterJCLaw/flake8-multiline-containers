import os

from flake8.api import legacy as flake8

import pytest


@pytest.fixture
def conditional_block_file_path(dummy_file_path):
    return f'{dummy_file_path}/conditional_block.py'


def test_pl101_conditional_block(conditional_block_file_path):
    style_guide = flake8.get_style_guide(
        select=['PL101'],
    )

    p = os.path.abspath(conditional_block_file_path)
    r = style_guide.check_files([p])

    assert 2 == r.total_errors


def test_pl110_conditional_block(conditional_block_file_path):
    style_guide = flake8.get_style_guide(
        select=['PL110'],
    )

    p = os.path.abspath(conditional_block_file_path)
    r = style_guide.check_files([p])

    assert 2 == r.total_errors
