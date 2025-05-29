"""M-Bus Value Information Field Code module."""

from dataclasses import dataclass
from enum import Enum

from pymbus.telegrams.fields import (
    ValueInformationField as VIF,
)
from pymbus.telegrams.fields import (
    ValueInformationFieldExtension as VIFE,
)


class VIFCodeKind(str, Enum):
    """VIF code description(s)."""

    unknown = ""
    energy = "energy"
    volume = "volume"
    mass = "mass"
    on_time = "on time"
    operating_time = "operating time"
    power = "power"
    volume_flow = "volume flow"
    mass_flow = "mass flow"
    flow_temperature = "flow temperature"
    return_temperature = "return temperature"
    temperature_difference = "temperature difference"
    external_temperature = "external temperature"
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
    extension = "extension"  # the true VIF is in the next VIFE


class VIFCodeUnit(str, Enum):
    """VIF code unit(s)."""

    unknown = ""
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


class VIFCodeFBExtUnit(str, Enum):
    mega_watt_hour = "MWh"
    giga_joule = "GJ"
    meter_cubic = "m^3"
    tonne = "t"
    feet_cubic = "feet^3"
    american_gallon = "american gallon"
    american_gallon_per_minute = "(american gallon)/min"
    american_gallon_per_hour = "(american gallon)/h"
    mega_watt = "MW"
    giga_joule_per_hour = "GJ/h"
    fahrenheit = "F"
    celsius = "C"
    watt = "W"


@dataclass
class VIFCode:
    """Value Information Code."""

    coef: int | float = 1
    kind: str = VIFCodeKind.unknown
    unit: str = VIFCodeUnit.unknown


_VIF_CODE_MAP: dict[int, VIFCode] = {
    # E000_0nnn - Energy (Watt * hour = Wh)
    0b0000_0000: VIFCode(
        # code=0x00,
        coef=1e-3,
        kind=VIFCodeKind.energy,
        unit=VIFCodeUnit.watt_hour,
    ),
    0b0000_0001: VIFCode(
        # code=0x01,
        coef=1e-2,
        kind=VIFCodeKind.energy,
        unit=VIFCodeUnit.watt_hour,
    ),
    0b0000_0010: VIFCode(
        # code=0x02,
        coef=1e-1,
        kind=VIFCodeKind.energy,
        unit=VIFCodeUnit.watt_hour,
    ),
    0b0000_0011: VIFCode(
        # code=0x03,
        coef=1e0,
        kind=VIFCodeKind.energy,
        unit=VIFCodeUnit.watt_hour,
    ),
    0b0000_0100: VIFCode(
        # code=0x04,
        coef=1e1,
        kind=VIFCodeKind.energy,
        unit=VIFCodeUnit.watt_hour,
    ),
    0b0000_0101: VIFCode(
        # code=0x05,
        coef=1e2,
        kind=VIFCodeKind.energy,
        unit=VIFCodeUnit.watt_hour,
    ),
    0b0000_0110: VIFCode(
        # code=0x06,
        coef=1e3,
        kind=VIFCodeKind.energy,
        unit=VIFCodeUnit.watt_hour,
    ),
    0b0000_0111: VIFCode(
        # code=0x07,
        coef=1e4,
        kind=VIFCodeKind.energy,
        unit=VIFCodeUnit.watt_hour,
    ),
    # E000_1nnn - Energy (Joule = J)
    0b0000_1000: VIFCode(
        # code=0x08,
        coef=1e0,
        kind=VIFCodeKind.energy,
        unit=VIFCodeUnit.joule,
    ),
    0b0000_1001: VIFCode(
        # code=0x09,
        coef=1e1,
        kind=VIFCodeKind.energy,
        unit=VIFCodeUnit.joule,
    ),
    0b0000_1010: VIFCode(
        # code=0x0A,
        coef=1e2,
        kind=VIFCodeKind.energy,
        unit=VIFCodeUnit.joule,
    ),
    0b0000_1011: VIFCode(
        # code=0x0B,
        coef=1e3,
        kind=VIFCodeKind.energy,
        unit=VIFCodeUnit.joule,
    ),
    0b0000_1100: VIFCode(
        # code=0x0C,
        coef=1e4,
        kind=VIFCodeKind.energy,
        unit=VIFCodeUnit.joule,
    ),
    0b0000_1101: VIFCode(
        # code=0x0D,
        coef=1e5,
        kind=VIFCodeKind.energy,
        unit=VIFCodeUnit.joule,
    ),
    0b0000_1110: VIFCode(
        # code=0x0E,
        coef=1e6,
        kind=VIFCodeKind.energy,
        unit=VIFCodeUnit.joule,
    ),
    0b0000_1111: VIFCode(
        # code=0x0F,
        coef=1e7,
        kind=VIFCodeKind.energy,
        unit=VIFCodeUnit.joule,
    ),
    # E001_0nnn - Volume (Meter cubic = m^3)
    0b0001_0000: VIFCode(
        # code=0x10,
        coef=1e-6,
        kind=VIFCodeKind.volume,
        unit=VIFCodeUnit.meter_cubic,
    ),
    0b0001_0001: VIFCode(
        # code=0x11,
        coef=1e-5,
        kind=VIFCodeKind.volume,
        unit=VIFCodeUnit.meter_cubic,
    ),
    0b0001_0010: VIFCode(
        # code=0x12,
        coef=1e-4,
        kind=VIFCodeKind.volume,
        unit=VIFCodeUnit.meter_cubic,
    ),
    0b0001_0011: VIFCode(
        # code=0x13,
        coef=1e-3,
        kind=VIFCodeKind.volume,
        unit=VIFCodeUnit.meter_cubic,
    ),
    0b0001_0100: VIFCode(
        # code=0x14,
        coef=1e-2,
        kind=VIFCodeKind.volume,
        unit=VIFCodeUnit.meter_cubic,
    ),
    0b0001_0101: VIFCode(
        # code=0x15,
        coef=1e-1,
        kind=VIFCodeKind.volume,
        unit=VIFCodeUnit.meter_cubic,
    ),
    0b0001_0110: VIFCode(
        # code=0x16,
        coef=1e0,
        kind=VIFCodeKind.volume,
        unit=VIFCodeUnit.meter_cubic,
    ),
    0b0001_0111: VIFCode(
        # code=0x17,
        coef=1e1,
        kind=VIFCodeKind.volume,
        unit=VIFCodeUnit.meter_cubic,
    ),
    # E001_1nnn - Mass (Kilogram = kg)
    0b0001_1000: VIFCode(
        # code=0x18,
        coef=1e-3,
        kind=VIFCodeKind.mass,
        unit=VIFCodeUnit.kilogram,
    ),
    0b0001_1001: VIFCode(
        # code=0x19,
        coef=1e-2,
        kind=VIFCodeKind.mass,
        unit=VIFCodeUnit.kilogram,
    ),
    0b0001_1010: VIFCode(
        # code=0x1A,
        coef=1e-1,
        kind=VIFCodeKind.mass,
        unit=VIFCodeUnit.kilogram,
    ),
    0b0001_1011: VIFCode(
        # code=0x1B,
        coef=1e0,
        kind=VIFCodeKind.mass,
        unit=VIFCodeUnit.kilogram,
    ),
    0b0001_1100: VIFCode(
        # code=0x1C,
        coef=1e1,
        kind=VIFCodeKind.mass,
        unit=VIFCodeUnit.kilogram,
    ),
    0b0001_1101: VIFCode(
        # code=0x1D,
        coef=1e2,
        kind=VIFCodeKind.mass,
        unit=VIFCodeUnit.kilogram,
    ),
    0b0001_1110: VIFCode(
        # code=0x1E,
        coef=1e3,
        kind=VIFCodeKind.mass,
        unit=VIFCodeUnit.kilogram,
    ),
    0b0001_1111: VIFCode(
        # code=0x1F,
        coef=1e4,
        kind=VIFCodeKind.mass,
        unit=VIFCodeUnit.kilogram,
    ),
    # E010_00nn - On time (in seconds)
    0b0010_0000: VIFCode(
        # code=0x20,
        coef=1,
        kind=VIFCodeKind.on_time,
        unit=VIFCodeUnit.second,
    ),
    0b0010_0001: VIFCode(
        # code=0x21,
        coef=60,
        kind=VIFCodeKind.on_time,
        unit=VIFCodeUnit.second,
    ),
    0b0010_0010: VIFCode(
        # code=0x22,
        coef=3600,
        kind=VIFCodeKind.on_time,
        unit=VIFCodeUnit.second,
    ),
    0b0010_0011: VIFCode(
        # code=0x23,
        coef=86400,
        kind=VIFCodeKind.on_time,
        unit=VIFCodeUnit.second,
    ),
    # E010_01nn - Operating Time (like On Time)
    0b0010_0100: VIFCode(
        # code=0x24,
        coef=1,
        kind=VIFCodeKind.operating_time,
        unit=VIFCodeUnit.second,
    ),
    0b0010_0101: VIFCode(
        # code=0x25,
        coef=60,
        kind=VIFCodeKind.operating_time,
        unit=VIFCodeUnit.second,
    ),
    0b0010_0110: VIFCode(
        # code=0x26,
        coef=3600,
        kind=VIFCodeKind.operating_time,
        unit=VIFCodeUnit.second,
    ),
    0b0010_0111: VIFCode(
        # code=0x27,
        coef=86400,
        kind=VIFCodeKind.operating_time,
        unit=VIFCodeUnit.second,
    ),
    # E010_1nnn - Power (Watt = W)
    0b0010_1000: VIFCode(
        # code=0x28,
        coef=1e-3,
        kind=VIFCodeKind.power,
        unit=VIFCodeUnit.watt,
    ),
    0b0010_1001: VIFCode(
        # code=0x29,
        coef=1e-2,
        kind=VIFCodeKind.power,
        unit=VIFCodeUnit.watt,
    ),
    0b0010_1010: VIFCode(
        # code=0x2A,
        coef=1e-1,
        kind=VIFCodeKind.power,
        unit=VIFCodeUnit.watt,
    ),
    0b0010_1011: VIFCode(
        # code=0x2B,
        coef=1e0,
        kind=VIFCodeKind.power,
        unit=VIFCodeUnit.watt,
    ),
    0b0010_1100: VIFCode(
        # code=0x2C,
        coef=1e1,
        kind=VIFCodeKind.power,
        unit=VIFCodeUnit.watt,
    ),
    0b0010_1101: VIFCode(
        # code=0x2D,
        coef=1e2,
        kind=VIFCodeKind.power,
        unit=VIFCodeUnit.watt,
    ),
    0b0010_1110: VIFCode(
        # code=0x2E,
        coef=1e3,
        kind=VIFCodeKind.power,
        unit=VIFCodeUnit.watt,
    ),
    0b0010_1111: VIFCode(
        # code=0x2F,
        coef=1e4,
        kind=VIFCodeKind.power,
        unit=VIFCodeUnit.watt,
    ),
    # E011_0nnn - Power (Joule per hour = J/h)
    0b0011_0000: VIFCode(
        # code=0x30,
        coef=1e0,
        kind=VIFCodeKind.power,
        unit=VIFCodeUnit.joule_per_hour,
    ),
    0b0011_0001: VIFCode(
        # code=0x31,
        coef=1e1,
        kind=VIFCodeKind.power,
        unit=VIFCodeUnit.joule_per_hour,
    ),
    0b0011_0010: VIFCode(
        # code=0x32,
        coef=1e2,
        kind=VIFCodeKind.power,
        unit=VIFCodeUnit.joule_per_hour,
    ),
    0b0011_0011: VIFCode(
        # code=0x33,
        coef=1e3,
        kind=VIFCodeKind.power,
        unit=VIFCodeUnit.joule_per_hour,
    ),
    0b0011_0100: VIFCode(
        # code=0x34,
        coef=1e4,
        kind=VIFCodeKind.power,
        unit=VIFCodeUnit.joule_per_hour,
    ),
    0b0011_0101: VIFCode(
        # code=0x35,
        coef=1e5,
        kind=VIFCodeKind.power,
        unit=VIFCodeUnit.joule_per_hour,
    ),
    0b0011_0110: VIFCode(
        # code=0x36,
        coef=1e6,
        kind=VIFCodeKind.power,
        unit=VIFCodeUnit.joule_per_hour,
    ),
    0b0011_0111: VIFCode(
        # code=0x37,
        coef=1e7,
        kind=VIFCodeKind.power,
        unit=VIFCodeUnit.joule_per_hour,
    ),
    # E011_1nnn - Volume flow (Meter cubic per hour = m^3/h)
    0b0011_1000: VIFCode(
        # code=0x38,
        coef=1e-6,
        kind=VIFCodeKind.volume_flow,
        unit=VIFCodeUnit.meter_cubic_per_hour,
    ),
    0b0011_1001: VIFCode(
        # code=0x39,
        coef=1e-5,
        kind=VIFCodeKind.volume_flow,
        unit=VIFCodeUnit.meter_cubic_per_hour,
    ),
    0b0011_1010: VIFCode(
        # code=0x3A,
        coef=1e-4,
        kind=VIFCodeKind.volume_flow,
        unit=VIFCodeUnit.meter_cubic_per_hour,
    ),
    0b0011_1011: VIFCode(
        # code=0x3B,
        coef=1e-3,
        kind=VIFCodeKind.volume_flow,
        unit=VIFCodeUnit.meter_cubic_per_hour,
    ),
    0b0011_1100: VIFCode(
        # code=0x3C,
        coef=1e-2,
        kind=VIFCodeKind.volume_flow,
        unit=VIFCodeUnit.meter_cubic_per_hour,
    ),
    0b0011_1101: VIFCode(
        # code=0x3D,
        coef=1e-1,
        kind=VIFCodeKind.volume_flow,
        unit=VIFCodeUnit.meter_cubic_per_hour,
    ),
    0b0011_1110: VIFCode(
        # code=0x3E,
        coef=1e0,
        kind=VIFCodeKind.volume_flow,
        unit=VIFCodeUnit.meter_cubic_per_hour,
    ),
    0b0011_1111: VIFCode(
        # code=0x3F,
        coef=1e1,
        kind=VIFCodeKind.volume_flow,
        unit=VIFCodeUnit.meter_cubic_per_hour,
    ),
    # E100_0nnn - Volume flow (Meter cubic per minute = m^3/min)
    0b0100_0000: VIFCode(
        # code=0x40,
        coef=1e-7,
        kind=VIFCodeKind.volume_flow,
        unit=VIFCodeUnit.meter_cubic_per_minute,
    ),
    0b0100_0001: VIFCode(
        # code=0x41,
        coef=1e-6,
        kind=VIFCodeKind.volume_flow,
        unit=VIFCodeUnit.meter_cubic_per_minute,
    ),
    0b0100_0010: VIFCode(
        # code=0x42,
        coef=1e-5,
        kind=VIFCodeKind.volume_flow,
        unit=VIFCodeUnit.meter_cubic_per_minute,
    ),
    0b0100_0011: VIFCode(
        # code=0x43,
        coef=1e-4,
        kind=VIFCodeKind.volume_flow,
        unit=VIFCodeUnit.meter_cubic_per_minute,
    ),
    0b0100_0100: VIFCode(
        # code=0x44,
        coef=1e-3,
        kind=VIFCodeKind.volume_flow,
        unit=VIFCodeUnit.meter_cubic_per_minute,
    ),
    0b0100_0101: VIFCode(
        # code=0x45,
        coef=1e-2,
        kind=VIFCodeKind.volume_flow,
        unit=VIFCodeUnit.meter_cubic_per_minute,
    ),
    0b0100_0110: VIFCode(
        # code=0x46,
        coef=1e-1,
        kind=VIFCodeKind.volume_flow,
        unit=VIFCodeUnit.meter_cubic_per_minute,
    ),
    0b0100_0111: VIFCode(
        # code=0x47,
        coef=1e0,
        kind=VIFCodeKind.volume_flow,
        unit=VIFCodeUnit.meter_cubic_per_minute,
    ),
    # E100_1nnn - Volume flow (Meter cubic per second = m^3/s)
    0b0100_1000: VIFCode(
        # code=0x48,
        coef=1e-9,
        kind=VIFCodeKind.volume_flow,
        unit=VIFCodeUnit.meter_cubic_per_second,
    ),
    0b0100_1001: VIFCode(
        # code=0x49,
        coef=1e-8,
        kind=VIFCodeKind.volume_flow,
        unit=VIFCodeUnit.meter_cubic_per_second,
    ),
    0b0100_1010: VIFCode(
        # code=0x4A,
        coef=1e-7,
        kind=VIFCodeKind.volume_flow,
        unit=VIFCodeUnit.meter_cubic_per_second,
    ),
    0b0100_1011: VIFCode(
        # code=0x4B,
        coef=1e-6,
        kind=VIFCodeKind.volume_flow,
        unit=VIFCodeUnit.meter_cubic_per_second,
    ),
    0b0100_1100: VIFCode(
        # code=0x4C,
        coef=1e-5,
        kind=VIFCodeKind.volume_flow,
        unit=VIFCodeUnit.meter_cubic_per_second,
    ),
    0b0100_1101: VIFCode(
        # code=0x4D,
        coef=1e-4,
        kind=VIFCodeKind.volume_flow,
        unit=VIFCodeUnit.meter_cubic_per_second,
    ),
    0b0100_1110: VIFCode(
        # code=0x4E,
        coef=1e-3,
        kind=VIFCodeKind.volume_flow,
        unit=VIFCodeUnit.meter_cubic_per_second,
    ),
    0b0100_1111: VIFCode(
        # code=0x4F,
        coef=1e-2,
        kind=VIFCodeKind.volume_flow,
        unit=VIFCodeUnit.meter_cubic_per_second,
    ),
    # E101_0nnn - Mass flow (Kilogram per hour = kg/h)
    0b0101_0000: VIFCode(
        # code=0x50,
        coef=1e-3,
        kind=VIFCodeKind.mass_flow,
        unit=VIFCodeUnit.kilogram_per_hour,
    ),
    0b0101_0001: VIFCode(
        # code=0x51,
        coef=1e-2,
        kind=VIFCodeKind.mass_flow,
        unit=VIFCodeUnit.kilogram_per_hour,
    ),
    0b0101_0010: VIFCode(
        # code=0x52,
        coef=1e-1,
        kind=VIFCodeKind.mass_flow,
        unit=VIFCodeUnit.kilogram_per_hour,
    ),
    0b0101_0011: VIFCode(
        # code=0x53,
        coef=1e0,
        kind=VIFCodeKind.mass_flow,
        unit=VIFCodeUnit.kilogram_per_hour,
    ),
    0b0101_0100: VIFCode(
        # code=0x54,
        coef=1e1,
        kind=VIFCodeKind.mass_flow,
        unit=VIFCodeUnit.kilogram_per_hour,
    ),
    0b0101_0101: VIFCode(
        # code=0x55,
        coef=1e2,
        kind=VIFCodeKind.mass_flow,
        unit=VIFCodeUnit.kilogram_per_hour,
    ),
    0b0101_0110: VIFCode(
        # code=0x56,
        coef=1e3,
        kind=VIFCodeKind.mass_flow,
        unit=VIFCodeUnit.kilogram_per_hour,
    ),
    0b0101_0111: VIFCode(
        # code=0x57,
        coef=1e4,
        kind=VIFCodeKind.mass_flow,
        unit=VIFCodeUnit.kilogram_per_hour,
    ),
    # E101_10nn - Flow temperature (Celsius = C)
    0b0101_1000: VIFCode(
        # code=0x58,
        coef=1e-3,
        kind=VIFCodeKind.flow_temperature,
        unit=VIFCodeUnit.celsius,
    ),
    0b0101_1001: VIFCode(
        # code=0x59,
        coef=1e-2,
        kind=VIFCodeKind.flow_temperature,
        unit=VIFCodeUnit.celsius,
    ),
    0b0101_1010: VIFCode(
        # code=0x5A,
        coef=1e-1,
        kind=VIFCodeKind.flow_temperature,
        unit=VIFCodeUnit.celsius,
    ),
    0b0101_1011: VIFCode(
        # code=0x5B,
        coef=1e0,
        kind=VIFCodeKind.flow_temperature,
        unit=VIFCodeUnit.celsius,
    ),
    # # E101_11nn - Return temperature (Celsius = C)
    0b0101_1100: VIFCode(
        # code=0x5C,
        coef=1e-3,
        kind=VIFCodeKind.return_temperature,
        unit=VIFCodeUnit.celsius,
    ),
    0b0101_1101: VIFCode(
        # code=0x5D,
        coef=1e-2,
        kind=VIFCodeKind.return_temperature,
        unit=VIFCodeUnit.celsius,
    ),
    0b0101_1110: VIFCode(
        # code=0x5E,
        coef=1e-1,
        kind=VIFCodeKind.return_temperature,
        unit=VIFCodeUnit.celsius,
    ),
    0b0101_1111: VIFCode(
        # code=0x5F,
        coef=1e0,
        kind=VIFCodeKind.return_temperature,
        unit=VIFCodeUnit.celsius,
    ),
    # E110_00nn - Temperature difference (Kelvin = K)
    0b0110_0000: VIFCode(
        # code=0x60,
        coef=1e-3,
        kind=VIFCodeKind.temperature_difference,
        unit=VIFCodeUnit.kelvin,
    ),
    0b0110_0001: VIFCode(
        # code=0x61,
        coef=1e-2,
        kind=VIFCodeKind.temperature_difference,
        unit=VIFCodeUnit.kelvin,
    ),
    0b0110_0010: VIFCode(
        # code=0x62,
        coef=1e-1,
        kind=VIFCodeKind.temperature_difference,
        unit=VIFCodeUnit.kelvin,
    ),
    0b0110_0011: VIFCode(
        # code=0x63,
        coef=1e0,
        kind=VIFCodeKind.temperature_difference,
        unit=VIFCodeUnit.kelvin,
    ),
    # E110_01nn - External temperature (Celsius = C)
    0b0110_0100: VIFCode(
        # code=0x64,
        coef=1e-3,
        kind=VIFCodeKind.external_temperature,
        unit=VIFCodeUnit.celsius,
    ),
    0b0110_0101: VIFCode(
        # code=0x65,
        coef=1e-2,
        kind=VIFCodeKind.external_temperature,
        unit=VIFCodeUnit.celsius,
    ),
    0b0110_0110: VIFCode(
        # code=0x66,
        coef=1e-1,
        kind=VIFCodeKind.external_temperature,
        unit=VIFCodeUnit.celsius,
    ),
    0b0110_0111: VIFCode(
        # code=0x67,
        coef=1e0,
        kind=VIFCodeKind.external_temperature,
        unit=VIFCodeUnit.celsius,
    ),
    # E110_10nn - Pressure (bar)
    0b0110_1000: VIFCode(
        # code=0x68,
        coef=1e-3,
        kind=VIFCodeKind.pressure,
        unit=VIFCodeUnit.bar,
    ),
    0b0110_1001: VIFCode(
        # code=0x69,
        coef=1e-2,
        kind=VIFCodeKind.pressure,
        unit=VIFCodeUnit.bar,
    ),
    0b0110_1010: VIFCode(
        # code=0x6A,
        coef=1e-1,
        kind=VIFCodeKind.pressure,
        unit=VIFCodeUnit.bar,
    ),
    0b0110_1011: VIFCode(
        # code=0x6B,
        coef=1e0,
        kind=VIFCodeKind.pressure,
        unit=VIFCodeUnit.bar,
    ),
    # E110_110n - Time point (date or datetime)
    0b0110_1100: VIFCode(
        # code=0x6C,
        coef=1,
        kind=VIFCodeKind.time_point,
        unit=VIFCodeUnit.date,
    ),
    0b0110_1101: VIFCode(
        # code=0x6D,
        coef=1,
        kind=VIFCodeKind.time_point,
        unit=VIFCodeUnit.datetime,
    ),
    # E110_1110 = Heat Cost Allocator (H.C.A.) Units
    0b0110_1110: VIFCode(
        # code=0x6E,
        coef=1e0,
        kind=VIFCodeKind.hca,
        unit=VIFCodeUnit.hca,
    ),
    # Reserved
    0b0110_1111: VIFCode(
        # code=0x6F,
        kind=VIFCodeKind.reserved
    ),
    # E111_00nn - Averaging duration (in seconds)
    0b0111_0000: VIFCode(
        # code=0x70,
        coef=1,
        kind=VIFCodeKind.averaging_duration,
        unit=VIFCodeUnit.second,
    ),
    0b0111_0001: VIFCode(
        # code=0x71,
        coef=60,
        kind=VIFCodeKind.averaging_duration,
        unit=VIFCodeUnit.second,
    ),
    0b0111_0010: VIFCode(
        # code=0x72,
        coef=3600,
        kind=VIFCodeKind.averaging_duration,
        unit=VIFCodeUnit.second,
    ),
    0b0111_0011: VIFCode(
        # code=0x73,
        coef=86400,
        kind=VIFCodeKind.averaging_duration,
        unit=VIFCodeUnit.second,
    ),
    # E111_01nn - Actuality duration (in seconds)
    0b0111_0100: VIFCode(
        # code=0x74,
        coef=1,
        kind=VIFCodeKind.actuality_duration,
        unit=VIFCodeUnit.second,
    ),
    0b0111_0101: VIFCode(
        # code=0x75,
        coef=60,
        kind=VIFCodeKind.actuality_duration,
        unit=VIFCodeUnit.second,
    ),
    0b0111_0110: VIFCode(
        # code=0x76,
        coef=3600,
        kind=VIFCodeKind.actuality_duration,
        unit=VIFCodeUnit.second,
    ),
    0b0111_0111: VIFCode(
        # code=0x77,
        coef=86400,
        kind=VIFCodeKind.actuality_duration,
        unit=VIFCodeUnit.second,
    ),
    # E111_1000
    0b0111_1000: VIFCode(
        # code=0x78,
        kind=VIFCodeKind.fabrication_no
    ),
    # E111_1001
    0b0111_1001: VIFCode(
        # code=0x79,
        kind=VIFCodeKind.enhanced
    ),
    # E111_1010
    0b0111_1010: VIFCode(
        # code=0x7A,
        kind=VIFCodeKind.bus_address
    ),
    # special purpose VIF codes
    0b0111_1100: VIFCode(
        # code=0x7C,
        kind=VIFCodeKind.user
    ),
    0b0111_1110: VIFCode(
        # code=0x7E,
        kind=VIFCodeKind.any
    ),
    0b0111_1111: VIFCode(
        # code=0x7F,
        kind=VIFCodeKind.manufacturer
    ),
    # special purpose VIF codes
    0b1111_1011: VIFCode(
        # code=0xFB,
        kind=VIFCodeKind.extension
    ),
    0b1111_1101: VIFCode(
        # code=0xFD,
        kind=VIFCodeKind.extension
    ),
}

_VIF_CODE_FB_EXTENSION_MAP: dict[int, VIFCode] = {
    0b000_0000: VIFCode(
        coef=1e-1, kind=VIFCodeKind.energy, unit=VIFCodeFBExtUnit.mega_watt_hour
    ),
    0b000_0001: VIFCode(
        coef=1, kind=VIFCodeKind.energy, unit=VIFCodeFBExtUnit.mega_watt_hour
    ),
    0b000_0010: VIFCode(kind=VIFCodeKind.reserved),
    0b000_0011: VIFCode(kind=VIFCodeKind.reserved),
    0b000_0100: VIFCode(kind=VIFCodeKind.reserved),
    0b000_0101: VIFCode(kind=VIFCodeKind.reserved),
    0b000_0110: VIFCode(kind=VIFCodeKind.reserved),
    0b000_0111: VIFCode(kind=VIFCodeKind.reserved),
    0b000_1000: VIFCode(
        coef=1e-1, kind=VIFCodeKind.energy, unit=VIFCodeFBExtUnit.giga_joule
    ),
    0b000_1001: VIFCode(
        coef=1e0, kind=VIFCodeKind.energy, unit=VIFCodeFBExtUnit.giga_joule
    ),
}


def get_vif_code(value: int) -> None | VIFCode:
    """Return the VIFCode according to the given VIF.

    Parameters
    ----------
    value : int
        either an integer or VIF class

    Raises
    ------
    MBusValidationError
        if `value` is not within the byte range

    Returns
    -------
    None | VIFCode
    """
    # Value validation by casting to VIF.
    # The `int(value)` is important:
    # VIF < TelegramField < int and (!)
    # a VIF does not accept a TelegramField.
    vif = VIF(int(value))
    if code := _VIF_CODE_MAP.get(vif.data):
        return code
    # trying with an extension bit set
    return _VIF_CODE_MAP.get(int(vif))


class VIFTablet:
    """VIFCode Table(t) Manager class."""

    def __call__(self, value: int | VIF | VIFE) -> None | VIFCode:
        return get_vif_code(value)
