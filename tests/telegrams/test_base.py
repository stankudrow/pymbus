from contextlib import AbstractContextManager
from contextlib import nullcontext as does_not_raise

import pytest

from pymbus.exceptions import MBusError
from pymbus.telegrams.base import (
    TelegramContainer,
    TelegramField,
)


class TestTelegramField:
    @pytest.mark.parametrize(
        ("nbr", "expectation"),
        [
            (-1, pytest.raises(MBusError)),
            (0, does_not_raise()),
            (128, does_not_raise()),
            (255, does_not_raise()),
            (256, pytest.raises(MBusError)),
        ],
    )
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

    def test_byte_property(self):
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

    @pytest.mark.parametrize(
        ("container", "key", "answer"),
        [
            (TelegramContainer([21, 42]), 0, TelegramField(21)),
            (TelegramContainer([21, 42]), 1, TelegramField(42)),
            (
                TelegramContainer([21, 42]),
                slice(0, 2, 1),
                TelegramContainer([21, 42]),
            ),
            (
                TelegramContainer([21, 42]),
                slice(0, 1, 1),
                TelegramContainer([21]),
            ),
            (
                TelegramContainer([21, 42]),
                slice(1, 2, 1),
                TelegramContainer([42]),
            ),
        ],
    )
    def test_getitem(
        self,
        container: TelegramContainer,
        key: int | slice,
        answer: TelegramField | TelegramContainer,
    ):
        assert container[key] == answer

    def test_as_bytes(self):
        tc = TelegramContainer.from_integers([0, 12, 23, 66])

        bytez = bytes(tf.byte for tf in tc)

        assert tc.as_bytes() == bytez
