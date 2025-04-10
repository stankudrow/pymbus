"""Basic Telegram objects module.

Glossary:

- a byte is an integer witing the range(0, 256)
- an instance of the TelegramField class is a wrapper over a byte
- a telegram byte refers to the "int | TelegramField"
"""

from collections.abc import Iterable, Iterator
from typing import cast

from pymbus.exceptions import MBusValidationError


def _validate_byte(nbr: int) -> int:
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
        raise MBusValidationError from e

    return nbr


class TelegramField:
    """The base "Field" class.

    It is a base wrapper over a byte value (validation is ensured).
    A Field is a part of blocks, frames and other Telegram containers.
    """

    def __init__(self, byte: int) -> None:
        self._byte = _validate_byte(byte)

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


def _convert_to_telegram_fields(
    ibytes: Iterable[TelegramByteType],
) -> list[TelegramField]:
    return [
        ibyte if isinstance(ibyte, TelegramField) else TelegramField(ibyte)
        for ibyte in ibytes
    ]


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
        self._fields = _convert_to_telegram_fields(ibytes)

    def __eq__(self, other: object) -> bool:
        sfields = self._fields
        if isinstance(other, TelegramContainer):
            other = other._fields
        return sfields == other

    def __getitem__(
        self, key: int | slice
    ) -> "TelegramField | TelegramContainer":
        result = self._fields[key]
        if isinstance(key, int):
            return cast(TelegramField, result)
        return type(self)(ibytes=cast("list[TelegramField]", result))

    def __iter__(self) -> Iterator[TelegramField]:
        yield from self._fields

    def __len__(self) -> int:
        return len(self._fields)

    def __repr__(self) -> str:
        cls_name = type(self).__name__
        return f"{cls_name}(ibytes={self._fields})"

    def __str__(self) -> str:
        return str(list(self))

    def as_bytes(self) -> bytes:
        return bytes(field.byte for field in self._fields)
