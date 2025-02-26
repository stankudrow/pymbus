"""Telegram frames of the M-Bus protocol.

The fields:

- A = address
- C = control
- CI = control information
- L = length

"""

from collections.abc import Iterator

# from typing import Self
from pymbus.exceptions import MBusError
from pymbus.telegrams.base import (
    TelegramBytesType,
    TelegramContainer,
    TelegramField,
    parse_byte,
)
from pymbus.telegrams.fields.address import AddressField
from pymbus.telegrams.fields.control import ControlField
from pymbus.telegrams.fields.control_info import ControlInformationField

ACK_BYTE = 0xE5

FRAME_STOP_BYTE = 0x16

SHORT_FRAME_START_BYTE = 0x10
CONTROL_FRAME_START_BYTE = 0x68
LONG_FRAME_START_BYTE = CONTROL_FRAME_START_BYTE


class TelegramFrame(TelegramContainer):
    """Base Telegram Frame class."""


class SingleFrame(TelegramFrame):
    """The "Single Character" Frame class.

    This format consists of a single character, namely the 0xE5 (229),
    and serves to acknowledge receipt of transmissions.
    """

    @classmethod
    def from_byte(cls, byte: int):
        """Decode a Single (ACK) Frame from a byte integer.

        Parameters
        ----------
        byte: int
            a byte integer candidate for being a Single Character (ACK) Frame.

        Raises
        ------
        MBusError:
            if the byte integer is not a Single Character Frame.

        Returns
        -------
        Self
        """

        cls.validate_ack_byte(byte=byte)

        return SingleFrame()

    def __init__(self, ibytes: None | TelegramBytesType = None) -> None:
        if ibytes:
            cls_name = type(self).__name__
            if not len(ibytes) == 1:
                msg = (
                    f"only one byte is acceptable for a "
                    f"{cls_name} instance, got {ibytes}"
                )
                raise MBusError(msg)
            byte = ibytes[0]
            SingleFrame.validate_ack_byte(byte=byte)
        self._fields = [TelegramField(ACK_BYTE)]

    @classmethod
    def validate_ack_byte(cls, byte: int) -> None:
        cls_name = cls.__name__
        if byte != ACK_BYTE:
            msg = f"the {byte!r} cannot be {cls_name}"
            raise MBusError(msg)


class ShortFrame(TelegramFrame):
    """The "Short Frame" class.

    This format with a fixed length begins with the start character 10h,
    and besides the C and A fields includes the check sum
    (this is made up from the two last mentioned characters),
    and the stop character 16h.This format consists of a single character,
    namely the E5h (decimal 229),
    and serves to acknowledge receipt of transmissions.

    The "Short Frame" elements scheme:

    1. start 0x10;
    2. C field;
    3. A field;
    4. check sum;
    5. stop 0x16.
    """

    def __init__(self, ibytes: TelegramBytesType):
        try:
            self._parse_frame(iter(ibytes))
        except StopIteration as e:
            cls_name = type(self).__name__
            msg = f"failed to parse {ibytes} as {cls_name}"
            raise MBusError(msg) from e

        self._fields: list[TelegramField] = [
            self._start,
            self._c,
            self._a,
            self._check_sum,
            self._stop,
        ]

    def _parse_frame(self, it: Iterator[int | TelegramField]):
        cls_name = type(self).__name__

        field = TelegramField(parse_byte(next(it)))
        if (byte := field.byte) != SHORT_FRAME_START_BYTE:
            msg = f"the first byte {byte!r} is invalid {cls_name} start byte"
            raise MBusError(msg)
        self._start = field

        self._c = ControlField(parse_byte(next(it)))
        self._a = AddressField(parse_byte(next(it)))
        self._check_sum = TelegramField(parse_byte(next(it)))

        field = TelegramField(parse_byte(next(it)))
        if (byte := field.byte) != FRAME_STOP_BYTE:
            msg = f"the fifth byte {byte!r} is invalid {cls_name} stop byte"
            raise MBusError(msg)
        self._stop = field


class ControlFrame(TelegramFrame):
    """The "Control Frame" class.

    The control sentence conforms to the long sentence without user data,
    with an L field from the contents of 3. The check sum is calculated
    at this point from the fields C, A and CI.

    The "Control Frame" elements scheme:

    1. start 0x68;
    2. L field = 3;
    3. L field = 3;
    4. start 0x68;
    5. C field;
    6. A field;
    7. CI field;
    8. check sum;
    9. stop 0x16.
    """

    def __init__(self, ibytes: TelegramBytesType):
        try:
            self._parse_frame(iter(ibytes))
        except StopIteration as e:
            cls_name = self.__class__.__name__
            msg = f"failed to parse {ibytes} as {cls_name}"
            raise MBusError(msg) from e

        self._fields: list[TelegramField] = [
            self._start,
            self._len1,
            self._len2,
            self._start2,
            self._c,
            self._a,
            self._ci,
            self._check_sum,
            self._stop,
        ]

    def _parse_frame(self, it: Iterator[int | TelegramField]):
        cls_name = self.__class__.__name__

        field = TelegramField(parse_byte(next(it)))
        if (byte := field.byte) != CONTROL_FRAME_START_BYTE:
            msg = f"the first byte {byte!r} is invalid {cls_name} start byte"
            raise MBusError(msg)
        self._start = field

        self._len1 = TelegramField(parse_byte(next(it)))
        self._len2 = TelegramField(parse_byte(next(it)))

        field = TelegramField(parse_byte(next(it)))
        if (byte := field.byte) != CONTROL_FRAME_START_BYTE:
            msg = f"the fourth byte {byte!r} is invalid {cls_name} start byte"
            raise MBusError(msg)
        self._start2 = field

        self._c = ControlField(parse_byte(next(it)))
        self._a = AddressField(parse_byte(next(it)))
        self._ci = ControlInformationField(parse_byte(next(it)))
        self._check_sum = TelegramField(parse_byte(next(it)))

        field = TelegramField(parse_byte(next(it)))
        if (byte := field.byte) != FRAME_STOP_BYTE:
            msg = f"the ninth byte {byte!r} is invalid {cls_name} stop byte"
            raise MBusError(msg)
        self._stop = field


class LongFrame(TelegramFrame):
    """The "Long Frame" class.

    With the long frame, after the start character 68h,
    the length field (L field) is first transmitted twice,
    followed by the start character once again.
    After this, there follow the function field (C field),
    the address field (A field) and the control information field (CI field).
    The L field gives the quantity of the user data inputs plus 3 (for C,A,CI).
    After the user data inputs, the check sum is transmitted,
    which is built up over the same area as the length field,
    and in conclusion the stop character 16h is transmitted.

    The "Long Frame" elements scheme:

    1. start 0x68;
    2. L field = 3;
    3. L field = 3;
    4. start 0x68;
    5. C field;
    6. A field;
    7. CI field;
    8. user data (0-252 byte)
    9. check sum;
    10. stop 0x16.
    """

    def __init__(self, ibytes: TelegramBytesType):
        try:
            self._parse_frame(iter(ibytes))
        except StopIteration as e:
            cls_name = self.__class__.__name__
            msg = f"failed to parse {ibytes} as {cls_name}"
            raise MBusError(msg) from e

        self._fields: list[TelegramField] = [
            self._start,
            self._len1,
            self._len2,
            self._start2,
            self._c,
            self._a,
            self._ci,
            self._data,
            self._check_sum,
            self._stop,
        ]

    def _parse_frame(self, it: Iterator[int]):
        cls_name = self.__class__.__name__

        field = TelegramField(parse_byte(next(it)))
        if (byte := field.byte) != CONTROL_FRAME_START_BYTE:
            msg = f"the first byte {byte!r} is invalid {cls_name} start byte"
            raise MBusError(msg)
        self._start = field

        self._len1 = TelegramField(parse_byte(next(it)))
        self._len2 = TelegramField(parse_byte(next(it)))

        field = TelegramField(parse_byte(next(it)))
        if (byte := field.byte) != CONTROL_FRAME_START_BYTE:
            msg = f"the fourth byte {byte!r} is invalid {cls_name} start byte"
            raise MBusError(msg)
        self._start2 = field

        self._c = ControlField(parse_byte(next(it)))
        self._a = AddressField(parse_byte(next(it)))
        self._ci = ControlInformationField(parse_byte(next(it)))
        self._data = TelegramField(parse_byte(next(it)))
        self._check_sum = TelegramField(parse_byte(next(it)))

        field = TelegramField(parse_byte(next(it)))
        if (byte := field.byte) != FRAME_STOP_BYTE:
            msg = f"the ninth byte {byte!r} is invalid {cls_name} stop byte"
            raise MBusError(msg)
        self._stop = field
