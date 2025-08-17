from collections.abc import Mapping
from datetime import timedelta
import logging
from typing import Any

from pymodbus import ModbusException
from pymodbus.client import (
    AsyncModbusSerialClient,
    AsyncModbusTcpClient,
    AsyncModbusUdpClient,
)
from pymodbus.client.base import ModbusBaseClient

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, CONF_PORT, CONF_PROTOCOL, CONF_SLAVE
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import CONF_BAUDRATE, CONF_PARITY, DOMAIN, ClivetNetworkModbusProtocol
from .exceptions import CommunicationException, OfflineException


class ClivetCoordinator(DataUpdateCoordinator[dict[int, int | None]]):
    def __init__(
        self, hass: HomeAssistant, config_entry: ConfigEntry, logger: logging.Logger
    ) -> None:
        self.client = self.build_client(config_entry.data)
        self.device_id = config_entry.data[CONF_SLAVE]
        self.unique_id = self.build_unique_id(config_entry.data)
        super().__init__(
            hass,
            update_interval=timedelta(seconds=10),
            name=DOMAIN,
            logger=logger,
            config_entry=config_entry,
        )

    @staticmethod
    def build_client(data: Mapping[str, Any]) -> ModbusBaseClient:
        """Create a new Modbus client."""
        if CONF_PROTOCOL in data:
            match data[CONF_PROTOCOL]:
                case ClivetNetworkModbusProtocol.TCP:
                    return AsyncModbusTcpClient(
                        host=data[CONF_HOST],
                        port=data[CONF_PORT],
                        timeout=10,
                    )
                case ClivetNetworkModbusProtocol.UDP:
                    return AsyncModbusUdpClient(
                        host=data[CONF_HOST],
                        port=data[CONF_PORT],
                        timeout=10,
                    )
        if CONF_BAUDRATE in data:
            return AsyncModbusSerialClient(
                port=data[CONF_PORT],
                baudrate=data[CONF_BAUDRATE],
                parity=data[CONF_PARITY],
                timeout=10,
            )
        raise ValueError("Invalid Modbus client configuration")

    @staticmethod
    def build_unique_id(data: Mapping[str, Any]) -> str:
        """Build a unique ID for the coordinator."""
        properties = [
            CONF_HOST,
            CONF_PORT,
            CONF_SLAVE,
        ]
        values = map(
            lambda x: str(x),
            filter(
                lambda x: x is not None, [data.get(prop, None) for prop in properties]
            ),
        )
        return "_".join(values)

    def model_name(self) -> str:
        device_size = self.data.get(4312, None)
        model_type = self.data.get(4318, None)
        model_name = "Sphera-T"
        if device_size is not None:
            model_name += f" ({device_size} kW)"
        match model_type:
            case 1:
                model_name += " bdr"
            case 2:
                model_name += " M-thermal"
            case 3:
                model_name += " Monobloc"
        return model_name

    async def async_shutdown(self) -> None:
        await super().async_shutdown()
        self.client.close()

    async def refresh_single_address(self, address: int) -> None:
        result = await self._get_modbus_register(address)
        if result:
            self.data[address] = result[0]
        self.async_update_listeners()

    async def _async_update_data(self) -> dict[int, int | None]:
        data_dict: dict[int, int | None] = {}

        async def _retrieve_multiple_values(address: int, count: int) -> None:
            values = await self._get_modbus_register(address, count)
            if values is None:
                return
            for i in range(count):
                data_dict[address + i] = values[i]

        try:
            await _retrieve_multiple_values(2600, 18)
            await _retrieve_multiple_values(2700, 12)
            await _retrieve_multiple_values(2800, 7)
            await _retrieve_multiple_values(3000, 6)
            await _retrieve_multiple_values(4200, 79)
            await _retrieve_multiple_values(4300, 19)
            await _retrieve_multiple_values(7000, 6)
        except CommunicationException as e:
            raise UpdateFailed("Could not retrieve data from Modbus client") from e

        return data_dict

    async def _get_modbus_register(
        self, address: int, count: int = 1
    ) -> list[int] | None:
        """Fetch value from Modbus."""
        try:
            if not self.client.connected:
                connected = await self.client.connect()
                if not connected:
                    raise OfflineException
            result = await self.client.read_holding_registers(
                address, count=count, slave=self.device_id
            )
            if result.isError():
                self.logger.error(
                    "Error reading Modbus register at address %s: %s",
                    address,
                    result,
                )
                return None
        except ModbusException as e:
            self.logger.error("Error fetching data for address %s: %s", address, e)
            raise CommunicationException from e
        else:
            return result.registers

    async def set_modbus_register(self, address: int, value: int) -> None:
        """Set value to Modbus."""
        try:
            if not self.client.connected:
                connected = await self.client.connect()
                if not connected:
                    raise OfflineException
            result = await self.client.write_register(
                address, value, slave=self.device_id
            )
            if result.isError():
                self.logger.error(
                    "Error writing Modbus register at address %s: %s",
                    address,
                    result,
                )
                raise CommunicationException(
                    f"Error writing to Modbus register {address}"
                )

            await self.refresh_single_address(address)
        except ModbusException as e:
            self.logger.error("Error setting data for address %s: %s", address, e)
            raise CommunicationException from e

    async def set_modbus_bit(self, address: int, bit: int, value: bool) -> None:
        """Set a specific bit in a Modbus register."""
        try:
            if not self.client.connected:
                connected = await self.client.connect()
                if not connected:
                    raise OfflineException
            current_value = await self._get_modbus_register(address)
            if current_value is None:
                raise CommunicationException(
                    f"Could not read current value from register {address}"
                )

            # Modify the specific bit
            if value:
                new_value = current_value[0] | (1 << bit)
            else:
                new_value = current_value[0] & ~(1 << bit)

            if new_value == current_value[0]:
                return

            result = await self.client.write_register(
                address, new_value, slave=self.device_id
            )
            if result.isError():
                self.logger.error(
                    "Error writing Modbus register at address %s: %s",
                    address,
                    result,
                )
                raise CommunicationException(
                    f"Failed to write Modbus register {address}"
                )

            await self.refresh_single_address(address)
        except ModbusException as e:
            self.logger.error("Error setting bit for address %s: %s", address, e)
            raise CommunicationException from e
