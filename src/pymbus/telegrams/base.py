"""Basic Telegram objects module.

Glossary:

- a byte is an integer witing the range(0, 256)
- an instance of the TelegramField class is a wrapper over a byte
- a telegram byte refers to the "int | TelegramField"
"""

from collections.abc import Iterable, Iterator

from pymbus.exceptions import MBusValidationError


def _validate_byte(number: int) -> int:
    """Returns an integer if it is a byte.

    In Python, a byte must be in range(0, 256).
    This is the range for an 8-bit unsigned integer.

    Parameters
    ----------
    number : int

    Raises
    ------
    MbusValidationError
        the `number` is out of the [0, 255] segment.

    Returns
    -------
    int
    """

    try:
        bytes([number])
    except ValueError as e:
        msg = f"{number} is not a valid byte"
        raise MBusValidationError(msg) from e

    return number


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

    def __lt__(self, other: "int | TelegramField") -> bool:
        sbyte = self.byte
        if isinstance(other, TelegramField):
            other = other.byte
        return sbyte < other

    def __int__(self) -> int:
        return self.byte

    def __repr__(self) -> str:
        cls_name = type(self).__name__
        return f"{cls_name}(byte={self.byte})"

    @property
    def byte(self) -> int:
        """Return the byte value of the field."""

        return self._byte


TelegramByteType = int | TelegramField
TelegramBytesType = bytes | bytearray | Iterable[TelegramByteType]
TelegramByteIterableType = TelegramBytesType | Iterator[TelegramByteType]


def _convert_to_telegram_fields(
    ibytes: TelegramByteIterableType,
) -> list[TelegramField]:
    return [
        ibyte if isinstance(ibyte, TelegramField) else TelegramField(ibyte)
        for ibyte in ibytes
    ]


class TelegramContainer:
    """The base class for Telegram containers.

    A telegram container consists of telegram fields
    and it is an iterable object, which may also be an iterator.

    The container accepts incoming bytes in a greedy manner.
    """

    @classmethod
    def from_hexstring(cls, hexstr: str) -> "TelegramContainer":
        """Return a class instance from a hexadecimal string."""

        try:
            return cls(bytearray.fromhex(hexstr))
        except ValueError as e:
            raise MBusValidationError(str(e)) from e

    @classmethod
    def from_integers(cls, ints: Iterable[int]) -> "TelegramContainer":
        """Return a class instance from a sequence of integers."""

        try:
            return cls(bytearray(iter(ints)))
        except ValueError as e:
            raise MBusValidationError(str(e)) from e

    def __init__(self, ibytes: None | TelegramByteIterableType = None) -> None:
        self._fields = _convert_to_telegram_fields(ibytes or [])

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

    def __repr__(self) -> str:
        cls_name = type(self).__name__
        return f"{cls_name}(ibytes={self._fields})"

    @staticmethod
    def _iterify(data: None | TelegramBytesType = None) -> Iterator:
        return iter(data or [])

    def as_bytes(self) -> bytes:
        """Return bytes as Python `bytes`."""

        return bytes(self.as_ints())

    def as_ints(self) -> list[int]:
        """Return bytes as a list of integers."""

        return [field.byte for field in self._fields]


def extract_bytes(it: Iterable) -> list[int]:
    """Return the list of integers from an iterable object.

    Notes
    -----
    The items are validated except `TelegramField`s.

    Parameters
    ----------
    it : Iterable

    Raises
    ------
    MbusValidationError:
        if any item is not a byte.

    Returns
    -------
    list[int]
    """

    return [
        item.byte if isinstance(item, TelegramField) else _validate_byte(item)
        for item in it
    ]
