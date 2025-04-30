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


class TestDataRecord:
    @pytest.mark.parametrize(
        ("it", "dib", "vib", "expectation"),
        [
            (
                [0b0111_0000, 0b0111_0000],
                DIB(ibytes=[0b0111_0000]),
                VIB(ibytes=[0b0111_0000]),
                does_not_raise(),
            ),
            ([-1], None, None, pytest.raises(MBusError)),
        ],
    )
    def test_dr_init(
        self,
        it: list[int],
        dib: None | DIB,
        vib: None | VIB,
        expectation: AbstractContextManager,
    ):
        with expectation:
            dr = DR(ibytes=it)

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
def test_binary_data_parsing(data: bytes, answer: list):
    dr = DR(ibytes=data)

    blocks = [dr.dib, dr.vib]

    assert dr.as_bytes() == data
    assert blocks == answer
