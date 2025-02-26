from collections.abc import Iterable

import pytest

from pymbus.mbtypes import parse_bool


@pytest.mark.parametrize(
    ("it", "answer"),
    [
        ([0b0000_0000], False),
        ([0b0000_0001], True),
        ([0b0000_0000, 0b0000_0001], True),
        ([0b0000_0001, 0b0000_0000], True),
        ([0b0000_0000, 0b0000_0000], False),
    ],
)
def test_parse_boolean(it: Iterable, answer: int):
    assert parse_bool(bytes(it)) == answer
