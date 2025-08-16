from enum import StrEnum

import voluptuous as vol

from homeassistant.const import (
    CONF_HOST,
    CONF_PORT,
    CONF_PROTOCOL,
    CONF_SLAVE,
    Platform,
)
import homeassistant.helpers.config_validation as cv

DOMAIN = "clivet"
PLATFORMS: list[Platform] = [
    Platform.BINARY_SENSOR,
    Platform.NUMBER,
    Platform.SENSOR,
    Platform.SWITCH,
    Platform.WATER_HEATER,
]

CONF_BAUDRATE = "baudrate"
CONF_BYTESIZE = "bytesize"
CONF_PARITY = "parity"
CONF_STOPBITS = "stopbits"
CONF_CONNECTION_TYPE = "connection_type"


class ClivetNetworkModbusProtocol(StrEnum):
    """Enum for Clivet Modbus protocols."""

    TCP = "tcp"
    UDP = "udp"


class ClivetNetworkModbusConnectionType(StrEnum):
    """Enum for Clivet Modbus connection types."""

    NETWORK = "network"
    SERIAL = "serial"


MODBUS_NETWORK_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_HOST): str,
        vol.Required(CONF_PORT, default=502): cv.port,
        vol.Required(CONF_SLAVE, default=2): int,  # Default device ID
        vol.Required(CONF_PROTOCOL, default=ClivetNetworkModbusProtocol.TCP): vol.In(
            list(ClivetNetworkModbusProtocol)
        ),
    }
)
MODBUS_SERIAL_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_PORT): str,
        vol.Required(CONF_BAUDRATE, default=9600): vol.In([4800, 9600, 19200]),
        vol.Required(CONF_PARITY, default="N"): vol.In(["N", "E", "O"]),
        vol.Required(CONF_SLAVE, default=2): cv.positive_int,  # Default device ID
    }
)
MODBUS_SELECTION_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_CONNECTION_TYPE): vol.In(
            list(ClivetNetworkModbusConnectionType)
        ),
    }
)
