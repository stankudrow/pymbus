from collections.abc import Iterable

from pymbus.exceptions import MBusLengthError
from pymbus.telegrams.base import (
    TelegramByteType,
    TelegramContainer,
    TelegramField,
)
from pymbus.telegrams.fields import DataInformationField as DIF
from pymbus.telegrams.fields import DataInformationFieldExtension as DIFE
from pymbus.telegrams.fields import ValueInformationField as VIF
from pymbus.telegrams.fields import ValueInformationFieldExtension as VIFE

DataFieldType = DIF | DIFE
ValueFieldType = VIF | VIFE


class TelegramBlock(TelegramContainer):
    """Base Telegram Block class"""


class DataInformationBlock(TelegramBlock):
    """The "Data Information Block" (DIB) class.

    The DIB describes the length, type and coding of the data.
    The DIB contains at least one byte (DIF - Data Information Field).
    The DIF of a DIB can be followed with DIF Extensions (DIFE):
    from 0 to 10 DIFE frames 1 byte each (as the DIF).

    The structure of the DIB:
    -------------------------------
    |   DIF  |        DIFE        |
    +--------+--------------------+
    | 1 byte | 0-10 (1 byte each) |
    -------------------------------
    """

    MAX_DIFE_FRAMES = 10

    def __init__(
        self, ibytes: None | Iterable[TelegramByteType] = None
    ) -> None:
        container = list(TelegramContainer(ibytes=ibytes))

        blocks = self._parse_blocks(container)
        dif = blocks[0]
        difes = blocks[1]

        super().__init__(ibytes=container[: (len(difes) + 1)])
        self._dif = dif
        self._difes = difes

    def _parse_blocks(
        self, fields: list[TelegramField]
    ) -> tuple[DIF, list[DIFE]]:
        cls_name = type(self)

        if len(fields) < 1:
            msg = f"no telegrams for {cls_name}"
            raise MBusLengthError(msg)

        dif = DIF(byte=fields[0].byte)
        if not dif.extension:
            return (dif, [])

        difes: list[DIFE] = []
        max_frame = self.MAX_DIFE_FRAMES + 1
        pos = 1
        while byte := fields[pos].byte:
            dife = DIFE(byte=byte)
            difes.append(dife)
            if not dife.extension:
                break
            pos += 1
            if pos == max_frame:
                if dife.extension:
                    msg = f"the last {dife} has the extension bit set"
                    raise MBusLengthError(msg)
                break
        return (dif, difes)

    @property
    def dif(self) -> DIF:
        return self._dif

    @property
    def difes(self) -> list[DIFE]:
        return self._difes


## Value blocks


class ValueInformationBlock(TelegramBlock):
    """The "Value Information Block" (VIB) class.

    The VIB describes the value of the unit and the multiplier.
    The VIB contains at least one byte (VIF - Value Information Field).
    The VIF of a VIB can be followed with VIF Extensions (VIFE):
    from 0 to 10 VIFE frames 1 byte each (as the VIF).

    The structure of the VIB:
    -------------------------------
    |   VIF  |        VIFE        |
    +--------+--------------------+
    | 1 byte | 0-10 (1 byte each) |
    -------------------------------
    """

    MAX_VIFE_FRAMES = 10

    def __init__(
        self, ibytes: None | Iterable[TelegramByteType] = None
    ) -> None:
        container = list(TelegramContainer(ibytes=ibytes))

        blocks = self._parse_blocks(container)
        vif = blocks[0]
        vifes = blocks[1]

        super().__init__(ibytes=container[: (len(vifes) + 1)])
        self._vif = vif
        self._vifes = vifes

    def _parse_blocks(
        self, fields: list[TelegramField]
    ) -> tuple[VIF, list[VIFE]]:
        cls_name = type(self)

        if len(fields) < 1:
            msg = f"no telegrams for {cls_name}"
            raise MBusLengthError(msg)

        vif = VIF(byte=fields[0].byte)
        if not vif.extension:
            return (vif, [])

        vifes: list[VIFE] = []
        max_frame = self.MAX_VIFE_FRAMES + 1
        pos = 1
        while byte := fields[pos].byte:
            vife = VIFE(byte=byte)
            vifes.append(vife)
            if not vife.extension:
                break
            pos += 1
            if pos == max_frame:
                if vife.extension:
                    msg = f"the last {vife} has the extension bit set"
                    raise MBusLengthError(msg)
                break
        return (vif, vifes)

    @property
    def vif(self) -> VIF:
        return self._vif

    @property
    def vifes(self) -> list[VIFE]:
        return self._vifes
