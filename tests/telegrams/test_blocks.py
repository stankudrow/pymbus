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
        ("ints", "expectation"),
        [
            ([-1], pytest.raises(MBusValidationError)),
            ([256], pytest.raises(MBusValidationError)),
            ([0b0111_0000], does_not_raise()),
            ([0b1000_1111, 0b0111_0000], does_not_raise()),
        ],
    )
    def test_dib_init_from_integers(
        self, ints: list[int], expectation: AbstractContextManager
    ):
        with expectation:
            DIB.from_integers(ints)

    @pytest.mark.parametrize(
        ("hexstr", "expectation"),
        [
            ("123", pytest.raises(MBusValidationError)),
            ("8f 70", does_not_raise()),
        ],
    )
    def test_dib_init_from_hexstring(
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
    def test_dib_init(
        self, ints: list[int], expectation: AbstractContextManager
    ):
        with expectation:
            DIB(ints)

    def test_dib_iterability(self):
        it = [0b1000_0000, 0b1000_0001, 0b0111_0010]
        dib = DIB(it)

        for df, byte in zip(dib, it, strict=True):
            assert df.byte == byte

    def test_dib_fields_init_non_greedy_capture(self):
        it = [0b1000_0000, 0b1000_0001, 0b0111_0010]
        dib = DIB(it)

        assert list(dib) == it


class TestVIB:
    @pytest.mark.parametrize(
        ("ints", "expectation"),
        [
            ([-1], pytest.raises(MBusValidationError)),
            ([256], pytest.raises(MBusValidationError)),
            ([0b0111_0000], does_not_raise()),
            ([0b1000_1111, 0b0111_0000], does_not_raise()),
        ],
    )
    def test_vib_init_from_integers(
        self, ints: list[int], expectation: AbstractContextManager
    ):
        with expectation:
            VIB.from_integers(ints)

    @pytest.mark.parametrize(
        ("hexstr", "expectation"),
        [
            ("123", pytest.raises(MBusValidationError)),
            ("8f 70", does_not_raise()),
        ],
    )
    def test_vib_init_from_hexstring(
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
    def test_vib_init(
        self, ints: list[int], expectation: AbstractContextManager
    ):
        with expectation:
            VIB(ints)

    def test_vib_iterability(self):
        it = [0b1000_0000, 0b1000_0001, 0b0111_0010]
        vib = VIB(it)

        for df, byte in zip(vib, it, strict=True):
            assert df.byte == byte

    def test_vib_fields_init_non_greedy_capture(self):
        it = [0b1000_0000, 0b1000_0001, 0b0111_0010]
        vib = VIB(it)

        assert list(vib) == it
