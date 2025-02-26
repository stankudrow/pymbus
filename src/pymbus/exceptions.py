class MBusError(Exception):
    """Meter-Bus Base Error."""


class MBusLengthError(MBusError):
    """Invalid length/size error."""
