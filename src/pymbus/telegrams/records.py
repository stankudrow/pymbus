"""M-Bus Telegram Data Record module."""

from pymbus.telegrams.base import TelegramByteIterableType, TelegramContainer
from pymbus.telegrams.blocks import (
    DataInformationBlock as DIB,
)
from pymbus.telegrams.blocks import (
    ValueInformationBlock as VIB,
)


class DataRecordHeader(TelegramContainer):
    """The "Data Record Header" (DRH) class.

    The structure of the DRH:
    -----------------
    |   DIB  |  VIB |
    -----------------

    DIB = Data Information Block.
    VIB = Value Information Block.
    """

    def __init__(self, ibytes: None | TelegramByteIterableType = None) -> None:
        it = iter(ibytes if ibytes else [])

        dib = DIB(ibytes=it)
        vib = VIB(ibytes=it)

        fields = list(dib) + list(vib)
        super().__init__(ibytes=fields)
        self._dib = dib
        self._vib = vib

    @property
    def dib(self) -> DIB:
        """Return DI block."""

        return self._dib

    @property
    def vib(self) -> VIB:
        """Return VI block."""

        return self._vib


class DataRecord(TelegramContainer):
    """The "Data Record" (DR) class.

    The structure of the DR:
    ----------------
    |   DRH | data |
    ----------------

    DRH = Data Record Header.
    data = data associated with the DRH.
    """

    def __init__(self, ibytes: None | TelegramByteIterableType = None) -> None:
        it = iter(ibytes if ibytes else [])

        drh = DataRecordHeader(ibytes=it)
        data = TelegramContainer(ibytes=it)

        fields = list(drh) + list(data)
        super().__init__(ibytes=fields)
        self._drh = drh
        self._data = data

    @property
    def drh(self) -> DataRecordHeader:
        """Return DataRecordHeader."""

        return self._drh

    @property
    def data(self) -> TelegramContainer:
        """Return data fields."""

        return self._data
