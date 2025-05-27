"""M-Bus Telegram Control Field module."""

from pymbus.telegrams.base import TelegramField


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

    CF_DIRECTION_MASK = 0x40
    CF_FUNCTION_CODE_MASK = 0x0F
    CF_FCB_OR_ACD_MASK = 0x20
    CF_FCV_OR_DFC_MASK = 0x10

    def __init__(self, byte: int) -> None:
        super().__init__(byte)

        self._code = byte & self.CF_FUNCTION_CODE_MASK
        self._fcv_or_dfc = int((byte & self.CF_FCV_OR_DFC_MASK) != 0)
        self._fcb_or_acd = int((byte & self.CF_FCB_OR_ACD_MASK) != 0)
        self._direction = int((byte & self.CF_DIRECTION_MASK) != 0)

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
        """Return True if the 6th bit is 1."""
        return bool(self._direction)

    def is_reply_direction(self) -> bool:
        """Return True if the 6th bit is 0."""
        return not self._direction
