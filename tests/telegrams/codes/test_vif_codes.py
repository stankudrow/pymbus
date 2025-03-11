import pytest

from pymbus.telegrams.codes.value_info import (
    EnergyJouleVIFCode,
    EnergyWattHourVIFCode,
    MassKilogramVIFCode,
    OnTimeVIFCode,
    OperatingTimeVIFCode,
    PowerJoulePerHourVIFCode,
    PowerWattVIFCode,
    VolumeFlowCubicMeterPerHourVIFCode,
    VolumeFlowCubicMeterPerMinuteVIFCode,
    VolumeFlowCubicMeterPerSecondVIFCode,
    VolumeMeterCubeVIFCode,
    get_vif_code,
)
from pymbus.telegrams.codes.value_info import (
    ValueInformationFieldCode as VIFC,
)
from pymbus.telegrams.fields.value_info import ValueInformationField as VIF


def _assert_vif_code(
    vif: VIF, code_type: VIFC | None, multiplier: float
) -> None:
    res = get_vif_code(vif)
    if res is None:
        msg = f"no match for {vif}"
        raise ValueError(msg)

    assert type(res) is code_type
    assert res.multiplier == multiplier


@pytest.mark.parametrize(
    ("vif", "code_type", "multiplier"),
    [
        (
            VIF(0b0000_0000),
            EnergyWattHourVIFCode,
            1e-3,
        ),
        (
            VIF(0b0000_0111),
            EnergyWattHourVIFCode,
            1e4,
        ),
        (
            VIF(0b1000_0000),
            EnergyWattHourVIFCode,
            1e-3,
        ),
        (
            VIF(0b1000_0111),
            EnergyWattHourVIFCode,
            1e4,
        ),
        (
            VIF(0b0000_1000),
            EnergyJouleVIFCode,
            1e0,
        ),
        (
            VIF(0b0000_1111),
            EnergyJouleVIFCode,
            1e7,
        ),
        (
            VIF(0b1000_1000),
            EnergyJouleVIFCode,
            1e0,
        ),
        (
            VIF(0b1000_1111),
            EnergyJouleVIFCode,
            1e7,
        ),
    ],
)
def test_energy_vifcodes(vif: VIF, code_type: VIFC | None, multiplier: float):
    _assert_vif_code(vif, code_type, multiplier)


@pytest.mark.parametrize(
    ("vif", "code_type", "multiplier"),
    [
        (
            VIF(0b0001_0000),
            VolumeMeterCubeVIFCode,
            1e-6,
        ),
        (
            VIF(0b0001_0111),
            VolumeMeterCubeVIFCode,
            1e1,
        ),
        (
            VIF(0b1001_0000),
            VolumeMeterCubeVIFCode,
            1e-6,
        ),
        (
            VIF(0b1001_0111),
            VolumeMeterCubeVIFCode,
            1e1,
        ),
    ],
)
def test_volume_vifcodes(vif: VIF, code_type: VIFC | None, multiplier: float):
    _assert_vif_code(vif, code_type, multiplier)


@pytest.mark.parametrize(
    ("vif", "code_type", "multiplier"),
    [
        (
            VIF(0b0001_1000),
            MassKilogramVIFCode,
            1e-3,
        ),
        (
            VIF(0b0001_1111),
            MassKilogramVIFCode,
            1e4,
        ),
        (
            VIF(0b1001_1000),
            MassKilogramVIFCode,
            1e-3,
        ),
        (
            VIF(0b1001_1111),
            MassKilogramVIFCode,
            1e4,
        ),
    ],
)
def test_mass_vifcodes(vif: VIF, code_type: VIFC | None, multiplier: float):
    _assert_vif_code(vif, code_type, multiplier)


@pytest.mark.parametrize(
    ("vif", "code_type", "unit"),
    [
        (
            VIF(0b0010_0000),
            OnTimeVIFCode,
            "second",
        ),
        (
            VIF(0b0010_0001),
            OnTimeVIFCode,
            "minute",
        ),
        (
            VIF(0b0010_0010),
            OnTimeVIFCode,
            "hour",
        ),
        (
            VIF(0b0010_0011),
            OnTimeVIFCode,
            "day",
        ),
        (
            VIF(0b0010_0100),
            OperatingTimeVIFCode,
            "second",
        ),
        (
            VIF(0b0010_0101),
            OperatingTimeVIFCode,
            "minute",
        ),
        (
            VIF(0b0010_0110),
            OperatingTimeVIFCode,
            "hour",
        ),
        (
            VIF(0b0010_0111),
            OperatingTimeVIFCode,
            "day",
        ),
    ],
)
def test_ontime_vifcodes(vif: VIF, code_type: VIFC | None, unit: str):
    res = get_vif_code(vif)
    if res is None:
        msg = f"no match for {vif}"
        raise ValueError(msg)

    assert type(res) is code_type
    assert res.UNIT == unit


@pytest.mark.parametrize(
    ("vif", "code_type", "multiplier"),
    [
        (
            VIF(0b0010_1000),
            PowerWattVIFCode,
            1e-3,
        ),
        (
            VIF(0b0010_1111),
            PowerWattVIFCode,
            1e4,
        ),
        (
            VIF(0b0011_0000),
            PowerJoulePerHourVIFCode,
            1,
        ),
        (
            VIF(0b0011_0111),
            PowerJoulePerHourVIFCode,
            1e7,
        ),
    ],
)
def test_power_vifcodes(vif: VIF, code_type: VIFC | None, multiplier: float):
    _assert_vif_code(vif, code_type, multiplier)


@pytest.mark.parametrize(
    ("vif", "code_type", "multiplier"),
    [
        (
            VIF(0b0011_1000),
            VolumeFlowCubicMeterPerHourVIFCode,
            1e-6,
        ),
        (
            VIF(0b0011_1111),
            VolumeFlowCubicMeterPerHourVIFCode,
            10,
        ),
        (
            VIF(0b0100_0000),
            VolumeFlowCubicMeterPerMinuteVIFCode,
            1e-7,
        ),
        (
            VIF(0b0100_0111),
            VolumeFlowCubicMeterPerMinuteVIFCode,
            1,
        ),
        (
            VIF(0b0100_1000),
            VolumeFlowCubicMeterPerSecondVIFCode,
            1e-9,
        ),
        (
            VIF(0b0100_1111),
            VolumeFlowCubicMeterPerSecondVIFCode,
            1e-2,
        ),
    ],
)
def test_volume_flow_vifcodes(
    vif: VIF, code_type: VIFC | None, multiplier: float
):
    _assert_vif_code(vif, code_type, multiplier)
