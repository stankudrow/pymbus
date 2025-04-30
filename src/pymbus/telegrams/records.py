"""M-Bus Telegram Data Record module."""

from pymbus.telegrams.base import (
    TelegramBytesType,
    TelegramContainer,
)
from pymbus.telegrams.blocks import (
    DataInformationBlock as DIB,
)
from pymbus.telegrams.blocks import (
    ValueInformationBlock as VIB,
)


class TelegramRecord(TelegramContainer):
    """Base Telegram Record class."""


class DataRecord(TelegramRecord):
    """The "Data Record" (DR) class.

    Typically encountered as Data Record Header (DRH).

    The structure of the DRH:
    -----------------
    |   DIB  |  VIB |
    -----------------

    DIB = Data Information Block.
    VIB = Value Information Block.
    """

    def __init__(self, ibytes: None | TelegramBytesType = None) -> None:
        container = list(TelegramContainer(ibytes=ibytes))

        dib = DIB(ibytes=container)
        vib = VIB(ibytes=container[len(dib) :])

        super().__init__(ibytes=container)
        self._dib = dib
        self._vib = vib

    @property
    def dib(self) -> DIB:
        return self._dib

    @property
    def vib(self) -> VIB:
        return self._vib
