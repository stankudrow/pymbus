from contextlib import AbstractContextManager
from contextlib import nullcontext as does_not_raise

import pytest

from pymbus.exceptions import MBusError
from pymbus.mbtypes import (
    UnitType,
    parse_unit_type,
)


@pytest.mark.parametrize(
    ("ibytes", "expectation"),
    [
        ([], pytest.raises(MBusError)),
        ([1, 2], does_not_raise()),
    ],
)
def test_unit_type_info_parsing(
    ibytes: list[int], expectation: AbstractContextManager
):
    with expectation:
        ut = parse_unit_type(ibytes)

        assert ut == UnitType.from_bytes(ibytes)
