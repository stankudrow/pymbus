"""Pymbus utilities."""

from pymbus.exceptions import MBusValidationError


def validate_byte(number: int) -> int:
    """Return an integer if it is a byte.

    In Python, a byte must be in range(0, 256).
    This is the range for an 8-bit unsigned integer.

    Parameters
    ----------
    number : int

    Raises
    ------
    MbusValidationError
        the `number` is out of the [0, 255] segment.

    Returns
    -------
    int
    """
    if -1 < number < 256:
        return number

    msg = f"{number} is not a valid byte"
    raise MBusValidationError(msg) from None
