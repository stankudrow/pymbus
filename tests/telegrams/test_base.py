from collections.abc import Iterable
from contextlib import AbstractContextManager
from contextlib import nullcontext as does_not_raise
from operator import and_, or_, xor
from typing import Any

import pytest

from pymbus.exceptions import MBusValidationError
from pymbus.telegrams.base import (
    TelegramContainer,
    TelegramField,
)


class TestTelegramField:
    @pytest.mark.parametrize(
        ("nbr", "expectation"),
        [
            (-1, pytest.raises(MBusValidationError)),
            (0, does_not_raise()),
            (128, does_not_raise()),
            (255, does_not_raise()),
            (256, pytest.raises(MBusValidationError)),
        ],
    )
    def test_init(self, nbr: int, expectation: AbstractContextManager):
        with expectation:
            TelegramField(nbr)

    def test_is_int(self):
        assert isinstance(TelegramField(4), int)

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

        assert (tf << 2) == (nbr << 2)
        assert (tf >> 1) == (nbr >> 1)

    def test_repr(self):
        tf = TelegramField(255)
        assert repr(tf) == "TelegramField(255)"


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
        answer: None | Iterable[int],
        expectation: AbstractContextManager,
    ):
        with expectation:
            tc = TelegramContainer.from_hexstring(hexstr)
            assert tc == answer

    def test_init(self):
        ctx = does_not_raise()
        nums = [0, 128, 255]

        with ctx:
            assert TelegramContainer(bytes(nums))
        with ctx:
            assert TelegramContainer(bytearray(nums))
        with ctx:
            assert TelegramContainer(nums)
        with ctx:
            assert TelegramContainer(TelegramField(num) for num in nums)

    @pytest.mark.parametrize(
        ("it", "value", "answer"),
        [([], 0, False), ([1], 1, True), ([2], 3, False), ([4, 5], 5, True)],
    )
    def test_contains(self, it: Iterable, value: Any, answer: bool):
        assert (value in TelegramContainer(it)) == answer

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

    @pytest.mark.parametrize("it", [[], [1], [3, 2]])
    def test_reversed(self, it: list[int]):
        tc = TelegramContainer(it)

        assert tuple(reversed(tc)) == tuple(reversed(it))

    @pytest.mark.parametrize(
        ("it", "value", "start", "stop", "expectation"),
        [
            ([], 0, 0, 0, pytest.raises(ValueError)),
            ([1, 2], 2, 0, 2, does_not_raise()),
            ([1, 2], 2, 1, 2, does_not_raise()),
            ([1, 2], 2, 0, 1, pytest.raises(ValueError)),
            ([1, 2], 1, 1, 2, pytest.raises(ValueError)),
        ],
    )
    def test_index(
        self,
        it: Iterable,
        value: Any,
        *,
        start: int,
        stop: int,
        expectation: AbstractContextManager,
    ):
        res, ans = None, None
        seq = list(it)

        with expectation:
            res = TelegramContainer(seq).index(value, start, stop)

        with expectation:
            ans = seq.index(value, start, stop)

        assert res == ans

    @pytest.mark.parametrize(
        ("it", "value", "answer"),
        [
            ([], 0, 0),
            ([1], 0, 0),
            ([2, 3], 2, 1),
            ([1, 2, 1, 3], 1, 2),
            ([3, 4, 1], 1, 1),
        ],
    )
    def test_count(self, it: Iterable, value: Any, answer: Any):
        assert TelegramContainer(it).count(value) == answer
