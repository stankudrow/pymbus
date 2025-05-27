from contextlib import AbstractContextManager
from contextlib import nullcontext as does_not_raise

import pytest

from pymbus.exceptions import MBusError
from pymbus.telegrams.blocks import (
    DataInformationBlock as DIB,
)
from pymbus.telegrams.blocks import (
    ValueInformationBlock as VIB,
)
from pymbus.telegrams.records import DataRecord as DR
from pymbus.telegrams.records import DataRecordHeader as DRH


class TestDataRecordHeader:
    @pytest.mark.parametrize(
        ("it", "dib", "vib", "expectation"),
        [
            (
                [0b0111_0000, 0b0111_0000],
                DIB(ibytes=[0b0111_0000]),
                VIB(ibytes=[0b0111_0000]),
                does_not_raise(),
            ),
            ([], [], [], pytest.raises(MBusError)),
            ([-1], None, None, pytest.raises(MBusError)),
        ],
    )
    def test_init(
        self,
        it: list[int],
        dib: None | DIB,
        vib: None | VIB,
        expectation: AbstractContextManager,
    ):
        with expectation:
            dr = DRH(ibytes=it)

            assert dr.dib == dib
            assert dr.vib == vib

    @pytest.mark.parametrize(
        ("data", "answer"),
        [
            (
                b"\x93\xff\x81m\x00\x00\x04\x8d\x00\x03",
                [DIB(ibytes=[147, 255, 129, 109]), VIB(ibytes=[0])],
            )
        ],
    )
    def test_non_greediness(self, data: bytes, answer: list):
        gen = (item for item in data)
        dr = DRH(ibytes=gen)

        blocks = [dr.dib, dr.vib]
        fields = [field for block in blocks for field in block]
        nfields = len(fields)

        assert bytes(map(int, dr)) == data[:nfields]
        assert blocks == answer
        assert list(gen) == list(map(int, data[nfields:]))


class TestDataRecord:
    @pytest.mark.parametrize(
        ("it", "drh", "data", "expectation"),
        [
            (
                [0b0111_0000, 0b0111_0000, 21, 42],
                DRH(ibytes=[0b0111_0000, 0b0111_0000]),
                [21, 42],
                does_not_raise(),
            ),
            ([], [], [], pytest.raises(MBusError)),
            ([-1], None, None, pytest.raises(MBusError)),
        ],
    )
    def test_init(
        self,
        it: list[int],
        drh: None | DRH,
        data: None | list[int],
        expectation: AbstractContextManager,
    ):
        with expectation:
            dr = DR(it)

            assert dr.drh == drh
            assert list(map(int, dr.data)) == data
