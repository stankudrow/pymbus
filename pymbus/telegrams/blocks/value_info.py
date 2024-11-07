from collections.abc import Iterator

from pymbus.exceptions import MBusError
from pymbus.telegrams.base import (
    TelegramBytesType,
)
from pymbus.telegrams.base import (
    TelegramContainer as TelegramBlock,
)
from pymbus.telegrams.fields.value_info import (
    ValueInformationField as VIF,
)
from pymbus.telegrams.fields.value_info import (
    ValueInformationFieldExtension as VIFE,
)

ValueFieldType = VIF | VIFE


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

    def __init__(self, ibytes: TelegramBytesType):
        try:
            blocks = self._parse_blocks(iter(ibytes))
        except StopIteration as e:
            cls_name = self.__class__.__name__
            msg = f"failed to parse {ibytes} as {cls_name}"
            raise MBusError(msg) from e

        self._vif = blocks[0]
        self._vifes = blocks[1:]

        self._fields = blocks

    @property
    def vif(self) -> VIF:
        return self._vif

    @property
    def vifes(self) -> list[VIFE]:
        return self._vifes

    def _parse_blocks(self, ibytes: Iterator[int]) -> list[ValueFieldType]:
        vif = VIF(byte=next(ibytes))

        blocks: list[ValueFieldType] = [vif]
        if not vif.extension:
            return blocks

        pos = 1
        max_frame = self.MAX_VIFE_FRAMES + 1
        while byte := next(ibytes):
            vife = VIFE(byte=byte)
            blocks.append(vife)
            if not vife.extension:
                break
            pos += 1
            if pos == max_frame:
                if vife.extension:
                    msg = f"the last {vife} has the extension bit set"
                    raise MBusError(msg)
                break
        return blocks
