"""M-Bus Value Information Field Code module."""

from pymbus.exceptions import MBusValidationError
from pymbus.telegrams.fields import ValueInformationField as VIF


class VIFCode:
    CMASK: int  # coding mask
    RCMASK: int = 0  # range coding mask

    def __init__(self, vif: VIF) -> None:
        self._validate_vif(vif)
        self._vif = vif

    def _validate_vif(self, vif: VIF) -> None:
        code = int(vif) & (~self.RCMASK)
        if (code & 0x7F) != self.CMASK:
            cls_name = type(self).__name__
            msg = f"{vif} does not match {cls_name}"
            raise MBusValidationError(msg)


class PhysicalUnitVIFCode(VIFCode):
    def __init__(self, vif: VIF) -> None:
        super().__init__(vif=vif)
        self._power = vif & self.RCMASK
        self._coef: int | float = 1

    @property
    def multiplier(self) -> int | float:
        """Return multiplier/coeffiecent value.

        By default, the value is 1.
        """
        return self._coef


class EnergyWattHourVIFCode(PhysicalUnitVIFCode):
    CMASK = 0b0000_0000
    RCMASK = 0b0000_0111

    def __init__(self, vif: VIF) -> None:
        super().__init__(vif)
        self._coef = 10 ** (self._power - 3)


class EnergyJouleVIFCode(PhysicalUnitVIFCode):
    CMASK = 0b0000_1000
    RCMASK = 0b0000_0111

    def __init__(self, vif: VIF) -> None:
        super().__init__(vif)
        self._coef = 10**self._power


class VolumeMeterCubicVIFCode(PhysicalUnitVIFCode):
    CMASK = 0b0001_0000
    RCMASK = 0b0000_0111

    def __init__(self, vif: VIF) -> None:
        super().__init__(vif)
        self._coef = 10 ** (self._power - 6)


class MassKilogramVIFCode(PhysicalUnitVIFCode):
    CMASK = 0b0001_1000
    RCMASK = 0b0000_0111

    def __init__(self, vif: VIF) -> None:
        super().__init__(vif)
        self._coef = 10 ** (self._power - 3)


class TimePartVIFCode(PhysicalUnitVIFCode):
    """Time part VIF code class.

    A helper class for subtyping time VIF codes.
    """

    # CMASK is defined in the subclasses
    RCMASK = 0b0000_0011

    def __init__(self, vif: VIF) -> None:
        super().__init__(vif)

    def is_day(self) -> bool:
        """Return True if Time is in days."""
        return self._power == 3

    def is_hour(self) -> bool:
        """Return True if Time is in hours."""
        return self._power == 2

    def is_minute(self) -> bool:
        """Return True if Time is in minutes."""
        return self._power == 1

    def is_second(self) -> bool:
        """Return True if Time is in seconds."""
        return not self._power


class OnTimeVIFCode(TimePartVIFCode):
    CMASK = 0b0010_0000


class OperatingTimeVIFCode(TimePartVIFCode):
    CMASK = 0b0010_0100


class PowerWattVIFCode(PhysicalUnitVIFCode):
    CMASK = 0b0010_1000
    RCMASK = 0b0000_0111

    def __init__(self, vif: VIF) -> None:
        super().__init__(vif)
        self._coef = 10 ** (self._power - 3)


class PowerJoulePerHourVIFCode(PhysicalUnitVIFCode):
    CMASK = 0b0011_0000
    RCMASK = 0b0000_0111

    def __init__(self, vif: VIF) -> None:
        super().__init__(vif)
        self._coef = 10**self._power


class VolumeFlowMeterCubicPerHourVIFCode(PhysicalUnitVIFCode):
    CMASK = 0b0011_1000
    RCMASK = 0b0000_0111

    def __init__(self, vif: VIF) -> None:
        super().__init__(vif)
        self._coef = 10 ** (self._power - 6)


class VolumeFlowMeterCubicPerMinuteVIFCode(PhysicalUnitVIFCode):
    CMASK = 0b0100_0000
    RCMASK = 0b0000_0111

    def __init__(self, vif: VIF) -> None:
        super().__init__(vif)
        self._coef = 10 ** (self._power - 7)


class VolumeFlowMeterCubicPerSecondVIFCode(PhysicalUnitVIFCode):
    CMASK = 0b0100_1000
    RCMASK = 0b0000_0111

    def __init__(self, vif: VIF) -> None:
        super().__init__(vif)
        self._coef = 10 ** (self._power - 9)


class MassFlowKilogramPerHourVIFCode(PhysicalUnitVIFCode):
    CMASK = 0b0101_0000
    RCMASK = 0b0000_0111

    def __init__(self, vif: VIF) -> None:
        super().__init__(vif)
        self._coef = 10 ** (self._power - 3)


class TemperatureFlowCelsiusVIFCode(PhysicalUnitVIFCode):
    CMASK = 0b0101_1000
    RCMASK = 0b0000_0011

    def __init__(self, vif: VIF) -> None:
        super().__init__(vif)
        self._coef = 10 ** (self._power - 3)


class TemperatureReturnCelsiusVIFCode(PhysicalUnitVIFCode):
    CMASK = 0b0101_1100
    RCMASK = 0b0000_0011

    def __init__(self, vif: VIF) -> None:
        super().__init__(vif)
        self._coef = 10 ** (self._power - 3)


class TemperatureDifferenceKelvinVIFCode(PhysicalUnitVIFCode):
    CMASK = 0b0110_0000
    RCMASK = 0b0000_0011

    def __init__(self, vif: VIF) -> None:
        super().__init__(vif)
        self._coef = 10 ** (self._power - 3)


class TemperatureExternalCelsiusVIFCode(PhysicalUnitVIFCode):
    CMASK = 0b0110_0100
    RCMASK = 0b0000_0011

    def __init__(self, vif: VIF) -> None:
        super().__init__(vif)
        self._coef = 10 ** (self._power - 3)


class PressureBarVIFCode(PhysicalUnitVIFCode):
    CMASK = 0b0110_1000
    RCMASK = 0b0000_0011

    def __init__(self, vif: VIF) -> None:
        super().__init__(vif)
        self._coef = 10 ** (self._power - 3)


class TimePointVIFCode(PhysicalUnitVIFCode):
    CMASK = 0b0110_1100
    RCMASK = 0b0000_0001

    def __init__(self, vif: VIF) -> None:
        super().__init__(vif)
        self.UNIT = "datetime" if self._power else "date"
        self._coef = 1

    def is_date(self) -> bool:
        """Return True if TimePoint has the LSB=0."""
        return not self._power

    def is_datetime(self) -> bool:
        """Return True if TimePoint has the LSB=1."""
        return bool(self._power)


class HeatCostAllocatorUnitsVIFCode(PhysicalUnitVIFCode):
    CMASK = 0b0110_1110


class ReservedVIFCode(VIFCode):
    CMASK = 0b0110_1111


class DurationAveragingVIFCode(TimePartVIFCode):
    CMASK = 0b0111_0000


class DurationActualityVIFCode(TimePartVIFCode):
    CMASK = 0b0111_0100


class FabricationNoVIFCode(VIFCode):
    CMASK = 0b0111_1000


class EnhancedIdentificationVIFCode(VIFCode):
    CMASK = 0b0111_1001


class BusAddressVIFCode(VIFCode):
    CMASK = 0b0111_1010


def get_vif_code(byte: int | VIF) -> None | VIFCode:  # noqa: C901
    """Return the VIFCode according to the given VIF.

    Parameters
    ----------
    vif : int | VIF

    Returns
    -------
    None | ValueInformationFieldCode
    """

    vif = VIF(int(byte))
    if vif < 0x08:  # Energy (Wh) -> E000_0nnn
        return EnergyWattHourVIFCode(vif)
    if vif < 0x10:  # Energy (J) -> E000_1nnn
        return EnergyJouleVIFCode(vif)
    if vif < 0x18:  # Volume (m^3) -> E001_0nnn
        return VolumeMeterCubicVIFCode(vif)
    if vif < 0x20:  # Mass (kg) -> E001_1nnn
        return MassKilogramVIFCode(vif)
    if vif < 0x24:  # On Time -> E010_00nn
        return OnTimeVIFCode(vif)
    if vif < 0x28:  # Operating Time (like OnTime) -> E010_01nn
        return OperatingTimeVIFCode(vif)
    if vif < 0x30:  # Power (W) -> E010_1nnn
        return PowerWattVIFCode(vif)
    if vif < 0x38:  # Power (J/h) -> E011_0nnn
        return PowerJoulePerHourVIFCode(vif)
    if vif < 0x40:  # Volume flow (m^3/h) -> E011_1nnn
        return VolumeFlowMeterCubicPerHourVIFCode(vif)
    if vif < 0x48:  # Volume flow ext. (m^3/min) -> E100_0nnn
        return VolumeFlowMeterCubicPerMinuteVIFCode(vif)
    if vif < 0x50:  # Volume flow (m^3/s) -> E100_1nnn
        return VolumeFlowMeterCubicPerSecondVIFCode(vif)
    if vif < 0x58:  # Mass flow (kg/h) -> E101_0nnn
        return MassFlowKilogramPerHourVIFCode(vif)
    if vif < 0x5C:  # Flow temperature (C) -> E101_10nn
        return TemperatureFlowCelsiusVIFCode(vif)
    if vif < 0x60:  # Return temperature (C) -> E101_11nn
        return TemperatureReturnCelsiusVIFCode(vif)
    if vif < 0x64:  # Temperature difference (K) -> E110_00nn
        return TemperatureDifferenceKelvinVIFCode(vif)
    if vif < 0x68:  # Temperature difference (C) -> E110_01nn
        return TemperatureExternalCelsiusVIFCode(vif)
    if vif < 0x6C:  # Pressure (bar) -> E110_10nn
        return PressureBarVIFCode(vif)
    if vif < 0x6E:  # Time point (date or datetime) -> E110_110n
        return TimePointVIFCode(vif)
    if vif == 0x6E:
        return HeatCostAllocatorUnitsVIFCode(vif)
    if vif == 0x6F:
        return ReservedVIFCode(vif)
    if vif < 0x74:  # Averaging duration (like OnTime) -> E111_00nn
        return DurationAveragingVIFCode(vif)
    if vif < 0x78:  # Actuality duration (like OnTime) -> E111_01nn
        return DurationActualityVIFCode(vif)
    if vif == 0x78:
        return FabricationNoVIFCode(vif)
    if vif == 0x79:
        return EnhancedIdentificationVIFCode(vif)
    if vif == 0x7A:
        return BusAddressVIFCode(vif)
    return None
