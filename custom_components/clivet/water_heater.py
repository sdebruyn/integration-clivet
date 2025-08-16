from typing import Any

from homeassistant.components.water_heater import (
    STATE_ECO,
    STATE_ELECTRIC,
    STATE_HEAT_PUMP,
    STATE_OFF,
    STATE_PERFORMANCE,
    WaterHeaterEntity,
    WaterHeaterEntityFeature,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import ATTR_TEMPERATURE, UnitOfTemperature
from homeassistant.core import HomeAssistant, callback
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .coordinator import ClivetCoordinator
from .entity import ClivetBooleanBaseEntity, ClivetDevice, ClivetNumericBaseEntity
from .exceptions import CommunicationException


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up platform."""
    async_add_entities([ClivetWaterHeater(coordinator=config_entry.runtime_data)], True)


# Eco: Energy efficient mode, provides energy savings and fast heating.
# Electric: Electric only mode. This mode uses the most energy.
# Performance: High performance mode.
# High demand: Meet high demands when the water heater is undersized.
# Heat pump: Heat pump is the slowest to heat, but it uses less energy.

# Storage mode: heat pump
# Resistance only: electric
# Boost mode: performance
# Maintenance mode: eco


class ClivetWaterHeater(ClivetNumericBaseEntity, WaterHeaterEntity):
    def __init__(self, coordinator: ClivetCoordinator) -> None:
        super().__init__(
            address=0,
            name="Water Heater",
            coordinator=coordinator,
            device=ClivetDevice.DHW,
            scale=0.1,
        )
        self._attr_min_temp = 40.0
        self._attr_precision = 0.1
        self._attr_target_temperature_step = 0.1
        self._attr_unit_of_measurement = UnitOfTemperature.CELSIUS
        self._attr_temperature_unit = UnitOfTemperature.CELSIUS
        self._attr_supported_features = (
            WaterHeaterEntityFeature.TARGET_TEMPERATURE
            | WaterHeaterEntityFeature.ON_OFF
            | WaterHeaterEntityFeature.OPERATION_MODE
        )
        self._attr_operation_list = [
            STATE_OFF,
            STATE_HEAT_PUMP,
            STATE_ELECTRIC,
            STATE_PERFORMANCE,
            STATE_ECO,
        ]

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return self._attr_current_operation is not None

    @callback
    def _handle_coordinator_update(self) -> None:
        self._attr_current_operation = None
        self._attr_target_temperature = None
        self._attr_target_temperature_low = None
        self._attr_target_temperature_high = None
        self._attr_max_temp = 55.0

        storage_temperature = self.decode_numeric_value(self.coordinator.data.get(2701))
        boost_temperature = self.decode_numeric_value(self.coordinator.data.get(2707))
        current_temperature = self.decode_numeric_value(self.coordinator.data.get(2800))
        sanitary_band = (
            self.decode_numeric_value(self.coordinator.data.get(2702)) or 0.0
        )

        system_status_data = self.coordinator.data.get(4264)
        dhw_status_data = self.coordinator.data.get(2700)

        on_off = ClivetBooleanBaseEntity.decode_bool(system_status_data, 0)
        storage_mode = ClivetBooleanBaseEntity.decode_bool(dhw_status_data, 2)
        resistance_only = ClivetBooleanBaseEntity.decode_bool(dhw_status_data, 5)
        boost_mode = ClivetBooleanBaseEntity.decode_bool(dhw_status_data, 6)

        self._attr_current_temperature = current_temperature

        if (
            ((not storage_mode) and boost_mode)
            or current_temperature is None
            or system_status_data is None
            or dhw_status_data is None
        ):
            # This should never happen, so everything is unknown
            self.async_write_ha_state()
            return

        if boost_mode:
            self._attr_target_temperature = boost_temperature
            self._attr_target_temperature_high = boost_temperature
            self._attr_max_temp = 65.0
            if boost_temperature:
                self._attr_target_temperature_low = boost_temperature - sanitary_band
        else:
            self._attr_target_temperature = storage_temperature
            self._attr_target_temperature_high = storage_temperature
            if storage_temperature:
                self._attr_target_temperature_low = storage_temperature - sanitary_band

        if not on_off:
            self._attr_current_operation = STATE_OFF
        elif resistance_only:
            self._attr_current_operation = STATE_ELECTRIC
        elif boost_mode:
            self._attr_current_operation = STATE_PERFORMANCE
        elif storage_mode:
            self._attr_current_operation = STATE_HEAT_PUMP
        else:
            self._attr_current_operation = STATE_ECO

        self.async_write_ha_state()

    async def async_set_temperature(self, **kwargs: Any) -> None:
        if (temperature := kwargs.get(ATTR_TEMPERATURE)) is None:
            return

        dhw_status_data = self.coordinator.data.get(2700)
        boost_mode = ClivetBooleanBaseEntity.decode_bool(dhw_status_data, 7)

        if boost_mode:
            address = 2707
        else:
            address = 2701
        try:
            await self.coordinator.set_modbus_register(
                address, self.encode_numeric_value(temperature)
            )
        except CommunicationException as e:
            raise HomeAssistantError from e

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn on the water heater."""
        try:
            await self.coordinator.set_modbus_bit(2700, 0, True)
        except CommunicationException as e:
            raise HomeAssistantError from e

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn off the water heater."""
        try:
            await self.coordinator.set_modbus_bit(2700, 0, False)
        except CommunicationException as e:
            raise HomeAssistantError from e

    async def async_set_operation_mode(self, operation_mode: str) -> None:
        """Set the operation mode of the water heater."""
        if operation_mode == STATE_OFF:
            await self.async_turn_off()
            return

        current_2700 = self.coordinator.data.get(2700)
        current_2709 = self.coordinator.data.get(2709)
        if current_2700 is None or current_2709 is None:
            raise HomeAssistantError("Failed to retrieve current operation mode")

        new_2709 = self.set_bit_values(
            current_2709, {0: True, 1: True, 2: True, 3: False}
        )

        if operation_mode == STATE_ELECTRIC:
            # set storage mode on, resistance only on, boost mode off
            new_2700 = self.set_bit_values(
                current_2700, {0: True, 2: True, 5: True, 6: False}
            )
        elif operation_mode == STATE_HEAT_PUMP:
            new_2700 = self.set_bit_values(
                current_2700, {0: True, 2: True, 5: False, 6: False}
            )
        elif operation_mode == STATE_PERFORMANCE:
            new_2700 = self.set_bit_values(
                current_2700, {0: True, 2: True, 5: False, 6: True}
            )
        elif operation_mode == STATE_ECO:
            new_2700 = self.set_bit_values(
                current_2700, {0: True, 2: False, 5: False, 6: False}
            )
        else:
            raise HomeAssistantError(f"Unsupported operation mode: {operation_mode}")

        try:
            await self.coordinator.set_modbus_register(2700, new_2700)
            await self.coordinator.set_modbus_register(2709, new_2709)
        except CommunicationException as e:
            raise HomeAssistantError from e
