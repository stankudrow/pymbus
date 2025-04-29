"""The Meter-Bus (M-Bus) type classes and functions.

Glossary:

- a byte = 8 bits
- a nibble = 4 bits
- a BCD = a "Binary-Coded Decimal".

The standard IEC 870-5-4 defines the following data types
for usage inside the application layer:

- Type A = Unsigned Integer BCD;
- Type B = Binary Integer;
- Type C = Unsigned Integer;
- Type D = Boolean (can be a subtype of Integer);
- Type E = Compound CP16 -> types and units information;
- Type F = Compound CP32 -> date and time;
- Type G = Compound CP16 -> date;
- Type H = Floating point according to IEEE-standard 754


Type A, or Unsigned Integer BCD -> 1 or more bytes.
Decoded per nibbles (4 bits).

Type B, or Signed Binary Integer -> 1 or more bytes.
The most significant bit (MSB) of the last byte denotes the sign (S):
if S is 0 (zero), the number is positive,
otherwise, the rest bits are negative values in two's complement.

Type C, or Unsigned Integer -> 1 or more bytes.
Computed as a unit of concatenated bytes.

Type D, or Boolean -> 1 or more bytes.
The boolean of a unit of concatenated bytes.

Type E, or Compound CP16 (types and units information) -> 2 bytes.

Type F = Compound CP32: Date and Time -> 4 bytes.

Type G, or Compound CP16: Date -> 2 bytes.
"""

import struct
from collections.abc import Iterable
from datetime import date, datetime, time, timezone, tzinfo

from pymbus.constants import BIG_ENDIAN, BYTE, NIBBLE
from pymbus.exceptions import MBusError, MBusLengthError, MBusValidationError

BytesType = bytes | bytearray | Iterable[int]


## integer types section


def _validate_non_empty_bytes(ibytes: BytesType) -> bytes:
    ibytes = bytes(list(ibytes))
    if not ibytes:
        msg = "cannot parse empty bytes"
        raise MBusLengthError(msg)
    return ibytes


def parse_bcd_uint(ibytes: BytesType) -> int:
    """Returns the unsigned integer from a byte sequence.

    BCD = Binary-Coded Decimal.
    The "Unsigned Integer BCD" type = "Type A".
    The bytes are parsed along the Big endian order.

    The function is greedy.

    Parameters
    ----------
    ibytes: BytesType
        the sequence of bytes for "Type A" parsing

    Raises
    ------
    MBusLengthError
        if an empty byte sequence is given

    Returns
    -------
    int
    """

    bytez = _validate_non_empty_bytes(ibytes)

    msp, lsp = 0b1111_0000, 0b0000_1111
    masks = (lsp, msp)

    number, power = 0, 0
    for byte in bytez:
        for mask in masks:
            digit = byte & mask
            number += digit * 10**power
            power += 1

    return number


def parse_int(ibytes: BytesType) -> int:
    """Returns the signed integer from a byte sequence.

    The "Binary Integer" type = "Type B".
    The bytes are parsed along the Big endian order.

    The function is greedy.

    Notes:
    ------
    An older implementation:
    ```python
    neg_sign = bytez[-1] & 0x80
    value = 0
    for byte in reversed(bytez):
        value = value << BYTE
        if neg_sign:
            value += byte ^ 0xFF  # two's compliment
        else:
            value += byte
    if neg_sign:
        value = (-value) - 1  # two's compliment
    return value
    ```

    Parameters
    ----------
    ibytes: BytesType
        the sequence of bytes for "Type B" parsing

    Raises
    ------
    MBusLengthError
        if an empty byte sequence is given

    Returns
    -------
    int
    """

    bytez = _validate_non_empty_bytes(ibytes)

    return int.from_bytes(
        bytes(reversed(bytez)), byteorder=BIG_ENDIAN, signed=True
    )


def parse_uint(ibytes: BytesType) -> int:
    """Returns the unsigned integer from a byte sequence.

    The "Unsigned Integer" type = "Type C".
    The bytes are parsed along the Big endian order.

    Parameters
    ----------
    ibytes: BytesType
        the sequence of bytes for "Type C" parsing

    Raises
    ------
    MBusLengthError
        if an empty byte sequence is given

    Returns
    -------
    int
    """

    bytez = _validate_non_empty_bytes(ibytes)

    return int.from_bytes(
        bytes(reversed(bytez)), byteorder=BIG_ENDIAN, signed=False
    )


## boolean section


def parse_bool(ibytes: BytesType) -> bool:
    """Returns the boolean from a byte sequence.

    The "Boolean" type = "Type D".
    The bytes are parsed along the Big endian order.

    Parameters
    ----------
    ibytes: BytesType
        the sequence of bytes for "Type D" parsing

    Raises
    ------
    MBusLengthError
        if an empty byte sequence is given

    Returns
    -------
    bool
    """

    return bool(parse_uint(ibytes))


## floating point (real) numbers section


def parse_float(ibytes: BytesType) -> float:
    """Returns the float from a byte sequence.

    Type H: Floating point according to IEEE-standard.

    Parameters
    ----------
    ibytes: BytesType
        the sequence of bytes for "Type H" parsing

    Raises
    ------
    MBusLengthError:
        invalid number of bytes to parse
    MBusError
        float-parsing error

    Returns
    -------
    float
    """

    it = iter(ibytes)
    try:
        frame = [next(it) for _ in range(4)]
    except StopIteration as e:
        raise MBusLengthError(str(ibytes)) from e

    try:
        return float(struct.unpack("f", bytes(frame))[0])
    except (struct.error, ValueError) as e:
        msg = f"float parsing error for {frame}: {e}"
        raise MBusError(msg) from e


## types and units information (Type E = Compound CP16)


class UnitType:
    """Type E = Compound CP16: types and units information."""

    @classmethod
    def from_bytes(cls, frame: BytesType) -> "UnitType":
        """Return a `UnitType` from an array of bytes."""

        return cls(frame)

    @classmethod
    def from_hexstring(cls, hexstr: str) -> "UnitType":
        """Return a `UnitType` from a hexadecimal string."""

        barr = bytearray.fromhex(hexstr)
        return cls.from_bytes(barr)

    def __init__(self, ibytes: BytesType) -> None:
        it = iter(ibytes)
        try:
            lst = [next(it) for _ in range(2)]
        except StopIteration as e:
            raise MBusLengthError(str(ibytes)) from e

        fields = bytes(lst)

        unit_mask, media_mask = 0b1100_0000, 0b0011_1111
        self._unit1 = fields[1] & unit_mask
        self._unit2 = fields[0] & unit_mask
        self._media = bytes(
            [
                fields[0] & media_mask,
                fields[1] & media_mask,
            ]
        )

    def __eq__(self, other: object) -> bool:
        units = (self.unit1, self.unit2, self.media)
        if isinstance(other, UnitType):
            other = (other.unit1, other.unit2, other.media)
        return units == other

    @property
    def media(self) -> bytes:
        return self._media

    @property
    def unit1(self) -> int:
        return self._unit1

    @property
    def unit2(self) -> int:
        return self._unit2


def parse_unit_type(ibytes: BytesType) -> UnitType:
    """Returns the "unit_type" from a byte sequence.

    The "Types and Units Information" = "Type E".

    Parameters
    ----------
    ibytes: BytesType
        the sequence of bytes for "Type E" parsing

    Raises
    ------
    MBusError
        unit_type parsing error

    Returns
    -------
    UnitType
    """

    return UnitType(ibytes)


## date, time and datetime types section


YEAR_MASK_LSB = 0xE0
YEAR_MASK_MSB = 0xF0
MONTH_MASK = 0xF
DAY_MASK = 0x1F

HOUR_MASK = 0x1F
MINUTE_MASK = 0x3F
SECOND_MASK = 0x3F


### Date section


def get_year(lsp: int, msp: int) -> int:
    """Return the value of years from `lsp` and `msp` parts."""

    year_lsp = lsp & YEAR_MASK_LSB
    year_msp = msp & YEAR_MASK_MSB

    # concatenating MS and LS parts
    year = (year_msp | (year_lsp >> NIBBLE)) >> 1

    if year < 81:
        return 2000 + year
    return 1900 + year


def get_month(byte: int) -> int:
    """Return the value of months from a byte."""

    return byte & MONTH_MASK


def get_day(byte: int) -> int:
    """Return the value of days from a byte."""

    return byte & DAY_MASK


def parse_date(ibytes: BytesType) -> date:
    """Return the Python date from a byte sequence.

    The "Date" type = Type G (Compound CP16).

    Parameters
    ----------
    frame: BytesType
        a byte sequence for date parsing

    Raises
    ------
    MBusLengthError

    Returns
    -------
    date
    """

    it = iter(ibytes)
    try:
        lst = [next(it) for _ in range(2)]
    except StopIteration as e:
        raise MBusLengthError(str(ibytes)) from e

    fields = bytes(lst)

    dt0 = fields[0]
    dt1 = fields[1]

    return date(
        year=get_year(lsp=dt0, msp=dt1),
        month=get_month(byte=dt1),
        day=get_day(byte=dt0),
    )


class Date:
    """Type G = Compound CP16: Date."""

    @classmethod
    def from_date(cls, pydate: date) -> "Date":
        """Return a `Date` from a Python date."""

        return cls(year=pydate.year, month=pydate.month, day=pydate.day)

    @classmethod
    def from_bytes(cls, frame: BytesType) -> "Date":
        """Return a `Date` from an array of bytes."""

        pydate = parse_date(frame)
        return cls.from_date(pydate)

    @classmethod
    def from_hexstring(cls, hexstr: str) -> "Date":
        """Return a `Date` from a hexadecimal string."""

        barr = bytearray.fromhex(hexstr)
        return cls.from_bytes(barr)

    def __init__(self, year: int, month: int, day: int) -> None:
        self._date = date(year=year, month=month, day=day)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Date):
            other = other.to_date()
        return self._date == other

    def __repr__(self) -> str:
        cls_name = type(self).__name__
        return (
            f"{cls_name}(year={self.year}, month={self.month}, day={self.day})"
        )

    @property
    def year(self) -> int:
        return self._date.year

    @property
    def month(self) -> int:
        return self._date.month

    @property
    def day(self) -> int:
        return self._date.day

    def to_date(self) -> date:
        return self._date

    def to_iso_format(self) -> str:
        return self._date.isoformat()


### Time section


def get_hour(byte: int) -> int:
    """Return the value of hours from a byte."""

    return byte & HOUR_MASK


def get_minute(byte: int) -> int:
    """Return the value of minutes from a byte."""

    return byte & MINUTE_MASK


def get_second(byte: int) -> int:
    """Return the value of seconds from a byte."""

    return byte & SECOND_MASK


def parse_time(ibytes: BytesType) -> time:
    """Return the Python time from a byte sequence.

    Parameters
    ----------
    ibytes: BytesType
        a byte sequence for time parsing

    Returns
    -------
    time
    """

    it = iter(ibytes)
    lst = [next(it) for _ in range(2)]

    sec_byte: None | int = None
    try:
        sec_byte = next(it)
        next(it)
        sec_byte = next(it)
    except StopIteration:
        pass

    if sec_byte:
        lst += [sec_byte]

    fields = bytes(lst)

    dt0 = fields[0]
    dt1 = fields[1]
    sec_byte = 0

    length = len(fields)
    if length == 3:
        sec_byte = fields[2]
    if length == 5:
        sec_byte = fields[4]

    return time(
        hour=get_hour(byte=dt1),
        minute=get_minute(byte=dt0),
        second=get_second(byte=sec_byte),
    )


class Time:
    """Time class.

    Not a part of the Meter-Bus standard types.
    """

    _sep: str = ":"

    @classmethod
    def from_time(cls, pytime: time) -> "Time":
        return cls(
            hour=pytime.hour,
            minute=pytime.minute,
            second=pytime.second,
        )

    @classmethod
    def from_bytes(cls, frame: BytesType) -> "Time":
        """Return a `Time` from an array of bytes."""

        pytime = parse_time(frame)
        return cls.from_time(pytime)

    @classmethod
    def from_hexstring(cls, hexstr: str) -> "Time":
        """Return a `Time` from a hexadecimal string."""

        barr = bytearray.fromhex(hexstr)
        return cls.from_bytes(barr)

    def __init__(self, hour: int, minute: int, second: int = 0) -> None:
        self._time = time(hour=hour, minute=minute, second=second)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Time):
            other = other.to_time()
        return self._time == other

    def __repr__(self) -> str:
        cls_name = type(self).__name__
        return (
            f"{cls_name}(hour={self.hour}, "
            f"minute={self.minute}, "
            f"second={self.second})"
        )

    @property
    def hour(self) -> int:
        return self._time.hour

    @property
    def minute(self) -> int:
        return self._time.minute

    @property
    def second(self) -> int:
        return self._time.second

    def to_iso_format(self, *, timespec: str = "auto") -> str:
        return self._time.isoformat(timespec=timespec)

    def to_time(self) -> time:
        return self._time


### DateTime section


def parse_datetime(ibytes: BytesType) -> datetime:
    """Return the Python date from a byte sequence.

    Type F = Compound CP32: Date and Time.

    Parameters
    ----------
    ibytes: BytesType
        a byte sequence for datetime parsing

    Raises
    ------
    MBusLengthError

    Returns
    -------
    datetime
    """

    it = iter(ibytes)
    try:
        lst = [next(it) for _ in range(4)]
    except StopIteration as e:
        raise MBusLengthError(str(ibytes)) from e

    try:
        lst += [next(it)]
    except StopIteration:
        pass

    fields = bytes(lst)

    dt0 = fields[0]
    dt1 = fields[1]
    dt2 = fields[2]
    dt3 = fields[3]

    dt4 = 0
    if len(fields) == 5:
        dt4 = fields[4]

    return datetime(
        year=get_year(lsp=dt2, msp=dt3),
        month=get_month(dt3),
        day=get_day(dt2),
        hour=get_hour(dt1),
        minute=get_minute(dt0),
        second=get_second(dt4),
        tzinfo=timezone.utc,
    )


class DateTime:
    """Type F = Compound CP32: Date and Time."""

    @classmethod
    def from_datetime(cls, pydatetime: datetime) -> "DateTime":
        """Return a `DateTime` from a Python datetime."""

        return cls(
            year=pydatetime.year,
            month=pydatetime.month,
            day=pydatetime.day,
            hour=pydatetime.hour,
            minute=pydatetime.minute,
            second=pydatetime.second,
            tzinfo=pydatetime.tzinfo,
        )

    @classmethod
    def from_bytes(cls, frame: BytesType) -> "DateTime":
        """Return a `DateTime` from an array of bytes."""

        pydatetime = parse_datetime(frame)
        return cls.from_datetime(pydatetime)

    @classmethod
    def from_hexstring(cls, hexstr: str) -> "DateTime":
        """Return a `DateTime` from a hexadecimal string."""

        barr = bytes.fromhex(hexstr)
        return cls.from_bytes(barr)

    def __init__(
        self,
        year: int,
        month: int,
        day: int,
        hour: int,
        minute: int,
        second: int = 0,
        tzinfo: tzinfo | None = None,
    ) -> None:
        self._datetime = datetime(
            year=year,
            month=month,
            day=day,
            hour=hour,
            minute=minute,
            second=second,
            tzinfo=tzinfo,
        )

    def __eq__(self, other: object) -> bool:
        sdt = self._datetime
        if isinstance(other, DateTime):
            other = other.to_datetime()
        return sdt == other  # noqa: DTZ001

    def __repr__(self) -> str:
        cls_name = type(self).__name__
        return (
            f"{cls_name}("
            f"year={self.year}, month={self.month}, day={self.day}, "
            f"hour={self.hour}, minute={self.minute}, second={self.second}, "
            f"tzinfo={self.tzinfo})"
        )

    @property
    def year(self) -> int:
        return self._datetime.year

    @property
    def month(self) -> int:
        return self._datetime.month

    @property
    def day(self) -> int:
        return self._datetime.day

    @property
    def hour(self) -> int:
        return self._datetime.hour

    @property
    def minute(self) -> int:
        return self._datetime.minute

    @property
    def second(self) -> int:
        return self._datetime.second

    @property
    def tzinfo(self) -> tzinfo | None:
        return self._datetime.tzinfo

    def to_datetime(self) -> datetime:
        return self._datetime

    def to_iso(self) -> str:
        return self._datetime.isoformat()
