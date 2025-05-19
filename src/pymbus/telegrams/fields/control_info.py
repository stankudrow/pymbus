"""M-Bus Telegram Control Information Field module."""

from pymbus.telegrams.base import TelegramField


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
