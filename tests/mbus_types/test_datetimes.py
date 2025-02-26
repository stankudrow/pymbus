from contextlib import AbstractContextManager
from contextlib import nullcontext as does_not_raise
from datetime import date, datetime, time, timezone

import pytest

from pymbus.exceptions import MBusError
from pymbus.mbtypes import (
    Date,
    DateTime,
    Time,
    parse_date,
    parse_datetime,
    parse_time,
)

### date section


@pytest.mark.parametrize(
    ("year", "month", "day", "expectation"),
    [
        (2000, 1, 2, does_not_raise()),
        (0, 0, 0, pytest.raises(ValueError)),
        (1, 0, 0, pytest.raises(ValueError)),
        (
            1,
            1,
            0,
            pytest.raises(ValueError),
        ),
        (1, 1, 1, does_not_raise()),
    ],
)
def test_date_init(
    year: int, month: int, day: None | int, expectation: AbstractContextManager
):
    with expectation:
        date_ = Date(year=year, month=month, day=day)

        assert date_ == date_
        assert date_ == date(year=year, month=month, day=day)
        assert date_ == (year, month, day)

        assert date_.year == year
        assert date_.month == month
        assert date_.day == day


@pytest.mark.parametrize(
    ("hexdata", "dd"),
    [
        (
            "0A 25",
            date(year=2016, month=5, day=10),
        ),
        (
            "6A 28",
            date(year=2019, month=8, day=10),
        ),
        (
            "45 2C",
            date(year=2018, month=12, day=5),
        ),
        (
            "6A 25",
            date(year=2019, month=5, day=10),
        ),
    ],
)
def test_parse_date(hexdata: str, dd: date):
    bindata = bytearray.fromhex(hexdata)
    integers = list(bindata)

    assert Date.from_bytes(bindata) == dd
    assert Date.from_hexstring(hexdata) == dd

    assert parse_date(integers) == dd


def test_date_repr():
    year, month, day = 2000, 11, 23

    date_ = Date(year=year, month=month, day=day)

    assert repr(date_) == f"Date(year={year}, month={month}, day={day})"


def test_date_to_iso():
    year, month, day = 2000, 11, 23

    date_ = Date(year=year, month=month, day=day)

    assert date_.to_iso_format() == f"{year}-{month}-{day}"


### time section


@pytest.mark.parametrize(
    ("hour", "minute", "second", "expectation"),
    [
        (23, 59, 59, does_not_raise()),
        (0, 0, 0, does_not_raise()),
        (1, 2, None, does_not_raise()),
        (24, 0, 0, pytest.raises(ValueError)),
    ],
)
def test_time_init(
    hour: int,
    minute: int,
    second: None | int,
    expectation: AbstractContextManager,
):
    with expectation:
        if second is None:
            time_ = Time(hour=hour, minute=minute)
            second = 0
        else:
            time_ = Time(hour=hour, minute=minute, second=second)

        assert time_ == time_
        assert time_ == time(hour=hour, minute=minute, second=second)
        assert time_ == (hour, minute, second)

        assert time_.hour == hour
        assert time_.minute == minute
        assert time_.second == second


@pytest.mark.parametrize(
    ("hexdata", "tt"),
    [
        (
            "1E 0A",
            time(hour=10, minute=30, second=0),
        ),
        (
            "1E 09 0F",
            time(hour=9, minute=30, second=15),
        ),
        (
            "1E 0B 37",
            time(hour=11, minute=30, second=55),
        ),
        (
            "3B 17 3B",
            time(hour=23, minute=59, second=59),
        ),
        (
            "3B 17 FF FF 3B",
            time(hour=23, minute=59, second=59),
        ),
    ],
)
def test_parse_time(hexdata: str, tt: time):
    bindata = bytearray.fromhex(hexdata)
    integers = list(bindata)

    assert Time.from_bytes(bindata) == tt
    assert Time.from_hexstring(hexdata) == tt

    assert parse_time(integers) == tt


def test_time_repr():
    hour, minute, second = 23, 59, 59

    time_ = Time(hour=hour, minute=minute, second=second)

    assert repr(time_) == f"Time(hour={hour}, minute={minute}, second={second})"


def test_time_to_iso():
    hour, minute, second = 23, 59, 59

    time_ = Time(hour=hour, minute=minute, second=second)

    assert time_.to_iso_format() == f"{hour}:{minute}:{second}"


def test_time_to_strings():
    hour, minute, second = 23, 59, 59

    time_ = Time(hour=hour, minute=minute, second=second)

    assert time_.to_iso_format() == time_.to_hhmmss_format()
    assert time_.to_hhmm_format() == f"{hour}:{minute}"


### datetime section


@pytest.mark.parametrize(
    (
        "year",
        "month",
        "day",
        "hour",
        "minute",
        "second",
        "tzinfo",
        "expectation",
    ),
    [
        (2000, 1, 2, 3, 4, 5, None, does_not_raise()),
        (
            0,
            0,
            0,
            1,
            1,
            1,
            None,
            pytest.raises(ValueError),
        ),
        (
            1,
            0,
            0,
            1,
            1,
            1,
            None,
            pytest.raises(ValueError),
        ),
        (
            1,
            1,
            0,
            1,
            1,
            1,
            None,
            pytest.raises(ValueError),
        ),
        (1, 1, 1, 0, 0, 0, None, does_not_raise()),
        (1, 1, 1, 1, 1, 1, None, does_not_raise()),
    ],
)
def test_datetime_init(
    year: int,
    month: int,
    day: int,
    hour: int,
    minute: int,
    second: int,
    tzinfo: None | timezone,
    expectation: AbstractContextManager,
):
    with expectation:
        datetime_ = DateTime(
            year=year,
            month=month,
            day=day,
            hour=hour,
            minute=minute,
            second=second,
            tzinfo=tzinfo,
        )

        assert datetime_ == datetime_
        assert datetime_ == datetime(
            year=year,
            month=month,
            day=day,
            hour=hour,
            minute=minute,
            second=second,
            tzinfo=tzinfo,
        )
        assert datetime_ == (year, month, day, hour, minute, second)

        assert datetime_.year == year
        assert datetime_.month == month
        assert datetime_.day == day
        assert datetime_.hour == hour
        assert datetime_.minute == minute
        assert datetime_.second == second


@pytest.mark.parametrize(
    ("hexdata", "dt"),
    [
        (
            "1E 0A 0A 25 0F",
            datetime(
                year=2016,
                month=5,
                day=10,
                hour=10,
                minute=30,
                second=15,
                tzinfo=timezone.utc,
            ),
        ),
        (
            "1E 09 6A 28 00",
            datetime(
                year=2019,
                month=8,
                day=10,
                hour=9,
                minute=30,
                second=0,
                tzinfo=timezone.utc,
            ),
        ),
        (
            "1E 0B 45 2C 37",
            datetime(
                year=2018,
                month=12,
                day=5,
                hour=11,
                minute=30,
                second=55,
                tzinfo=timezone.utc,
            ),
        ),
        (
            "3B 17 6A 25 3B",
            datetime(
                year=2019,
                month=5,
                day=10,
                hour=23,
                minute=59,
                second=59,
                tzinfo=timezone.utc,
            ),
        ),
        (
            "3B 17 6A 25",
            datetime(
                year=2019,
                month=5,
                day=10,
                hour=23,
                minute=59,
                second=0,
                tzinfo=timezone.utc,
            ),
        ),
        (
            "3B 17 6A 25 3B FF",
            datetime(
                year=2019,
                month=5,
                day=10,
                hour=23,
                minute=59,
                second=59,
                tzinfo=timezone.utc,
            ),
        ),
    ],
)
def test_parse_datetime(hexdata: str, dt: datetime):
    bindata = bytearray.fromhex(hexdata)
    integers = list(bindata)

    assert DateTime.from_bytes(bindata) == dt
    assert DateTime.from_hexstring(hexdata) == dt

    assert parse_datetime(integers) == dt


def test_parse_datetime_byte_mismatch():
    frame = "3B 17 6A"
    bindata = bytearray.fromhex(frame)

    answer = datetime(
        year=2019,
        month=5,
        day=10,
        hour=23,
        minute=59,
        second=0,
        tzinfo=timezone.utc,
    )

    with pytest.raises(MBusError):
        assert parse_datetime(bindata) == answer


def test_datetime_repr():
    year, month, day = 2000, 11, 23
    hour, minute, second = 21, 22, 23

    dt = DateTime(
        year=year, month=month, day=day, hour=hour, minute=minute, second=second
    )
    repstr = (
        f"DateTime(year={year}, month={month}, day={day}, "
        f"hour={hour}, minute={minute}, second={second})"
    )

    assert repr(dt) == repstr


def test_datetime_to_iso():
    year, month, day, hour, minute, second = 1999, 12, 31, 23, 59, 59

    dt = DateTime(
        year=year, month=month, day=day, hour=hour, minute=minute, second=second
    )
    ans_base = f"{year}-{month}-{day}T{hour}:{minute}:{second}"

    assert dt.to_iso() == ans_base
    assert dt.to_iso(with_tz=True) == f"{ans_base}+00:00"
