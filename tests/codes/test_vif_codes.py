import pytest

from pymbus.codes.vif import (
    VIFCode,
    VIFCodeCategory,
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
    ("vif", "coef", "desc", "unit"),
    [
        # Energy (Watt * hour)
        (
            VIF(0b0000_0000),
            1e-3,
            VIFCodeCategory.energy,
            VIFCodeUnit.watt_hour,
        ),
        (
            VIF(0b0000_0001),
            1e-2,
            VIFCodeCategory.energy,
            VIFCodeUnit.watt_hour,
        ),
        (
            VIF(0b0000_0010),
            1e-1,
            VIFCodeCategory.energy,
            VIFCodeUnit.watt_hour,
        ),
        (
            VIF(0b0000_0011),
            1e0,
            VIFCodeCategory.energy,
            VIFCodeUnit.watt_hour,
        ),
        (
            VIF(0b0000_0100),
            1e1,
            VIFCodeCategory.energy,
            VIFCodeUnit.watt_hour,
        ),
        (
            VIF(0b0000_0101),
            1e2,
            VIFCodeCategory.energy,
            VIFCodeUnit.watt_hour,
        ),
        (
            VIF(0b0000_0110),
            1e3,
            VIFCodeCategory.energy,
            VIFCodeUnit.watt_hour,
        ),
        (
            VIF(0b0000_0111),
            1e4,
            VIFCodeCategory.energy,
            VIFCodeUnit.watt_hour,
        ),
        # Energy (Joule)
        (VIF(0b0000_1000), 1e0, VIFCodeCategory.energy, VIFCodeUnit.joule),
        (VIF(0b0000_1001), 1e1, VIFCodeCategory.energy, VIFCodeUnit.joule),
        (VIF(0b0000_1010), 1e2, VIFCodeCategory.energy, VIFCodeUnit.joule),
        (VIF(0b0000_1011), 1e3, VIFCodeCategory.energy, VIFCodeUnit.joule),
        (VIF(0b0000_1100), 1e4, VIFCodeCategory.energy, VIFCodeUnit.joule),
        (VIF(0b0000_1101), 1e5, VIFCodeCategory.energy, VIFCodeUnit.joule),
        (VIF(0b0000_1110), 1e6, VIFCodeCategory.energy, VIFCodeUnit.joule),
        (VIF(0b0000_1111), 1e7, VIFCodeCategory.energy, VIFCodeUnit.joule),
        # Volume (Meter cubic)
        (
            VIF(0b0001_0000),
            1e-6,
            VIFCodeCategory.volume,
            VIFCodeUnit.meter_cubic,
        ),
        (
            VIF(0b0001_0001),
            1e-5,
            VIFCodeCategory.volume,
            VIFCodeUnit.meter_cubic,
        ),
        (
            VIF(0b0001_0010),
            1e-4,
            VIFCodeCategory.volume,
            VIFCodeUnit.meter_cubic,
        ),
        (
            VIF(0b0001_0011),
            1e-3,
            VIFCodeCategory.volume,
            VIFCodeUnit.meter_cubic,
        ),
        (
            VIF(0b0001_0100),
            1e-2,
            VIFCodeCategory.volume,
            VIFCodeUnit.meter_cubic,
        ),
        (
            VIF(0b0001_0101),
            1e-1,
            VIFCodeCategory.volume,
            VIFCodeUnit.meter_cubic,
        ),
        (
            VIF(0b0001_0110),
            1e0,
            VIFCodeCategory.volume,
            VIFCodeUnit.meter_cubic,
        ),
        (
            VIF(0b0001_0111),
            1e1,
            VIFCodeCategory.volume,
            VIFCodeUnit.meter_cubic,
        ),
        # Mass (Kilogram)
        (VIF(0b0001_1000), 1e-3, VIFCodeCategory.mass, VIFCodeUnit.kilogram),
        (VIF(0b0001_1001), 1e-2, VIFCodeCategory.mass, VIFCodeUnit.kilogram),
        (VIF(0b0001_1010), 1e-1, VIFCodeCategory.mass, VIFCodeUnit.kilogram),
        (VIF(0b0001_1011), 1e0, VIFCodeCategory.mass, VIFCodeUnit.kilogram),
        (VIF(0b0001_1100), 1e1, VIFCodeCategory.mass, VIFCodeUnit.kilogram),
        (VIF(0b0001_1101), 1e2, VIFCodeCategory.mass, VIFCodeUnit.kilogram),
        (VIF(0b0001_1110), 1e3, VIFCodeCategory.mass, VIFCodeUnit.kilogram),
        (VIF(0b0001_1111), 1e4, VIFCodeCategory.mass, VIFCodeUnit.kilogram),
        # On Time (time parts -> days, hours, minutes, seconds)
        (VIF(0b0010_0000), 1, VIFCodeCategory.on_time, VIFCodeUnit.second),
        (VIF(0b0010_0001), 60, VIFCodeCategory.on_time, VIFCodeUnit.second),
        (
            VIF(0b0010_0010),
            3600,
            VIFCodeCategory.on_time,
            VIFCodeUnit.second,
        ),
        (
            VIF(0b0010_0011),
            86400,
            VIFCodeCategory.on_time,
            VIFCodeUnit.second,
        ),
        # Operating Time (like On Time)
        (
            VIF(0b0010_0100),
            1,
            VIFCodeCategory.operating_time,
            VIFCodeUnit.second,
        ),
        (
            VIF(0b0010_0101),
            60,
            VIFCodeCategory.operating_time,
            VIFCodeUnit.second,
        ),
        (
            VIF(0b0010_0110),
            3600,
            VIFCodeCategory.operating_time,
            VIFCodeUnit.second,
        ),
        (
            VIF(0b0010_0111),
            86400,
            VIFCodeCategory.operating_time,
            VIFCodeUnit.second,
        ),
        # Power (Watt)
        (VIF(0b0010_1000), 1e-3, VIFCodeCategory.power, VIFCodeUnit.watt),
        (VIF(0b0010_1001), 1e-2, VIFCodeCategory.power, VIFCodeUnit.watt),
        (VIF(0b0010_1010), 1e-1, VIFCodeCategory.power, VIFCodeUnit.watt),
        (VIF(0b0010_1011), 1e0, VIFCodeCategory.power, VIFCodeUnit.watt),
        (VIF(0b0010_1100), 1e1, VIFCodeCategory.power, VIFCodeUnit.watt),
        (VIF(0b0010_1101), 1e2, VIFCodeCategory.power, VIFCodeUnit.watt),
        (VIF(0b0010_1110), 1e3, VIFCodeCategory.power, VIFCodeUnit.watt),
        (VIF(0b0010_1111), 1e4, VIFCodeCategory.power, VIFCodeUnit.watt),
        # Power (Joule/hour)
        (
            VIF(0b0011_0000),
            1e0,
            VIFCodeCategory.power,
            VIFCodeUnit.joule_per_hour,
        ),
        (
            VIF(0b0011_0001),
            1e1,
            VIFCodeCategory.power,
            VIFCodeUnit.joule_per_hour,
        ),
        (
            VIF(0b0011_0010),
            1e2,
            VIFCodeCategory.power,
            VIFCodeUnit.joule_per_hour,
        ),
        (
            VIF(0b0011_0011),
            1e3,
            VIFCodeCategory.power,
            VIFCodeUnit.joule_per_hour,
        ),
        (
            VIF(0b0011_0100),
            1e4,
            VIFCodeCategory.power,
            VIFCodeUnit.joule_per_hour,
        ),
        (
            VIF(0b0011_0101),
            1e5,
            VIFCodeCategory.power,
            VIFCodeUnit.joule_per_hour,
        ),
        (
            VIF(0b0011_0110),
            1e6,
            VIFCodeCategory.power,
            VIFCodeUnit.joule_per_hour,
        ),
        (
            VIF(0b0011_0111),
            1e7,
            VIFCodeCategory.power,
            VIFCodeUnit.joule_per_hour,
        ),
        # Volume flow (m^3/hour)
        (
            VIF(0b0011_1000),
            1e-6,
            VIFCodeCategory.volume_flow,
            VIFCodeUnit.meter_cubic_per_hour,
        ),
        (
            VIF(0b0011_1001),
            1e-5,
            VIFCodeCategory.volume_flow,
            VIFCodeUnit.meter_cubic_per_hour,
        ),
        (
            VIF(0b0011_1010),
            1e-4,
            VIFCodeCategory.volume_flow,
            VIFCodeUnit.meter_cubic_per_hour,
        ),
        (
            VIF(0b0011_1011),
            1e-3,
            VIFCodeCategory.volume_flow,
            VIFCodeUnit.meter_cubic_per_hour,
        ),
        (
            VIF(0b0011_1100),
            1e-2,
            VIFCodeCategory.volume_flow,
            VIFCodeUnit.meter_cubic_per_hour,
        ),
        (
            VIF(0b0011_1101),
            1e-1,
            VIFCodeCategory.volume_flow,
            VIFCodeUnit.meter_cubic_per_hour,
        ),
        (
            VIF(0b0011_1110),
            1e0,
            VIFCodeCategory.volume_flow,
            VIFCodeUnit.meter_cubic_per_hour,
        ),
        (
            VIF(0b0011_1111),
            1e1,
            VIFCodeCategory.volume_flow,
            VIFCodeUnit.meter_cubic_per_hour,
        ),
        # Volume flow (m^3/min)
        (
            VIF(0b0100_0000),
            1e-7,
            VIFCodeCategory.volume_flow,
            VIFCodeUnit.meter_cubic_per_minute,
        ),
        (
            VIF(0b0100_0001),
            1e-6,
            VIFCodeCategory.volume_flow,
            VIFCodeUnit.meter_cubic_per_minute,
        ),
        (
            VIF(0b0100_0010),
            1e-5,
            VIFCodeCategory.volume_flow,
            VIFCodeUnit.meter_cubic_per_minute,
        ),
        (
            VIF(0b0100_0011),
            1e-4,
            VIFCodeCategory.volume_flow,
            VIFCodeUnit.meter_cubic_per_minute,
        ),
        (
            VIF(0b0100_0100),
            1e-3,
            VIFCodeCategory.volume_flow,
            VIFCodeUnit.meter_cubic_per_minute,
        ),
        (
            VIF(0b0100_0101),
            1e-2,
            VIFCodeCategory.volume_flow,
            VIFCodeUnit.meter_cubic_per_minute,
        ),
        (
            VIF(0b0100_0110),
            1e-1,
            VIFCodeCategory.volume_flow,
            VIFCodeUnit.meter_cubic_per_minute,
        ),
        (
            VIF(0b0100_0111),
            1e0,
            VIFCodeCategory.volume_flow,
            VIFCodeUnit.meter_cubic_per_minute,
        ),
        # Volume flow (m^3/min)
        (
            VIF(0b0100_1000),
            1e-9,
            VIFCodeCategory.volume_flow,
            VIFCodeUnit.meter_cubic_per_second,
        ),
        (
            VIF(0b0100_1001),
            1e-8,
            VIFCodeCategory.volume_flow,
            VIFCodeUnit.meter_cubic_per_second,
        ),
        (
            VIF(0b0100_1010),
            1e-7,
            VIFCodeCategory.volume_flow,
            VIFCodeUnit.meter_cubic_per_second,
        ),
        (
            VIF(0b0100_1011),
            1e-6,
            VIFCodeCategory.volume_flow,
            VIFCodeUnit.meter_cubic_per_second,
        ),
        (
            VIF(0b0100_1100),
            1e-5,
            VIFCodeCategory.volume_flow,
            VIFCodeUnit.meter_cubic_per_second,
        ),
        (
            VIF(0b0100_1101),
            1e-4,
            VIFCodeCategory.volume_flow,
            VIFCodeUnit.meter_cubic_per_second,
        ),
        (
            VIF(0b0100_1110),
            1e-3,
            VIFCodeCategory.volume_flow,
            VIFCodeUnit.meter_cubic_per_second,
        ),
        (
            VIF(0b0100_1111),
            1e-2,
            VIFCodeCategory.volume_flow,
            VIFCodeUnit.meter_cubic_per_second,
        ),
        # Mass flow (kg/h)
        (
            VIF(0b0101_0000),
            1e-3,
            VIFCodeCategory.mass_flow,
            VIFCodeUnit.kilogram_per_hour,
        ),
        (
            VIF(0b0101_0001),
            1e-2,
            VIFCodeCategory.mass_flow,
            VIFCodeUnit.kilogram_per_hour,
        ),
        (
            VIF(0b0101_0010),
            1e-1,
            VIFCodeCategory.mass_flow,
            VIFCodeUnit.kilogram_per_hour,
        ),
        (
            VIF(0b0101_0011),
            1e0,
            VIFCodeCategory.mass_flow,
            VIFCodeUnit.kilogram_per_hour,
        ),
        (
            VIF(0b0101_0100),
            1e1,
            VIFCodeCategory.mass_flow,
            VIFCodeUnit.kilogram_per_hour,
        ),
        (
            VIF(0b0101_0101),
            1e2,
            VIFCodeCategory.mass_flow,
            VIFCodeUnit.kilogram_per_hour,
        ),
        (
            VIF(0b0101_0110),
            1e3,
            VIFCodeCategory.mass_flow,
            VIFCodeUnit.kilogram_per_hour,
        ),
        (
            VIF(0b0101_0111),
            1e4,
            VIFCodeCategory.mass_flow,
            VIFCodeUnit.kilogram_per_hour,
        ),
        # Flow Temperature (C)
        (
            VIF(0b0101_1000),
            1e-3,
            VIFCodeCategory.flow_temperature,
            VIFCodeUnit.celsius,
        ),
        (
            VIF(0b0101_1001),
            1e-2,
            VIFCodeCategory.flow_temperature,
            VIFCodeUnit.celsius,
        ),
        (
            VIF(0b0101_1010),
            1e-1,
            VIFCodeCategory.flow_temperature,
            VIFCodeUnit.celsius,
        ),
        (
            VIF(0b0101_1011),
            1e0,
            VIFCodeCategory.flow_temperature,
            VIFCodeUnit.celsius,
        ),
        # Return Temperature (C)
        (
            VIF(0b0101_1100),
            1e-3,
            VIFCodeCategory.return_temperature,
            VIFCodeUnit.celsius,
        ),
        (
            VIF(0b0101_1101),
            1e-2,
            VIFCodeCategory.return_temperature,
            VIFCodeUnit.celsius,
        ),
        (
            VIF(0b0101_1110),
            1e-1,
            VIFCodeCategory.return_temperature,
            VIFCodeUnit.celsius,
        ),
        (
            VIF(0b0101_1111),
            1e0,
            VIFCodeCategory.return_temperature,
            VIFCodeUnit.celsius,
        ),
        # Temperature Difference (K)
        (
            VIF(0b0110_0000),
            1e-3,
            VIFCodeCategory.temperature_difference,
            VIFCodeUnit.kelvin,
        ),
        (
            VIF(0b0110_0001),
            1e-2,
            VIFCodeCategory.temperature_difference,
            VIFCodeUnit.kelvin,
        ),
        (
            VIF(0b0110_0010),
            1e-1,
            VIFCodeCategory.temperature_difference,
            VIFCodeUnit.kelvin,
        ),
        (
            VIF(0b0110_0011),
            1e-0,
            VIFCodeCategory.temperature_difference,
            VIFCodeUnit.kelvin,
        ),
        # External Temperature (C)
        (
            VIF(0b0110_0100),
            1e-3,
            VIFCodeCategory.external_temperature,
            VIFCodeUnit.celsius,
        ),
        (
            VIF(0b0110_0101),
            1e-2,
            VIFCodeCategory.external_temperature,
            VIFCodeUnit.celsius,
        ),
        (
            VIF(0b0110_0110),
            1e-1,
            VIFCodeCategory.external_temperature,
            VIFCodeUnit.celsius,
        ),
        (
            VIF(0b0110_0111),
            1e-0,
            VIFCodeCategory.external_temperature,
            VIFCodeUnit.celsius,
        ),
        # Pressure (bar)
        (VIF(0b0110_1000), 1e-3, VIFCodeCategory.pressure, VIFCodeUnit.bar),
        (VIF(0b0110_1001), 1e-2, VIFCodeCategory.pressure, VIFCodeUnit.bar),
        (VIF(0b0110_1010), 1e-1, VIFCodeCategory.pressure, VIFCodeUnit.bar),
        (VIF(0b0110_1011), 1e0, VIFCodeCategory.pressure, VIFCodeUnit.bar),
        # TIme Point
        (VIF(0b0110_1100), 1, VIFCodeCategory.time_point, VIFCodeUnit.date),
        (
            VIF(0b0110_1101),
            1,
            VIFCodeCategory.time_point,
            VIFCodeUnit.datetime,
        ),
        # H.C.A. = Heat Cost Allocator
        (VIF(0b0110_1110), 1, VIFCodeCategory.hca, VIFCodeUnit.hca),
        # Reserved
        (VIF(0b0110_1111), 1, VIFCodeCategory.reserved, VIFCodeUnit.unknown),
        # Averaging duration (in seconds)
        (
            VIF(0b0111_0000),
            1,
            VIFCodeCategory.averaging_duration,
            VIFCodeUnit.second,
        ),
        (
            VIF(0b0111_0001),
            60,
            VIFCodeCategory.averaging_duration,
            VIFCodeUnit.second,
        ),
        (
            VIF(0b0111_0010),
            3600,
            VIFCodeCategory.averaging_duration,
            VIFCodeUnit.second,
        ),
        (
            VIF(0b0111_0011),
            86400,
            VIFCodeCategory.averaging_duration,
            VIFCodeUnit.second,
        ),
        # Actuality duration (in seconds)
        (
            VIF(0b0111_0100),
            1,
            VIFCodeCategory.actuality_duration,
            VIFCodeUnit.second,
        ),
        (
            VIF(0b0111_0101),
            60,
            VIFCodeCategory.actuality_duration,
            VIFCodeUnit.second,
        ),
        (
            VIF(0b0111_0110),
            3600,
            VIFCodeCategory.actuality_duration,
            VIFCodeUnit.second,
        ),
        (
            VIF(0b0111_0111),
            86400,
            VIFCodeCategory.actuality_duration,
            VIFCodeUnit.second,
        ),
        # Fabrication No
        (
            VIF(0b0111_1000),
            1,
            VIFCodeCategory.fabrication_no,
            VIFCodeUnit.unknown,
        ),
        # Enhanced
        (VIF(0b0111_1001), 1, VIFCodeCategory.enhanced, VIFCodeUnit.unknown),
        # Bus address
        (
            VIF(0b0111_1010),
            1,
            VIFCodeCategory.bus_address,
            VIFCodeUnit.unknown,
        ),
        # special purpose
        (VIF(0b0111_1100), 1, VIFCodeCategory.user, VIFCodeUnit.unknown),
        (VIF(0b0111_1110), 1, VIFCodeCategory.any, VIFCodeUnit.unknown),
        (
            VIF(0b0111_1111),
            1,
            VIFCodeCategory.manufacturer,
            VIFCodeUnit.unknown,
        ),
        (
            VIF(0b1111_1011),
            1,
            VIFCodeCategory.extension,
            VIFCodeUnit.unknown,
        ),
        (
            VIF(0b1111_1101),
            1,
            VIFCodeCategory.extension,
            VIFCodeUnit.unknown,
        ),
    ],
)
def test_vif_codes(
    vif: VIF, coef: float, desc: VIFCodeCategory, unit: VIFCodeUnit
):
    table = VIFTablet()
    assert table(vif) == VIFCode(
        coef=coef,
        desc=desc,
        unit=unit,
    )
