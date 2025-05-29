import pytest

from pymbus.codes.vif import (
    VIFCode,
    VIFCodeKind,
    VIFCodeUnit,
    VIFTablet,
)
from pymbus.exceptions import MBusValidationError
from pymbus.telegrams.fields import ValueInformationField as VIF


def test_bad_nonbyte_value():
    with pytest.raises(MBusValidationError):
        VIFTablet()(266)


def test_no_vif_code():
    assert VIFTablet()(VIF(0b0111_1011)) is None


@pytest.mark.parametrize(
    ("vif", "coef", "kind", "unit"),
    [
        # Energy (Watt * hour)
        (
            VIF(0b0000_0000),
            1e-3,
            VIFCodeKind.energy,
            VIFCodeUnit.watt_hour,
        ),
        (
            VIF(0b0000_0001),
            1e-2,
            VIFCodeKind.energy,
            VIFCodeUnit.watt_hour,
        ),
        (
            VIF(0b0000_0010),
            1e-1,
            VIFCodeKind.energy,
            VIFCodeUnit.watt_hour,
        ),
        (
            VIF(0b0000_0011),
            1e0,
            VIFCodeKind.energy,
            VIFCodeUnit.watt_hour,
        ),
        (
            VIF(0b0000_0100),
            1e1,
            VIFCodeKind.energy,
            VIFCodeUnit.watt_hour,
        ),
        (
            VIF(0b0000_0101),
            1e2,
            VIFCodeKind.energy,
            VIFCodeUnit.watt_hour,
        ),
        (
            VIF(0b0000_0110),
            1e3,
            VIFCodeKind.energy,
            VIFCodeUnit.watt_hour,
        ),
        (
            VIF(0b0000_0111),
            1e4,
            VIFCodeKind.energy,
            VIFCodeUnit.watt_hour,
        ),
        # Energy (Joule)
        (VIF(0b0000_1000), 1e0, VIFCodeKind.energy, VIFCodeUnit.joule),
        (VIF(0b0000_1001), 1e1, VIFCodeKind.energy, VIFCodeUnit.joule),
        (VIF(0b0000_1010), 1e2, VIFCodeKind.energy, VIFCodeUnit.joule),
        (VIF(0b0000_1011), 1e3, VIFCodeKind.energy, VIFCodeUnit.joule),
        (VIF(0b0000_1100), 1e4, VIFCodeKind.energy, VIFCodeUnit.joule),
        (VIF(0b0000_1101), 1e5, VIFCodeKind.energy, VIFCodeUnit.joule),
        (VIF(0b0000_1110), 1e6, VIFCodeKind.energy, VIFCodeUnit.joule),
        (VIF(0b0000_1111), 1e7, VIFCodeKind.energy, VIFCodeUnit.joule),
        # Volume (Meter cubic)
        (
            VIF(0b0001_0000),
            1e-6,
            VIFCodeKind.volume,
            VIFCodeUnit.meter_cubic,
        ),
        (
            VIF(0b0001_0001),
            1e-5,
            VIFCodeKind.volume,
            VIFCodeUnit.meter_cubic,
        ),
        (
            VIF(0b0001_0010),
            1e-4,
            VIFCodeKind.volume,
            VIFCodeUnit.meter_cubic,
        ),
        (
            VIF(0b0001_0011),
            1e-3,
            VIFCodeKind.volume,
            VIFCodeUnit.meter_cubic,
        ),
        (
            VIF(0b0001_0100),
            1e-2,
            VIFCodeKind.volume,
            VIFCodeUnit.meter_cubic,
        ),
        (
            VIF(0b0001_0101),
            1e-1,
            VIFCodeKind.volume,
            VIFCodeUnit.meter_cubic,
        ),
        (
            VIF(0b0001_0110),
            1e0,
            VIFCodeKind.volume,
            VIFCodeUnit.meter_cubic,
        ),
        (
            VIF(0b0001_0111),
            1e1,
            VIFCodeKind.volume,
            VIFCodeUnit.meter_cubic,
        ),
        # Mass (Kilogram)
        (VIF(0b0001_1000), 1e-3, VIFCodeKind.mass, VIFCodeUnit.kilogram),
        (VIF(0b0001_1001), 1e-2, VIFCodeKind.mass, VIFCodeUnit.kilogram),
        (VIF(0b0001_1010), 1e-1, VIFCodeKind.mass, VIFCodeUnit.kilogram),
        (VIF(0b0001_1011), 1e0, VIFCodeKind.mass, VIFCodeUnit.kilogram),
        (VIF(0b0001_1100), 1e1, VIFCodeKind.mass, VIFCodeUnit.kilogram),
        (VIF(0b0001_1101), 1e2, VIFCodeKind.mass, VIFCodeUnit.kilogram),
        (VIF(0b0001_1110), 1e3, VIFCodeKind.mass, VIFCodeUnit.kilogram),
        (VIF(0b0001_1111), 1e4, VIFCodeKind.mass, VIFCodeUnit.kilogram),
        # On Time (time parts -> days, hours, minutes, seconds)
        (VIF(0b0010_0000), 1, VIFCodeKind.on_time, VIFCodeUnit.second),
        (VIF(0b0010_0001), 60, VIFCodeKind.on_time, VIFCodeUnit.second),
        (
            VIF(0b0010_0010),
            3600,
            VIFCodeKind.on_time,
            VIFCodeUnit.second,
        ),
        (
            VIF(0b0010_0011),
            86400,
            VIFCodeKind.on_time,
            VIFCodeUnit.second,
        ),
        # Operating Time (like On Time)
        (
            VIF(0b0010_0100),
            1,
            VIFCodeKind.operating_time,
            VIFCodeUnit.second,
        ),
        (
            VIF(0b0010_0101),
            60,
            VIFCodeKind.operating_time,
            VIFCodeUnit.second,
        ),
        (
            VIF(0b0010_0110),
            3600,
            VIFCodeKind.operating_time,
            VIFCodeUnit.second,
        ),
        (
            VIF(0b0010_0111),
            86400,
            VIFCodeKind.operating_time,
            VIFCodeUnit.second,
        ),
        # Power (Watt)
        (VIF(0b0010_1000), 1e-3, VIFCodeKind.power, VIFCodeUnit.watt),
        (VIF(0b0010_1001), 1e-2, VIFCodeKind.power, VIFCodeUnit.watt),
        (VIF(0b0010_1010), 1e-1, VIFCodeKind.power, VIFCodeUnit.watt),
        (VIF(0b0010_1011), 1e0, VIFCodeKind.power, VIFCodeUnit.watt),
        (VIF(0b0010_1100), 1e1, VIFCodeKind.power, VIFCodeUnit.watt),
        (VIF(0b0010_1101), 1e2, VIFCodeKind.power, VIFCodeUnit.watt),
        (VIF(0b0010_1110), 1e3, VIFCodeKind.power, VIFCodeUnit.watt),
        (VIF(0b0010_1111), 1e4, VIFCodeKind.power, VIFCodeUnit.watt),
        # Power (Joule/hour)
        (
            VIF(0b0011_0000),
            1e0,
            VIFCodeKind.power,
            VIFCodeUnit.joule_per_hour,
        ),
        (
            VIF(0b0011_0001),
            1e1,
            VIFCodeKind.power,
            VIFCodeUnit.joule_per_hour,
        ),
        (
            VIF(0b0011_0010),
            1e2,
            VIFCodeKind.power,
            VIFCodeUnit.joule_per_hour,
        ),
        (
            VIF(0b0011_0011),
            1e3,
            VIFCodeKind.power,
            VIFCodeUnit.joule_per_hour,
        ),
        (
            VIF(0b0011_0100),
            1e4,
            VIFCodeKind.power,
            VIFCodeUnit.joule_per_hour,
        ),
        (
            VIF(0b0011_0101),
            1e5,
            VIFCodeKind.power,
            VIFCodeUnit.joule_per_hour,
        ),
        (
            VIF(0b0011_0110),
            1e6,
            VIFCodeKind.power,
            VIFCodeUnit.joule_per_hour,
        ),
        (
            VIF(0b0011_0111),
            1e7,
            VIFCodeKind.power,
            VIFCodeUnit.joule_per_hour,
        ),
        # Volume flow (m^3/hour)
        (
            VIF(0b0011_1000),
            1e-6,
            VIFCodeKind.volume_flow,
            VIFCodeUnit.meter_cubic_per_hour,
        ),
        (
            VIF(0b0011_1001),
            1e-5,
            VIFCodeKind.volume_flow,
            VIFCodeUnit.meter_cubic_per_hour,
        ),
        (
            VIF(0b0011_1010),
            1e-4,
            VIFCodeKind.volume_flow,
            VIFCodeUnit.meter_cubic_per_hour,
        ),
        (
            VIF(0b0011_1011),
            1e-3,
            VIFCodeKind.volume_flow,
            VIFCodeUnit.meter_cubic_per_hour,
        ),
        (
            VIF(0b0011_1100),
            1e-2,
            VIFCodeKind.volume_flow,
            VIFCodeUnit.meter_cubic_per_hour,
        ),
        (
            VIF(0b0011_1101),
            1e-1,
            VIFCodeKind.volume_flow,
            VIFCodeUnit.meter_cubic_per_hour,
        ),
        (
            VIF(0b0011_1110),
            1e0,
            VIFCodeKind.volume_flow,
            VIFCodeUnit.meter_cubic_per_hour,
        ),
        (
            VIF(0b0011_1111),
            1e1,
            VIFCodeKind.volume_flow,
            VIFCodeUnit.meter_cubic_per_hour,
        ),
        # Volume flow (m^3/min)
        (
            VIF(0b0100_0000),
            1e-7,
            VIFCodeKind.volume_flow,
            VIFCodeUnit.meter_cubic_per_minute,
        ),
        (
            VIF(0b0100_0001),
            1e-6,
            VIFCodeKind.volume_flow,
            VIFCodeUnit.meter_cubic_per_minute,
        ),
        (
            VIF(0b0100_0010),
            1e-5,
            VIFCodeKind.volume_flow,
            VIFCodeUnit.meter_cubic_per_minute,
        ),
        (
            VIF(0b0100_0011),
            1e-4,
            VIFCodeKind.volume_flow,
            VIFCodeUnit.meter_cubic_per_minute,
        ),
        (
            VIF(0b0100_0100),
            1e-3,
            VIFCodeKind.volume_flow,
            VIFCodeUnit.meter_cubic_per_minute,
        ),
        (
            VIF(0b0100_0101),
            1e-2,
            VIFCodeKind.volume_flow,
            VIFCodeUnit.meter_cubic_per_minute,
        ),
        (
            VIF(0b0100_0110),
            1e-1,
            VIFCodeKind.volume_flow,
            VIFCodeUnit.meter_cubic_per_minute,
        ),
        (
            VIF(0b0100_0111),
            1e0,
            VIFCodeKind.volume_flow,
            VIFCodeUnit.meter_cubic_per_minute,
        ),
        # Volume flow (m^3/min)
        (
            VIF(0b0100_1000),
            1e-9,
            VIFCodeKind.volume_flow,
            VIFCodeUnit.meter_cubic_per_second,
        ),
        (
            VIF(0b0100_1001),
            1e-8,
            VIFCodeKind.volume_flow,
            VIFCodeUnit.meter_cubic_per_second,
        ),
        (
            VIF(0b0100_1010),
            1e-7,
            VIFCodeKind.volume_flow,
            VIFCodeUnit.meter_cubic_per_second,
        ),
        (
            VIF(0b0100_1011),
            1e-6,
            VIFCodeKind.volume_flow,
            VIFCodeUnit.meter_cubic_per_second,
        ),
        (
            VIF(0b0100_1100),
            1e-5,
            VIFCodeKind.volume_flow,
            VIFCodeUnit.meter_cubic_per_second,
        ),
        (
            VIF(0b0100_1101),
            1e-4,
            VIFCodeKind.volume_flow,
            VIFCodeUnit.meter_cubic_per_second,
        ),
        (
            VIF(0b0100_1110),
            1e-3,
            VIFCodeKind.volume_flow,
            VIFCodeUnit.meter_cubic_per_second,
        ),
        (
            VIF(0b0100_1111),
            1e-2,
            VIFCodeKind.volume_flow,
            VIFCodeUnit.meter_cubic_per_second,
        ),
        # Mass flow (kg/h)
        (
            VIF(0b0101_0000),
            1e-3,
            VIFCodeKind.mass_flow,
            VIFCodeUnit.kilogram_per_hour,
        ),
        (
            VIF(0b0101_0001),
            1e-2,
            VIFCodeKind.mass_flow,
            VIFCodeUnit.kilogram_per_hour,
        ),
        (
            VIF(0b0101_0010),
            1e-1,
            VIFCodeKind.mass_flow,
            VIFCodeUnit.kilogram_per_hour,
        ),
        (
            VIF(0b0101_0011),
            1e0,
            VIFCodeKind.mass_flow,
            VIFCodeUnit.kilogram_per_hour,
        ),
        (
            VIF(0b0101_0100),
            1e1,
            VIFCodeKind.mass_flow,
            VIFCodeUnit.kilogram_per_hour,
        ),
        (
            VIF(0b0101_0101),
            1e2,
            VIFCodeKind.mass_flow,
            VIFCodeUnit.kilogram_per_hour,
        ),
        (
            VIF(0b0101_0110),
            1e3,
            VIFCodeKind.mass_flow,
            VIFCodeUnit.kilogram_per_hour,
        ),
        (
            VIF(0b0101_0111),
            1e4,
            VIFCodeKind.mass_flow,
            VIFCodeUnit.kilogram_per_hour,
        ),
        # Flow Temperature (C)
        (
            VIF(0b0101_1000),
            1e-3,
            VIFCodeKind.flow_temperature,
            VIFCodeUnit.celsius,
        ),
        (
            VIF(0b0101_1001),
            1e-2,
            VIFCodeKind.flow_temperature,
            VIFCodeUnit.celsius,
        ),
        (
            VIF(0b0101_1010),
            1e-1,
            VIFCodeKind.flow_temperature,
            VIFCodeUnit.celsius,
        ),
        (
            VIF(0b0101_1011),
            1e0,
            VIFCodeKind.flow_temperature,
            VIFCodeUnit.celsius,
        ),
        # Return Temperature (C)
        (
            VIF(0b0101_1100),
            1e-3,
            VIFCodeKind.return_temperature,
            VIFCodeUnit.celsius,
        ),
        (
            VIF(0b0101_1101),
            1e-2,
            VIFCodeKind.return_temperature,
            VIFCodeUnit.celsius,
        ),
        (
            VIF(0b0101_1110),
            1e-1,
            VIFCodeKind.return_temperature,
            VIFCodeUnit.celsius,
        ),
        (
            VIF(0b0101_1111),
            1e0,
            VIFCodeKind.return_temperature,
            VIFCodeUnit.celsius,
        ),
        # Temperature Difference (K)
        (
            VIF(0b0110_0000),
            1e-3,
            VIFCodeKind.temperature_difference,
            VIFCodeUnit.kelvin,
        ),
        (
            VIF(0b0110_0001),
            1e-2,
            VIFCodeKind.temperature_difference,
            VIFCodeUnit.kelvin,
        ),
        (
            VIF(0b0110_0010),
            1e-1,
            VIFCodeKind.temperature_difference,
            VIFCodeUnit.kelvin,
        ),
        (
            VIF(0b0110_0011),
            1e-0,
            VIFCodeKind.temperature_difference,
            VIFCodeUnit.kelvin,
        ),
        # External Temperature (C)
        (
            VIF(0b0110_0100),
            1e-3,
            VIFCodeKind.external_temperature,
            VIFCodeUnit.celsius,
        ),
        (
            VIF(0b0110_0101),
            1e-2,
            VIFCodeKind.external_temperature,
            VIFCodeUnit.celsius,
        ),
        (
            VIF(0b0110_0110),
            1e-1,
            VIFCodeKind.external_temperature,
            VIFCodeUnit.celsius,
        ),
        (
            VIF(0b0110_0111),
            1e-0,
            VIFCodeKind.external_temperature,
            VIFCodeUnit.celsius,
        ),
        # Pressure (bar)
        (VIF(0b0110_1000), 1e-3, VIFCodeKind.pressure, VIFCodeUnit.bar),
        (VIF(0b0110_1001), 1e-2, VIFCodeKind.pressure, VIFCodeUnit.bar),
        (VIF(0b0110_1010), 1e-1, VIFCodeKind.pressure, VIFCodeUnit.bar),
        (VIF(0b0110_1011), 1e0, VIFCodeKind.pressure, VIFCodeUnit.bar),
        # TIme Point
        (VIF(0b0110_1100), 1, VIFCodeKind.time_point, VIFCodeUnit.date),
        (
            VIF(0b0110_1101),
            1,
            VIFCodeKind.time_point,
            VIFCodeUnit.datetime,
        ),
        # H.C.A. = Heat Cost Allocator
        (VIF(0b0110_1110), 1, VIFCodeKind.hca, VIFCodeUnit.hca),
        # Reserved
        (VIF(0b0110_1111), 1, VIFCodeKind.reserved, VIFCodeUnit.unknown),
        # Averaging duration (in seconds)
        (
            VIF(0b0111_0000),
            1,
            VIFCodeKind.averaging_duration,
            VIFCodeUnit.second,
        ),
        (
            VIF(0b0111_0001),
            60,
            VIFCodeKind.averaging_duration,
            VIFCodeUnit.second,
        ),
        (
            VIF(0b0111_0010),
            3600,
            VIFCodeKind.averaging_duration,
            VIFCodeUnit.second,
        ),
        (
            VIF(0b0111_0011),
            86400,
            VIFCodeKind.averaging_duration,
            VIFCodeUnit.second,
        ),
        # Actuality duration (in seconds)
        (
            VIF(0b0111_0100),
            1,
            VIFCodeKind.actuality_duration,
            VIFCodeUnit.second,
        ),
        (
            VIF(0b0111_0101),
            60,
            VIFCodeKind.actuality_duration,
            VIFCodeUnit.second,
        ),
        (
            VIF(0b0111_0110),
            3600,
            VIFCodeKind.actuality_duration,
            VIFCodeUnit.second,
        ),
        (
            VIF(0b0111_0111),
            86400,
            VIFCodeKind.actuality_duration,
            VIFCodeUnit.second,
        ),
        # Fabrication No
        (
            VIF(0b0111_1000),
            1,
            VIFCodeKind.fabrication_no,
            VIFCodeUnit.unknown,
        ),
        # Enhanced
        (VIF(0b0111_1001), 1, VIFCodeKind.enhanced, VIFCodeUnit.unknown),
        # Bus address
        (
            VIF(0b0111_1010),
            1,
            VIFCodeKind.bus_address,
            VIFCodeUnit.unknown,
        ),
        # special purpose
        (VIF(0b0111_1100), 1, VIFCodeKind.user, VIFCodeUnit.unknown),
        (VIF(0b0111_1110), 1, VIFCodeKind.any, VIFCodeUnit.unknown),
        (
            VIF(0b0111_1111),
            1,
            VIFCodeKind.manufacturer,
            VIFCodeUnit.unknown,
        ),
    ],
)
def test_vif_codes(vif: VIF, coef: float, kind: VIFCodeKind, unit: VIFCodeUnit):
    table = VIFTablet()
    assert table(vif) == VIFCode(
        coef=coef,
        kind=kind,
        unit=unit,
    )


@pytest.mark.parametrize(
    ("code", "answer"),
    [
        (
            0b0000_0000,
            VIFCode(
                coef=1e-3, kind=VIFCodeKind.energy, unit=VIFCodeUnit.watt_hour
            ),
        ),
        (
            0b0010_0110,
            VIFCode(
                coef=3600,
                kind=VIFCodeKind.operating_time,
                unit=VIFCodeUnit.second,
            ),
        ),
        (
            0b0111_1000,
            VIFCode(
                coef=1,
                kind=VIFCodeKind.fabrication_no,
                unit=VIFCodeUnit.unknown,
            ),
        ),
    ],
)
def test_vif_code_with_extensions(code: int, answer: VIF):
    table = VIFTablet()

    assert table(code) == answer
    assert table(0x80 | code) == answer
