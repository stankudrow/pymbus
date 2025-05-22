from typing import cast

import pytest

from pymbus.codes.vif import (
    BusAddressVIFCode,
    DurationActualityVIFCode,
    DurationAveragingVIFCode,
    EnergyJouleVIFCode,
    EnergyWattHourVIFCode,
    EnhancedIdentificationVIFCode,
    FabricationNoVIFCode,
    HeatCostAllocatorUnitsVIFCode,
    MassFlowKilogramPerHourVIFCode,
    MassKilogramVIFCode,
    OnTimeVIFCode,
    OperatingTimeVIFCode,
    PhysicalUnitVIFCode,
    PowerJoulePerHourVIFCode,
    PowerWattVIFCode,
    PressureBarVIFCode,
    ReservedVIFCode,
    TemperatureDifferenceKelvinVIFCode,
    TemperatureExternalCelsiusVIFCode,
    TemperatureFlowCelsiusVIFCode,
    TemperatureReturnCelsiusVIFCode,
    TimePartVIFCode,
    TimePointVIFCode,
    VolumeFlowMeterCubicPerHourVIFCode,
    VolumeFlowMeterCubicPerMinuteVIFCode,
    VolumeFlowMeterCubicPerSecondVIFCode,
    VolumeMeterCubicVIFCode,
    get_vif_code,
)
from pymbus.codes.vif import (
    VIFCode as VIFC,
)
from pymbus.telegrams.fields import ValueInformationField as VIF


def _assert_vif_code(vif: VIF, code_type: type[VIFC]) -> VIFC:
    code = get_vif_code(vif)
    if code is None:
        msg = f"no match for {vif}"
        raise ValueError(msg)
    assert isinstance(code, code_type)
    return code


def _assert_physical_vif_code(
    vif: VIF, code_type: type[PhysicalUnitVIFCode], multiplier: float = 1
) -> PhysicalUnitVIFCode:
    code = cast("PhysicalUnitVIFCode", _assert_vif_code(vif, code_type))
    assert code.multiplier == multiplier
    return code


def _assert_time_vif_code(
    vif: VIF, code_type: type[PhysicalUnitVIFCode], multiplier: float = 1
) -> TimePartVIFCode:
    tcode = cast(
        "TimePartVIFCode", _assert_physical_vif_code(vif, code_type, multiplier)
    )
    match vif & 0x03:
        case 0:
            assert tcode.is_second()
        case 1:
            assert tcode.is_minute()
        case 2:
            assert tcode.is_hour()
        case 3:
            assert tcode.is_day()
    return tcode


@pytest.mark.parametrize(
    ("vif", "multiplier"),
    [
        (VIF(0b0000_0000), 1e-3),
        (VIF(0b0000_0001), 1e-2),
        (VIF(0b0000_0010), 1e-1),
        (VIF(0b0000_0011), 1e-0),
        (VIF(0b0000_0100), 1e1),
        (VIF(0b0000_0101), 1e2),
        (VIF(0b0000_0110), 1e3),
        (VIF(0b0000_0111), 1e4),
    ],
)
def test_energy_watt_hour_vif_codes(vif: VIF, multiplier: float):
    _assert_physical_vif_code(vif, EnergyWattHourVIFCode, multiplier)


@pytest.mark.parametrize(
    ("vif", "multiplier"),
    [
        (VIF(0b0000_1000), 1e0),
        (VIF(0b0000_1001), 1e1),
        (VIF(0b0000_1010), 1e2),
        (VIF(0b0000_1011), 1e3),
        (VIF(0b0000_1100), 1e4),
        (VIF(0b0000_1101), 1e5),
        (VIF(0b0000_1110), 1e6),
        (VIF(0b0000_1111), 1e7),
    ],
)
def test_energy_joule_vif_codes(vif: VIF, multiplier: float):
    _assert_physical_vif_code(vif, EnergyJouleVIFCode, multiplier)


@pytest.mark.parametrize(
    ("vif", "multiplier"),
    [
        (VIF(0b0001_0000), 1e-6),
        (VIF(0b0001_0001), 1e-5),
        (VIF(0b0001_0010), 1e-4),
        (VIF(0b0001_0011), 1e-3),
        (VIF(0b0001_0100), 1e-2),
        (VIF(0b0001_0101), 1e-1),
        (VIF(0b0001_0110), 1e0),
        (VIF(0b0001_0111), 1e1),
    ],
)
def test_volume_meter_cubic_vif_codes(vif: VIF, multiplier: float):
    _assert_physical_vif_code(vif, VolumeMeterCubicVIFCode, multiplier)


@pytest.mark.parametrize(
    ("vif", "multiplier"),
    [
        (VIF(0b0001_1000), 1e-3),
        (VIF(0b0001_1001), 1e-2),
        (VIF(0b0001_1010), 1e-1),
        (VIF(0b0001_1011), 1e0),
        (VIF(0b0001_1100), 1e1),
        (VIF(0b0001_1101), 1e2),
        (VIF(0b0001_1110), 1e3),
        (VIF(0b0001_1111), 1e4),
    ],
)
def test_mass_kilogram_vif_codes(vif: VIF, multiplier: float):
    _assert_physical_vif_code(vif, MassKilogramVIFCode, multiplier)


@pytest.mark.parametrize(
    "vif",
    [VIF(0b0010_0000), VIF(0b0010_0001), VIF(0b0010_0010), VIF(0b0010_0011)],
)
def test_on_time_vif_codes(vif: VIF):
    _assert_time_vif_code(vif, OnTimeVIFCode, 1)


@pytest.mark.parametrize(
    "vif",
    [VIF(0b0010_0100), VIF(0b0010_0101), VIF(0b0010_0110), VIF(0b0010_0111)],
)
def test_operating_time_vif_codes(vif: VIF):
    _assert_time_vif_code(vif, OperatingTimeVIFCode, 1)


@pytest.mark.parametrize(
    ("vif", "multiplier"),
    [
        (VIF(0b0010_1000), 1e-3),
        (VIF(0b0010_1001), 1e-2),
        (VIF(0b0010_1010), 1e-1),
        (VIF(0b0010_1011), 1e0),
        (VIF(0b0010_1100), 1e1),
        (VIF(0b0010_1101), 1e2),
        (VIF(0b0010_1110), 1e3),
        (VIF(0b0010_1111), 1e4),
    ],
)
def test_power_watt_vif_codes(vif: VIF, multiplier: float):
    _assert_physical_vif_code(vif, PowerWattVIFCode, multiplier)


@pytest.mark.parametrize(
    ("vif", "multiplier"),
    [
        (VIF(0b0011_0000), 1e0),
        (VIF(0b0011_0001), 1e1),
        (VIF(0b0011_0010), 1e2),
        (VIF(0b0011_0011), 1e3),
        (VIF(0b0011_0100), 1e4),
        (VIF(0b0011_0101), 1e5),
        (VIF(0b0011_0110), 1e6),
        (VIF(0b0011_0111), 1e7),
    ],
)
def test_power_joule_per_hour_vif_codes(vif: VIF, multiplier: float):
    _assert_physical_vif_code(vif, PowerJoulePerHourVIFCode, multiplier)


@pytest.mark.parametrize(
    ("vif", "multiplier"),
    [
        (VIF(0b0011_1000), 1e-6),
        (VIF(0b0011_1001), 1e-5),
        (VIF(0b0011_1010), 1e-4),
        (VIF(0b0011_1011), 1e-3),
        (VIF(0b0011_1100), 1e-2),
        (VIF(0b0011_1101), 1e-1),
        (VIF(0b0011_1110), 1e0),
        (VIF(0b0011_1111), 1e1),
    ],
)
def test_volume_flow_meter_cubic_per_hour_vif_codes(
    vif: VIF, multiplier: float
):
    _assert_physical_vif_code(
        vif, VolumeFlowMeterCubicPerHourVIFCode, multiplier
    )


@pytest.mark.parametrize(
    ("vif", "multiplier"),
    [
        (VIF(0b0100_0000), 1e-7),
        (VIF(0b0100_0001), 1e-6),
        (VIF(0b0100_0010), 1e-5),
        (VIF(0b0100_0011), 1e-4),
        (VIF(0b0100_0100), 1e-3),
        (VIF(0b0100_0101), 1e-2),
        (VIF(0b0100_0110), 1e-1),
        (VIF(0b0100_0111), 1e0),
    ],
)
def test_volume_flow_meter_cubic_per_minute_vif_codes(
    vif: VIF, multiplier: float
):
    _assert_physical_vif_code(
        vif, VolumeFlowMeterCubicPerMinuteVIFCode, multiplier
    )


@pytest.mark.parametrize(
    ("vif", "multiplier"),
    [
        (VIF(0b0100_1000), 1e-9),
        (VIF(0b0100_1001), 1e-8),
        (VIF(0b0100_1010), 1e-7),
        (VIF(0b0100_1011), 1e-6),
        (VIF(0b0100_1100), 1e-5),
        (VIF(0b0100_1101), 1e-4),
        (VIF(0b0100_1110), 1e-3),
        (VIF(0b0100_1111), 1e-2),
    ],
)
def test_volume_flow_meter_cubic_per_second_vif_codes(
    vif: VIF, multiplier: float
):
    _assert_physical_vif_code(
        vif, VolumeFlowMeterCubicPerSecondVIFCode, multiplier
    )


@pytest.mark.parametrize(
    ("vif", "multiplier"),
    [
        (VIF(0b0101_0000), 1e-3),
        (VIF(0b0101_0001), 1e-2),
        (VIF(0b0101_0010), 1e-1),
        (VIF(0b0101_0011), 1e0),
        (VIF(0b0101_0100), 1e1),
        (VIF(0b0101_0101), 1e2),
        (VIF(0b0101_0110), 1e3),
        (VIF(0b0101_0111), 1e4),
    ],
)
def test_mass_flow_kilogram_per_hour_vif_codes(vif: VIF, multiplier: float):
    _assert_physical_vif_code(vif, MassFlowKilogramPerHourVIFCode, multiplier)


@pytest.mark.parametrize(
    ("vif", "multiplier"),
    [
        (VIF(0b0101_1000), 1e-3),
        (VIF(0b0101_1001), 1e-2),
        (VIF(0b0101_1010), 1e-1),
        (VIF(0b0101_1011), 1e0),
    ],
)
def test_temperature_flow_celsius_vif_codes(vif: VIF, multiplier: float):
    _assert_physical_vif_code(vif, TemperatureFlowCelsiusVIFCode, multiplier)


@pytest.mark.parametrize(
    ("vif", "multiplier"),
    [
        (VIF(0b0101_1100), 1e-3),
        (VIF(0b0101_1101), 1e-2),
        (VIF(0b0101_1110), 1e-1),
        (VIF(0b0101_1111), 1e0),
    ],
)
def test_temperature_return_celsius_vif_codes(vif: VIF, multiplier: float):
    _assert_physical_vif_code(vif, TemperatureReturnCelsiusVIFCode, multiplier)


@pytest.mark.parametrize(
    ("vif", "multiplier"),
    [
        (VIF(0b0110_0000), 1e-3),
        (VIF(0b0110_0001), 1e-2),
        (VIF(0b0110_0010), 1e-1),
        (VIF(0b0110_0011), 1e-0),
    ],
)
def test_temperature_difference_kelvin_vif_codes(vif: VIF, multiplier: float):
    _assert_physical_vif_code(
        vif, TemperatureDifferenceKelvinVIFCode, multiplier
    )


@pytest.mark.parametrize(
    ("vif", "multiplier"),
    [
        (VIF(0b0110_0100), 1e-3),
        (VIF(0b0110_0101), 1e-2),
        (VIF(0b0110_0110), 1e-1),
        (VIF(0b0110_0111), 1e-0),
    ],
)
def test_temperature_external_celsius_vif_codes(vif: VIF, multiplier: float):
    _assert_physical_vif_code(
        vif, TemperatureExternalCelsiusVIFCode, multiplier
    )


@pytest.mark.parametrize(
    ("vif", "multiplier"),
    [
        (VIF(0b0110_1000), 1e-3),
        (VIF(0b0110_1001), 1e-2),
        (VIF(0b0110_1010), 1e-1),
        (VIF(0b0110_1011), 1e0),
    ],
)
def test_pressure_bar_vif_codes(vif: VIF, multiplier: float):
    _assert_physical_vif_code(vif, PressureBarVIFCode, multiplier)


@pytest.mark.parametrize(
    "vif",
    [VIF(0b0110_1100), VIF(0b0110_1101)],
)
def test_time_point_vif_codes(vif: VIF):
    code = cast(
        "TimePointVIFCode", _assert_physical_vif_code(vif, TimePointVIFCode, 1)
    )
    match vif & 0x01:
        case 0:
            assert code.is_date()
        case 1:
            assert code.is_datetime()


def test_hca_units_vif_code():
    _assert_physical_vif_code(
        VIF(0b0110_1110), HeatCostAllocatorUnitsVIFCode, 1
    )


def test_reserved_e110_1111_vif_code():
    _assert_vif_code(VIF(0b0110_1111), ReservedVIFCode)


@pytest.mark.parametrize(
    "vif",
    [VIF(0b0111_0000), VIF(0b0111_0001), VIF(0b0111_0010), VIF(0b0111_0011)],
)
def test_averaging_duration_vif_codes(vif: VIF):
    _assert_physical_vif_code(vif, DurationAveragingVIFCode, 1)


@pytest.mark.parametrize(
    "vif",
    [VIF(0b0111_0100), VIF(0b0111_0101), VIF(0b0111_0110), VIF(0b0111_0111)],
)
def test_actuality_duration_vif_codes(vif: VIF):
    _assert_physical_vif_code(vif, DurationActualityVIFCode, 1)


def test_fabriaction_no_vif_code():
    _assert_vif_code(VIF(0b0111_1000), FabricationNoVIFCode)


def test_enhanced_identification_vif_code():
    _assert_vif_code(VIF(0b0111_1001), EnhancedIdentificationVIFCode)


def test_bus_address_vif_code():
    _assert_vif_code(VIF(0b0111_1010), BusAddressVIFCode)
