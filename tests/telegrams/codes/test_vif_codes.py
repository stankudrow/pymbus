import pytest

from pymbus.telegrams.codes.value_info import (
    EnergyJouleVIFCode,
    EnergyWattHourVIFCode,
    VolumeMassKilogramVIFCode,
    VolumeMeterCubeVIFCode,
    get_vif_code,
)
from pymbus.telegrams.codes.value_info import (
    ValueInformationFieldCode as VIFC,
)
from pymbus.telegrams.fields.value_info import ValueInformationField as VIF


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
    res = get_vif_code(vif)

    assert type(res) is code_type
    assert res.multiplier == multiplier


@pytest.mark.parametrize(
    ("vif", "code_type", "multiplier"),
    [
        (VIF(0b0001_1000), VolumeMassKilogramVIFCode, 1e-3),
        (VIF(0b0001_1111), VolumeMassKilogramVIFCode, 1e4),
        (VIF(0b1001_1000), VolumeMassKilogramVIFCode, 1e-3),
        (VIF(0b1001_1111), VolumeMassKilogramVIFCode, 1e4),
        (VIF(0b0001_0000), VolumeMeterCubeVIFCode, 1e-6),
        (VIF(0b0001_0111), VolumeMeterCubeVIFCode, 1e1),
        (VIF(0b1001_0000), VolumeMeterCubeVIFCode, 1e-6),
        (VIF(0b1001_0111), VolumeMeterCubeVIFCode, 1e1),
    ],
)
def test_volume_vifcodes(vif: VIF, code_type: VIFC | None, multiplier: float):
    res = get_vif_code(vif)

    assert type(res) is code_type
    assert res.multiplier == multiplier
