from contextlib import AbstractContextManager
from contextlib import nullcontext as does_not_raise

import pytest

from pymbus.exceptions import MBusLengthError, MBusValidationError
from pymbus.telegrams.frames import (
    ACK_BYTE,
    CONTROL_FRAME_START_BYTE,
    FRAME_STOP_BYTE,
    LONG_FRAME_START_BYTE,
    SHORT_FRAME_START_BYTE,
    ControlFrame,
    LongFrame,
    ShortFrame,
    SingleFrame,
)

## Single Character Frame section


class TestSingleFrame:
    @pytest.mark.parametrize(
        ("it", "expectation"),
        [
            ([ACK_BYTE], does_not_raise()),
            ([ACK_BYTE - 1], pytest.raises(MBusValidationError)),
            ([], does_not_raise()),
            ([ACK_BYTE, ACK_BYTE], does_not_raise()),
        ],
    )
    def test_init(self, it: list[int], expectation: AbstractContextManager):
        with expectation:
            SingleFrame(it, validate=True)


## Short Frame section


class TestShortFrame:
    @pytest.mark.parametrize(
        ("it", "expectation"),
        [
            ([], pytest.raises(MBusLengthError)),
            (
                [
                    SHORT_FRAME_START_BYTE,
                    FRAME_STOP_BYTE,
                ],
                pytest.raises(MBusLengthError),
            ),
            (
                [SHORT_FRAME_START_BYTE, 2, 3, 4, FRAME_STOP_BYTE],
                does_not_raise(),
            ),
            (
                [
                    SHORT_FRAME_START_BYTE,
                    2,
                    1234,  # failure
                    4,
                    FRAME_STOP_BYTE,
                ],
                pytest.raises(MBusValidationError),
            ),
        ],
    )
    def test_init(self, it: list[int], expectation: AbstractContextManager):
        with expectation:
            ShortFrame(it, validate=True)

    def test_non_greediness(self):
        it = [SHORT_FRAME_START_BYTE, 2, 3, 4, FRAME_STOP_BYTE, 5]
        gen = (b for b in it)

        ShortFrame(gen)

        assert list(gen) == [5]


## Control Frame section


class TestControlFrame:
    @pytest.mark.parametrize(
        ("it", "expectation"),
        [
            ([], pytest.raises(MBusLengthError)),
            (
                [
                    CONTROL_FRAME_START_BYTE,
                    FRAME_STOP_BYTE,
                ],
                pytest.raises(MBusLengthError),
            ),
            (
                [
                    CONTROL_FRAME_START_BYTE,
                    1,
                    2,
                    CONTROL_FRAME_START_BYTE,
                    4,
                    5,
                    6,
                    7,
                    FRAME_STOP_BYTE,
                ],
                does_not_raise(),
            ),
            (
                [
                    CONTROL_FRAME_START_BYTE,
                    1,
                    2,
                    CONTROL_FRAME_START_BYTE,
                    4,
                    1234,  # failure
                    6,
                    7,
                    FRAME_STOP_BYTE,
                ],
                pytest.raises(MBusValidationError),
            ),
        ],
    )
    def test_init(self, it: list[int], expectation: AbstractContextManager):
        with expectation:
            ControlFrame(it, validate=True)

    def test_non_greediness(self):
        it = [
            CONTROL_FRAME_START_BYTE,
            1,
            2,
            CONTROL_FRAME_START_BYTE,
            4,
            5,
            6,
            7,
            FRAME_STOP_BYTE,
            21,
        ]
        gen = (b for b in it)

        ControlFrame(gen)

        assert list(gen) == [21]


## Long Frame section


class TestLongFrame:
    @pytest.mark.parametrize(
        ("it", "expectation"),
        [
            ([], pytest.raises(MBusLengthError)),
            (
                [
                    CONTROL_FRAME_START_BYTE,
                    FRAME_STOP_BYTE,
                ],
                pytest.raises(MBusLengthError),
            ),
            (
                [
                    LONG_FRAME_START_BYTE,
                    1,
                    2,
                    LONG_FRAME_START_BYTE,
                    4,
                    5,
                    6,
                    0,  # user data
                    7,
                    FRAME_STOP_BYTE,
                ],
                does_not_raise(),
            ),
            (
                [
                    LONG_FRAME_START_BYTE,
                    1,
                    2,
                    LONG_FRAME_START_BYTE,
                    4,
                    5,
                    6,
                    252,  # user data
                    7,
                    FRAME_STOP_BYTE,
                ],
                does_not_raise(),
            ),
            (
                [
                    LONG_FRAME_START_BYTE,
                    1,
                    2,
                    LONG_FRAME_START_BYTE,
                    4,
                    5,
                    6,
                    253,  # user data - failure
                    7,
                    FRAME_STOP_BYTE,
                ],
                pytest.raises(MBusValidationError),
            ),
        ],
    )
    def test_init(self, it: list[int], expectation: AbstractContextManager):
        with expectation:
            LongFrame(it, validate=True)

    def test_non_greediness(self):
        it = [
            LONG_FRAME_START_BYTE,
            1,
            2,
            LONG_FRAME_START_BYTE,
            4,
            5,
            6,
            252,  # user data
            7,
            FRAME_STOP_BYTE,
            42,
        ]
        gen = (b for b in it)

        LongFrame(gen)

        assert list(gen) == [42]
