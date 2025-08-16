from homeassistant.exceptions import HomeAssistantError


class OfflineException(Exception):
    """Exception raised when the Modbus client is offline."""

    def __init__(self, message: str = "Modbus client is offline") -> None:
        super().__init__(message)


class CommunicationException(Exception):
    """Exception raised for communication errors with the Modbus client."""

    def __init__(self, message: str = "Communication error with Modbus client") -> None:
        super().__init__(message)


class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect."""
