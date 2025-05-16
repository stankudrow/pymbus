from contextlib import AbstractContextManager
from contextlib import nullcontext as does_not_raise
from operator import and_, or_, xor

import pytest

from pymbus.exceptions import MBusValidationError
from pymbus.telegrams.base import (
    TelegramContainer,
    TelegramField,
)


class TestTelegramField:
    @pytest.mark.parametrize(
        ("nbr", "validate", "expectation"),
        [
            (-1, True, pytest.raises(MBusValidationError)),
            (-1, False, does_not_raise()),
            (0, False, does_not_raise()),
            (0, True, does_not_raise()),
            (128, True, does_not_raise()),
            (255, False, does_not_raise()),
            (255, True, does_not_raise()),
            (256, True, pytest.raises(MBusValidationError)),
            (256, False, does_not_raise()),
        ],
    )
    def test_init(
        self, nbr: int, validate: bool, expectation: AbstractContextManager
    ):
        with expectation:
            TelegramField(nbr, validate=validate)

    def test_comparison_ops(self):
        nbr = 21
        tf = TelegramField(nbr + 1)

        assert TelegramField(nbr) == nbr
        assert tf != nbr
        assert tf > nbr
        assert tf >= nbr
        assert nbr < tf
        assert nbr <= tf

    def test_to_int(self):
        nbr = 21

        result = int(TelegramField(nbr))

        assert isinstance(result, int)
        assert result == nbr

    def test_bitwise_ops(self):
        nbr = 42
        tf = TelegramField(nbr)

        for op in (and_, or_, xor):
            assert op(tf, 21) == op(nbr, 21)

        assert ~tf == ~nbr


class TestTelegramContainer:
    @pytest.mark.parametrize(
        ("hexstr", "answer", "expectation"),
        [
            ("", [], does_not_raise()),
            ("00 80 FF", [0, 128, 255], does_not_raise()),
            ("XY", None, pytest.raises(MBusValidationError)),
        ],
    )
    def test_from_hexstring(
        self,
        hexstr: str,
        answer: None | list[int],
        expectation: AbstractContextManager,
    ):
        with expectation:
            tc = TelegramContainer.from_hexstring(hexstr)
            assert tc == answer

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

    def test_comparison_ops(self):
        assert TelegramContainer([2, 1]) == [2, 1]
        assert TelegramContainer([2, 1]) != [1, 2]
        assert TelegramContainer([1, 2]) < [2, 1]
        assert TelegramContainer([1, 2]) <= [2, 1]
        assert TelegramContainer([2, 1]) > [1]
        assert TelegramContainer([2, 1]) >= [1]
