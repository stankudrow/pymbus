"""M-Bus Telegram Frames module.

The fields:

- A = address
- C = control
- CI = control information
- L = length

"""

from pymbus.exceptions import MBusLengthError, MBusValidationError
from pymbus.telegrams.base import (
    TelegramBytesType,
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

    def __init__(self, ibytes: None | TelegramBytesType = None) -> None:
        if ibytes is None:
            ibytes = [TelegramField(ACK_BYTE)]

        fields = list(TelegramContainer(ibytes=ibytes))
        if len(fields) != 1:
            cls_name = type(self).__name__
            msg = f"{cls_name} accepts only {ACK_BYTE}"
            raise MBusLengthError(msg)

        if (byte := fields[0].byte) != ACK_BYTE:
            msg = f"{byte} != {ACK_BYTE}"
            raise MBusValidationError(msg)

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

    def __init__(self, ibytes: None | TelegramBytesType = None) -> None:
        fields, length = list(TelegramContainer(ibytes=ibytes)), 5
        if len(fields) != length:
            msg = f"the length is not equal to {length}"
            raise MBusLengthError(msg)

        cls_name = type(self).__name__
        start_field = fields[0]
        if (byte := start_field.byte) != SHORT_FRAME_START_BYTE:
            msg = f"the first byte {byte!r} is an invalid {cls_name} start byte"
            raise MBusValidationError(msg)
        control_field = ControlField(fields[1].byte)
        address_field = AddressField(fields[2].byte)
        check_sum_field = TelegramField(fields[3].byte)
        stop_field = fields[4]
        if (byte := stop_field.byte) != FRAME_STOP_BYTE:
            msg = f"the fifth byte {byte!r} is an invalid {cls_name} stop byte"
            raise MBusValidationError(msg)

        super().__init__(
            [
                start_field,
                control_field,
                address_field,
                check_sum_field,
                stop_field,
            ]
        )


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

    def __init__(self, ibytes: None | TelegramBytesType = None) -> None:
        fields, length = list(TelegramContainer(ibytes=ibytes)), 9
        if len(fields) != length:
            msg = f"the length is not equal to {length}"
            raise MBusLengthError(msg)

        cls_name = type(self).__name__
        start_field = fields[0]
        if (byte := start_field.byte) != CONTROL_FRAME_START_BYTE:
            msg = f"the first byte {byte!r} is invalid {cls_name} start byte"
            raise MBusValidationError(msg)

        length1_field = TelegramField(fields[1].byte)
        length2_field = TelegramField(fields[2].byte)

        start2_field = fields[3]
        if (byte := start2_field.byte) != CONTROL_FRAME_START_BYTE:
            msg = f"the fourth byte {byte!r} is invalid {cls_name} start byte"
            raise MBusValidationError(msg)

        control_field = ControlField(fields[4].byte)
        address_field = AddressField(fields[5].byte)
        control_info_field = ControlInformationField(fields[6].byte)
        check_sum_field = TelegramField(fields[7].byte)

        stop_field = fields[8]
        if (byte := stop_field.byte) != FRAME_STOP_BYTE:
            msg = f"the ninth byte {byte!r} is invalid {cls_name} stop byte"
            raise MBusValidationError(msg)

        super().__init__(
            [
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
        )


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

    def __init__(self, ibytes: None | TelegramBytesType = None) -> None:
        fields, length = list(TelegramContainer(ibytes=ibytes)), 10
        if len(fields) != length:
            msg = f"the length is not equal to {length}"
            raise MBusLengthError(msg)

        cls_name = type(self).__name__
        start_field = fields[0]
        if (byte := start_field.byte) != CONTROL_FRAME_START_BYTE:
            msg = f"the first byte {byte!r} is invalid {cls_name} start byte"
            raise MBusValidationError(msg)

        length1_field = TelegramField(fields[1].byte)
        length2_field = TelegramField(fields[2].byte)

        start2_field = fields[3]
        if (byte := start2_field.byte) != CONTROL_FRAME_START_BYTE:
            msg = f"the fourth byte {byte!r} is invalid {cls_name} start byte"
            raise MBusValidationError(msg)

        control_field = ControlField(fields[4].byte)
        address_field = AddressField(fields[5].byte)
        control_info_field = ControlInformationField(fields[6].byte)

        if not (0 <= (user_byte := fields[7].byte) <= 252):
            msg = (
                f"the eighth byte {byte!r} is invalid {cls_name} user data byte"
            )
            raise MBusValidationError(msg)
        user_data_field = TelegramField(user_byte)

        check_sum_field = TelegramField(fields[8].byte)

        stop_field = fields[9]
        if (byte := stop_field.byte) != FRAME_STOP_BYTE:
            msg = f"the tenth byte {byte!r} is invalid {cls_name} stop byte"
            raise MBusValidationError(msg)

        super().__init__(
            [
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
        )
