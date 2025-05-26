"""Basic Telegram objects module.

Glossary:

- a byte is an integer witing the range(0, 256)
- an instance of the TelegramField class is a wrapper over a byte
- a telegram byte refers to the "int | TelegramField"
"""

import sys
from collections.abc import Iterable, Iterator, Sequence
from functools import total_ordering
from typing import Any

from pymbus.exceptions import MBusValidationError
from pymbus.utils import validate_byte


class TelegramField(int):
    """The base "Field" class.

    Restricts int values to the byte range [0, 255].
    Supports all operations that the `int` class does.
    """

    def __init__(self, byte: int) -> None:
        self._byte = validate_byte(byte)

    def __repr__(self) -> str:
        cls_name = type(self).__name__
        return f"{cls_name}({self._byte})"


TelegramByteType = int | TelegramField
TelegramBytesType = bytes | bytearray | Iterable[TelegramByteType]
TelegramByteIterableType = TelegramBytesType | Iterator[TelegramByteType]


@total_ordering
class TelegramContainer(Sequence):
    """The base class for Telegram containers.

    A telegram container consists of telegram fields.
    When being instantiated, the incoming bytes are consumed greedily.
    """

    @classmethod
    def from_hexstring(cls, hexstr: str) -> "TelegramContainer":
        """Return a class instance from a hexadecimal string."""

        try:
            return cls(bytearray.fromhex(hexstr))
        except ValueError as e:
            raise MBusValidationError(str(e)) from e

    def __init__(
        self,
        ibytes: None | TelegramByteIterableType = None,
    ) -> None:
        self._fields: list[TelegramField] = (
            [TelegramField(ibyte) for ibyte in ibytes] if ibytes else []
        )

    def __contains__(self, value: Any) -> bool:
        return value in self._fields

    def __eq__(self, other: object) -> bool:
        sfields = self._fields
        if isinstance(other, TelegramContainer):
            other = other._fields
        return sfields == other

    def __getitem__(self, key: int | slice, /) -> Any | Sequence[Any]:
        if isinstance(key, int):
            return self._fields[key]
        return type(self)(self._fields[key])

    def __iter__(self) -> Iterator[TelegramField]:
        yield from self._fields

    def __len__(self) -> int:
        return len(self._fields)

    def __lt__(self, other: Iterable) -> bool:
        sfields = self._fields
        if isinstance(other, TelegramContainer):
            other = other._fields
        return bool(sfields < list(other))

    def __repr__(self) -> str:
        cls_name = type(self).__name__
        return f"{cls_name}({self._fields})"

    def __reversed__(self) -> Iterator[TelegramField]:
        yield from reversed(self._fields)

    def index(self, value: Any, start: int = 0, stop: None | int = None) -> int:
        """Return the first index of the value.

        Raises
        ------
        ValueError
            if the value is not present

        Returns
        -------
        int
        """
        stop = sys.maxsize if stop is None else stop
        return self._fields.index(TelegramField(value), start, stop)

    def count(self, value: Any) -> int:
        """Return the number of occurrences of value."""

        return self._fields.count(TelegramField(value))
