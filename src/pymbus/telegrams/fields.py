"""M-Bus Telegram Fields module."""

from enum import IntEnum

from pymbus.telegrams.base import TelegramField

AF_UNCONFIGURED_SLAVE_BYTE = 0x00
AF_SLAVE_MIN_RANGE_VALUE_BYTE = 0x01
AF_SLAVE_MAX_RANGE_VALUE_BYTE = 0xFA
AF_BROADCAST_ALL_SLAVES_REPLY_BYTE = 0xFE
AF_BROADCAST_NO_SLAVE_REPLIES_BYTE = 0xFF
AF_NETWORK_LAYER_BYTE = 0xFD


class AddressField(TelegramField):
    """The "Address (A) Field" class.

    The address field serves to address the recipient in the calling direction,
    and to identify the sender of information in the receiving direction.

    The size of this field is one byte,
    and can therefore take values from 0 to 255.
    The addresses 1 to 250 can be allocated to the individual slaves,
    up to a maximum of 250.
    Unconfigured slaves are given the address 0 at manufacture,
    and as a rule are allocated one of these addresses
    when connected to the M-Bus.

    The addresses 254 (FEh) and 255 (FFh) are used to transmit
    information to all participants (Broadcast).
    With address 255, none of the slaves reply,
    and with address 254 all slaves reply with their own addresses.
    The latter case naturally results in collisions
    when two or more slaves are connected,
    and should only be used for test purposes.

    The address 253 (FDh) indicates that the adressing
    has been performed in the Network Layer
    instead of Data Link Layer.

    The remaining addresses 251 and 252 have been kept for future applications.
    """

    def is_configured_slave(self) -> bool:
        return (
            AF_SLAVE_MIN_RANGE_VALUE_BYTE
            <= self._byte
            <= AF_SLAVE_MAX_RANGE_VALUE_BYTE
        )

    def is_unconfigured_slave(self) -> bool:
        return self._byte == AF_UNCONFIGURED_SLAVE_BYTE

    def is_slave(self) -> bool:
        return self.is_configured_slave() or self.is_unconfigured_slave()

    def is_broadcast_all_reply(self) -> bool:
        return self._byte == AF_BROADCAST_ALL_SLAVES_REPLY_BYTE

    def is_broadcast_no_replies(self) -> bool:
        return self._byte == AF_BROADCAST_NO_SLAVE_REPLIES_BYTE

    def is_broadcast(self) -> bool:
        return self.is_broadcast_all_reply() or self.is_broadcast_no_replies()

    def is_network_layer(self) -> bool:
        return self._byte == AF_NETWORK_LAYER_BYTE


CF_FUNCTION_CODE_MASK = 0x0F
CF_FCV_OR_DFC_MASK = 0x10
CF_FCB_OR_ACD_MASK = 0x20
CF_DIRECTION_MASK = 0x40


class ControlField(TelegramField):
    """The "Control (C) Field" class.

    The "Control Field" scheme:
    ------------------------------------------------------------
    |        bit        | 7 | 6 |  5  |  4  |  3 |  2 |  1 |  0 |
    --------------------+---+-  +-----+-----+----+----+----+----+
    | calling direction | 0 | 1 | FCB | FCV | F3 | F2 | F1 | F0 |
    --------------------+---+---+---- +---- +----+----+----+----+
    |  reply direction  | 0 | 0 | ACD | DFC | F3 | F2 | F1 | F0 |
    -------------------------------------------------------------

    The highest value (most significant) bit is reserved for future functions,
    and at present is allocated the value 0.

    The bit number 6 is used to specify the direction of data flow.
    If 1, than it is interpreted as a calling direction,
    else, a reply direction.

    For calling direction.
    The bit 5 -> FCB = Frame Count Bit.
    The bit 4 -> FCV = Frame Count Valid (Bit).

    The FCB indicates successful transmission procedures
    in order to avoid transmission loss or multiplication.
    If the expected reply is missing or reception is faulty,
    the master sends again the same telegram with an identical FCB,
    and the slave replies with the same telegram as previously.
    The master indicates with a 1 in the FCV bit, that the FCB is used.
    Otherwise, the slave should ignore the FCB.

    For reply direction:
    The bit 5 -> ACD = Access Demand.
    The bit 4 -> DFC = Data Flow Control.

    In the replying direction, both these bits can undertake other tasks.
    The DFC serves to control the flow of data,
    in that the slave with a DFC=1
    indicates that it can accept no further data.
    With an ACD bit (access demand) with a value of 1,
    the slave shows that it wants to transmit Class 1 data.
    The master should then send it a command to request Class 1 data.
    Such Class 1 data is of higher priority,
    which (in contrast to Class 2 data)
    should be transmitted as soon as possible.
    The support of Class 1 data and the bits DFC and ADC
    is not required by the standard.

    The bits 0 to 3 of the control field
    code the true function or action of the message.
    """

    def __init__(self, byte: int, *, validate: bool = False) -> None:
        super().__init__(byte, validate=validate)

        self._code = byte & CF_FUNCTION_CODE_MASK
        self._fcv_or_dfc = int((byte & CF_FCV_OR_DFC_MASK) != 0)
        self._fcb_or_acd = int((byte & CF_FCB_OR_ACD_MASK) != 0)
        self._direction = int((byte & CF_DIRECTION_MASK) != 0)

    @property
    def code(self) -> int:
        """Return the action/function code value."""

        return self._code

    @property
    def fcb(self) -> int:
        """Return the "Frame Count Bit" (FCB) value."""

        if not self.is_calling_direction():
            msg = f'the {self} has no "Frame Count Bit" (FCB)'
            raise AttributeError(msg)
        return self._fcb_or_acd

    @property
    def fcv(self) -> int:
        """Return the "Frame Count Valid" (FCV) bit."""

        if not self.is_calling_direction():
            msg = f'the {self} has no "Frame Count Valid" (FCV) bit'
            raise AttributeError(msg)
        return self._fcv_or_dfc

    @property
    def acd(self) -> int:
        """Return the "Access Demand" (ACD) bit."""

        if not self.is_reply_direction():
            msg = f'the {self} has no "Access Demand" (ACD) bit'
            raise AttributeError(msg)
        return self._fcb_or_acd

    @property
    def dfc(self) -> int:
        """Return the "Data Flow Control" (DFC) value."""

        if not self.is_reply_direction():
            msg = f'the {self} has no "Data Flow Control" (DFC) bit'
            raise AttributeError(msg)
        return self._fcv_or_dfc

    @property
    def direction(self) -> int:
        """Return the direction bit value."""

        return self._direction

    def is_calling_direction(self) -> bool:
        return self._direction == 1

    def is_reply_direction(self) -> bool:
        return self._direction == 0


class ControlInformationField(TelegramField):
    """The "Control Information (CI) Field" class.

    The CI-Field codes the type and sequence of application data
    to be transmitted in this frame.
    The EN1434-3 defines two possible data sequences in multibyte records.
    The bit two (counting begins with bit 0, value 4),
    which is called M bit or Mode bit, in the CI field gives
    an information about the used byte sequence in multibyte data structures.
    If the Mode bit is not set (Mode 1),
    the least significant byte of a multibyte record is transmitted first,
    otherwise (Mode 2) the most significant byte.

    The Usergroup recommends to use only the Mode 1 in future applications.
    """


class DataInformationField(TelegramField):
    """Data Information Field (DIF) class.

    The structure of the DIF:
    --------------------------------------------------------------
    |  bit |     7     |          6         |   5  4   | 3 2 1 0 |
    +------+-----------+--------------------+----------+---------+
    | desc | extension | storage number LSB | function |   data  |
    --------------------------------------------------------------
    """

    DATA_FIELD_MASK = 0x0F  # 0b0000_1111
    FUNCTION_FIELD_MASK = 0x30  # 0b0011_0000
    STORAGE_NUMBER_LSB_MASK = 0x40  # 0b0100_0000
    EXTENSION_BIT_MASK = 0x80  # 0b1000_0000

    def __init__(self, byte: int, *, validate: bool = False) -> None:
        super().__init__(byte, validate=validate)

        self._data = byte & self.DATA_FIELD_MASK
        self._func = (byte & self.FUNCTION_FIELD_MASK) >> 4
        self._sn_lsb = int((byte & self.STORAGE_NUMBER_LSB_MASK) != 0)
        self._ext = int((byte & self.EXTENSION_BIT_MASK) != 0)

    @property
    def data(self) -> int:
        return self._data

    @property
    def function(self) -> int:
        return self._func

    @property
    def storage_number_lsb(self) -> int:
        return self._sn_lsb

    @property
    def extension(self) -> int:
        return self._ext


# BCD = Type A. Integer = Type B. Real = Type H.
class DataFieldCode(IntEnum):
    no_data = 0b0000
    int8 = 0b0001
    int16 = 0b0010
    int24 = 0b0011
    int32 = 0b0100
    real32 = 0b0101
    int48 = 0b0110
    int64 = 0b0111
    readout = 0b1000
    bcd2 = 0b1001
    bcd4 = 0b1010
    bcd6 = 0b1011
    bcd8 = 0b1100
    varlen = 0b1101
    bcd12 = 0b1110
    special_func = 0b1111


class FunctionFieldCode(IntEnum):
    instantaneous = 0b00
    maximum = 0b01
    minimum = 0b10
    error = 0b11


class DataInformationFieldExtension(TelegramField):
    """Data Information Field Extension (DIFE) class.

    The structure of the DIFE:
    ----------------------------------------------------------------
    |  bit |     7     |       6       |   5  4   |   3  2  1  0   |
    +------+-----------+---------------+----------+----------------+
    | desc | extension | device (unit) |  tariff  | storage number |
    ----------------------------------------------------------------
    """

    STORAGE_NUMBER_MASK = 0x0F  # 0b0000_1111
    TARIFF_MASK = 0x30  # 0b0011_0000
    DEVICE_UNIT_MASK = 0x40  # 0b0100_0000
    EXTENSION_BIT_MASK = 0x80  # 0b1000_0000

    def __init__(self, byte: int, *, validate: bool = False) -> None:
        super().__init__(byte, validate=validate)

        self._storage_number = byte & self.STORAGE_NUMBER_MASK
        self._tariff = (byte & self.TARIFF_MASK) >> 4
        self._device_unit = int((byte & self.DEVICE_UNIT_MASK) != 0)
        self._ext = int((byte & self.EXTENSION_BIT_MASK) != 0)

    @property
    def storage_number(self) -> int:
        return self._storage_number

    @property
    def tariff(self) -> int:
        return self._tariff

    @property
    def device_unit(self) -> int:
        return self._device_unit

    @property
    def extension(self) -> int:
        return self._ext


class ValueInformationField(TelegramField):
    """Value Information Field (VIF) class.

    The structure of the VIF:
    --------------------------------------------------
    |  bit |     7     |     6  5  4  3  2  1  0     |
    +------+-----------+-----------------------------+
    | desc | extension | unit and multiplier (value) |
    --------------------------------------------------
    """

    UNIT_AND_MULTIPLIER_MASK = 0x7F  # 0b0111_1111
    EXTENSION_BIT_MASK = 0x80  # 0b1000_0000

    def __init__(self, byte: int, *, validate: bool = False) -> None:
        super().__init__(byte, validate=validate)

        self._data = byte & self.UNIT_AND_MULTIPLIER_MASK
        self._ext = int((byte & self.EXTENSION_BIT_MASK) != 0)

    @property
    def unit(self) -> int:
        return self._data

    @property
    def extension(self) -> int:
        return self._ext


class ValueInformationFieldExtension(TelegramField):
    """Value Information Field Extension (VIFE) class.

    The structure of the VIFE (the same as VIF):
    --------------------------------------------------
    |  bit |     7     |     6  5  4  3  2  1  0     |
    +------+-----------+-----------------------------+
    | desc | extension | unit and multiplier (value) |
    --------------------------------------------------
    """

    UNIT_AND_MULTIPLIER_MASK = 0x7F  # 0b0111_1111
    EXTENSION_BIT_MASK = 0x80  # 0b1000_0000

    def __init__(self, byte: int, *, validate: bool = False) -> None:
        super().__init__(byte, validate=validate)

        self._data = byte & self.UNIT_AND_MULTIPLIER_MASK
        self._ext = int((byte & self.EXTENSION_BIT_MASK) != 0)

    @property
    def unit(self) -> int:
        return self._data

    @property
    def extension(self) -> int:
        return self._ext
