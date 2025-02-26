from pymbus.exceptions import MBusError
from pymbus.telegrams.base import (
    TelegramBytesType,
)
from pymbus.telegrams.base import (
    TelegramContainer as TelegramRecord,
)
from pymbus.telegrams.blocks import (
    DataInformationBlock as DIB,
)
from pymbus.telegrams.blocks import (
    ValueInformationBlock as VIB,
)


class DataRecord(TelegramRecord):
    """The "Data Record" (DR) class.

    Typically encountered as Data Record Header (DRH).

    The structure of the DR(H):
    -----------------
    |   DIB  |  VIB |
    -----------------

    DIB = Data Information Block.
    VIB = Value Information Block.
    """

    def __init__(self, ibytes: TelegramBytesType):
        try:
            it = iter(ibytes)
        except TypeError as e:
            msg = f"{ibytes} is not iterable"
            raise MBusError(msg) from e

        self._dib = DIB(it)
        self._vib = VIB(it)

    @property
    def dib(self) -> DIB:
        return self._dib

    @property
    def vib(self) -> VIB:
        return self._vib
