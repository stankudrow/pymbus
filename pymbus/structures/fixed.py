from enum import IntEnum


class MeasuredMedium(IntEnum):
    """The table (enum) for media.

    1. Record Medium/Unit is always least significant byte first.
    2. H.C.A. = Heat Cost Allocator.
    3. Media from "Gas Mode2" to "H.C.A. Mode2" are defined in EN1434-3
       for some existing meters with CI-Field 73h (intentionally mode1),
       which transmit the multibyte records with high byte first
       in contrast to the CI-Field. The master must know that
       these media codes mean mode 2 or high byte first.
       Further use of these codes for "pseudo media"
       is NOT ALLOWED for new developments.
    """

    other = 0x00  # 0000
    oil = 0x01  # 0001
    electricity = 0x02  # 0010
    gas = 0x03  # 0011
    heat = 0x04  # 0100
    steam = 0x05  # 0101
    hot_water = 0x06  # 0110
    water = 0x07  # 0111
    hca = 0x08  # 1000
    reserved1 = 0x09  # 1001
    gas_mode_2 = 0x0A  # 1010
    heat_mode_2 = 0x0B  # 1011
    hot_water_mode_2 = 0x0C  # 1100
    water_mode_2 = 0x0D  # 1101
    hca_mode_2 = 0x0E  # 1110
    reserved2 = 0x0F  # 1111


class PhysicalUnits(IntEnum):
    """The table of physical units."""

    hour_minute_second = 0x00
    day_month_year = 0x01

    watt_hour = 0x02
    watt_hour_times_10 = 0x03
    watt_hour_times_100 = 0x04

    kilo_watt_hour = 0x05
    kilo_watt_hour_times_10 = 0x06
    kilo_watt_hour_times_100 = 0x07

    mega_watt_hour = 0x08
    mega_watt_hour_times_10 = 0x09
    mega_watt_hour_times_100 = 0x0A

    kilo_joule = 0x0B
    kilo_joule_times_10 = 0x0C
    kilo_joule_times_100 = 0x0D

    mega_joule = 0x0E
    mega_joule_times_10 = 0x0F
    mega_joule_times_100 = 0x10

    giga_joule = 0x11
    giga_joule_times_10 = 0x12
    giga_joule_times_100 = 0x13

    watt = 0x14
    watt_times_10 = 0x15
    watt_times_100 = 0x16

    kilo_watt = 0x17
    kilo_watt_times_10 = 0x18
    kilo_watt_times_100 = 0x19

    mega_watt = 0x1A
    mega_watt_times_10 = 0x1B
    mega_watt_times_100 = 0x1C

    kilo_joule_per_hour = 0x1D
    kilo_joule_per_hour_times_10 = 0x1E
    kilo_joule_per_hour_times_100 = 0x1F

    mega_joule_per_hour = 0x20
    mega_joule_per_hour_times_10 = 0x21
    mega_joule_per_hour_times_100 = 0x22

    giga_joule_per_hour = 0x23
    giga_joule_per_hour_times_10 = 0x24
    giga_joule_per_hour_times_100 = 0x25

    milli_liter = 0x26
    milli_liter_times_10 = 0x27
    milli_liter_times_100 = 0x28

    liter = 0x29
    liter_times_10 = 0x2A
    liter_times_100 = 0x2B

    meter_cubic = 0x2C
    meter_cubic_times_10 = 0x2D
    meter_cubic_times_100 = 0x2E

    milli_liter_per_hour = 0x2F
    milli_liter_per_hour_times_10 = 0x30
    milli_liter_per_hour_times_100 = 0x31

    liter_per_hour = 0x32
    liter_per_hour_times_10 = 0x33
    liter_per_hour_times_100 = 0x34

    meter_cubic_per_h = 0x35
    meter_cubic_per_h_times_10 = 0x36
    meter_cubic_per_h_times_100 = 0x37

    celsius_times_10_to_minus_3 = 0x38  # Celsius * 10^(-3)

    units_for_hca = 0x39  # H.C.A. = Heat Cost Allocator

    reserved1 = 0x3A
    reserved2 = 0x3B
    reserved3 = 0x3C
    reserved4 = 0x3D

    same_but_historic = 0x3E

    without_units = 0x3F  # dimensionless
