from typing import Any

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .entity import ClivetBooleanBaseEntity, ClivetDevice


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    coordinator = config_entry.runtime_data
    entities: list[ClivetSwitchEntity] = [
        ClivetSwitchEntity(
            address=2600,
            bit=0,
            name="System status",
            device=ClivetDevice.HEAT_PUMP,
            coordinator=coordinator,
        ),
        ClivetSwitchEntity(
            address=2600,
            bit=2,
            name="Heat/cool mode",
            device=ClivetDevice.HEAT_PUMP,
            coordinator=coordinator,
        ),
        ClivetSwitchEntity(
            address=2600,
            bit=2,
            name="Cool/heat mode",
            device=ClivetDevice.HEAT_PUMP,
            coordinator=coordinator,
            invert=True,
        ),
        ClivetSwitchEntity(
            address=2600,
            bit=4,
            name="DHW only mode",
            device=ClivetDevice.HEAT_PUMP,
            coordinator=coordinator,
        ),
        ClivetSwitchEntity(
            address=2600,
            bit=9,
            name="Room thermoregulation request",
            device=ClivetDevice.HEAT_PUMP,
            coordinator=coordinator,
        ),
        ClivetSwitchEntity(
            address=2601,
            bit=2,
            name="Enable remote unit mode",
            device=ClivetDevice.HEAT_PUMP,
            coordinator=coordinator,
        ),
        ClivetSwitchEntity(
            address=2601,
            bit=4,
            name="Enable remote DHW only",
            device=ClivetDevice.HEAT_PUMP,
            coordinator=coordinator,
        ),
        ClivetSwitchEntity(
            address=2601,
            bit=5,
            name="Enable remote unit state",
            device=ClivetDevice.HEAT_PUMP,
            coordinator=coordinator,
        ),
        ClivetSwitchEntity(
            address=2601,
            bit=15,
            name="Enable remote demand limit",
            device=ClivetDevice.HEAT_PUMP,
            coordinator=coordinator,
        ),
        ClivetSwitchEntity(
            address=2602,
            bit=1,
            name="Enable thermoregulation request",
            device=ClivetDevice.HEAT_PUMP,
            coordinator=coordinator,
        ),
        ClivetSwitchEntity(
            address=2602,
            bit=3,
            name="Enable remote DHW control",
            device=ClivetDevice.HEAT_PUMP,
            coordinator=coordinator,
        ),
        ClivetSwitchEntity(
            address=2709,
            bit=0,
            name="Enable remote DHW control",
            device=ClivetDevice.DHW,
            coordinator=coordinator,
        ),
        ClivetSwitchEntity(
            address=2709,
            bit=1,
            name="Enable remote storage tank setpoint",
            device=ClivetDevice.DHW,
            coordinator=coordinator,
        ),
        ClivetSwitchEntity(
            address=2709,
            bit=2,
            name="Enable remote DHW range",
            device=ClivetDevice.DHW,
            coordinator=coordinator,
        ),
        ClivetSwitchEntity(
            address=2709,
            bit=3,
            name="Enable remote maintenance setpoint",
            device=ClivetDevice.DHW,
            coordinator=coordinator,
        ),
        ClivetSwitchEntity(
            address=2709,
            bit=4,
            name="Enable remote anti-legionella setpoint",
            device=ClivetDevice.DHW,
            coordinator=coordinator,
        ),
        ClivetSwitchEntity(
            address=2709,
            bit=6,
            name="Enable remote anti-legionionella interval",
            device=ClivetDevice.DHW,
            coordinator=coordinator,
        ),
    ]
    async_add_entities(entities, True)


class ClivetSwitchEntity(ClivetBooleanBaseEntity, SwitchEntity):
    @callback
    def _handle_coordinator_update(self) -> None:
        data = self.coordinator.data.get(self.address)
        self._attr_is_on = self.decode_bool_value(data) if data is not None else None
        self.async_write_ha_state()

    async def async_turn_on(self, **kwargs: Any) -> None:
        assert self.bit is not None
        await self.coordinator.set_modbus_bit(self.address, self.bit, not self.invert)

    async def async_turn_off(self, **kwargs: Any) -> None:
        assert self.bit is not None
        await self.coordinator.set_modbus_bit(self.address, self.bit, self.invert)
