from collections.abc import Iterable, Iterator

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

    def __init__(self, byte: int) -> None:
        self._byte = validate_byte(byte)

    def __eq__(self, other: object) -> bool:
        sbyte = self.byte
        if isinstance(other, TelegramField):
            other = other.byte
        return sbyte == other

    def __repr__(self) -> str:
        cls_name = type(self).__name__
        return f"{cls_name}(byte={self.byte})"

    @property
    def byte(self) -> int:
        """Return the byte value of the field."""

        return self._byte


TelegramByteType = int | TelegramField


def parse_byte(value: TelegramByteType) -> int:
    """Return the byte value from the `byte_like` argument.

    Parameters
    ----------
    value: TelegramByteType
        either a byte-like integer or a TelegramField instance

    Returns
    -------
    int
    """

    if isinstance(value, TelegramField):
        return value.byte
    return validate_byte(value)


class TelegramContainer:
    """The base class for Telegram containers.

    A telegram container consists of telegram fields
    and it is an iterable object, which may also be an iterator.
    """

    @classmethod
    def from_hexstring(cls, hexstr: str) -> "TelegramContainer":
        """Return a class instance from a hexadecimal string."""

        barr = bytearray.fromhex(hexstr)
        return cls(barr)

    @classmethod
    def from_integers(cls, ints: Iterable[int]) -> "TelegramContainer":
        """Return a class instance from a sequence of integers."""

        barr = bytearray(iter(ints))
        return cls(barr)

    def __init__(self, ibytes: Iterable[TelegramByteType]) -> None:
        self._fields: list[TelegramField] = [
            ibyte if isinstance(ibyte, TelegramField) else TelegramField(ibyte)
            for ibyte in ibytes
        ]

    def __eq__(self, other: object) -> bool:
        sfields = self._fields
        if isinstance(other, TelegramContainer):
            other = other._fields
        return sfields == other

    def __getitem__(self, idx: int) -> TelegramField:
        return self._fields[idx]

    def __iter__(self) -> Iterator[TelegramField]:
        yield from self._fields

    def __len__(self) -> int:
        return len(self._fields)

    def __repr__(self) -> str:
        cls_name = type(self).__name__
        return f"{cls_name}(fields={self._fields})"

    def __str__(self) -> str:
        return str(list(self))

    def as_bytes(self) -> bytes:
        return bytes(field.byte for field in self._fields)
