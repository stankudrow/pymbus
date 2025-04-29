from contextlib import AbstractContextManager
from contextlib import nullcontext as does_not_raise

import pytest

from pymbus.exceptions import MBusLengthError
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
            )
        ],
    )
    def test_dr_init(
        self,
        it: list[int],
        dib: DIB,
        vib: VIB,
        expectation: AbstractContextManager,
    ):
        with expectation:
            dr = DR(ibytes=it)

            assert dr.dib == dib
            assert dr.vib == vib
