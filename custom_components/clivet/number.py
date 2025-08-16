from homeassistant.components.number import NumberDeviceClass, NumberEntity, NumberMode
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfPower, UnitOfTemperature, UnitOfTime
from homeassistant.core import HomeAssistant, callback
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .coordinator import ClivetCoordinator
from .entity import ClivetDevice, ClivetNumericBaseEntity
from .exceptions import CommunicationException


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    coordinator = config_entry.runtime_data
    entities = [
        ClivetNumberEntity(
            address=2614,
            name="Demand limit",
            device=ClivetDevice.HEAT_PUMP,
            coordinator=coordinator,
            device_class=NumberDeviceClass.POWER,
            unit=UnitOfPower.KILO_WATT,
            min_value=0,
            max_value=10,
        ),
        ClivetTemperatureNumberEntity(
            address=2702,
            name="Sanitary band",
            device=ClivetDevice.DHW,
            coordinator=coordinator,
            min_value=0,
            max_value=20,
        ),
        ClivetTemperatureNumberEntity(
            address=2704,
            name="Anti-legionella setpoint",
            device=ClivetDevice.DHW,
            coordinator=coordinator,
            min_value=55,
            max_value=70,
        ),
        ClivetNumberEntity(
            address=2706,
            name="Anti-legionella interval",
            device=ClivetDevice.DHW,
            coordinator=coordinator,
            device_class=NumberDeviceClass.DURATION,
            unit=UnitOfTime.MINUTES,
            min_value=0,
            max_value=86400,
            mode=NumberMode.BOX,
        ),
    ]
    async_add_entities(entities, True)


class ClivetNumberEntity(ClivetNumericBaseEntity, NumberEntity):
    def __init__(
        self,
        *,
        address: int,
        name: str,
        device: ClivetDevice,
        device_class: NumberDeviceClass,
        unit: str,
        scale: float = 1,
        coordinator: ClivetCoordinator,
        min_value: float = 0,
        max_value: float = 100,
        mode: NumberMode = NumberMode.AUTO,
    ) -> None:
        self._attr_device_class = device_class
        self._attr_native_unit_of_measurement = unit
        self._attr_native_step = scale
        self._attr_mode = mode
        self._attr_native_min_value = min_value
        self._attr_native_max_value = max_value
        super().__init__(
            address=address,
            name=name,
            device=device,
            coordinator=coordinator,
            scale=scale,
            signed=min_value < 0,
        )

    @callback
    def _handle_coordinator_update(self) -> None:
        data = self.coordinator.data.get(self.address)
        self._attr_native_value = (
            self.decode_numeric_value(data) if data is not None else None
        )
        self.async_write_ha_state()

    async def async_set_native_value(self, value: float) -> None:
        try:
            await self.coordinator.set_modbus_register(
                self.address, self.encode_numeric_value(value)
            )
        except CommunicationException as e:
            raise HomeAssistantError from e


class ClivetTemperatureNumberEntity(ClivetNumberEntity):
    def __init__(
        self,
        *,
        address: int,
        name: str,
        device: ClivetDevice,
        coordinator: ClivetCoordinator,
        min_value: float = 18,
        max_value: float = 65,
    ) -> None:
        super().__init__(
            address=address,
            name=name,
            device=device,
            device_class=NumberDeviceClass.TEMPERATURE,
            unit=UnitOfTemperature.CELSIUS,
            coordinator=coordinator,
            scale=0.1,
            min_value=min_value,
            max_value=max_value,
        )
