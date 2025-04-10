from contextlib import AbstractContextManager
from contextlib import nullcontext as does_not_raise

import pytest

from pymbus.telegrams.fields import (
    AF_BROADCAST_ALL_SLAVES_REPLY_BYTE,
    AF_BROADCAST_NO_SLAVE_REPLIES_BYTE,
    AF_NETWORK_LAYER_BYTE,
    AF_SLAVE_MAX_RANGE_VALUE_BYTE,
    AF_SLAVE_MIN_RANGE_VALUE_BYTE,
    AF_UNCONFIGURED_SLAVE_BYTE,
    AddressField,
    ControlField,
)
from pymbus.telegrams.fields import (
    DataInformationField as DIF,
)
from pymbus.telegrams.fields import (
    DataInformationFieldExtension as DIFE,
)
from pymbus.telegrams.fields import (
    ValueInformationField as VIF,
)
from pymbus.telegrams.fields import (
    ValueInformationFieldExtension as VIFE,
)


class TestAddressField:
    def test_is_unconfigured_slave(self):
        af = AddressField(AF_UNCONFIGURED_SLAVE_BYTE)

        assert af.is_unconfigured_slave()
        assert not af.is_configured_slave()

    @pytest.mark.parametrize(
        "byte",
        [
            AF_SLAVE_MIN_RANGE_VALUE_BYTE,
            AF_SLAVE_MIN_RANGE_VALUE_BYTE + 1,
            AF_SLAVE_MAX_RANGE_VALUE_BYTE - 1,
            AF_SLAVE_MAX_RANGE_VALUE_BYTE,
        ],
    )
    def test_is_configured_slave(self, byte: int):
        af = AddressField(byte)

        assert af.is_configured_slave()
        assert not af.is_unconfigured_slave()

    @pytest.mark.parametrize(
        "byte",
        [
            AF_UNCONFIGURED_SLAVE_BYTE,
            AF_SLAVE_MIN_RANGE_VALUE_BYTE,
            AF_SLAVE_MIN_RANGE_VALUE_BYTE + 1,
            AF_SLAVE_MAX_RANGE_VALUE_BYTE - 1,
            AF_SLAVE_MAX_RANGE_VALUE_BYTE,
        ],
    )
    def test_is_slave(self, byte: int):
        af = AddressField(byte)

        assert af.is_slave()

    @pytest.mark.parametrize(
        ("byte", "answer"),
        [
            (AF_BROADCAST_ALL_SLAVES_REPLY_BYTE, True),
            (AF_BROADCAST_NO_SLAVE_REPLIES_BYTE, True),
            (AF_NETWORK_LAYER_BYTE, False),
        ],
    )
    def test_is_broadcast(self, byte: int, answer: bool):
        af = AddressField(byte)

        assert af.is_broadcast() == answer

    def test_is_network_layer(self):
        af = AddressField(AF_NETWORK_LAYER_BYTE)

        assert not af.is_broadcast()
        assert not af.is_slave()

        assert af.is_network_layer()


class TestControlField:
    @pytest.mark.parametrize(
        ("byte", "answer"),
        [
            (0b0000_0000, 0x00),
            (0b0000_0101, 0x05),
            (0b0000_1010, 0x0A),
            (0b0000_1111, 0x0F),
        ],
    )
    def test_code_property(self, byte: int, answer: int):
        cf = ControlField(byte)

        assert cf.code == answer

    @pytest.mark.parametrize(
        ("byte", "answer", "expectation"),
        [
            (0b0100_0000, 0, does_not_raise()),
            (0b0101_0000, 1, does_not_raise()),
            (0b0000_0000, None, pytest.raises(AttributeError)),
        ],
    )
    def test_fcv_property(
        self, byte: int, answer: None | int, expectation: AbstractContextManager
    ):
        with expectation:
            cf = ControlField(byte)

            assert cf.fcv == answer

            assert cf.is_calling_direction()
            assert cf.direction == 1

    @pytest.mark.parametrize(
        ("byte", "answer", "expectation"),
        [
            (0b0100_0000, 0, does_not_raise()),
            (0b0110_0000, 1, does_not_raise()),
            (0b0000_0000, None, pytest.raises(AttributeError)),
        ],
    )
    def test_fcb_property(
        self, byte: int, answer: None | int, expectation: AbstractContextManager
    ):
        with expectation:
            cf = ControlField(byte)

            assert cf.fcb == answer

            assert cf.is_calling_direction()
            assert cf.direction == 1

    @pytest.mark.parametrize(
        ("byte", "answer", "expectation"),
        [
            (0b0000_0000, 0, does_not_raise()),
            (0b0001_0000, 1, does_not_raise()),
            (0b0100_0000, None, pytest.raises(AttributeError)),
        ],
    )
    def test_dfc_property(
        self, byte: int, answer: None | int, expectation: AbstractContextManager
    ):
        with expectation:
            cf = ControlField(byte)

            assert cf.dfc == answer

            assert cf.is_reply_direction()
            assert cf.direction == 0

    @pytest.mark.parametrize(
        ("byte", "answer", "expectation"),
        [
            (0b0000_0000, 0, does_not_raise()),
            (0b0010_0000, 1, does_not_raise()),
            (0b0100_0000, None, pytest.raises(AttributeError)),
        ],
    )
    def test_acd_property(
        self, byte: int, answer: None | int, expectation: AbstractContextManager
    ):
        with expectation:
            cf = ControlField(byte)

            assert cf.acd == answer

            assert cf.is_reply_direction()
            assert cf.direction == 0


class TestDIF:
    @pytest.mark.parametrize(
        ("byte", "ext_bit"),
        [
            (0b1111_1111, 1),
            (0b0111_1111, 0),
        ],
    )
    def test_dif_extension_bit(self, byte: int, ext_bit: int):
        dif = DIF(byte=byte)

        assert dif.extension == ext_bit

    @pytest.mark.parametrize(
        ("byte", "sn_lsb"),
        [
            (0b1111_1111, 1),
            (0b1011_1111, 0),
        ],
    )
    def test_dif_storage_number_lsb(self, byte: int, sn_lsb: int):
        dif = DIF(byte=byte)

        assert dif.storage_number_lsb == sn_lsb

    @pytest.mark.parametrize(
        ("byte", "function_field"),
        [
            (0b1100_1111, 0b00),
            (0b1101_1111, 0b01),
            (0b1010_1111, 0b10),
            (0b1011_1111, 0b11),
        ],
    )
    def test_dif_function_field(self, byte: int, function_field: int):
        dif = DIF(byte=byte)

        assert dif.function == function_field

    @pytest.mark.parametrize(
        ("byte", "data_field"),
        [
            (0b1110_0000, 0b0000),
            (0b1110_1010, 0b1010),
            (0b1110_0101, 0b0101),
            (0b1100_1111, 0b1111),
        ],
    )
    def test_dif_data_field(self, byte: int, data_field: int):
        dif = DIF(byte=byte)

        assert dif.data == data_field


class TestDIFE:
    @pytest.mark.parametrize(
        ("byte", "ext_bit"),
        [
            (0b1111_1111, 1),
            (0b0111_1111, 0),
        ],
    )
    def test_dife_extension_bit(self, byte: int, ext_bit: int):
        dif = DIFE(byte=byte)

        assert dif.extension == ext_bit

    @pytest.mark.parametrize(
        ("byte", "device_unit"),
        [
            (0b1111_1111, 1),
            (0b1011_1111, 0),
        ],
    )
    def test_dife_storage_number_lsb(self, byte: int, device_unit: int):
        dif = DIFE(byte=byte)

        assert dif.device_unit == device_unit

    @pytest.mark.parametrize(
        ("byte", "tariff"),
        [
            (0b1100_1111, 0b00),
            (0b1101_1111, 0b01),
            (0b1010_1111, 0b10),
            (0b1011_1111, 0b11),
        ],
    )
    def test_dife_tariff(self, byte: int, tariff: int):
        dif = DIFE(byte=byte)

        assert dif.tariff == tariff

    @pytest.mark.parametrize(
        ("byte", "storage_number"),
        [
            (0b1110_0000, 0b0000),
            (0b1110_1010, 0b1010),
            (0b1110_0101, 0b0101),
            (0b1100_1111, 0b1111),
        ],
    )
    def test_dife_storage_number(self, byte: int, storage_number: int):
        dif = DIFE(byte=byte)

        assert dif.storage_number == storage_number


class TestVIF:
    @pytest.mark.parametrize(
        ("byte", "ext_bit"),
        [
            (0b1111_1111, 1),
            (0b0111_1111, 0),
        ],
    )
    def test_vif_extension_bit(self, byte: int, ext_bit: int):
        vif = VIF(byte=byte)

        assert vif.extension == ext_bit

    @pytest.mark.parametrize(
        ("byte", "unit"),
        [
            (0b1111_1111, 0b0111_1111),
            (0b0011_1111, 0b0011_1111),
        ],
    )
    def test_vif_unit(self, byte: int, unit: int):
        vif = VIF(byte=byte)

        assert vif.unit == unit


class TestVIFE:
    @pytest.mark.parametrize(
        ("byte", "ext_bit"),
        [
            (0b1111_1111, 1),
            (0b0111_1111, 0),
        ],
    )
    def test_vife_extension_bit(self, byte: int, ext_bit: int):
        vife = VIFE(byte=byte)

        assert vife.extension == ext_bit

    @pytest.mark.parametrize(
        ("byte", "unit"),
        [
            (0b1111_1111, 0b0111_1111),
            (0b0011_1111, 0b0011_1111),
        ],
    )
    def test_vife_unit(self, byte: int, unit: int):
        vife = VIFE(byte=byte)

        assert vife.unit == unit
