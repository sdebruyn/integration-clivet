"""Config flow for the Clivet (modbus) integration."""

from __future__ import annotations

import logging
from typing import Any

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult

from .const import (
    CONF_CONNECTION_TYPE,
    DOMAIN,
    MODBUS_NETWORK_SCHEMA,
    MODBUS_SELECTION_SCHEMA,
    MODBUS_SERIAL_SCHEMA,
    ClivetNetworkModbusConnectionType,
)
from .coordinator import ClivetCoordinator
from .exceptions import CannotConnect

_LOGGER = logging.getLogger(__name__)


_selection_map = {
    ClivetNetworkModbusConnectionType.NETWORK: MODBUS_NETWORK_SCHEMA,
    ClivetNetworkModbusConnectionType.SERIAL: MODBUS_SERIAL_SCHEMA,
}


async def validate_input(data: dict[str, Any]) -> None:
    client = ClivetCoordinator.build_client(data)
    try:
        connected = await client.connect()
    except Exception as e:
        _LOGGER.error("Failed to connect to Modbus server: %s", e)
        raise CannotConnect from e
    else:
        if not connected:
            raise CannotConnect("Could not connect to Modbus server")
    client.close()


class ClivetConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Clivet."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            connection_type = user_input.get(CONF_CONNECTION_TYPE)
            if connection_type in _selection_map:
                # Store the connection type and proceed to the specific configuration step
                return await getattr(self, f"async_step_{connection_type}")(None)

            _LOGGER.error("Unknown connection type: %s", connection_type)
            errors["base"] = "unknown"

        return self.async_show_form(
            data_schema=MODBUS_SELECTION_SCHEMA,
            errors=errors,
        )

    async def _async_step_connection_config(
        self,
        connection_type: ClivetNetworkModbusConnectionType,
        schema: Any,
        user_input: dict[str, Any] | None = None,
    ) -> ConfigFlowResult:
        """Handle connection configuration for any connection type."""
        errors: dict[str, str] = {}

        if user_input is not None:
            self._async_abort_entries_match(user_input)
            try:
                await validate_input(user_input)
                return self.async_create_entry(title="Clivet", data=user_input)
            except CannotConnect:
                errors["base"] = "cannot_connect"
            except Exception:
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"

        return self.async_show_form(
            data_schema=schema,
            errors=errors,
            step_id=connection_type.value,
        )

    async def async_step_network(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle network modbus configuration."""
        return await self._async_step_connection_config(
            ClivetNetworkModbusConnectionType.NETWORK,
            MODBUS_NETWORK_SCHEMA,
            user_input,
        )

    async def async_step_serial(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle serial modbus configuration."""
        return await self._async_step_connection_config(
            ClivetNetworkModbusConnectionType.SERIAL,
            MODBUS_SERIAL_SCHEMA,
            user_input,
        )
