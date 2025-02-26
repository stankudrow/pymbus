from collections.abc import Iterable

import pytest

from pymbus.exceptions import MBusError
from pymbus.mbtypes import (
    parse_int,
    parse_uint,
)


@pytest.mark.parametrize(
    ("it", "answer"),
    [
        ([0b0000_0000], 0),
        ([0b1000_0000], -128),
        ([0b1000_0001], -127),
        ([0b0111_1111], 127),
        ([0b1111_1111], -1),
        (
            # 0b0000_0001 <+> 0b1111_1111
            # 256 + 255 = 511
            [0b1111_1111, 0b0000_0001],
            511,
        ),
        (
            # 0b1000_0001 <+> 0b1111_1111
            # 0b0111_1110 <+> 0b0000_0000
            # -(0b0111_1110_0000_0000 + 1)
            # -(32356 + 1) -> -32257
            [0b1111_1111, 0b1000_0001],
            -32257,
        ),
    ],
)
def test_parse_int(it: Iterable, answer: int):
    assert parse_int(bytes(it)) == answer


def test_parse_int_empty():
    with pytest.raises(MBusError):
        parse_int(bytes([]))


@pytest.mark.parametrize(
    ("it", "answer"),
    [
        ([0b0000_0000], 0),
        ([0b1000_0000], 128),
        ([0b1111_1111], 255),
        (
            # 0b0000_0001 <+> 0b1111_1111
            # 256 + 255 = 511
            [0b0000_0001, 0b1111_1111],
            511,
        ),
    ],
)
def test_parse_uint(it: Iterable, answer: int):
    assert parse_uint(bytes(it)) == answer


def test_parse_uint_empty():
    with pytest.raises(MBusError):
        parse_uint(bytes([]))
