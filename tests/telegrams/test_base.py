from contextlib import nullcontext as does_not_raise
from typing import ContextManager

import pytest

from pymbus.exceptions import MBusError
from pymbus.telegrams.base import TelegramField, parse_byte, validate_byte


@pytest.mark.parametrize(
    ("nbr", "expectation"),
    [
        (-129, pytest.raises(MBusError)),
        (-1, pytest.raises(MBusError)),
        (0, does_not_raise()),
        (255, does_not_raise()),
        (256, pytest.raises(MBusError)),
    ],
)
def test_byte_validator(nbr: int, expectation: ContextManager):
    with expectation:
        validate_byte(nbr=nbr)


def test_byte_parsing():
    for byte in (0, 255):
        assert parse_byte(byte) == parse_byte(TelegramField(byte))
