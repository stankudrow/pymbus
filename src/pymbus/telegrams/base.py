"""Basic Telegram objects module.

Glossary:

- a byte is an integer witing the range(0, 256)
- an instance of the TelegramField class is a wrapper over a byte
- a telegram byte refers to the "int | TelegramField"
"""

from collections.abc import Iterable, Iterator
from functools import total_ordering

from pymbus.exceptions import MBusValidationError
from pymbus.utils import validate_byte


@total_ordering
class TelegramField:
    """The base "Field" class.

    It is a base wrapper over a byte value.
    """

    def __init__(self, byte: int, *, validate: bool = False) -> None:
        self._byte = validate_byte(byte) if validate else byte

    def __and__(self, other: "int | TelegramField") -> int:
        if isinstance(other, TelegramField):
            other = other._byte
        return self._byte & other

    def __bool__(self) -> bool:
        return bool(self._byte)

    def __eq__(self, other: object) -> bool:
        sbyte = self._byte
        if isinstance(other, TelegramField):
            other = other._byte
        return sbyte == other

    def __int__(self) -> int:
        return self._byte

    def __invert__(self) -> int:
        return ~self._byte

    def __lt__(self, other: "int | TelegramField") -> bool:
        sbyte = self._byte
        if isinstance(other, TelegramField):
            other = other._byte
        return sbyte < other

    def __or__(self, other: "int | TelegramField") -> int:
        if isinstance(other, TelegramField):
            other = other._byte
        return self._byte | other

    def __repr__(self) -> str:
        cls_name = type(self).__name__
        return f"{cls_name}(byte={self._byte})"

    def __xor__(self, other: "int | TelegramField") -> int:
        if isinstance(other, TelegramField):
            other = other._byte
        return self._byte ^ other


TelegramByteType = int | TelegramField
TelegramBytesType = bytes | bytearray | Iterable[TelegramByteType]
TelegramByteIterableType = TelegramBytesType | Iterator[TelegramByteType]


@total_ordering
class TelegramContainer:
    """The base class for Telegram containers.

    TelegramContainer consists of telegram fields.
    When being instantiated, the incomin bytes are consumed greedily.
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
        *,
        validate: bool = False,
    ) -> None:
        self._fields: list[TelegramField] = (
            [TelegramField(int(ibyte), validate=validate) for ibyte in ibytes]
            if ibytes
            else []
        )

    def __eq__(self, other: object) -> bool:
        sfields = self._fields
        if isinstance(other, TelegramContainer):
            other = other._fields
        return sfields == other

    def __getitem__(
        self, key: int | slice
    ) -> "TelegramField | TelegramContainer":
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
        return f"{cls_name}(ibytes={self._fields})"
