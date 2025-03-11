from contextlib import AbstractContextManager
from contextlib import nullcontext as does_not_raise

import pytest

from pymbus.exceptions import MBusError
from pymbus.telegrams.fields.value_info import (
    ValueInformationField as VIF,
)
from pymbus.telegrams.fields.value_info import (
    ValueInformationFieldExtension as VIFE,
)

## the VIF section


@pytest.mark.parametrize(
    ("byte", "expectation"),
    [
        (-1, pytest.raises(MBusError)),
        (0, does_not_raise()),
        (255, does_not_raise()),
        (256, pytest.raises(MBusError)),
    ],
)
def test_vif_init(byte: int, expectation: AbstractContextManager):
    with expectation:
        VIF(byte=byte)


def test_vif_repr():
    byte = 0xFF

    vif = VIF(byte)
    assert repr(vif) == f"ValueInformationField(byte={byte})"


@pytest.mark.parametrize(
    ("byte", "ext_bit"),
    [
        (0b1111_1111, 1),
        (0b0111_1111, 0),
    ],
)
def test_vif_extension_bit(byte: int, ext_bit: int):
    vif = VIF(byte=byte)

    assert vif.extension == ext_bit


@pytest.mark.parametrize(
    ("byte", "unit"),
    [
        (0b1111_1111, 0b0111_1111),
        (0b0011_1111, 0b0011_1111),
    ],
)
def test_vif_unit(byte: int, unit: int):
    vif = VIF(byte=byte)

    assert vif.unit == unit


## the VIFE section


@pytest.mark.parametrize(
    ("byte", "expectation"),
    [
        (-1, pytest.raises(MBusError)),
        (0, does_not_raise()),
        (255, does_not_raise()),
        (256, pytest.raises(MBusError)),
    ],
)
def test_vife_init(byte: int, expectation: AbstractContextManager):
    with expectation:
        VIFE(byte=byte)


def test_vife_repr():
    byte = 0xFF

    vife = VIFE(byte)
    assert repr(vife) == f"ValueInformationFieldExtension(byte={byte})"


@pytest.mark.parametrize(
    ("byte", "ext_bit"),
    [
        (0b1111_1111, 1),
        (0b0111_1111, 0),
    ],
)
def test_vife_extension_bit(byte: int, ext_bit: int):
    vife = VIFE(byte=byte)

    assert vife.extension == ext_bit


@pytest.mark.parametrize(
    ("byte", "unit"),
    [
        (0b1111_1111, 0b0111_1111),
        (0b0011_1111, 0b0011_1111),
    ],
)
def test_vife_unit(byte: int, unit: int):
    vife = VIFE(byte=byte)

    assert vife.unit == unit
