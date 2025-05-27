"""M-Bus Value Information Field Code module."""

from pymbus.exceptions import MBusValidationError
from pymbus.telegrams.fields import ValueInformationField as VIF


class VIFCode:
    """VIF Code generic class.

    Attributes
    ----------
    CMASK : int
        coding mask - valid positions in the VIF code table
    RMASK : int, default 0
        range coding mask - useful for range VIF codes
    UNIT : str, default ""
        a unit of measurement for the class
        individual codes may define own unit subclass
    """

    CMASK: int
    RMASK: int = 0
    UNIT: str = ""

    def __init__(self, vif: VIF) -> None:
        self._validate_vif_range(vif)
        self._range: int = vif & self.RMASK
        self._coef: int | float = 1
        self._unit: str = self.UNIT

    def _validate_vif_range(self, vif: VIF) -> None:
        code = int(vif) & (~self.RMASK)
        if (code & 0x7F) != self.CMASK:
            cls_name = type(self).__name__
            msg = f"{vif} does not match {cls_name}"
            raise MBusValidationError(msg)

    @property
    def coef(self) -> int | float:
        """Return multiplier/coeffiecent value.

        By default, the value is 1.
        """

        return self._coef

    @property
    def range_code(self) -> int:
        """Return range code value.

        Roughly equivalent to `vif & self.RMASK`.
        For ranged codes, this value may determine
        the value of the `coef` attribute.
        """

        return self._range

    @property
    def unit(self) -> str:
        """Return unit of measurement.

        By default, an empty string -> non measureable.
        """

        return self._unit


class EnergyWattHourVIFCode(VIFCode):
    CMASK = 0b0000_0000
    RMASK = 0b0000_0111
    UNIT = "Wh"

    def __init__(self, vif: VIF) -> None:
        super().__init__(vif)
        self._coef = 10 ** (self.range_code - 3)


class EnergyJouleVIFCode(VIFCode):
    CMASK = 0b0000_1000
    RMASK = 0b0000_0111
    UNIT = "J"

    def __init__(self, vif: VIF) -> None:
        super().__init__(vif)
        self._coef = 10**self.range_code


class VolumeMeterCubicVIFCode(VIFCode):
    CMASK = 0b0001_0000
    RMASK = 0b0000_0111
    UNIT = "m^3"

    def __init__(self, vif: VIF) -> None:
        super().__init__(vif)
        self._coef = 10 ** (self.range_code - 6)


class MassKilogramVIFCode(VIFCode):
    CMASK = 0b0001_1000
    RMASK = 0b0000_0111
    UNIT = "kg"

    def __init__(self, vif: VIF) -> None:
        super().__init__(vif)
        self._coef = 10 ** (self.range_code - 3)


class TimePartVIFCode(VIFCode):
    """Time part VIF code class.

    A helper class for subtyping time VIF codes.
    """

    # CMASK is defined in the subclasses
    RMASK = 0b0000_0011
    UNIT = "time"

    def __init__(self, vif: VIF) -> None:
        super().__init__(vif)
        match self.range_code:
            case 3:
                self._unit = "day"
            case 2:
                self._unit = "hour"
            case 1:
                self._unit = "minute"
            case 0:
                self._unit = "second"

    def is_day(self) -> bool:
        """Return True if Time is in days."""
        return self.range_code == 3

    def is_hour(self) -> bool:
        """Return True if Time is in hours."""
        return self.range_code == 2

    def is_minute(self) -> bool:
        """Return True if Time is in minutes."""
        return self.range_code == 1

    def is_second(self) -> bool:
        """Return True if Time is in seconds."""
        return not self.range_code


class OnTimeVIFCode(TimePartVIFCode):
    CMASK = 0b0010_0000


class OperatingTimeVIFCode(TimePartVIFCode):
    CMASK = 0b0010_0100


class PowerWattVIFCode(VIFCode):
    CMASK = 0b0010_1000
    RMASK = 0b0000_0111
    UNIT = "W"

    def __init__(self, vif: VIF) -> None:
        super().__init__(vif)
        self._coef = 10 ** (self.range_code - 3)


class PowerJoulePerHourVIFCode(VIFCode):
    CMASK = 0b0011_0000
    RMASK = 0b0000_0111
    UNIT = "J/h"

    def __init__(self, vif: VIF) -> None:
        super().__init__(vif)
        self._coef = 10**self.range_code


class VolumeFlowMeterCubicPerHourVIFCode(VIFCode):
    CMASK = 0b0011_1000
    RMASK = 0b0000_0111

    def __init__(self, vif: VIF) -> None:
        super().__init__(vif)
        self._coef = 10 ** (self.range_code - 6)


class VolumeFlowMeterCubicPerMinuteVIFCode(VIFCode):
    CMASK = 0b0100_0000
    RMASK = 0b0000_0111

    def __init__(self, vif: VIF) -> None:
        super().__init__(vif)
        self._coef = 10 ** (self.range_code - 7)


class VolumeFlowMeterCubicPerSecondVIFCode(VIFCode):
    CMASK = 0b0100_1000
    RMASK = 0b0000_0111

    def __init__(self, vif: VIF) -> None:
        super().__init__(vif)
        self._coef = 10 ** (self.range_code - 9)


class MassFlowKilogramPerHourVIFCode(VIFCode):
    CMASK = 0b0101_0000
    RMASK = 0b0000_0111

    def __init__(self, vif: VIF) -> None:
        super().__init__(vif)
        self._coef = 10 ** (self.range_code - 3)


class TemperatureFlowCelsiusVIFCode(VIFCode):
    CMASK = 0b0101_1000
    RMASK = 0b0000_0011

    def __init__(self, vif: VIF) -> None:
        super().__init__(vif)
        self._coef = 10 ** (self.range_code - 3)


class TemperatureReturnCelsiusVIFCode(VIFCode):
    CMASK = 0b0101_1100
    RMASK = 0b0000_0011

    def __init__(self, vif: VIF) -> None:
        super().__init__(vif)
        self._coef = 10 ** (self.range_code - 3)


class TemperatureDifferenceKelvinVIFCode(VIFCode):
    CMASK = 0b0110_0000
    RMASK = 0b0000_0011

    def __init__(self, vif: VIF) -> None:
        super().__init__(vif)
        self._coef = 10 ** (self.range_code - 3)


class TemperatureExternalCelsiusVIFCode(VIFCode):
    CMASK = 0b0110_0100
    RMASK = 0b0000_0011

    def __init__(self, vif: VIF) -> None:
        super().__init__(vif)
        self._coef = 10 ** (self.range_code - 3)


class PressureBarVIFCode(VIFCode):
    CMASK = 0b0110_1000
    RMASK = 0b0000_0011

    def __init__(self, vif: VIF) -> None:
        super().__init__(vif)
        self._coef = 10 ** (self.range_code - 3)


class TimePointVIFCode(VIFCode):
    CMASK = 0b0110_1100
    RMASK = 0b0000_0001
    UNIT = "date | datetime"

    def __init__(self, vif: VIF) -> None:
        super().__init__(vif)
        self._unit = "datetime" if self.range_code else "date"
        self._coef = 1

    def is_date(self) -> bool:
        """Return True if TimePoint has the LSB=0."""

        return not self.range_code

    def is_datetime(self) -> bool:
        """Return True if TimePoint has the LSB=1."""

        return bool(self.range_code)


class HeatCostAllocatorUnitsVIFCode(VIFCode):
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


class UserDefinedVIFCode(VIFCode):
    CMASK = 0b0111_1100


class AnyVIFCode(VIFCode):
    CMASK = 0b0111_1110


class ManufacturerSpecificVIFCode(VIFCode):
    CMASK = 0b0111_1111


_VIF_CODE_MAP: dict[int, type[VIFCode]] = {
    # E000_0nnn
    0b0000_0000: EnergyWattHourVIFCode,
    0b0000_0001: EnergyWattHourVIFCode,
    0b0000_0010: EnergyWattHourVIFCode,
    0b0000_0011: EnergyWattHourVIFCode,
    0b0000_0100: EnergyWattHourVIFCode,
    0b0000_0101: EnergyWattHourVIFCode,
    0b0000_0110: EnergyWattHourVIFCode,
    0b0000_0111: EnergyWattHourVIFCode,
    # E000_1nnn
    0b0000_1000: EnergyJouleVIFCode,
    0b0000_1001: EnergyJouleVIFCode,
    0b0000_1010: EnergyJouleVIFCode,
    0b0000_1011: EnergyJouleVIFCode,
    0b0000_1100: EnergyJouleVIFCode,
    0b0000_1101: EnergyJouleVIFCode,
    0b0000_1110: EnergyJouleVIFCode,
    0b0000_1111: EnergyJouleVIFCode,
    # E001_0nnn
    0b0001_0000: VolumeMeterCubicVIFCode,
    0b0001_0001: VolumeMeterCubicVIFCode,
    0b0001_0010: VolumeMeterCubicVIFCode,
    0b0001_0011: VolumeMeterCubicVIFCode,
    0b0001_0100: VolumeMeterCubicVIFCode,
    0b0001_0101: VolumeMeterCubicVIFCode,
    0b0001_0110: VolumeMeterCubicVIFCode,
    0b0001_0111: VolumeMeterCubicVIFCode,
    # E001_1nnn
    0b0001_1000: MassKilogramVIFCode,
    0b0001_1001: MassKilogramVIFCode,
    0b0001_1010: MassKilogramVIFCode,
    0b0001_1011: MassKilogramVIFCode,
    0b0001_1100: MassKilogramVIFCode,
    0b0001_1101: MassKilogramVIFCode,
    0b0001_1110: MassKilogramVIFCode,
    0b0001_1111: MassKilogramVIFCode,
    # E010_00nn
    0b0010_0000: OnTimeVIFCode,
    0b0010_0001: OnTimeVIFCode,
    0b0010_0010: OnTimeVIFCode,
    0b0010_0011: OnTimeVIFCode,
    # E010_01nn
    0b0010_0100: OperatingTimeVIFCode,
    0b0010_0101: OperatingTimeVIFCode,
    0b0010_0110: OperatingTimeVIFCode,
    0b0010_0111: OperatingTimeVIFCode,
    # E010_1nnn
    0b0010_1000: PowerWattVIFCode,
    0b0010_1001: PowerWattVIFCode,
    0b0010_1010: PowerWattVIFCode,
    0b0010_1011: PowerWattVIFCode,
    0b0010_1100: PowerWattVIFCode,
    0b0010_1101: PowerWattVIFCode,
    0b0010_1110: PowerWattVIFCode,
    0b0010_1111: PowerWattVIFCode,
    # E011_0nnn
    0b0011_0000: PowerJoulePerHourVIFCode,
    0b0011_0001: PowerJoulePerHourVIFCode,
    0b0011_0010: PowerJoulePerHourVIFCode,
    0b0011_0011: PowerJoulePerHourVIFCode,
    0b0011_0100: PowerJoulePerHourVIFCode,
    0b0011_0101: PowerJoulePerHourVIFCode,
    0b0011_0110: PowerJoulePerHourVIFCode,
    0b0011_0111: PowerJoulePerHourVIFCode,
    # E011_1nnn
    0b0011_1000: VolumeFlowMeterCubicPerHourVIFCode,
    0b0011_1001: VolumeFlowMeterCubicPerHourVIFCode,
    0b0011_1010: VolumeFlowMeterCubicPerHourVIFCode,
    0b0011_1011: VolumeFlowMeterCubicPerHourVIFCode,
    0b0011_1100: VolumeFlowMeterCubicPerHourVIFCode,
    0b0011_1101: VolumeFlowMeterCubicPerHourVIFCode,
    0b0011_1110: VolumeFlowMeterCubicPerHourVIFCode,
    0b0011_1111: VolumeFlowMeterCubicPerHourVIFCode,
    # E100_0nnn
    0b0100_0000: VolumeFlowMeterCubicPerMinuteVIFCode,
    0b0100_0001: VolumeFlowMeterCubicPerMinuteVIFCode,
    0b0100_0010: VolumeFlowMeterCubicPerMinuteVIFCode,
    0b0100_0011: VolumeFlowMeterCubicPerMinuteVIFCode,
    0b0100_0100: VolumeFlowMeterCubicPerMinuteVIFCode,
    0b0100_0101: VolumeFlowMeterCubicPerMinuteVIFCode,
    0b0100_0110: VolumeFlowMeterCubicPerMinuteVIFCode,
    0b0100_0111: VolumeFlowMeterCubicPerMinuteVIFCode,
    # E100_1nnn
    0b0100_1000: VolumeFlowMeterCubicPerSecondVIFCode,
    0b0100_1001: VolumeFlowMeterCubicPerSecondVIFCode,
    0b0100_1010: VolumeFlowMeterCubicPerSecondVIFCode,
    0b0100_1011: VolumeFlowMeterCubicPerSecondVIFCode,
    0b0100_1100: VolumeFlowMeterCubicPerSecondVIFCode,
    0b0100_1101: VolumeFlowMeterCubicPerSecondVIFCode,
    0b0100_1110: VolumeFlowMeterCubicPerSecondVIFCode,
    0b0100_1111: VolumeFlowMeterCubicPerSecondVIFCode,
    # E101_0nnn
    0b0101_0000: MassFlowKilogramPerHourVIFCode,
    0b0101_0001: MassFlowKilogramPerHourVIFCode,
    0b0101_0010: MassFlowKilogramPerHourVIFCode,
    0b0101_0011: MassFlowKilogramPerHourVIFCode,
    0b0101_0100: MassFlowKilogramPerHourVIFCode,
    0b0101_0101: MassFlowKilogramPerHourVIFCode,
    0b0101_0110: MassFlowKilogramPerHourVIFCode,
    0b0101_0111: MassFlowKilogramPerHourVIFCode,
    # E101_10nn
    0b0101_1000: TemperatureFlowCelsiusVIFCode,
    0b0101_1001: TemperatureFlowCelsiusVIFCode,
    0b0101_1010: TemperatureFlowCelsiusVIFCode,
    0b0101_1011: TemperatureFlowCelsiusVIFCode,
    # E101_11nn
    0b0101_1100: TemperatureReturnCelsiusVIFCode,
    0b0101_1101: TemperatureReturnCelsiusVIFCode,
    0b0101_1110: TemperatureReturnCelsiusVIFCode,
    0b0101_1111: TemperatureReturnCelsiusVIFCode,
    # E110_00nn
    0b0110_0000: TemperatureDifferenceKelvinVIFCode,
    0b0110_0001: TemperatureDifferenceKelvinVIFCode,
    0b0110_0010: TemperatureDifferenceKelvinVIFCode,
    0b0110_0011: TemperatureDifferenceKelvinVIFCode,
    # E110_01nn
    0b0110_0100: TemperatureExternalCelsiusVIFCode,
    0b0110_0101: TemperatureExternalCelsiusVIFCode,
    0b0110_0110: TemperatureExternalCelsiusVIFCode,
    0b0110_0111: TemperatureExternalCelsiusVIFCode,
    # E110_10nn
    0b0110_1000: PressureBarVIFCode,
    0b0110_1001: PressureBarVIFCode,
    0b0110_1010: PressureBarVIFCode,
    0b0110_1011: PressureBarVIFCode,
    # E110_110n
    0b0110_1100: TimePointVIFCode,
    0b0110_1101: TimePointVIFCode,
    # E110_1110
    0b0110_1110: HeatCostAllocatorUnitsVIFCode,
    # E110_1111 -> reserved
    0b0110_1111: ReservedVIFCode,
    # E111_00nn
    0b0111_0000: DurationAveragingVIFCode,
    0b0111_0001: DurationAveragingVIFCode,
    0b0111_0010: DurationAveragingVIFCode,
    0b0111_0011: DurationAveragingVIFCode,
    # E111_01nn
    0b0111_0100: DurationActualityVIFCode,
    0b0111_0101: DurationActualityVIFCode,
    0b0111_0110: DurationActualityVIFCode,
    0b0111_0111: DurationActualityVIFCode,
    # E111_1000
    0b0111_1000: FabricationNoVIFCode,
    # E111_1001
    0b0111_1001: EnhancedIdentificationVIFCode,
    # E111_1010
    0b0111_1010: BusAddressVIFCode,
    # special purpose VIF codes
    0b0111_1100: UserDefinedVIFCode,
    0b0111_1110: AnyVIFCode,
    0b0111_1111: ManufacturerSpecificVIFCode,
}


def get_vif_code(byte: int | VIF) -> None | VIFCode:  # noqa: C901
    """Return the VIFCode according to the given VIF.

    Parameters
    ----------
    byte : int | VIF
        either an integer or VIF class

    Returns
    -------
    None | VIFCode
    """

    byte = int(byte)  # ensure int
    vif = VIF(byte)  # validate byte range

    vif_code_type = _VIF_CODE_MAP.get(byte)
    if vif_code_type is not None:
        return vif_code_type(vif)
    return None
