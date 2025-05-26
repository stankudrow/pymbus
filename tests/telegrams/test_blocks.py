from contextlib import AbstractContextManager
from contextlib import nullcontext as does_not_raise

import pytest

from pymbus.exceptions import MBusLengthError, MBusValidationError
from pymbus.telegrams.blocks import (
    DataInformationBlock as DIB,
)
from pymbus.telegrams.blocks import (
    ValueInformationBlock as VIB,
)


class TestDIB:
    @pytest.mark.parametrize(
        ("hexstr", "expectation"),
        [
            ("123", pytest.raises(MBusValidationError)),
            ("8f 70", does_not_raise()),
        ],
    )
    def test_init_from_hexstring(
        self, hexstr: str, expectation: AbstractContextManager
    ):
        with expectation:
            DIB.from_hexstring(hexstr)

    @pytest.mark.parametrize(
        ("ints", "expectation"),
        [
            ([-1], pytest.raises(MBusValidationError)),
            ([256], pytest.raises(MBusValidationError)),
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
                pytest.raises(MBusLengthError),
            ),
        ],
    )
    def test_init(self, ints: list[int], expectation: AbstractContextManager):
        with expectation:
            DIB(ints)

    def test_iterability(self):
        it = [0b1000_0000, 0b1000_0001, 0b0111_0010]
        dib = DIB(it)

        for df, byte in zip(dib, it, strict=True):
            assert int(df) == byte

    @pytest.mark.parametrize(
        ("it", "nbytes"),
        [
            ([0b1000_0000, 0b1000_0001, 0b0111_0010], 3),
            ([0b1000_0000, 0b0000_0000, 0b1111_1111], 2),
        ],
    )
    def test_non_greediness(self, it: list[int], nbytes: int):
        gen = (el for el in it)
        dib = DIB(gen)

        assert list(dib) == it[:nbytes]
        assert list(gen) == it[nbytes:]


class TestVIB:
    @pytest.mark.parametrize(
        ("hexstr", "expectation"),
        [
            ("123", pytest.raises(MBusValidationError)),
            ("8f 70", does_not_raise()),
        ],
    )
    def test_init_from_hexstring(
        self, hexstr: str, expectation: AbstractContextManager
    ):
        with expectation:
            VIB.from_hexstring(hexstr)

    @pytest.mark.parametrize(
        ("ints", "expectation"),
        [
            ([-1], pytest.raises(MBusValidationError)),
            ([256], pytest.raises(MBusValidationError)),
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
                pytest.raises(MBusLengthError),
            ),
        ],
    )
    def test_init(self, ints: list[int], expectation: AbstractContextManager):
        with expectation:
            VIB(ints)

    def test_iterability(self):
        it = [0b1000_0000, 0b1000_0001, 0b0111_0010]
        vib = VIB(it)

        for df, byte in zip(vib, it, strict=True):
            assert int(df) == byte

    @pytest.mark.parametrize(
        ("it", "nbytes"),
        [
            ([0b1000_0000, 0b1000_0001, 0b0111_0010], 3),
            ([0b1000_0000, 0b0000_0000, 0b1111_1111], 2),
        ],
    )
    def test_non_greediness(self, it: list[int], nbytes: int):
        gen = (el for el in it)
        dib = DIB(gen)

        assert list(dib) == it[:nbytes]
        assert list(gen) == it[nbytes:]
