from collections.abc import Iterable
from contextlib import AbstractContextManager
from contextlib import nullcontext as does_not_raise

import pytest

from pymbus.exceptions import MBusError
from pymbus.telegrams.base import TelegramField
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


@pytest.mark.parametrize(
    ("byte", "expectation"),
    [
        (ACK_BYTE, does_not_raise()),
        (ACK_BYTE - 1, pytest.raises(MBusError)),
    ],
)
def test_single_frame_init(byte: int, expectation: AbstractContextManager):
    with expectation:
        SingleFrame.from_byte(byte)
    with expectation:
        SingleFrame([byte])


def test_single_frame_init_from_iterable():
    ibytes = [ACK_BYTE]

    SingleFrame(ibytes)

    with pytest.raises(MBusError):
        SingleFrame(ibytes + ibytes)


def test_single_frame_container_interface():
    frame = SingleFrame()

    lst = list(frame)

    assert len(lst) == len(frame)
    assert lst[0] == frame[0]


def test_single_frame_repr_str():
    frame = SingleFrame()

    repstr = repr(frame)
    strstr = str(frame)
    fields = frame.fields

    assert repstr == f"SingleFrame(fields={fields})"
    assert strstr == str(fields)


## Short Frame section


@pytest.mark.parametrize(
    ("data", "expectation"),
    [
        ([1], pytest.raises(MBusError)),
        (
            [
                SHORT_FRAME_START_BYTE,
                FRAME_STOP_BYTE,
            ],
            pytest.raises(MBusError),
        ),
        (
            [SHORT_FRAME_START_BYTE, 2, 3, 4, FRAME_STOP_BYTE],
            does_not_raise(),
        ),
    ],
)
def test_short_frame_init(data: Iterable, expectation: AbstractContextManager):
    with expectation:
        sh = ShortFrame(data)

        frame = list(sh)

        for pos in range(len(sh)):
            assert frame[pos] is sh[pos]


def test_short_frame_repr_str():
    ibytes = [
        SHORT_FRAME_START_BYTE,
        TelegramField(1),
        2,
        0b0000_0011,
        FRAME_STOP_BYTE,
    ]
    frame = ShortFrame(ibytes)

    repstr = repr(frame)
    strstr = str(frame)
    fields = frame.fields

    assert repstr == f"ShortFrame(fields={fields})"
    assert strstr == str(fields)


## Control Frame section


@pytest.mark.parametrize(
    ("data", "expectation"),
    [
        ([1], pytest.raises(MBusError)),
        (
            [
                CONTROL_FRAME_START_BYTE,
                FRAME_STOP_BYTE,
            ],
            pytest.raises(MBusError),
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
    ],
)
def test_control_frame_init(
    data: Iterable, expectation: AbstractContextManager
):
    with expectation:
        ctrl = ControlFrame(data)

        frame = list(ctrl)

        for pos in range(len(ctrl)):
            assert frame[pos] is ctrl[pos]


def test_control_frame_repr_str():
    ibytes = [
        CONTROL_FRAME_START_BYTE,
        TelegramField(1),
        2,
        CONTROL_FRAME_START_BYTE,
        TelegramField(0b0000_0011),
        4,
        5,
        6,
        FRAME_STOP_BYTE,
    ]
    frame = ControlFrame(ibytes)

    repstr = repr(frame)
    strstr = str(frame)
    fields = frame.fields

    assert repstr == f"ControlFrame(fields={fields})"
    assert strstr == str(fields)


## Long Frame section


@pytest.mark.parametrize(
    ("data", "expectation"),
    [
        ([1], pytest.raises(MBusError)),
        (
            [
                CONTROL_FRAME_START_BYTE,
                FRAME_STOP_BYTE,
            ],
            pytest.raises(MBusError),
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
    ],
)
def test_long_frame_init(data: Iterable, expectation: AbstractContextManager):
    with expectation:
        long = LongFrame(data)

        frame = list(long)

        for pos in range(len(long)):
            assert frame[pos] is long[pos]


def test_long_frame_repr_str():
    ibytes = [
        CONTROL_FRAME_START_BYTE,
        TelegramField(1),
        2,
        CONTROL_FRAME_START_BYTE,
        TelegramField(0b0000_0011),
        4,
        5,
        42,
        6,
        FRAME_STOP_BYTE,
    ]
    frame = LongFrame(ibytes)

    repstr = repr(frame)
    strstr = str(frame)
    fields = frame.fields

    assert repstr == f"LongFrame(fields={fields})"
    assert strstr == str(fields)
