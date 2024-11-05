from contextlib import nullcontext as does_not_raise
from typing import ContextManager

import pytest

from pymbus.exceptions import MBusError
from pymbus.telegrams.fields.control import (
    ControlField,
)


@pytest.mark.parametrize(
    ("byte", "expectation"),
    [
        (-1, pytest.raises(MBusError)),
        (0, does_not_raise()),
        (255, does_not_raise()),
        (256, pytest.raises(MBusError)),
    ],
)
def test_field_init(byte: int, expectation: ContextManager):
    with expectation:
        field = ControlField(byte)

        assert field.byte == byte


@pytest.mark.parametrize(
    ("byte", "answer"),
    [
        (0b0000_0000, 0x00),
        (0b0000_0101, 0x05),
        (0b0000_1010, 0x0A),
        (0b0000_1111, 0x0F),
    ],
)
def test_code_property(byte: int, answer: int):
    cf = ControlField(byte)

    assert cf.code == answer


@pytest.mark.parametrize(
    ("byte", "answer", "expectation"),
    [
        (0b0100_0000, 0, does_not_raise()),
        (0b0101_0000, 1, does_not_raise()),
        (0b0000_0000, None, pytest.raises(AttributeError)),
    ],
)
def test_fcv_property(
    byte: int, answer: None | int, expectation: ContextManager
):
    with expectation:
        cf = ControlField(byte)

        assert cf.fcv == answer

        assert cf.is_calling_direction()
        assert cf.direction == 1


@pytest.mark.parametrize(
    ("byte", "answer", "expectation"),
    [
        (0b0100_0000, 0, does_not_raise()),
        (0b0110_0000, 1, does_not_raise()),
        (0b0000_0000, None, pytest.raises(AttributeError)),
    ],
)
def test_fcb_property(
    byte: int, answer: None | int, expectation: ContextManager
):
    with expectation:
        cf = ControlField(byte)

        assert cf.fcb == answer

        assert cf.is_calling_direction()
        assert cf.direction == 1


@pytest.mark.parametrize(
    ("byte", "answer", "expectation"),
    [
        (0b0000_0000, 0, does_not_raise()),
        (0b0001_0000, 1, does_not_raise()),
        (0b0100_0000, None, pytest.raises(AttributeError)),
    ],
)
def test_dfc_property(
    byte: int, answer: None | int, expectation: ContextManager
):
    with expectation:
        cf = ControlField(byte)

        assert cf.dfc == answer

        assert cf.is_reply_direction()
        assert cf.direction == 0


@pytest.mark.parametrize(
    ("byte", "answer", "expectation"),
    [
        (0b0000_0000, 0, does_not_raise()),
        (0b0010_0000, 1, does_not_raise()),
        (0b0100_0000, None, pytest.raises(AttributeError)),
    ],
)
def test_acd_property(
    byte: int, answer: None | int, expectation: ContextManager
):
    with expectation:
        cf = ControlField(byte)

        assert cf.acd == answer

        assert cf.is_reply_direction()
        assert cf.direction == 0
