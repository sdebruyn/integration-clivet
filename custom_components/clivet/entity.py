from enum import StrEnum

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import ClivetCoordinator


class ClivetDevice(StrEnum):
    HEAT_PUMP = "heat_pump"
    DHW = "dhw"
    COMPRESSOR = "compressor"

    def device_name(self) -> str:
        match self.value:
            case ClivetDevice.HEAT_PUMP:
                return "Heat Pump"
            case ClivetDevice.DHW:
                return "Domestic Hot Water"
            case ClivetDevice.COMPRESSOR:
                return "Compressor"
            case _:
                raise NotImplementedError(
                    f"Device type {self.value} is not implemented"
                )


class ClivetBaseEntity(CoordinatorEntity[ClivetCoordinator]):
    def __init__(
        self,
        *,
        address: int,
        name: str,
        device: ClivetDevice,
        coordinator: ClivetCoordinator,
    ) -> None:
        self._attr_has_entity_name = True
        self.address = address
        self._attr_name = name
        self._attr_unique_id = f"{coordinator.unique_id}_{address}"

        self._attr_device_info = DeviceInfo(
            manufacturer="Clivet",
            name=device.device_name(),
            model=coordinator.model_name(),
            identifiers={(DOMAIN, f"{coordinator.unique_id}_{device}")},
        )
        super().__init__(coordinator)

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return super().available and self.address in self.coordinator.data

    @staticmethod
    def set_bit_value(current_value: int, bit: int, value: bool) -> int:
        """Set a specific bit in an integer value."""
        if value:
            return current_value | (1 << bit)
        return current_value & ~(1 << bit)

    @staticmethod
    def set_bit_values(current_value: int, bits: dict[int, bool]) -> int:
        """Set multiple bits in an integer value."""
        for bit, value in bits.items():
            current_value = ClivetBaseEntity.set_bit_value(current_value, bit, value)
        return current_value


class ClivetBooleanBaseEntity(ClivetBaseEntity):
    def __init__(
        self,
        *,
        address: int,
        name: str,
        device: ClivetDevice,
        coordinator: ClivetCoordinator,
        bit: int | None = None,
        invert: bool = False,
    ) -> None:
        self.bit = bit
        self.invert = invert
        super().__init__(
            address=address, name=name, device=device, coordinator=coordinator
        )
        self._attr_unique_id = (
            f"{self._attr_unique_id}_{bit}" if bit is not None else self._attr_unique_id
        )
        self._attr_unique_id += f"_{'inverted' if invert else ''}"

    @staticmethod
    def decode_bool(
        register: int | None, bit: int | None = None, invert: bool = False
    ) -> bool | None:
        if register is None:
            return None
        return (
            bool(register & (1 << bit)) ^ invert
            if bit is not None
            else bool(register) ^ invert
        )

    def decode_bool_value(self, register: int) -> bool | None:
        return self.decode_bool(register, self.bit, self.invert)


class ClivetNumericBaseEntity(ClivetBaseEntity):
    def __init__(
        self,
        *,
        address: int,
        name: str,
        device: ClivetDevice,
        coordinator: ClivetCoordinator,
        signed: bool = False,
        scale: float = 1.0,
    ) -> None:
        self.signed = signed
        self.scale = scale
        super().__init__(
            address=address, name=name, device=device, coordinator=coordinator
        )

    @staticmethod
    def encode_number(value: float, scale: float, signed: bool):
        encoded_value = int(value / scale)
        if signed and encoded_value < 0:
            # Convert negative value to unsigned 16-bit two's complement
            encoded_value = (1 << 16) + encoded_value
        return encoded_value

    def encode_numeric_value(self, value: float) -> int:
        return self.encode_number(value=value, scale=self.scale, signed=self.signed)

    @staticmethod
    def decode_number(
        register: int | None, scale: float, signed: bool
    ) -> int | float | None:
        if register is None or register == 0x7FFE:
            return None
        if signed and register >= 0x8000:
            register -= 0x10000  # convert 16-bit two's complement to negative value
        if scale != 1:
            return register * scale
        return register

    def decode_numeric_value(self, register: int | None) -> int | float | None:
        return self.decode_number(
            register=register, scale=self.scale, signed=self.signed
        )
