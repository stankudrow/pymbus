from contextlib import AbstractContextManager
from contextlib import nullcontext as does_not_raise

import pytest

from pymbus.exceptions import MBusError
from pymbus.telegrams.fields.address import (
    AF_BROADCAST_ALL_SLAVES_REPLY_BYTE,
    AF_BROADCAST_NO_SLAVE_REPLIES_BYTE,
    AF_NETWORK_LAYER_BYTE,
    AF_SLAVE_MAX_RANGE_VALUE_BYTE,
    AF_SLAVE_MIN_RANGE_VALUE_BYTE,
    AF_UNCONFIGURED_SLAVE_BYTE,
    AddressField,
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
def test_address_field_init(byte: int, expectation: AbstractContextManager):
    with expectation:
        field = AddressField(byte)

        assert field.byte == byte


def test_is_unconfigured_slave():
    af = AddressField(AF_UNCONFIGURED_SLAVE_BYTE)

    assert af.is_unconfigured_slave()
    assert not af.is_configured_slave()


@pytest.mark.parametrize(
    "byte",
    [
        AF_UNCONFIGURED_SLAVE_BYTE,
        AF_SLAVE_MIN_RANGE_VALUE_BYTE,
        AF_SLAVE_MIN_RANGE_VALUE_BYTE + 1,
        AF_SLAVE_MAX_RANGE_VALUE_BYTE - 1,
        AF_SLAVE_MAX_RANGE_VALUE_BYTE,
    ],
)
def test_is_configured_slave(byte: int):
    af = AddressField(byte)

    assert af.is_configured_slave()
    assert not af.is_unconfigured_slave()


@pytest.mark.parametrize(
    "byte",
    [
        AF_UNCONFIGURED_SLAVE_BYTE,
        AF_SLAVE_MIN_RANGE_VALUE_BYTE,
        AF_SLAVE_MIN_RANGE_VALUE_BYTE + 1,
        AF_SLAVE_MAX_RANGE_VALUE_BYTE - 1,
        AF_SLAVE_MAX_RANGE_VALUE_BYTE,
    ],
)
def test_is_slave(byte: int):
    af = AddressField(byte)

    assert af.is_slave()


@pytest.mark.parametrize(
    ("byte", "answer"),
    [
        (AF_BROADCAST_ALL_SLAVES_REPLY_BYTE, True),
        (AF_BROADCAST_NO_SLAVE_REPLIES_BYTE, True),
        (AF_NETWORK_LAYER_BYTE, False),
    ],
)
def test_is_broadcast(byte: int, answer: bool):
    af = AddressField(byte)

    assert af.is_broadcast() == answer


def test_is_network_layer():
    af = AddressField(AF_NETWORK_LAYER_BYTE)

    assert not af.is_broadcast()
    assert not af.is_slave()

    assert af.is_network_layer()
