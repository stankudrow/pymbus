"""M-Bus Telegram Value Information Field module."""

from pymbus.telegrams.base import TelegramField


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

    def __init__(self, byte: int) -> None:
        super().__init__(byte)

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

    def __init__(self, byte: int) -> None:
        super().__init__(byte)

        self._data = byte & self.UNIT_AND_MULTIPLIER_MASK
        self._ext = int((byte & self.EXTENSION_BIT_MASK) != 0)

    @property
    def unit(self) -> int:
        return self._data

    @property
    def extension(self) -> int:
        return self._ext
