from contextlib import AbstractContextManager
from contextlib import nullcontext as does_not_raise

import pytest

from pymbus.exceptions import MBusError
from pymbus.telegrams.base import (
    TelegramContainer,
    TelegramField,
    parse_byte,
    validate_byte,
)


def _get_byte_test_data() -> tuple[
    tuple[str, str], list[tuple[int, AbstractContextManager]]
]:
    params = ("nbr", "expectation")
    matrix = [
        (-1, pytest.raises(MBusError)),
        (0, does_not_raise()),
        (128, does_not_raise()),
        (255, does_not_raise()),
        (256, pytest.raises(MBusError)),
    ]
    return (params, matrix)


@pytest.mark.parametrize(*_get_byte_test_data())
def test_byte_validator(nbr: int, expectation: AbstractContextManager):
    with expectation:
        validate_byte(nbr=nbr)


@pytest.mark.parametrize(*_get_byte_test_data())
def test_byte_parsing(nbr: int, expectation: AbstractContextManager):
    with expectation:
        assert parse_byte(nbr) == parse_byte(TelegramField(nbr))


class TestTelegramField:
    @pytest.mark.parametrize(*_get_byte_test_data())
    def test_init(self, nbr: int, expectation: AbstractContextManager):
        with expectation:
            TelegramField(nbr)

    def test_equality(self):
        nbr = 5
        tf = TelegramField(nbr)

        assert tf == TelegramField(nbr)
        assert tf == nbr
        assert tf != "5"

        non_nbr = nbr + 1
        assert tf != TelegramField(non_nbr)
        assert tf != non_nbr

    def test_byte_ro(self):
        nbr = 128
        tf = TelegramField(nbr)

        assert tf.byte == nbr


class TestTelegramContainer:
    def test_init_from(self):
        hexstr = "00 FF"
        ints = [0, 255]

        tf1 = TelegramContainer.from_hexstring(hexstr)
        tf2 = TelegramContainer.from_integers(ints)

        assert tf1 == tf2

    def test_as_bytes(self):
        tc = TelegramContainer.from_integers([0, 12, 23, 66])

        bytez = bytes(tf.byte for tf in tc)

        assert tc.as_bytes() == bytez
