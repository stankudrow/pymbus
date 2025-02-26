from collections.abc import Iterator

from pymbus.exceptions import MBusError
from pymbus.telegrams.base import (
    TelegramBytesType,
)
from pymbus.telegrams.base import (
    TelegramContainer as TelegramBlock,
)
from pymbus.telegrams.fields.data_info import (
    DataInformationField as DIF,
)
from pymbus.telegrams.fields.data_info import (
    DataInformationFieldExtension as DIFE,
)

DataFieldType = DIF | DIFE


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

    def __init__(self, ibytes: TelegramBytesType):
        try:
            blocks = self._parse_blocks(iter(ibytes))
        except StopIteration as e:
            cls_name = self.__class__.__name__
            msg = f"failed to parse {ibytes} as {cls_name}"
            raise MBusError(msg) from e

        self._dif = blocks[0]
        self._difes = blocks[1:]

        self._fields = blocks

    @property
    def dif(self) -> DIF:
        return self._dif

    @property
    def difes(self) -> list[DIFE]:
        return self._difes

    def _parse_blocks(self, ibytes: Iterator[int]) -> list[DataFieldType]:
        dif = DIF(byte=next(ibytes))

        blocks: list[DataFieldType] = [dif]
        if not dif.extension:
            return blocks

        pos = 1
        max_frame = self.MAX_DIFE_FRAMES + 1
        while byte := next(ibytes):
            dife = DIFE(byte=byte)
            blocks.append(dife)
            if not dife.extension:
                break
            pos += 1
            if pos == max_frame:
                if dife.extension:
                    msg = f"the last {dife} has the extension bit set"
                    raise MBusError(msg)
                break
        return blocks
