import pytest

from pymbus.codes.vif import (
    VIFCode,
    VIFCodeDescription,
    VIFCodeUnit,
    get_vif_code,
)
from pymbus.exceptions import MBusValidationError
from pymbus.telegrams.fields import ValueInformationField as VIF


def test_bad_nonbyte_value():
    with pytest.raises(MBusValidationError):
        get_vif_code(266)


def test_no_vif_code():
    assert get_vif_code(VIF(0b0111_1011)) is None


@pytest.mark.parametrize(
    ("vif", "coef", "desc", "unit"),
    [
        # Energy (Watt * hour)
        (
            VIF(0b0000_0000),
            1e-3,
            VIFCodeDescription.energy,
            VIFCodeUnit.watt_hour,
        ),
        (
            VIF(0b0000_0001),
            1e-2,
            VIFCodeDescription.energy,
            VIFCodeUnit.watt_hour,
        ),
        (
            VIF(0b0000_0010),
            1e-1,
            VIFCodeDescription.energy,
            VIFCodeUnit.watt_hour,
        ),
        (
            VIF(0b0000_0011),
            1e0,
            VIFCodeDescription.energy,
            VIFCodeUnit.watt_hour,
        ),
        (
            VIF(0b0000_0100),
            1e1,
            VIFCodeDescription.energy,
            VIFCodeUnit.watt_hour,
        ),
        (
            VIF(0b0000_0101),
            1e2,
            VIFCodeDescription.energy,
            VIFCodeUnit.watt_hour,
        ),
        (
            VIF(0b0000_0110),
            1e3,
            VIFCodeDescription.energy,
            VIFCodeUnit.watt_hour,
        ),
        (
            VIF(0b0000_0111),
            1e4,
            VIFCodeDescription.energy,
            VIFCodeUnit.watt_hour,
        ),
        # Energy (Joule)
        (VIF(0b0000_1000), 1e0, VIFCodeDescription.energy, VIFCodeUnit.joule),
        (VIF(0b0000_1001), 1e1, VIFCodeDescription.energy, VIFCodeUnit.joule),
        (VIF(0b0000_1010), 1e2, VIFCodeDescription.energy, VIFCodeUnit.joule),
        (VIF(0b0000_1011), 1e3, VIFCodeDescription.energy, VIFCodeUnit.joule),
        (VIF(0b0000_1100), 1e4, VIFCodeDescription.energy, VIFCodeUnit.joule),
        (VIF(0b0000_1101), 1e5, VIFCodeDescription.energy, VIFCodeUnit.joule),
        (VIF(0b0000_1110), 1e6, VIFCodeDescription.energy, VIFCodeUnit.joule),
        (VIF(0b0000_1111), 1e7, VIFCodeDescription.energy, VIFCodeUnit.joule),
        # Volume (Meter cubic)
        (
            VIF(0b0001_0000),
            1e-6,
            VIFCodeDescription.volume,
            VIFCodeUnit.meter_cubic,
        ),
        (
            VIF(0b0001_0001),
            1e-5,
            VIFCodeDescription.volume,
            VIFCodeUnit.meter_cubic,
        ),
        (
            VIF(0b0001_0010),
            1e-4,
            VIFCodeDescription.volume,
            VIFCodeUnit.meter_cubic,
        ),
        (
            VIF(0b0001_0011),
            1e-3,
            VIFCodeDescription.volume,
            VIFCodeUnit.meter_cubic,
        ),
        (
            VIF(0b0001_0100),
            1e-2,
            VIFCodeDescription.volume,
            VIFCodeUnit.meter_cubic,
        ),
        (
            VIF(0b0001_0101),
            1e-1,
            VIFCodeDescription.volume,
            VIFCodeUnit.meter_cubic,
        ),
        (
            VIF(0b0001_0110),
            1e0,
            VIFCodeDescription.volume,
            VIFCodeUnit.meter_cubic,
        ),
        (
            VIF(0b0001_0111),
            1e1,
            VIFCodeDescription.volume,
            VIFCodeUnit.meter_cubic,
        ),
        # Mass (Kilogram)
        (VIF(0b0001_1000), 1e-3, VIFCodeDescription.mass, VIFCodeUnit.kilogram),
        (VIF(0b0001_1001), 1e-2, VIFCodeDescription.mass, VIFCodeUnit.kilogram),
        (VIF(0b0001_1010), 1e-1, VIFCodeDescription.mass, VIFCodeUnit.kilogram),
        (VIF(0b0001_1011), 1e0, VIFCodeDescription.mass, VIFCodeUnit.kilogram),
        (VIF(0b0001_1100), 1e1, VIFCodeDescription.mass, VIFCodeUnit.kilogram),
        (VIF(0b0001_1101), 1e2, VIFCodeDescription.mass, VIFCodeUnit.kilogram),
        (VIF(0b0001_1110), 1e3, VIFCodeDescription.mass, VIFCodeUnit.kilogram),
        (VIF(0b0001_1111), 1e4, VIFCodeDescription.mass, VIFCodeUnit.kilogram),
        # On Time (time parts -> days, hours, minutes, seconds)
        (VIF(0b0010_0000), 1, VIFCodeDescription.on_time, VIFCodeUnit.second),
        (VIF(0b0010_0001), 60, VIFCodeDescription.on_time, VIFCodeUnit.second),
        (
            VIF(0b0010_0010),
            3600,
            VIFCodeDescription.on_time,
            VIFCodeUnit.second,
        ),
        (
            VIF(0b0010_0011),
            86400,
            VIFCodeDescription.on_time,
            VIFCodeUnit.second,
        ),
        # Operating Time (like On Time)
        (
            VIF(0b0010_0100),
            1,
            VIFCodeDescription.operating_time,
            VIFCodeUnit.second,
        ),
        (
            VIF(0b0010_0101),
            60,
            VIFCodeDescription.operating_time,
            VIFCodeUnit.second,
        ),
        (
            VIF(0b0010_0110),
            3600,
            VIFCodeDescription.operating_time,
            VIFCodeUnit.second,
        ),
        (
            VIF(0b0010_0111),
            86400,
            VIFCodeDescription.operating_time,
            VIFCodeUnit.second,
        ),
        # Power (Watt)
        (VIF(0b0010_1000), 1e-3, VIFCodeDescription.power, VIFCodeUnit.watt),
        (VIF(0b0010_1001), 1e-2, VIFCodeDescription.power, VIFCodeUnit.watt),
        (VIF(0b0010_1010), 1e-1, VIFCodeDescription.power, VIFCodeUnit.watt),
        (VIF(0b0010_1011), 1e0, VIFCodeDescription.power, VIFCodeUnit.watt),
        (VIF(0b0010_1100), 1e1, VIFCodeDescription.power, VIFCodeUnit.watt),
        (VIF(0b0010_1101), 1e2, VIFCodeDescription.power, VIFCodeUnit.watt),
        (VIF(0b0010_1110), 1e3, VIFCodeDescription.power, VIFCodeUnit.watt),
        (VIF(0b0010_1111), 1e4, VIFCodeDescription.power, VIFCodeUnit.watt),
        # Power (Joule/hour)
        (
            VIF(0b0011_0000),
            1e0,
            VIFCodeDescription.power,
            VIFCodeUnit.joule_per_hour,
        ),
        (
            VIF(0b0011_0001),
            1e1,
            VIFCodeDescription.power,
            VIFCodeUnit.joule_per_hour,
        ),
        (
            VIF(0b0011_0010),
            1e2,
            VIFCodeDescription.power,
            VIFCodeUnit.joule_per_hour,
        ),
        (
            VIF(0b0011_0011),
            1e3,
            VIFCodeDescription.power,
            VIFCodeUnit.joule_per_hour,
        ),
        (
            VIF(0b0011_0100),
            1e4,
            VIFCodeDescription.power,
            VIFCodeUnit.joule_per_hour,
        ),
        (
            VIF(0b0011_0101),
            1e5,
            VIFCodeDescription.power,
            VIFCodeUnit.joule_per_hour,
        ),
        (
            VIF(0b0011_0110),
            1e6,
            VIFCodeDescription.power,
            VIFCodeUnit.joule_per_hour,
        ),
        (
            VIF(0b0011_0111),
            1e7,
            VIFCodeDescription.power,
            VIFCodeUnit.joule_per_hour,
        ),
        # Volume flow (m^3/hour)
        (
            VIF(0b0011_1000),
            1e-6,
            VIFCodeDescription.volume_flow,
            VIFCodeUnit.meter_cubic_per_hour,
        ),
        (
            VIF(0b0011_1001),
            1e-5,
            VIFCodeDescription.volume_flow,
            VIFCodeUnit.meter_cubic_per_hour,
        ),
        (
            VIF(0b0011_1010),
            1e-4,
            VIFCodeDescription.volume_flow,
            VIFCodeUnit.meter_cubic_per_hour,
        ),
        (
            VIF(0b0011_1011),
            1e-3,
            VIFCodeDescription.volume_flow,
            VIFCodeUnit.meter_cubic_per_hour,
        ),
        (
            VIF(0b0011_1100),
            1e-2,
            VIFCodeDescription.volume_flow,
            VIFCodeUnit.meter_cubic_per_hour,
        ),
        (
            VIF(0b0011_1101),
            1e-1,
            VIFCodeDescription.volume_flow,
            VIFCodeUnit.meter_cubic_per_hour,
        ),
        (
            VIF(0b0011_1110),
            1e0,
            VIFCodeDescription.volume_flow,
            VIFCodeUnit.meter_cubic_per_hour,
        ),
        (
            VIF(0b0011_1111),
            1e1,
            VIFCodeDescription.volume_flow,
            VIFCodeUnit.meter_cubic_per_hour,
        ),
        # Volume flow (m^3/min)
        (
            VIF(0b0100_0000),
            1e-7,
            VIFCodeDescription.volume_flow,
            VIFCodeUnit.meter_cubic_per_minute,
        ),
        (
            VIF(0b0100_0001),
            1e-6,
            VIFCodeDescription.volume_flow,
            VIFCodeUnit.meter_cubic_per_minute,
        ),
        (
            VIF(0b0100_0010),
            1e-5,
            VIFCodeDescription.volume_flow,
            VIFCodeUnit.meter_cubic_per_minute,
        ),
        (
            VIF(0b0100_0011),
            1e-4,
            VIFCodeDescription.volume_flow,
            VIFCodeUnit.meter_cubic_per_minute,
        ),
        (
            VIF(0b0100_0100),
            1e-3,
            VIFCodeDescription.volume_flow,
            VIFCodeUnit.meter_cubic_per_minute,
        ),
        (
            VIF(0b0100_0101),
            1e-2,
            VIFCodeDescription.volume_flow,
            VIFCodeUnit.meter_cubic_per_minute,
        ),
        (
            VIF(0b0100_0110),
            1e-1,
            VIFCodeDescription.volume_flow,
            VIFCodeUnit.meter_cubic_per_minute,
        ),
        (
            VIF(0b0100_0111),
            1e0,
            VIFCodeDescription.volume_flow,
            VIFCodeUnit.meter_cubic_per_minute,
        ),
        # Volume flow (m^3/min)
        (
            VIF(0b0100_1000),
            1e-9,
            VIFCodeDescription.volume_flow,
            VIFCodeUnit.meter_cubic_per_second,
        ),
        (
            VIF(0b0100_1001),
            1e-8,
            VIFCodeDescription.volume_flow,
            VIFCodeUnit.meter_cubic_per_second,
        ),
        (
            VIF(0b0100_1010),
            1e-7,
            VIFCodeDescription.volume_flow,
            VIFCodeUnit.meter_cubic_per_second,
        ),
        (
            VIF(0b0100_1011),
            1e-6,
            VIFCodeDescription.volume_flow,
            VIFCodeUnit.meter_cubic_per_second,
        ),
        (
            VIF(0b0100_1100),
            1e-5,
            VIFCodeDescription.volume_flow,
            VIFCodeUnit.meter_cubic_per_second,
        ),
        (
            VIF(0b0100_1101),
            1e-4,
            VIFCodeDescription.volume_flow,
            VIFCodeUnit.meter_cubic_per_second,
        ),
        (
            VIF(0b0100_1110),
            1e-3,
            VIFCodeDescription.volume_flow,
            VIFCodeUnit.meter_cubic_per_second,
        ),
        (
            VIF(0b0100_1111),
            1e-2,
            VIFCodeDescription.volume_flow,
            VIFCodeUnit.meter_cubic_per_second,
        ),
        # Mass flow (kg/h)
        (
            VIF(0b0101_0000),
            1e-3,
            VIFCodeDescription.mass_flow,
            VIFCodeUnit.kilogram_per_hour,
        ),
        (
            VIF(0b0101_0001),
            1e-2,
            VIFCodeDescription.mass_flow,
            VIFCodeUnit.kilogram_per_hour,
        ),
        (
            VIF(0b0101_0010),
            1e-1,
            VIFCodeDescription.mass_flow,
            VIFCodeUnit.kilogram_per_hour,
        ),
        (
            VIF(0b0101_0011),
            1e0,
            VIFCodeDescription.mass_flow,
            VIFCodeUnit.kilogram_per_hour,
        ),
        (
            VIF(0b0101_0100),
            1e1,
            VIFCodeDescription.mass_flow,
            VIFCodeUnit.kilogram_per_hour,
        ),
        (
            VIF(0b0101_0101),
            1e2,
            VIFCodeDescription.mass_flow,
            VIFCodeUnit.kilogram_per_hour,
        ),
        (
            VIF(0b0101_0110),
            1e3,
            VIFCodeDescription.mass_flow,
            VIFCodeUnit.kilogram_per_hour,
        ),
        (
            VIF(0b0101_0111),
            1e4,
            VIFCodeDescription.mass_flow,
            VIFCodeUnit.kilogram_per_hour,
        ),
        # Flow Temperature (C)
        (
            VIF(0b0101_1000),
            1e-3,
            VIFCodeDescription.flow_temp,
            VIFCodeUnit.celsius,
        ),
        (
            VIF(0b0101_1001),
            1e-2,
            VIFCodeDescription.flow_temp,
            VIFCodeUnit.celsius,
        ),
        (
            VIF(0b0101_1010),
            1e-1,
            VIFCodeDescription.flow_temp,
            VIFCodeUnit.celsius,
        ),
        (
            VIF(0b0101_1011),
            1e0,
            VIFCodeDescription.flow_temp,
            VIFCodeUnit.celsius,
        ),
        # Return Temperature (C)
        (
            VIF(0b0101_1100),
            1e-3,
            VIFCodeDescription.return_temp,
            VIFCodeUnit.celsius,
        ),
        (
            VIF(0b0101_1101),
            1e-2,
            VIFCodeDescription.return_temp,
            VIFCodeUnit.celsius,
        ),
        (
            VIF(0b0101_1110),
            1e-1,
            VIFCodeDescription.return_temp,
            VIFCodeUnit.celsius,
        ),
        (
            VIF(0b0101_1111),
            1e0,
            VIFCodeDescription.return_temp,
            VIFCodeUnit.celsius,
        ),
        # Temperature Difference (K)
        (
            VIF(0b0110_0000),
            1e-3,
            VIFCodeDescription.temp_difference,
            VIFCodeUnit.kelvin,
        ),
        (
            VIF(0b0110_0001),
            1e-2,
            VIFCodeDescription.temp_difference,
            VIFCodeUnit.kelvin,
        ),
        (
            VIF(0b0110_0010),
            1e-1,
            VIFCodeDescription.temp_difference,
            VIFCodeUnit.kelvin,
        ),
        (
            VIF(0b0110_0011),
            1e-0,
            VIFCodeDescription.temp_difference,
            VIFCodeUnit.kelvin,
        ),
        # External Temperature (C)
        (
            VIF(0b0110_0100),
            1e-3,
            VIFCodeDescription.external_temp,
            VIFCodeUnit.celsius,
        ),
        (
            VIF(0b0110_0101),
            1e-2,
            VIFCodeDescription.external_temp,
            VIFCodeUnit.celsius,
        ),
        (
            VIF(0b0110_0110),
            1e-1,
            VIFCodeDescription.external_temp,
            VIFCodeUnit.celsius,
        ),
        (
            VIF(0b0110_0111),
            1e-0,
            VIFCodeDescription.external_temp,
            VIFCodeUnit.celsius,
        ),
        # Pressure (bar)
        (VIF(0b0110_1000), 1e-3, VIFCodeDescription.pressure, VIFCodeUnit.bar),
        (VIF(0b0110_1001), 1e-2, VIFCodeDescription.pressure, VIFCodeUnit.bar),
        (VIF(0b0110_1010), 1e-1, VIFCodeDescription.pressure, VIFCodeUnit.bar),
        (VIF(0b0110_1011), 1e0, VIFCodeDescription.pressure, VIFCodeUnit.bar),
        # TIme Point
        (VIF(0b0110_1100), 1, VIFCodeDescription.time_point, VIFCodeUnit.date),
        (
            VIF(0b0110_1101),
            1,
            VIFCodeDescription.time_point,
            VIFCodeUnit.datetime,
        ),
        # H.C.A. = Heat Cost Allocator
        (VIF(0b0110_1110), 1, VIFCodeDescription.hca, VIFCodeUnit.hca),
        # Reserved
        (VIF(0b0110_1111), 1, VIFCodeDescription.reserved, VIFCodeUnit.unknown),
        # Averaging duration (in seconds)
        (
            VIF(0b0111_0000),
            1,
            VIFCodeDescription.averaging_duration,
            VIFCodeUnit.second,
        ),
        (
            VIF(0b0111_0001),
            60,
            VIFCodeDescription.averaging_duration,
            VIFCodeUnit.second,
        ),
        (
            VIF(0b0111_0010),
            3600,
            VIFCodeDescription.averaging_duration,
            VIFCodeUnit.second,
        ),
        (
            VIF(0b0111_0011),
            86400,
            VIFCodeDescription.averaging_duration,
            VIFCodeUnit.second,
        ),
        # Actuality duration (in seconds)
        (
            VIF(0b0111_0100),
            1,
            VIFCodeDescription.actuality_duration,
            VIFCodeUnit.second,
        ),
        (
            VIF(0b0111_0101),
            60,
            VIFCodeDescription.actuality_duration,
            VIFCodeUnit.second,
        ),
        (
            VIF(0b0111_0110),
            3600,
            VIFCodeDescription.actuality_duration,
            VIFCodeUnit.second,
        ),
        (
            VIF(0b0111_0111),
            86400,
            VIFCodeDescription.actuality_duration,
            VIFCodeUnit.second,
        ),
        # Fabrication No
        (
            VIF(0b0111_1000),
            1,
            VIFCodeDescription.fabrication_no,
            VIFCodeUnit.unknown,
        ),
        # Enhanced
        (VIF(0b0111_1001), 1, VIFCodeDescription.enhanced, VIFCodeUnit.unknown),
        # Bus address
        (
            VIF(0b0111_1010),
            1,
            VIFCodeDescription.bus_address,
            VIFCodeUnit.unknown,
        ),
        # special purpose
        (VIF(0b0111_1100), 1, VIFCodeDescription.user, VIFCodeUnit.unknown),
        (VIF(0b0111_1110), 1, VIFCodeDescription.any, VIFCodeUnit.unknown),
        (
            VIF(0b0111_1111),
            1,
            VIFCodeDescription.manufacturer,
            VIFCodeUnit.unknown,
        ),
        (
            VIF(0b1111_1011),
            1,
            VIFCodeDescription.extension,
            VIFCodeUnit.unknown,
        ),
        (
            VIF(0b1111_1101),
            1,
            VIFCodeDescription.extension,
            VIFCodeUnit.unknown,
        ),
    ],
)
def test_vif_codes(
    vif: VIF, coef: float, desc: VIFCodeDescription, unit: VIFCodeUnit
):
    assert get_vif_code(vif) == VIFCode(
        code=int(vif),
        coef=coef,
        desc=desc,
        unit=unit,
    )
