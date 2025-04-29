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
            # <255, 1>
            [0b1111_1111, 0b0000_0001],
            # non-negative -> 1 & 0x80 = 0 (False)
            # 11) 0 << 8 = 0
            # 12) 0 + 0000_0001 = 1
            # 21) 1 <<< 8 = 1_0000_0000 = 256
            # 22) 256 + 1111_1111 = 256 + 255 = 511
            511,
        ),
        (
            # <255, 129>
            [0b1111_1111, 0b1000_0001],
            # non-negative -> 129 & 0x80 = 1
            # 11) 0 << 8 = 0
            # 12) 0 + (129 ^ 0xFF) = 0 + 0111_1110 = 126
            # 21) 128 << 8 = 0111_1110_0000_0000 = 32256
            # 22) 32256 + (255 ^ 0xFF) = 32256
            # neg -> True -> (-32256) - 1 = -32257
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
            # <255, 1>
            [0b1111_1111, 0b0000_0001],
            # 11) 0 << 8 = 0
            # 12) 0 + 0000_0001 = 1
            # 21) 1 <<< 8 = 1_0000_0000 = 256
            # 22) 256 + 1111_1111 = 256 + 255 = 511
            511,
        ),
        (
            [0b0000_0001, 0b1111_1111],
            65281,
        ),
    ],
)
def test_parse_uint(it: Iterable, answer: int):
    bytez = bytes(it)

    result = parse_uint(bytez)

    assert result == answer


def test_parse_uint_empty():
    with pytest.raises(MBusError):
        parse_uint(bytes([]))
