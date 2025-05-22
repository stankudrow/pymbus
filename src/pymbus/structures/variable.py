"""M-Bus Variable structure module."""

from enum import IntEnum


# BCD = Type A. Integer = Type B. Real = Type H.
class DataFieldCode(IntEnum):
    no_data = 0b0000
    int8 = 0b0001
    int16 = 0b0010
    int24 = 0b0011
    int32 = 0b0100
    real32 = 0b0101
    int48 = 0b0110
    int64 = 0b0111
    readout = 0b1000
    bcd2 = 0b1001
    bcd4 = 0b1010
    bcd6 = 0b1011
    bcd8 = 0b1100
    varlen = 0b1101
    bcd12 = 0b1110
    func = 0b1111


class FunctionFieldCode(IntEnum):
    instantaneous = 0b00
    maximum = 0b01
    minimum = 0b10
    error = 0b11
