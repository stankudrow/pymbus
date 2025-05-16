"""M-Bus Telegram Blocks."""

from collections.abc import Iterator

from pymbus.exceptions import MBusLengthError
from pymbus.telegrams.base import (
    TelegramByteIterableType,
    TelegramContainer,
)
from pymbus.telegrams.fields import DataInformationField as DIF
from pymbus.telegrams.fields import DataInformationFieldExtension as DIFE
from pymbus.telegrams.fields import ValueInformationField as VIF
from pymbus.telegrams.fields import ValueInformationFieldExtension as VIFE

DataFieldType = DIF | DIFE
ValueFieldType = VIF | VIFE


class TelegramBlock(TelegramContainer):
    """Base Telegram Block class."""


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
        self,
        ibytes: None | TelegramByteIterableType = None,
        *,
        validate: bool = False,
    ) -> None:
        it = iter(ibytes if ibytes else [])

        try:
            blocks = self._parse(it, validate=validate)
        except StopIteration as e:
            msg = f"{ibytes!r} has invalid length"
            raise MBusLengthError(msg) from e

        dif: DIF = blocks[0]
        difes: list[DIFE] = blocks[1]

        super().__init__(ibytes=list(map(int, [dif] + difes)))  # type: ignore
        self._dif = dif
        self._difes = difes

    def _parse(
        self, it: Iterator, *, validate: bool = False
    ) -> tuple[DIF, list[DIFE]]:
        value: int = int(next(it))
        dif = DIF(byte=value, validate=validate)
        if not dif.extension:
            return (dif, [])

        difes: list[DIFE] = []
        max_frame = self.MAX_DIFE_FRAMES + 1
        dife_counter = 1
        while True:
            value = int(next(it))
            dife = DIFE(byte=value, validate=validate)
            difes.append(dife)
            if not dife.extension:
                break

            dife_counter += 1
            if dife_counter == max_frame:
                if dife.extension:
                    msg = f"the last {dife} has the extension bit set"
                    raise MBusLengthError(msg)
                break
        return (dif, difes)

    @property
    def dif(self) -> DIF:
        """Return the DIF field."""

        return self._dif

    @property
    def difes(self) -> list[DIFE]:
        """Return the list of DIFE fields."""

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
        self,
        ibytes: None | TelegramByteIterableType = None,
        *,
        validate: bool = False,
    ) -> None:
        it = iter(ibytes if ibytes else [])

        try:
            blocks = self._parse(it, validate=validate)
        except StopIteration as e:
            msg = f"{ibytes!r} has invalid length"
            raise MBusLengthError(msg) from e
        vif = blocks[0]
        vifes = blocks[1]

        super().__init__(ibytes=map(int, [vif] + vifes))  # type: ignore
        self._vif = vif
        self._vifes = vifes

    def _parse(
        self, it: Iterator, *, validate: bool = False
    ) -> tuple[VIF, list[VIFE]]:
        value: int = int(next(it))
        vif = VIF(byte=value, validate=validate)
        if not vif.extension:
            return (vif, [])

        vifes: list[VIFE] = []
        max_frame = self.MAX_VIFE_FRAMES + 1
        vife_counter = 1
        while True:
            value = int(next(it))
            vife = VIFE(byte=value, validate=validate)
            vifes.append(vife)
            if not vife.extension:
                break

            vife_counter += 1
            if vife_counter == max_frame:
                if vife.extension:
                    msg = f"the last {vife} has the extension bit set"
                    raise MBusLengthError(msg)
                break
        return (vif, vifes)

    @property
    def vif(self) -> VIF:
        """Return the VIF field."""

        return self._vif

    @property
    def vifes(self) -> list[VIFE]:
        """Return the list of VIFE fields."""

        return self._vifes
