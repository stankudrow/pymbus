from collections.abc import Iterable
from math import isclose
from typing import Literal

import pytest

from pymbus.constants import BIG_ENDIAN, LITTLE_ENDIAN
from pymbus.exceptions import MBusError
from pymbus.mbtypes import (
    parse_int,
    parse_uint,
)


@pytest.mark.parametrize("endianness", [BIG_ENDIAN, LITTLE_ENDIAN])
@pytest.mark.parametrize(
    ("it", "answer"),
    [
        ([0b0000_0000], 0),
        ([0b1000_0000], -128),
        ([0b1000_0001], -127),
        ([0b0111_1111], 127),
        ([0b1111_1111], -1),
        # (
        #     # <255, 1>
        #
        #     # non-negative -> 1 & 0x80 = 0 (False)
        #     # 11) 0 << 8 = 0
        #     # 12) 0 + 0000_0001 = 1
        #     # 21) 1 <<< 8 = 1_0000_0000 = 256
        #     # 22) 256 + 1111_1111 = 256 + 255 = 511
        #     511,
        # ),
        # (
        #     # <255, 129>
        #     [0b1111_1111, 0b1000_0001],
        #     # non-negative -> 129 & 0x80 = 1
        #     # 11) 0 << 8 = 0
        #     # 12) 0 + (129 ^ 0xFF) = 0 + 0111_1110 = 126
        #     # 21) 128 << 8 = 0111_1110_0000_0000 = 32256
        #     # 22) 32256 + (255 ^ 0xFF) = 32256
        #     # neg -> True -> (-32256) - 1 = -32257
        #     -32257,
        # ),
    ],
)
def test_parse_int_byte(
    it: Iterable, endianness: Literal["big", "little"], answer: int
):
    assert parse_int(bytes(it), byteorder=endianness) == answer


@pytest.mark.parametrize(
    ("it", "endianness", "answer"),
    [
        (
            [0b1111_1111, 0b0000_0001],
            # [0xFF, 0x01]
            # 0xFF => minus (MSB is 1) -> work with 0x7F = 127
            # ~0xFF = 0b0000_0000 -> 0x00 = 0
            # ~0x01 = 0b1111_1110 -> 0xFE = 254
            # Total: -((254 + 0) + 1) = -255
            BIG_ENDIAN,
            -255,
        ),
        (
            [0b1111_1111, 0b0000_0001],
            LITTLE_ENDIAN,
            511,  # [0x01, 0xFF] = 256 + 255 = 511
        ),
    ],
)
def test_parse_int_bytes(
    it: Iterable, endianness: Literal["big", "little"], answer: int
):
    assert parse_int(bytes(it), byteorder=endianness) == answer


def test_parse_int_empty():
    with pytest.raises(MBusError):
        parse_int(bytes([]))


@pytest.mark.parametrize("endianness", [BIG_ENDIAN, LITTLE_ENDIAN])
@pytest.mark.parametrize(
    ("it", "answer"),
    [
        ([0b0000_0000], 0),
        ([0b1000_0000], 128),
        ([0b1111_1111], 255),
    ],
)
def test_parse_uint_byte(
    it: Iterable, endianness: Literal["big", "little"], answer: int
):
    assert parse_uint(bytes(it), byteorder=endianness) == answer


@pytest.mark.parametrize(
    ("it", "endianness", "answer"),
    [
        (
            [0b1111_1111, 0b0000_0001],
            BIG_ENDIAN,
            65281,
        ),
        (
            [0b1111_1111, 0b0000_0001],
            LITTLE_ENDIAN,
            511,
        ),
    ],
)
def test_parse_uint_bytes(
    it: Iterable, endianness: Literal["big", "little"], answer: int
):
    assert parse_uint(bytes(it), byteorder=endianness) == answer


def test_parse_uint_empty():
    with pytest.raises(MBusError):
        parse_uint(bytes([]))


@pytest.mark.parametrize(
    ("data", "answer"),
    [
        (b"\x00\x00\x1f\x40", 8000),
        (b"\x00\x00\x27\xb6", 10166),
        (b"\x00\x00\x17\xf4", 6132),
        (b"\x00\x00\x00\x2f", 47),
        (b"\x00\x00\x0c\x72", 3186),
        (b"\x07\x6d", 1901),
        (b"\x07\x12", 1810),
        (b"\x00\x00\x4a\x45", 19013),
    ],
)
def test_positive_ints(data: bytes, answer: float):
    int_res = parse_int(data)
    uint_res = parse_uint(data)

    assert isclose(int_res, answer)
    assert isclose(uint_res, answer)
