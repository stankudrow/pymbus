"""M-Bus Value Information Field Code module."""

from dataclasses import dataclass
from enum import Enum

from pymbus.telegrams.fields import ValueInformationField as VIF


class VIFCodeDescription(str, Enum):
    """VIF code description(s)."""

    no_description = ""
    energy = "energy"
    volume = "volume"
    mass = "mass"
    on_time = "on time"
    operating_time = "operating time"
    power = "power"
    volume_flow = "volume flow"
    mass_flow = "mass flow"
    flow_temp = "flow temperature"
    return_temp = "return temperature"
    temp_difference = "temperature_difference"
    external_temp = "external_temperature"
    pressure = "pressure"
    time_point = "time point"
    hca = "heat cost allocator"
    reserved = "reserved"
    averaging_duration = "averaging duration"
    actuality_duration = "actuality duration"
    fabrication_no = "fabrication no"
    enhanced = "enhanced"
    bus_address = "bus address"
    user = "user definable"
    any = "any"
    manufacturer = "manufacturer specific"
    extension = "extension"


class VIFCodeUnit(str, Enum):
    """VIF code unit(s)."""

    unknown = "unknown"
    watt_hour = "Wh"
    joule = "J"
    meter_cubic = "m^3"
    kilogram = "kg"
    second = "s"
    watt = "W"
    joule_per_hour = "J/h"
    meter_cubic_per_hour = "m^3/h"
    meter_cubic_per_minute = "m^3/min"
    meter_cubic_per_second = "m^3/s"
    kilogram_per_hour = "kg/h"
    celsius = "C"
    kelvin = "K"
    bar = "bar"
    hca = "H.C.A. Units"
    date = "date"  # for a time point
    datetime = "datetime"  # for a time point


@dataclass
class VIFCode:
    """Value Information Code."""

    code: int
    coef: int | float = 1
    desc: str | VIFCodeDescription = VIFCodeDescription.no_description
    unit: str | VIFCodeUnit = VIFCodeUnit.unknown


_VIF_CODE_MAP: dict[int, VIFCode] = {
    # E000_0nnn - Energy (Watt * hour = Wh)
    0b0000_0000: VIFCode(
        code=0x00,
        coef=1e-3,
        desc=VIFCodeDescription.energy,
        unit=VIFCodeUnit.watt_hour,
    ),
    0b0000_0001: VIFCode(
        code=0x01,
        coef=1e-2,
        desc=VIFCodeDescription.energy,
        unit=VIFCodeUnit.watt_hour,
    ),
    0b0000_0010: VIFCode(
        code=0x02,
        coef=1e-1,
        desc=VIFCodeDescription.energy,
        unit=VIFCodeUnit.watt_hour,
    ),
    0b0000_0011: VIFCode(
        code=0x03,
        coef=1e0,
        desc=VIFCodeDescription.energy,
        unit=VIFCodeUnit.watt_hour,
    ),
    0b0000_0100: VIFCode(
        code=0x04,
        coef=1e1,
        desc=VIFCodeDescription.energy,
        unit=VIFCodeUnit.watt_hour,
    ),
    0b0000_0101: VIFCode(
        code=0x05,
        coef=1e2,
        desc=VIFCodeDescription.energy,
        unit=VIFCodeUnit.watt_hour,
    ),
    0b0000_0110: VIFCode(
        code=0x06,
        coef=1e3,
        desc=VIFCodeDescription.energy,
        unit=VIFCodeUnit.watt_hour,
    ),
    0b0000_0111: VIFCode(
        code=0x07,
        coef=1e4,
        desc=VIFCodeDescription.energy,
        unit=VIFCodeUnit.watt_hour,
    ),
    # E000_1nnn - Energy (Joule = J)
    0b0000_1000: VIFCode(
        code=0x08,
        coef=1e0,
        desc=VIFCodeDescription.energy,
        unit=VIFCodeUnit.joule,
    ),
    0b0000_1001: VIFCode(
        code=0x09,
        coef=1e1,
        desc=VIFCodeDescription.energy,
        unit=VIFCodeUnit.joule,
    ),
    0b0000_1010: VIFCode(
        code=0x0A,
        coef=1e2,
        desc=VIFCodeDescription.energy,
        unit=VIFCodeUnit.joule,
    ),
    0b0000_1011: VIFCode(
        code=0x0B,
        coef=1e3,
        desc=VIFCodeDescription.energy,
        unit=VIFCodeUnit.joule,
    ),
    0b0000_1100: VIFCode(
        code=0x0C,
        coef=1e4,
        desc=VIFCodeDescription.energy,
        unit=VIFCodeUnit.joule,
    ),
    0b0000_1101: VIFCode(
        code=0x0D,
        coef=1e5,
        desc=VIFCodeDescription.energy,
        unit=VIFCodeUnit.joule,
    ),
    0b0000_1110: VIFCode(
        code=0x0E,
        coef=1e6,
        desc=VIFCodeDescription.energy,
        unit=VIFCodeUnit.joule,
    ),
    0b0000_1111: VIFCode(
        code=0x0F,
        coef=1e7,
        desc=VIFCodeDescription.energy,
        unit=VIFCodeUnit.joule,
    ),
    # E001_0nnn - Volume (Meter cubic = m^3)
    0b0001_0000: VIFCode(
        code=0x10,
        coef=1e-6,
        desc=VIFCodeDescription.volume,
        unit=VIFCodeUnit.meter_cubic,
    ),
    0b0001_0001: VIFCode(
        code=0x11,
        coef=1e-5,
        desc=VIFCodeDescription.volume,
        unit=VIFCodeUnit.meter_cubic,
    ),
    0b0001_0010: VIFCode(
        code=0x12,
        coef=1e-4,
        desc=VIFCodeDescription.volume,
        unit=VIFCodeUnit.meter_cubic,
    ),
    0b0001_0011: VIFCode(
        code=0x13,
        coef=1e-3,
        desc=VIFCodeDescription.volume,
        unit=VIFCodeUnit.meter_cubic,
    ),
    0b0001_0100: VIFCode(
        code=0x14,
        coef=1e-2,
        desc=VIFCodeDescription.volume,
        unit=VIFCodeUnit.meter_cubic,
    ),
    0b0001_0101: VIFCode(
        code=0x15,
        coef=1e-1,
        desc=VIFCodeDescription.volume,
        unit=VIFCodeUnit.meter_cubic,
    ),
    0b0001_0110: VIFCode(
        code=0x16,
        coef=1e0,
        desc=VIFCodeDescription.volume,
        unit=VIFCodeUnit.meter_cubic,
    ),
    0b0001_0111: VIFCode(
        code=0x17,
        coef=1e1,
        desc=VIFCodeDescription.volume,
        unit=VIFCodeUnit.meter_cubic,
    ),
    # E001_1nnn - Mass (Kilogram = kg)
    0b0001_1000: VIFCode(
        code=0x18,
        coef=1e-3,
        desc=VIFCodeDescription.mass,
        unit=VIFCodeUnit.kilogram,
    ),
    0b0001_1001: VIFCode(
        code=0x19,
        coef=1e-2,
        desc=VIFCodeDescription.mass,
        unit=VIFCodeUnit.kilogram,
    ),
    0b0001_1010: VIFCode(
        code=0x1A,
        coef=1e-1,
        desc=VIFCodeDescription.mass,
        unit=VIFCodeUnit.kilogram,
    ),
    0b0001_1011: VIFCode(
        code=0x1B,
        coef=1e0,
        desc=VIFCodeDescription.mass,
        unit=VIFCodeUnit.kilogram,
    ),
    0b0001_1100: VIFCode(
        code=0x1C,
        coef=1e1,
        desc=VIFCodeDescription.mass,
        unit=VIFCodeUnit.kilogram,
    ),
    0b0001_1101: VIFCode(
        code=0x1D,
        coef=1e2,
        desc=VIFCodeDescription.mass,
        unit=VIFCodeUnit.kilogram,
    ),
    0b0001_1110: VIFCode(
        code=0x1E,
        coef=1e3,
        desc=VIFCodeDescription.mass,
        unit=VIFCodeUnit.kilogram,
    ),
    0b0001_1111: VIFCode(
        code=0x1F,
        coef=1e4,
        desc=VIFCodeDescription.mass,
        unit=VIFCodeUnit.kilogram,
    ),
    # E010_00nn - On time (in seconds)
    0b0010_0000: VIFCode(
        code=0x20,
        coef=1,
        desc=VIFCodeDescription.on_time,
        unit=VIFCodeUnit.second,
    ),
    0b0010_0001: VIFCode(
        code=0x21,
        coef=60,
        desc=VIFCodeDescription.on_time,
        unit=VIFCodeUnit.second,
    ),
    0b0010_0010: VIFCode(
        code=0x22,
        coef=3600,
        desc=VIFCodeDescription.on_time,
        unit=VIFCodeUnit.second,
    ),
    0b0010_0011: VIFCode(
        code=0x23,
        coef=86400,
        desc=VIFCodeDescription.on_time,
        unit=VIFCodeUnit.second,
    ),
    # E010_01nn - Operating Time (like On Time)
    0b0010_0100: VIFCode(
        code=0x24,
        coef=1,
        desc=VIFCodeDescription.operating_time,
        unit=VIFCodeUnit.second,
    ),
    0b0010_0101: VIFCode(
        code=0x25,
        coef=60,
        desc=VIFCodeDescription.operating_time,
        unit=VIFCodeUnit.second,
    ),
    0b0010_0110: VIFCode(
        code=0x26,
        coef=3600,
        desc=VIFCodeDescription.operating_time,
        unit=VIFCodeUnit.second,
    ),
    0b0010_0111: VIFCode(
        code=0x27,
        coef=86400,
        desc=VIFCodeDescription.operating_time,
        unit=VIFCodeUnit.second,
    ),
    # E010_1nnn - Power (Watt = W)
    0b0010_1000: VIFCode(
        code=0x28,
        coef=1e-3,
        desc=VIFCodeDescription.power,
        unit=VIFCodeUnit.watt,
    ),
    0b0010_1001: VIFCode(
        code=0x29,
        coef=1e-2,
        desc=VIFCodeDescription.power,
        unit=VIFCodeUnit.watt,
    ),
    0b0010_1010: VIFCode(
        code=0x2A,
        coef=1e-1,
        desc=VIFCodeDescription.power,
        unit=VIFCodeUnit.watt,
    ),
    0b0010_1011: VIFCode(
        code=0x2B,
        coef=1e0,
        desc=VIFCodeDescription.power,
        unit=VIFCodeUnit.watt,
    ),
    0b0010_1100: VIFCode(
        code=0x2C,
        coef=1e1,
        desc=VIFCodeDescription.power,
        unit=VIFCodeUnit.watt,
    ),
    0b0010_1101: VIFCode(
        code=0x2D,
        coef=1e2,
        desc=VIFCodeDescription.power,
        unit=VIFCodeUnit.watt,
    ),
    0b0010_1110: VIFCode(
        code=0x2E,
        coef=1e3,
        desc=VIFCodeDescription.power,
        unit=VIFCodeUnit.watt,
    ),
    0b0010_1111: VIFCode(
        code=0x2F,
        coef=1e4,
        desc=VIFCodeDescription.power,
        unit=VIFCodeUnit.watt,
    ),
    # E011_0nnn - Power (Joule per hour = J/h)
    0b0011_0000: VIFCode(
        code=0x30,
        coef=1e0,
        desc=VIFCodeDescription.power,
        unit=VIFCodeUnit.joule_per_hour,
    ),
    0b0011_0001: VIFCode(
        code=0x31,
        coef=1e1,
        desc=VIFCodeDescription.power,
        unit=VIFCodeUnit.joule_per_hour,
    ),
    0b0011_0010: VIFCode(
        code=0x32,
        coef=1e2,
        desc=VIFCodeDescription.power,
        unit=VIFCodeUnit.joule_per_hour,
    ),
    0b0011_0011: VIFCode(
        code=0x33,
        coef=1e3,
        desc=VIFCodeDescription.power,
        unit=VIFCodeUnit.joule_per_hour,
    ),
    0b0011_0100: VIFCode(
        code=0x34,
        coef=1e4,
        desc=VIFCodeDescription.power,
        unit=VIFCodeUnit.joule_per_hour,
    ),
    0b0011_0101: VIFCode(
        code=0x35,
        coef=1e5,
        desc=VIFCodeDescription.power,
        unit=VIFCodeUnit.joule_per_hour,
    ),
    0b0011_0110: VIFCode(
        code=0x36,
        coef=1e6,
        desc=VIFCodeDescription.power,
        unit=VIFCodeUnit.joule_per_hour,
    ),
    0b0011_0111: VIFCode(
        code=0x37,
        coef=1e7,
        desc=VIFCodeDescription.power,
        unit=VIFCodeUnit.joule_per_hour,
    ),
    # E011_1nnn - Volume flow (Meter cubic per hour = m^3/h)
    0b0011_1000: VIFCode(
        code=0x38,
        coef=1e-6,
        desc=VIFCodeDescription.volume_flow,
        unit=VIFCodeUnit.meter_cubic_per_hour,
    ),
    0b0011_1001: VIFCode(
        code=0x39,
        coef=1e-5,
        desc=VIFCodeDescription.volume_flow,
        unit=VIFCodeUnit.meter_cubic_per_hour,
    ),
    0b0011_1010: VIFCode(
        code=0x3A,
        coef=1e-4,
        desc=VIFCodeDescription.volume_flow,
        unit=VIFCodeUnit.meter_cubic_per_hour,
    ),
    0b0011_1011: VIFCode(
        code=0x3B,
        coef=1e-3,
        desc=VIFCodeDescription.volume_flow,
        unit=VIFCodeUnit.meter_cubic_per_hour,
    ),
    0b0011_1100: VIFCode(
        code=0x3C,
        coef=1e-2,
        desc=VIFCodeDescription.volume_flow,
        unit=VIFCodeUnit.meter_cubic_per_hour,
    ),
    0b0011_1101: VIFCode(
        code=0x3D,
        coef=1e-1,
        desc=VIFCodeDescription.volume_flow,
        unit=VIFCodeUnit.meter_cubic_per_hour,
    ),
    0b0011_1110: VIFCode(
        code=0x3E,
        coef=1e0,
        desc=VIFCodeDescription.volume_flow,
        unit=VIFCodeUnit.meter_cubic_per_hour,
    ),
    0b0011_1111: VIFCode(
        code=0x3F,
        coef=1e1,
        desc=VIFCodeDescription.volume_flow,
        unit=VIFCodeUnit.meter_cubic_per_hour,
    ),
    # E100_0nnn - Volume flow (Meter cubic per minute = m^3/min)
    0b0100_0000: VIFCode(
        code=0x40,
        coef=1e-7,
        desc=VIFCodeDescription.volume_flow,
        unit=VIFCodeUnit.meter_cubic_per_minute,
    ),
    0b0100_0001: VIFCode(
        code=0x41,
        coef=1e-6,
        desc=VIFCodeDescription.volume_flow,
        unit=VIFCodeUnit.meter_cubic_per_minute,
    ),
    0b0100_0010: VIFCode(
        code=0x42,
        coef=1e-5,
        desc=VIFCodeDescription.volume_flow,
        unit=VIFCodeUnit.meter_cubic_per_minute,
    ),
    0b0100_0011: VIFCode(
        code=0x43,
        coef=1e-4,
        desc=VIFCodeDescription.volume_flow,
        unit=VIFCodeUnit.meter_cubic_per_minute,
    ),
    0b0100_0100: VIFCode(
        code=0x44,
        coef=1e-3,
        desc=VIFCodeDescription.volume_flow,
        unit=VIFCodeUnit.meter_cubic_per_minute,
    ),
    0b0100_0101: VIFCode(
        code=0x45,
        coef=1e-2,
        desc=VIFCodeDescription.volume_flow,
        unit=VIFCodeUnit.meter_cubic_per_minute,
    ),
    0b0100_0110: VIFCode(
        code=0x46,
        coef=1e-1,
        desc=VIFCodeDescription.volume_flow,
        unit=VIFCodeUnit.meter_cubic_per_minute,
    ),
    0b0100_0111: VIFCode(
        code=0x47,
        coef=1e0,
        desc=VIFCodeDescription.volume_flow,
        unit=VIFCodeUnit.meter_cubic_per_minute,
    ),
    # E100_1nnn - Volume flow (Meter cubic per second = m^3/s)
    0b0100_1000: VIFCode(
        code=0x48,
        coef=1e-9,
        desc=VIFCodeDescription.volume_flow,
        unit=VIFCodeUnit.meter_cubic_per_second,
    ),
    0b0100_1001: VIFCode(
        code=0x49,
        coef=1e-8,
        desc=VIFCodeDescription.volume_flow,
        unit=VIFCodeUnit.meter_cubic_per_second,
    ),
    0b0100_1010: VIFCode(
        code=0x4A,
        coef=1e-7,
        desc=VIFCodeDescription.volume_flow,
        unit=VIFCodeUnit.meter_cubic_per_second,
    ),
    0b0100_1011: VIFCode(
        code=0x4B,
        coef=1e-6,
        desc=VIFCodeDescription.volume_flow,
        unit=VIFCodeUnit.meter_cubic_per_second,
    ),
    0b0100_1100: VIFCode(
        code=0x4C,
        coef=1e-5,
        desc=VIFCodeDescription.volume_flow,
        unit=VIFCodeUnit.meter_cubic_per_second,
    ),
    0b0100_1101: VIFCode(
        code=0x4D,
        coef=1e-4,
        desc=VIFCodeDescription.volume_flow,
        unit=VIFCodeUnit.meter_cubic_per_second,
    ),
    0b0100_1110: VIFCode(
        code=0x4E,
        coef=1e-3,
        desc=VIFCodeDescription.volume_flow,
        unit=VIFCodeUnit.meter_cubic_per_second,
    ),
    0b0100_1111: VIFCode(
        code=0x4F,
        coef=1e-2,
        desc=VIFCodeDescription.volume_flow,
        unit=VIFCodeUnit.meter_cubic_per_second,
    ),
    # E101_0nnn - Mass flow (Kilogram per hour = kg/h)
    0b0101_0000: VIFCode(
        code=0x50,
        coef=1e-3,
        desc=VIFCodeDescription.mass_flow,
        unit=VIFCodeUnit.kilogram_per_hour,
    ),
    0b0101_0001: VIFCode(
        code=0x51,
        coef=1e-2,
        desc=VIFCodeDescription.mass_flow,
        unit=VIFCodeUnit.kilogram_per_hour,
    ),
    0b0101_0010: VIFCode(
        code=0x52,
        coef=1e-1,
        desc=VIFCodeDescription.mass_flow,
        unit=VIFCodeUnit.kilogram_per_hour,
    ),
    0b0101_0011: VIFCode(
        code=0x53,
        coef=1e0,
        desc=VIFCodeDescription.mass_flow,
        unit=VIFCodeUnit.kilogram_per_hour,
    ),
    0b0101_0100: VIFCode(
        code=0x54,
        coef=1e1,
        desc=VIFCodeDescription.mass_flow,
        unit=VIFCodeUnit.kilogram_per_hour,
    ),
    0b0101_0101: VIFCode(
        code=0x55,
        coef=1e2,
        desc=VIFCodeDescription.mass_flow,
        unit=VIFCodeUnit.kilogram_per_hour,
    ),
    0b0101_0110: VIFCode(
        code=0x56,
        coef=1e3,
        desc=VIFCodeDescription.mass_flow,
        unit=VIFCodeUnit.kilogram_per_hour,
    ),
    0b0101_0111: VIFCode(
        code=0x57,
        coef=1e4,
        desc=VIFCodeDescription.mass_flow,
        unit=VIFCodeUnit.kilogram_per_hour,
    ),
    # E101_10nn - Flow temperature (Celsius = C)
    0b0101_1000: VIFCode(
        code=0x58,
        coef=1e-3,
        desc=VIFCodeDescription.flow_temp,
        unit=VIFCodeUnit.celsius,
    ),
    0b0101_1001: VIFCode(
        code=0x59,
        coef=1e-2,
        desc=VIFCodeDescription.flow_temp,
        unit=VIFCodeUnit.celsius,
    ),
    0b0101_1010: VIFCode(
        code=0x5A,
        coef=1e-1,
        desc=VIFCodeDescription.flow_temp,
        unit=VIFCodeUnit.celsius,
    ),
    0b0101_1011: VIFCode(
        code=0x5B,
        coef=1e0,
        desc=VIFCodeDescription.flow_temp,
        unit=VIFCodeUnit.celsius,
    ),
    # # E101_11nn - Return temperature (Celsius = C)
    0b0101_1100: VIFCode(
        code=0x5C,
        coef=1e-3,
        desc=VIFCodeDescription.return_temp,
        unit=VIFCodeUnit.celsius,
    ),
    0b0101_1101: VIFCode(
        code=0x5D,
        coef=1e-2,
        desc=VIFCodeDescription.return_temp,
        unit=VIFCodeUnit.celsius,
    ),
    0b0101_1110: VIFCode(
        code=0x5E,
        coef=1e-1,
        desc=VIFCodeDescription.return_temp,
        unit=VIFCodeUnit.celsius,
    ),
    0b0101_1111: VIFCode(
        code=0x5F,
        coef=1e0,
        desc=VIFCodeDescription.return_temp,
        unit=VIFCodeUnit.celsius,
    ),
    # E110_00nn - Temperature difference (Kelvin = K)
    0b0110_0000: VIFCode(
        code=0x60,
        coef=1e-3,
        desc=VIFCodeDescription.temp_difference,
        unit=VIFCodeUnit.kelvin,
    ),
    0b0110_0001: VIFCode(
        code=0x61,
        coef=1e-2,
        desc=VIFCodeDescription.temp_difference,
        unit=VIFCodeUnit.kelvin,
    ),
    0b0110_0010: VIFCode(
        code=0x62,
        coef=1e-1,
        desc=VIFCodeDescription.temp_difference,
        unit=VIFCodeUnit.kelvin,
    ),
    0b0110_0011: VIFCode(
        code=0x63,
        coef=1e0,
        desc=VIFCodeDescription.temp_difference,
        unit=VIFCodeUnit.kelvin,
    ),
    # E110_01nn - External temperature (Celsius = C)
    0b0110_0100: VIFCode(
        code=0x64,
        coef=1e-3,
        desc=VIFCodeDescription.external_temp,
        unit=VIFCodeUnit.celsius,
    ),
    0b0110_0101: VIFCode(
        code=0x65,
        coef=1e-2,
        desc=VIFCodeDescription.external_temp,
        unit=VIFCodeUnit.celsius,
    ),
    0b0110_0110: VIFCode(
        code=0x66,
        coef=1e-1,
        desc=VIFCodeDescription.external_temp,
        unit=VIFCodeUnit.celsius,
    ),
    0b0110_0111: VIFCode(
        code=0x67,
        coef=1e0,
        desc=VIFCodeDescription.external_temp,
        unit=VIFCodeUnit.celsius,
    ),
    # E110_10nn - Pressure (bar)
    0b0110_1000: VIFCode(
        code=0x68,
        coef=1e-3,
        desc=VIFCodeDescription.pressure,
        unit=VIFCodeUnit.bar,
    ),
    0b0110_1001: VIFCode(
        code=0x69,
        coef=1e-2,
        desc=VIFCodeDescription.pressure,
        unit=VIFCodeUnit.bar,
    ),
    0b0110_1010: VIFCode(
        code=0x6A,
        coef=1e-1,
        desc=VIFCodeDescription.pressure,
        unit=VIFCodeUnit.bar,
    ),
    0b0110_1011: VIFCode(
        code=0x6B,
        coef=1e0,
        desc=VIFCodeDescription.pressure,
        unit=VIFCodeUnit.bar,
    ),
    # E110_110n - Time point (date or datetime)
    0b0110_1100: VIFCode(
        code=0x6C,
        coef=1,
        desc=VIFCodeDescription.time_point,
        unit=VIFCodeUnit.date,
    ),
    0b0110_1101: VIFCode(
        code=0x6D,
        coef=1,
        desc=VIFCodeDescription.time_point,
        unit=VIFCodeUnit.datetime,
    ),
    # E110_1110 = Heat Cost Allocator (H.C.A.) Units
    0b0110_1110: VIFCode(
        code=0x6E, coef=1e0, desc=VIFCodeDescription.hca, unit=VIFCodeUnit.hca
    ),
    # Reserved
    0b0110_1111: VIFCode(code=0x6F, desc=VIFCodeDescription.reserved),
    # E111_00nn - Averaging duration (in seconds)
    0b0111_0000: VIFCode(
        code=0x70,
        coef=1,
        desc=VIFCodeDescription.averaging_duration,
        unit=VIFCodeUnit.second,
    ),
    0b0111_0001: VIFCode(
        code=0x71,
        coef=60,
        desc=VIFCodeDescription.averaging_duration,
        unit=VIFCodeUnit.second,
    ),
    0b0111_0010: VIFCode(
        code=0x72,
        coef=3600,
        desc=VIFCodeDescription.averaging_duration,
        unit=VIFCodeUnit.second,
    ),
    0b0111_0011: VIFCode(
        code=0x73,
        coef=86400,
        desc=VIFCodeDescription.averaging_duration,
        unit=VIFCodeUnit.second,
    ),
    # E111_01nn - Actuality duration (in seconds)
    0b0111_0100: VIFCode(
        code=0x74,
        coef=1,
        desc=VIFCodeDescription.actuality_duration,
        unit=VIFCodeUnit.second,
    ),
    0b0111_0101: VIFCode(
        code=0x75,
        coef=60,
        desc=VIFCodeDescription.actuality_duration,
        unit=VIFCodeUnit.second,
    ),
    0b0111_0110: VIFCode(
        code=0x76,
        coef=3600,
        desc=VIFCodeDescription.actuality_duration,
        unit=VIFCodeUnit.second,
    ),
    0b0111_0111: VIFCode(
        code=0x77,
        coef=86400,
        desc=VIFCodeDescription.actuality_duration,
        unit=VIFCodeUnit.second,
    ),
    # E111_1000
    0b0111_1000: VIFCode(code=0x78, desc=VIFCodeDescription.fabrication_no),
    # E111_1001
    0b0111_1001: VIFCode(code=0x79, desc=VIFCodeDescription.enhanced),
    # E111_1010
    0b0111_1010: VIFCode(code=0x7A, desc=VIFCodeDescription.bus_address),
    # special purpose VIF codes
    0b0111_1100: VIFCode(code=0x7C, desc=VIFCodeDescription.user),
    0b0111_1110: VIFCode(code=0x7E, desc=VIFCodeDescription.any),
    0b0111_1111: VIFCode(code=0x7F, desc=VIFCodeDescription.manufacturer),
    # special purpose VIF codes
    0b1111_1011: VIFCode(code=0xFB, desc=VIFCodeDescription.extension),
    0b1111_1101: VIFCode(code=0xFD, desc=VIFCodeDescription.extension),
}


def get_vif_code(byte: int | VIF) -> None | VIFCode:  # noqa: C901
    """Return the VIFCode according to the given VIF.

    Parameters
    ----------
    byte : int | VIF
        either an integer or VIF class

    Raises
    ------
    MBusValidationError
        if byte is not within the byte range

    Returns
    -------
    None | VIFCode
    """
    # validate byte -> ensure VIF
    byte = int(VIF(int(byte)))

    return _VIF_CODE_MAP.get(byte)
