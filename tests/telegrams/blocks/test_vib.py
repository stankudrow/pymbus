from collections.abc import Iterable
from contextlib import nullcontext as does_not_raise
from typing import ContextManager

import pytest

from pymbus.exceptions import MBusError
from pymbus.telegrams.blocks.value_info import ValueInformationBlock as VIB
from pymbus.telegrams.fields.value_info import (
    ValueInformationField as VIF,
)
from pymbus.telegrams.fields.value_info import (
    ValueInformationFieldExtension as VIFE,
)


@pytest.mark.parametrize(
    ("ints", "expectation"),
    [
        ([-1], pytest.raises(ValueError)),
        ([256], pytest.raises(ValueError)),
        ([0b1000_1111, 0b0111_0000], does_not_raise()),
    ],
)
def test_vib_init_from_integers(ints: list[int], expectation: ContextManager):
    with expectation:
        vib = VIB.from_integers(ints)

        assert vib.as_bytes() == bytes(ints)


@pytest.mark.parametrize(
    ("hexstr", "expectation"),
    [
        ("123", pytest.raises(ValueError)),
        ("8f 70", does_not_raise()),
    ],
)
def test_vib_init_from_hexstring(hexstr: str, expectation: ContextManager):
    with expectation:
        vib = VIB.from_hexstring(hexstr)

        assert vib.as_bytes() == bytes.fromhex(hexstr)


@pytest.mark.parametrize(
    ("ints", "expectation"),
    [
        ([-1], pytest.raises(MBusError)),
        ([256], pytest.raises(MBusError)),
        ([0b0111_1111], does_not_raise()),
        ([0b1000_1111, 0b0111_0000], does_not_raise()),
        (
            [
                0b1000_1111,
                0b1000_0000,
                0b1000_0001,
                0b1000_0010,
                0b1000_0011,
                0b1000_0100,
                0b1000_0101,
                0b1000_0110,
                0b1000_0111,
                0b1000_1000,
                0b0000_1001,
            ],
            does_not_raise(),
        ),
        (
            [
                0b1000_1111,
                0b1000_0000,
                0b1000_0001,
                0b1000_0010,
                0b1000_0011,
                0b1000_0100,
                0b1000_0101,
                0b1000_0110,
                0b1000_0111,
                0b1000_1000,
                0b1000_1001,
            ],
            pytest.raises(MBusError),
        ),
    ],
)
def test_vib_init(ints: list[int], expectation: ContextManager):
    with expectation:
        vib = VIB(ints)

        assert vib.as_bytes() == bytes(ints)


@pytest.mark.parametrize(
    ("it",),
    [([0b1000_1111, 0b0111_0000],), ([0b1000_1111, 0b0111_0000],)],
)
def test_dib_repr_and_str(it: Iterable):
    vib = VIB(it)

    fields = vib.fields
    repstr = f"ValueInformationBlock(fields={fields})"

    difes = it[1:] if len(it) > 1 else []
    strstr = str([VIF(it[0])] + [VIFE(bt) for bt in difes])

    assert repr(vib) == repstr
    assert str(vib) == strstr


def test_for_loop_over_vib():
    it = [0b1000_0000, 0b1000_0001, 0b0111_0010]
    dib = VIB(it)

    for df, byte in zip(dib, it, strict=True):
        assert df.byte == byte
