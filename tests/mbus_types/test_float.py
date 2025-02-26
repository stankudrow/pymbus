from collections.abc import Iterable
from contextlib import AbstractContextManager
from contextlib import nullcontext as does_not_raise

import pytest

from pymbus.exceptions import MBusError
from pymbus.mbtypes import parse_float


@pytest.mark.parametrize(
    ("frame", "answer", "expectation"),
    [
        ([0, 0, 0], 0.0, pytest.raises(MBusError)),
        ([0, 0, 0, 0], 0.0, does_not_raise()),
        ([-1, 0, 0, 0], 0.0, pytest.raises(MBusError)),
    ],
)
def test_parse_float(
    frame: Iterable[int], answer: float, expectation: AbstractContextManager
):
    with expectation:
        assert parse_float(frame) == answer
