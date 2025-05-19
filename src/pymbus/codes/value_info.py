"""M-Bus Value Information Field Code module."""

from contextlib import suppress
from typing import Any

from pymbus.exceptions import MBusValidationError
from pymbus.mbtypes import Date, DateTime
from pymbus.telegrams.fields import ValueInformationField as VIF


class ValueInformationFieldCode:
    CMASK: int  # coding mask
    RCMASK: int  # range coding mask
    DESC: str = ""
    UNIT: Any = None  # to be replaced with `pint` class

    def __init__(self, vif: VIF) -> None:
        self._validate_vif(vif)
        self._vif = vif
        self._power = vif & self.RCMASK
        self._coef: None | int | float = None

    @property
    def multiplier(self) -> None | int | float:
        return self._coef

    def _validate_vif(self, vif: VIF) -> None:
        code = int(vif) & (~self.RCMASK)
        if (code & 0x7F) != self.CMASK:
            cls_name = type(self).__name__
            msg = f"{vif} does not match {cls_name}"
            raise MBusValidationError(msg)


_VIFCode = ValueInformationFieldCode


class EnergyWattHourVIFCode(_VIFCode):
    CMASK = 0b0000_0000
    RCMASK = 0b0000_0111
    DESC = "energy"
    UNIT = "Wh"

    def __init__(self, vif: VIF) -> None:
        super().__init__(vif)
        self._coef = 10 ** (self._power - 3)


class EnergyJouleVIFCode(_VIFCode):
    CMASK = 0b0000_1000
    RCMASK = 0b0000_0111
    DESC = "energy"
    UNIT = "J"

    def __init__(self, vif: VIF) -> None:
        super().__init__(vif)
        self._coef = 10**self._power


class VolumeMeterCubicVIFCode(_VIFCode):
    CMASK = 0b0001_0000
    RCMASK = 0b0000_0111
    DESC = "volume"
    UNIT = "m^3"

    def __init__(self, vif: VIF) -> None:
        super().__init__(vif)
        self._coef = 10 ** (self._power - 6)


class MassKilogramVIFCode(_VIFCode):
    CMASK = 0b0001_1000
    RCMASK = 0b0000_0111
    DESC = "mass"
    UNIT = "kg"

    def __init__(self, vif: VIF) -> None:
        super().__init__(vif)
        self._coef = 10 ** (self._power - 3)


class OnTimeVIFCode(_VIFCode):
    CMASK = 0b0010_0000
    RCMASK = 0b0000_0011
    DESC = "on time"
    UNIT = None

    def __init__(self, vif: VIF) -> None:
        super().__init__(vif)

        unit = self._power
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
    DESC = "operating time"


class PowerWattVIFCode(_VIFCode):
    CMASK = 0b0010_1000
    RCMASK = 0b0000_0111
    DESC = "power"
    UNIT = "W"

    def __init__(self, vif: VIF) -> None:
        super().__init__(vif)
        self._coef = 10 ** (self._power - 3)


class PowerJoulePerHourVIFCode(_VIFCode):
    CMASK = 0b0011_0000
    RCMASK = 0b0000_0111
    DESC = "power"
    UNIT = "J/h"

    def __init__(self, vif: VIF) -> None:
        super().__init__(vif)
        self._coef = 10**self._power


class VolumeMeterCubicPerHourVIFCode(_VIFCode):
    CMASK = 0b0011_1000
    RCMASK = 0b0000_0111
    DESC = "volume flow"
    UNIT = "m^3/h"

    def __init__(self, vif: VIF) -> None:
        super().__init__(vif)
        self._coef = 10 ** (self._power - 6)


class VolumeMeterCubicPerMinuteVIFCode(_VIFCode):
    CMASK = 0b0100_0000
    RCMASK = 0b0000_0111
    DESC = "volume flow"
    UNIT = "m^3/min"

    def __init__(self, vif: VIF) -> None:
        super().__init__(vif)
        self._coef = 10 ** (self._power - 7)


class VolumeMeterCubicPerSecondVIFCode(_VIFCode):
    CMASK = 0b0100_1000
    RCMASK = 0b0000_0111
    DESC = "volume flow"
    UNIT = "m^3/s"

    def __init__(self, vif: VIF) -> None:
        super().__init__(vif)
        self._coef = 10 ** (self._power - 9)


class MassKilogramPerHourVIFCode(_VIFCode):
    CMASK = 0b0101_0000
    RCMASK = 0b0000_0111
    DESC = "mass flow"
    UNIT = "kg/h"

    def __init__(self, vif: VIF) -> None:
        super().__init__(vif)
        self._coef = 10 ** (self._power - 3)


class TemperatureFlowCelsiusVIFCode(_VIFCode):
    CMASK = 0b0101_1000
    RCMASK = 0b0000_0011
    DESC = "flow temperature"
    UNIT = "C"  # Celsius

    def __init__(self, vif: VIF) -> None:
        super().__init__(vif)
        self._coef = 10 ** (self._power - 3)


class TemperatureReturnCelsiusVIFCode(_VIFCode):
    CMASK = 0b0101_1100
    RCMASK = 0b0000_0011
    DESC = "return temperature"
    UNIT = "C"  # Celsius

    def __init__(self, vif: VIF) -> None:
        super().__init__(vif)
        self._coef = 10 ** (self._power - 3)


class TemperatureDifferenceKelvinVIFCode(_VIFCode):
    CMASK = 0b0110_0000
    RCMASK = 0b0000_0011
    DESC = "temperature difference"
    UNIT = "K"

    def __init__(self, vif: VIF) -> None:
        super().__init__(vif)
        self._coef = 10 ** (self._power - 3)


class TemperatureExternalCelsiusVIFCode(_VIFCode):
    CMASK = 0b0110_0100
    RCMASK = 0b0000_0011
    DESC = "external temperature"
    UNIT = "C"

    def __init__(self, vif: VIF) -> None:
        super().__init__(vif)
        self._coef = 10 ** (self._power - 3)


class PressureBarVIFCode(_VIFCode):
    CMASK = 0b0110_1100
    RCMASK = 0b0000_0011
    DESC = "pressure"
    UNIT = "bar"

    def __init__(self, vif: VIF) -> None:
        super().__init__(vif)
        self._coef = 10 ** (self._power - 3)


class TimePointVIFCode(_VIFCode):
    CMASK = 0b0110_1100
    RCMASK = 0b0000_0001
    DESC = "time point"

    def __init__(self, vif: VIF) -> None:
        super().__init__(vif)
        self.UNIT = DateTime if self._power else Date
        self._coef = self._power

    def is_date(self) -> bool:
        """Return True if the code is Date (type G)."""
        return self.UNIT is Date

    def is_datetime(self) -> bool:
        """Return True if the code is DateTime (type F)."""
        return self.UNIT is DateTime


_VIF_CODE_TYPES: set[type[_VIFCode]] = {
    EnergyWattHourVIFCode,
    EnergyJouleVIFCode,
    VolumeMeterCubicVIFCode,
    MassKilogramVIFCode,
    OnTimeVIFCode,
    OperatingTimeVIFCode,
    PowerWattVIFCode,
    PowerJoulePerHourVIFCode,
    VolumeMeterCubicPerHourVIFCode,
    VolumeMeterCubicPerMinuteVIFCode,
    VolumeMeterCubicPerSecondVIFCode,
    MassKilogramPerHourVIFCode,
    TemperatureFlowCelsiusVIFCode,
    TemperatureReturnCelsiusVIFCode,
    TemperatureDifferenceKelvinVIFCode,
    TemperatureExternalCelsiusVIFCode,
    PressureBarVIFCode,
    TimePointVIFCode,
}


def get_vif_code(vif: VIF) -> None | _VIFCode:
    """Return the VIF Code Type according to the given VIF.

    Parameters
    ----------
    vif : VIF

    Returns
    -------
    None | ValueInformationFieldCode
        the corresponding VIFCode if it exists else None
    """

    for code_type in _VIF_CODE_TYPES:
        with suppress(MBusValidationError):
            return code_type(vif)
    return None
