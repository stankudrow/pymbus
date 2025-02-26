from collections.abc import Generator, Iterable

# from typing import Self
from pymbus.exceptions import MBusError


def validate_byte(nbr: int) -> int:
    """Validates an integer number to be a byte.

    In Python, a byte must be in range(0, 256).
    This is the range for an 8-bit unsigned integer.

    Raises
    ------
    MbusError: `nbr` is out of the [0, 255] segment.

    Returns
    -------
    int - the validated byte
    """

    try:
        bytes([nbr])
    except ValueError as e:
        raise MBusError from e

    return nbr


class TelegramField:
    """The base "Field" class.

    It is a base wrapper for a byte value.
    A Field is a part of blocks, frames and other Telegram containers.
    """

    def __init__(self, byte: int):
        self._byte = validate_byte(byte)

    def __eq__(self, other) -> bool:
        sbyte = self.byte
        if isinstance(other, TelegramField):
            return sbyte == other.byte
        return sbyte == other

    def __repr__(self) -> str:
        cls_name = type(self).__name__
        return f"{cls_name}(byte={self.byte})"

    @property
    def byte(self) -> int:
        """Return the byte value of the field."""

        return self._byte


TelegramBytesType = bytes | bytearray | Iterable[int | TelegramField]


def parse_byte(byte_like: int | TelegramField) -> int:
    """Return the byte value from the `byte_like` argument.

    If byte_like is a TelegramField (TF),
    then its byte property get called.

    Parameters
    ----------
    byte_like: int | TelegramField (TF)
        either a byte-like integer or a TF as a byte wrapper

    Returns
    -------
    int
    """

    if isinstance(byte_like, TelegramField):
        return byte_like.byte
    return byte_like


class TelegramContainer:
    """The base class for Telegram containers.

    A telegram container consists of telegram fields
    and it is an iterable object, which may also be an iterator.
    """

    @classmethod
    def from_hexstring(cls, hexstr: str):
        """Return a class instance from a hexadecimal string."""

        barr = bytearray.fromhex(hexstr)
        return cls(barr)

    @classmethod
    def from_integers(cls, ints: Iterable[int]):
        """Return a class instance from a sequence of integers."""

        barr = bytearray(iter(ints))
        return cls(barr)

    def __init__(self, ibytes: TelegramBytesType) -> None:
        self._fields = []
        for ib in ibytes:
            field = ib if isinstance(ib, TelegramField) else TelegramField(ib)
            self._fields.append(field)

    def __eq__(self, other) -> bool:
        sfields = self.fields
        if isinstance(other, TelegramContainer):
            return sfields == other.fields
        return sfields == other

    def __getitem__(self, idx: int) -> TelegramField:
        return self._fields[idx]

    def __iter__(self) -> Generator[None, None, TelegramField]:
        yield from self.fields

    def __len__(self) -> int:
        return len(self.fields)

    def __repr__(self) -> str:
        cls_name = type(self).__name__
        return f"{cls_name}(fields={self.fields})"

    def __str__(self) -> str:
        return str(list(self))

    @property
    def fields(self) -> list[TelegramField]:
        return self._fields

    def as_bytes(self) -> bytes:
        return bytes(field.byte for field in self.fields)
