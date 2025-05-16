"""M-Bus Telegram Frames module.

The fields:

- A = address
- C = control
- CI = control information
- L = length
"""

from collections.abc import Iterator

from pymbus.exceptions import MBusLengthError, MBusValidationError
from pymbus.telegrams.base import (
    TelegramByteIterableType,
    TelegramContainer,
    TelegramField,
)
from pymbus.telegrams.fields import (
    AddressField,
    ControlField,
    ControlInformationField,
)

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
    def from_byte(cls, byte: int) -> "SingleFrame":
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

        return SingleFrame([byte])

    def __init__(
        self,
        ibytes: None | TelegramByteIterableType = None,
        *,
        validate: bool = False,
    ) -> None:
        fields = ibytes if ibytes else [TelegramField(ACK_BYTE)]

        it = iter(fields)
        try:
            field = TelegramField(int(next(it)), validate=validate)
        except StopIteration as e:
            msg = f"empty byte sequence: {ibytes!r}"
            raise MBusLengthError(msg) from e

        if field != ACK_BYTE:
            msg = f"{int(field)} != {ACK_BYTE}"
            raise MBusValidationError(msg) from None

        super().__init__(ibytes=fields)


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

    def __init__(
        self,
        ibytes: None | TelegramByteIterableType = None,
        *,
        validate: bool = False,
    ) -> None:
        it = iter(ibytes if ibytes else [])
        try:
            super().__init__(self._parse(it, validate=validate))
        except StopIteration as e:
            msg = f"{ibytes!r} has an invalid length"
            raise MBusLengthError(msg) from e

    def _parse(
        self, it: Iterator, *, validate: bool = False
    ) -> list[TelegramField]:
        start_field = TelegramField(int(next(it)), validate=validate)
        if (byte := start_field) != SHORT_FRAME_START_BYTE:
            msg = f"the first byte {byte!r} is an invalid start byte"
            raise MBusValidationError(msg)

        control_field = ControlField(int(next(it)), validate=validate)
        address_field = AddressField(int(next(it)), validate=validate)
        check_sum_field = TelegramField(int(next(it)), validate=validate)

        stop_field = TelegramField(int(next(it)), validate=validate)
        if (byte := stop_field) != FRAME_STOP_BYTE:
            msg = f"the fifth byte {byte!r} is an invalid stop byte"
            raise MBusValidationError(msg)

        return [
            start_field,
            control_field,
            address_field,
            check_sum_field,
            stop_field,
        ]


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

    def __init__(
        self,
        ibytes: None | TelegramByteIterableType = None,
        *,
        validate: bool = False,
    ) -> None:
        it = iter(ibytes if ibytes else [])
        try:
            super().__init__(self._parse(it, validate=validate))
        except StopIteration as e:
            msg = f"{ibytes!r} has an invalid length"
            raise MBusLengthError(msg) from e

    def _parse(
        self, it: Iterator, *, validate: bool = False
    ) -> list[TelegramField]:
        start_field = TelegramField(int(next(it)), validate=validate)
        if (byte := start_field) != CONTROL_FRAME_START_BYTE:
            msg = f"the first byte {byte!r} is invalid start byte"
            raise MBusValidationError(msg)

        length1_field = TelegramField(int(next(it)), validate=validate)
        length2_field = TelegramField(int(next(it)), validate=validate)

        start2_field = TelegramField(int(next(it)), validate=validate)
        if (byte := start2_field) != CONTROL_FRAME_START_BYTE:
            msg = f"the fourth byte {byte!r} is invalid start byte"
            raise MBusValidationError(msg)

        control_field = ControlField(int(next(it)), validate=validate)
        address_field = AddressField(int(next(it)), validate=validate)
        control_info_field = ControlInformationField(
            int(next(it)), validate=validate
        )
        check_sum_field = TelegramField(int(next(it)), validate=validate)

        stop_field = TelegramField(int(next(it)), validate=validate)
        if (byte := stop_field) != FRAME_STOP_BYTE:
            msg = f"the ninth byte {byte!r} is invalid stop byte"
            raise MBusValidationError(msg)

        return [
            start_field,
            length1_field,
            length2_field,
            start2_field,
            control_field,
            address_field,
            control_info_field,
            check_sum_field,
            stop_field,
        ]


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
    8. user data (a value from the 0-252 segment) (!)
    9. check sum;
    10. stop 0x16.
    """

    def __init__(
        self,
        ibytes: None | TelegramByteIterableType = None,
        *,
        validate: bool = False,
    ) -> None:
        it = iter(ibytes if ibytes else [])
        try:
            super().__init__(self._parse(it, validate=validate))
        except StopIteration as e:
            msg = f"{ibytes!r} has an invalid length"
            raise MBusLengthError(msg) from e

    def _parse(
        self, it: Iterator, *, validate: bool = False
    ) -> list[TelegramField]:
        start_field = TelegramField(int(next(it)), validate=validate)
        if (byte := start_field) != CONTROL_FRAME_START_BYTE:
            msg = f"the first byte {byte!r} is invalid start byte"
            raise MBusValidationError(msg)

        length1_field = TelegramField(int(next(it)), validate=validate)
        length2_field = TelegramField(int(next(it)), validate=validate)

        start2_field = TelegramField(int(next(it)), validate=validate)
        if (byte := start2_field) != CONTROL_FRAME_START_BYTE:
            msg = f"the fourth byte {byte!r} is invalid start byte"
            raise MBusValidationError(msg)

        control_field = ControlField(int(next(it)), validate=validate)
        address_field = AddressField(int(next(it)), validate=validate)
        control_info_field = ControlInformationField(
            int(next(it)), validate=validate
        )

        if not (0 <= (user_byte := int(next(it))) <= 252):
            msg = f"the eighth byte {user_byte!r} is invalid user data byte"
            raise MBusValidationError(msg)
        user_data_field = TelegramField(user_byte)

        check_sum_field = TelegramField(int(next(it)), validate=validate)

        stop_field = TelegramField(int(next(it)), validate=validate)
        if (byte := stop_field) != FRAME_STOP_BYTE:
            msg = f"the tenth byte {byte!r} is invalid stop byte"
            raise MBusValidationError(msg)

        return [
            start_field,
            length1_field,
            length2_field,
            start2_field,
            control_field,
            address_field,
            control_info_field,
            user_data_field,
            check_sum_field,
            stop_field,
        ]
