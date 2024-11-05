from typing import Any

from pymbus.exceptions import MBusError
from pymbus.telegrams.fields.value_info import ValueInformationField as VIF


class ValueInformationFieldCode:
    CMASK: int
    EMASK: None | int = None
    DESC: None | str = None
    UNIT: Any = None

    def __init__(self, vif: VIF):
        if not isinstance(vif, VIF):
            cls_name = self.__class__.__name__
            msg = f"{vif} is not of VIF type for {cls_name}"
            raise MBusError(msg)
        self.check_coding(vif)
        self._vif = vif
        self._range = None

    @property
    def multiplier(self) -> None | int | float:
        return self._range

    def check_coding(self, vif: VIF) -> None:
        byte = vif.byte
        cmask = self.CMASK
        emask = self.EMASK
        code = byte & (~emask)

        if (code & 0x7F) != cmask:
            msg = f"the {byte} does not fit to the code {cmask}"
            raise MBusError(msg)


class EnergyWattHourVIFCode(ValueInformationFieldCode):
    CMASK = 0b0000_0000
    EMASK = 0b0000_0111
    DESC = "energy"
    UNIT = "Wh"

    def __init__(self, vif: VIF):
        super().__init__(vif)

        pwr = self._vif.byte & self.EMASK
        self._range = 10 ** (pwr - 3)


class EnergyJouleVIFCode(ValueInformationFieldCode):
    CMASK = 0b0000_1000
    EMASK = 0b0000_0111
    DESC = "energy"
    UNIT = "J"

    def __init__(self, vif: VIF):
        super().__init__(vif)

        pwr = self._vif.byte & self.EMASK
        self._range = 10**pwr


class VolumeMassKilogramVIFCode(ValueInformationFieldCode):
    CMASK = 0b0001_1000
    EMASK = 0b0000_0111
    DESC = "mass"
    UNIT = "kg"

    def __init__(self, vif: VIF):
        super().__init__(vif)

        pwr = self._vif.byte & self.EMASK
        self._range = 10 ** (pwr - 3)


class VolumeMeterCubeVIFCode(ValueInformationFieldCode):
    CMASK = 0b0001_0000
    EMASK = 0b0000_0111
    DESC = "volume"
    UNIT = "m^3"

    def __init__(self, vif: VIF):
        super().__init__(vif)

        pwr = self._vif.byte & self.EMASK
        self._range = 10 ** (pwr - 6)


class OnTimeVIFCode(ValueInformationFieldCode):
    CMASK = 0b0010_0000
    EMASK = 0b0000_0011
    DESC = "on time"
    UNIT = None

    def __init__(self, vif: VIF):
        super().__init__(vif)

        unit = self._vif.byte & self.EMASK
        if unit == 3:
            self.UNIT = "day"
        if unit == 2:
            self.UNIT = "hour"
        if unit == 1:
            self.UNIT = "minute"
        else:
            self.UNIT = "second"


class OperatingTimeVIFCode(OnTimeVIFCode):
    CMASK = 0b0010_0100


class PowerWattVIFCode(ValueInformationFieldCode):
    CMASK = 0b0010_1000
    EMASK = 0b0000_0111
    DESC = "power"
    UNIT = "W"

    def __init__(self, vif: VIF):
        super().__init__(vif)

        pwr = self._vif.byte & self.EMASK
        self._range = 10 ** (pwr - 3)


VIF_CODE_TYPES: list[ValueInformationFieldCode] = {
    EnergyWattHourVIFCode,
    EnergyJouleVIFCode,
    VolumeMeterCubeVIFCode,
    VolumeMassKilogramVIFCode,
    OperatingTimeVIFCode,
    PowerWattVIFCode,
}


def get_vif_code(vif: VIF) -> None | ValueInformationFieldCode:
    for code_type in VIF_CODE_TYPES:
        try:
            return code_type(vif)
        except Exception:
            pass
    return None
