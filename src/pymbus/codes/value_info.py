from typing import Any

from pymbus.exceptions import MBusError
from pymbus.telegrams.fields import ValueInformationField as VIF


class ValueInformationFieldCode:
    CMASK: int
    EMASK: None | int = None
    DESC: None | str = None
    UNIT: Any = None

    def __init__(self, vif: VIF) -> None:
        self.validate_vif(vif)
        self._vif = vif
        self._range = None

    @property
    def multiplier(self) -> None | int | float:
        return self._range

    def validate_vif(self, vif: VIF) -> None:
        byte = vif
        cmask = self.CMASK
        if emask := self.EMASK:
            code = byte & (~emask)

            if (code & 0x7F) != cmask:
                msg = f"the {byte} does not fit to the code {cmask}"
                raise MBusError(msg)


class EnergyWattHourVIFCode(ValueInformationFieldCode):
    CMASK = 0b0000_0000
    EMASK = 0b0000_0111
    DESC = "energy"
    UNIT = "Wh"

    def __init__(self, vif: VIF) -> None:
        super().__init__(vif)

        pwr = self._vif & self.EMASK
        self._range = 10 ** (pwr - 3)


class EnergyJouleVIFCode(ValueInformationFieldCode):
    CMASK = 0b0000_1000
    EMASK = 0b0000_0111
    DESC = "energy"
    UNIT = "J"

    def __init__(self, vif: VIF) -> None:
        super().__init__(vif)

        pwr = self._vif & self.EMASK
        self._range = 10**pwr


class VolumeMeterCubeVIFCode(ValueInformationFieldCode):
    CMASK = 0b0001_0000
    EMASK = 0b0000_0111
    DESC = "volume"
    UNIT = "m^3"

    def __init__(self, vif: VIF) -> None:
        super().__init__(vif)

        pwr = self._vif & self.EMASK
        self._range = 10 ** (pwr - 6)


class MassKilogramVIFCode(ValueInformationFieldCode):
    CMASK = 0b0001_1000
    EMASK = 0b0000_0111
    DESC = "mass"
    UNIT = "kg"

    def __init__(self, vif: VIF) -> None:
        super().__init__(vif)

        pwr = self._vif & self.EMASK
        self._range = 10 ** (pwr - 3)


class OnTimeVIFCode(ValueInformationFieldCode):
    CMASK = 0b0010_0000
    EMASK = 0b0000_0011
    DESC = "on time"
    UNIT = None

    def __init__(self, vif: VIF) -> None:
        super().__init__(vif)

        unit = self._vif & self.EMASK
        if unit == 3:
            self.UNIT = "day"
        if unit == 2:
            self.UNIT = "hour"
        if unit == 1:
            self.UNIT = "minute"
        if unit == 0:
            self.UNIT = "second"


class OperatingTimeVIFCode(OnTimeVIFCode):
    CMASK = 0b0010_0100


class PowerWattVIFCode(ValueInformationFieldCode):
    CMASK = 0b0010_1000
    EMASK = 0b0000_0111
    DESC = "power"
    UNIT = "W"

    def __init__(self, vif: VIF) -> None:
        super().__init__(vif)

        pwr = self._vif & self.EMASK
        self._range = 10 ** (pwr - 3)


class PowerJoulePerHourVIFCode(ValueInformationFieldCode):
    CMASK = 0b0011_0000
    EMASK = 0b0000_0111
    DESC = "power"
    UNIT = "J/h"

    def __init__(self, vif: VIF) -> None:
        super().__init__(vif)

        pwr = self._vif & self.EMASK
        self._range = 10 ** (pwr)


class VolumeFlowCubicMeterPerHourVIFCode(ValueInformationFieldCode):
    CMASK = 0b0011_1000
    EMASK = 0b0000_0111
    DESC = "volume flow"
    UNIT = "m^3/h"

    def __init__(self, vif: VIF) -> None:
        super().__init__(vif)

        pwr = self._vif & self.EMASK
        self._range = 10 ** (pwr - 6)


class VolumeFlowCubicMeterPerMinuteVIFCode(ValueInformationFieldCode):
    CMASK = 0b0100_0000
    EMASK = 0b0000_0111
    DESC = "volume flow"
    UNIT = "m^3/min"

    def __init__(self, vif: VIF) -> None:
        super().__init__(vif)

        pwr = self._vif & self.EMASK
        self._range = 10 ** (pwr - 7)


class VolumeFlowCubicMeterPerSecondVIFCode(ValueInformationFieldCode):
    CMASK = 0b0100_1000
    EMASK = 0b0000_0111
    DESC = "volume flow"
    UNIT = "m^3/s"

    def __init__(self, vif: VIF) -> None:
        super().__init__(vif)

        pwr = self._vif & self.EMASK
        self._range = 10 ** (pwr - 9)


VIF_CODE_TYPES: set[type[ValueInformationFieldCode]] = {
    EnergyWattHourVIFCode,
    EnergyJouleVIFCode,
    VolumeMeterCubeVIFCode,
    MassKilogramVIFCode,
    OnTimeVIFCode,
    OperatingTimeVIFCode,
    PowerWattVIFCode,
    PowerJoulePerHourVIFCode,
    VolumeFlowCubicMeterPerHourVIFCode,
    VolumeFlowCubicMeterPerMinuteVIFCode,
    VolumeFlowCubicMeterPerSecondVIFCode,
}


def get_vif_code(vif: VIF) -> None | ValueInformationFieldCode:
    for code_type in VIF_CODE_TYPES:
        try:
            return code_type(vif)
        except MBusError:
            pass
    return None
