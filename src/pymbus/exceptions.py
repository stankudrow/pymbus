"""Meter-Bus (M-Bus) exception classes."""


class MBusError(Exception):
    """Meter-Bus Base Error."""


class MBusLengthError(MBusError):
    """Invalid Data Length/Size Error."""


class MBusValidationError(MBusError):
    """Data Validation Error."""
