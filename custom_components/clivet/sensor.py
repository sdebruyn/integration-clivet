from homeassistant.components.sensor import SensorEntity
from homeassistant.components.sensor.const import SensorDeviceClass, SensorStateClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    UnitOfElectricCurrent,
    UnitOfElectricPotential,
    UnitOfFrequency,
    UnitOfPower,
    UnitOfPressure,
    UnitOfTemperature,
    UnitOfTime,
    UnitOfVolume,
    UnitOfVolumeFlowRate,
)
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .coordinator import ClivetCoordinator
from .entity import ClivetDevice, ClivetNumericBaseEntity


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    coordinator = config_entry.runtime_data
    entities = [
        ClivetTemperatureSensorEntity(
            address=2804,
            name="Current setpoint",
            coordinator=coordinator,
            device=ClivetDevice.DHW,
        ),
        ClivetSensorEntity(
            address=2805,
            name="Resistance operation",
            unit=UnitOfTime.HOURS,
            coordinator=coordinator,
            device=ClivetDevice.DHW,
            state_class=SensorStateClass.TOTAL_INCREASING,
            device_class=SensorDeviceClass.DURATION,
        ),
        ClivetSensorEntity(
            address=2806,
            name="Resistance starts",
            unit=None,
            coordinator=coordinator,
            device=ClivetDevice.DHW,
        ),
        ClivetTemperatureSensorEntity(
            address=4200,
            name="Current setpoint",
            coordinator=coordinator,
            device=ClivetDevice.HEAT_PUMP,
        ),
        ClivetTemperatureSensorEntity(
            address=4201,
            name="Actual temperature difference (including compensation)",
            coordinator=coordinator,
            device=ClivetDevice.HEAT_PUMP,
        ),
        ClivetSensorEntity(
            address=4202,
            name="Timer relative to resource insertion ",
            coordinator=coordinator,
            device=ClivetDevice.HEAT_PUMP,
            unit=UnitOfTime.SECONDS,
            device_class=SensorDeviceClass.DURATION,
        ),
        ClivetSensorEntity(
            address=4203,
            name="Dynamic TimeScan relative to resource insertion ",
            coordinator=coordinator,
            device=ClivetDevice.HEAT_PUMP,
            unit=UnitOfTime.SECONDS,
            device_class=SensorDeviceClass.DURATION,
        ),
        ClivetTemperatureSensorEntity(
            address=4204,
            name="External T compensation",
            coordinator=coordinator,
            device=ClivetDevice.HEAT_PUMP,
        ),
        ClivetTemperatureSensorEntity(
            address=4205,
            name="Ambient T Compensation",
            coordinator=coordinator,
            device=ClivetDevice.HEAT_PUMP,
        ),
        ClivetTemperatureSensorEntity(
            address=4207,
            name="Charge compensation",
            coordinator=coordinator,
            device=ClivetDevice.HEAT_PUMP,
        ),
        ClivetTemperatureSensorEntity(
            address=4208,
            name="Duty Cycle compensation",
            coordinator=coordinator,
            device=ClivetDevice.HEAT_PUMP,
        ),
        ClivetTemperatureSensorEntity(
            address=4209,
            name="Compensation on duration",
            coordinator=coordinator,
            device=ClivetDevice.HEAT_PUMP,
        ),
        ClivetTemperatureSensorEntity(
            address=4210,
            name="Exchanger water inlet temperature (Return)",
            coordinator=coordinator,
            device=ClivetDevice.HEAT_PUMP,
        ),
        ClivetTemperatureSensorEntity(
            address=4211,
            name="Exchanger water outlet temperature (Supply)",
            coordinator=coordinator,
            device=ClivetDevice.HEAT_PUMP,
        ),
        ClivetTemperatureSensorEntity(
            address=4213,
            name="Outdoor air temperature",
            coordinator=coordinator,
            device=ClivetDevice.HEAT_PUMP,
        ),
        ClivetTemperatureSensorEntity(
            address=4215,
            name="DHW accumulation temperature (high probe)",
            coordinator=coordinator,
            device=ClivetDevice.HEAT_PUMP,
        ),
        ClivetSensorEntity(
            address=4216,
            name="Utility pump",
            unit="%",
            scale=0.1,
            coordinator=coordinator,
            device=ClivetDevice.HEAT_PUMP,
        ),
        ClivetSensorEntity(
            address=4219,
            name="Condensing pressure C1",
            unit=UnitOfPressure.BAR,
            scale=0.01,
            coordinator=coordinator,
            device=ClivetDevice.HEAT_PUMP,
            device_class=SensorDeviceClass.PRESSURE,
        ),
        ClivetSensorEntity(
            address=4220,
            name="Evaporating pressure C1",
            unit=UnitOfPressure.BAR,
            scale=0.01,
            coordinator=coordinator,
            device=ClivetDevice.HEAT_PUMP,
            device_class=SensorDeviceClass.PRESSURE,
        ),
        ClivetSensorEntity(
            address=4221,
            name="Auxiliary heater control signal (0-10V)",
            unit="%",
            scale=0.1,
            coordinator=coordinator,
            device=ClivetDevice.HEAT_PUMP,
        ),
        ClivetTemperatureSensorEntity(
            address=4223,
            name="boiler modulating (set)/ Boiler valves control",
            coordinator=coordinator,
            device=ClivetDevice.HEAT_PUMP,
        ),
        ClivetSensorEntity(
            address=4225,
            name="Thermoregulator request",
            unit="%",
            scale=0.1,
            coordinator=coordinator,
            device=ClivetDevice.HEAT_PUMP,
        ),
        ClivetSensorEntity(
            address=4226,
            name="Variable speed compressor (0-10V)",
            unit="%",
            scale=0.1,
            coordinator=coordinator,
            device=ClivetDevice.HEAT_PUMP,
        ),
        ClivetSensorEntity(
            address=4227,
            name="Compressor operating hours",
            unit=UnitOfTime.HOURS,
            coordinator=coordinator,
            device=ClivetDevice.HEAT_PUMP,
            state_class=SensorStateClass.TOTAL_INCREASING,
            device_class=SensorDeviceClass.DURATION,
        ),
        ClivetSensorEntity(
            address=4228,
            name="Compressor starts",
            unit=None,
            coordinator=coordinator,
            device=ClivetDevice.HEAT_PUMP,
            state_class=SensorStateClass.TOTAL_INCREASING,
        ),
        ClivetSensorEntity(
            address=4235,
            name="Electrical power absorbed",
            unit=UnitOfPower.KILO_WATT,
            coordinator=coordinator,
            device=ClivetDevice.COMPRESSOR,
            device_class=SensorDeviceClass.POWER,
            scale=0.1,
        ),
        ClivetSensorEntity(
            address=4236,
            name="Current M-ODU",
            unit=UnitOfElectricCurrent.AMPERE,
            coordinator=coordinator,
            device=ClivetDevice.COMPRESSOR,
            device_class=SensorDeviceClass.CURRENT,
            scale=0.1,
        ),
        ClivetSensorEntity(
            address=4237,
            name="Voltage M-ODU",
            unit=UnitOfElectricPotential.VOLT,
            coordinator=coordinator,
            device=ClivetDevice.COMPRESSOR,
            device_class=SensorDeviceClass.VOLTAGE,
        ),
        ClivetSensorEntity(
            address=4238,
            name="Frequency M-ODU",
            unit=UnitOfFrequency.HERTZ,
            coordinator=coordinator,
            device=ClivetDevice.COMPRESSOR,
            device_class=SensorDeviceClass.FREQUENCY,
            scale=0.1,
        ),
        ClivetTemperatureSensorEntity(
            address=4248,
            name="Return temperature",
            coordinator=coordinator,
            device=ClivetDevice.HEAT_PUMP,
        ),
        ClivetTemperatureSensorEntity(
            address=4249,
            name="Discharge temperature",
            coordinator=coordinator,
            device=ClivetDevice.HEAT_PUMP,
        ),
        ClivetSensorEntity(
            address=4252,
            name="Regolation valve opening percentage",
            unit="%",
            scale=0.1,
            coordinator=coordinator,
            device=ClivetDevice.HEAT_PUMP,
        ),
        ClivetSensorEntity(
            address=4262,
            name="Fan",
            unit=None,
            coordinator=coordinator,
            device=ClivetDevice.HEAT_PUMP,
            scale=0.1,
        ),
        ClivetTemperatureSensorEntity(
            address=4266,
            name="DHW setpoint",
            coordinator=coordinator,
            device=ClivetDevice.HEAT_PUMP,
        ),
        ClivetSensorEntity(
            address=4273,
            name="Primary flow rate",
            unit=UnitOfVolumeFlowRate.LITERS_PER_MINUTE,
            scale=0.1,
            coordinator=coordinator,
            device=ClivetDevice.HEAT_PUMP,
            device_class=SensorDeviceClass.VOLUME_FLOW_RATE,
        ),
        ClivetSensorEntity(
            address=4275,
            name="DHW circuit flow rate",
            unit=UnitOfVolumeFlowRate.LITERS_PER_MINUTE,
            scale=0.1,
            coordinator=coordinator,
            device=ClivetDevice.HEAT_PUMP,
            device_class=SensorDeviceClass.VOLUME_FLOW_RATE,
        ),
        ClivetSensorEntity(
            address=4276,
            name="DHW total consumption",
            unit=UnitOfVolume.LITERS,
            coordinator=coordinator,
            device=ClivetDevice.HEAT_PUMP,
            device_class=SensorDeviceClass.WATER,
            state_class=SensorStateClass.TOTAL_INCREASING,
            scale=0.1,
        ),
        ClivetStatusSensorEntity(
            address=4300,
            name="Set operating mode",
            device=ClivetDevice.COMPRESSOR,
            coordinator=coordinator,
            status_map={
                0: "Off",
                2: "Cooling",
                3: "Heating",
                4: "Forced Cooling",
                5: "Water Heating",
            },
        ),
        ClivetSensorEntity(
            address=4301,
            name="Requested work frequency",
            unit=UnitOfFrequency.HERTZ,
            coordinator=coordinator,
            device=ClivetDevice.COMPRESSOR,
            device_class=SensorDeviceClass.FREQUENCY,
        ),
        ClivetSensorEntity(
            address=4302,
            name="Operating work frequency",
            unit=UnitOfFrequency.HERTZ,
            coordinator=coordinator,
            device=ClivetDevice.COMPRESSOR,
            device_class=SensorDeviceClass.FREQUENCY,
        ),
        ClivetStatusSensorEntity(
            address=4303,
            name="M-ODU operating mode",
            device=ClivetDevice.COMPRESSOR,
            coordinator=coordinator,
            status_map={
                0: "Off",
                2: "Cooling",
                3: "Heating",
                4: "Forced Cooling",
                5: "Water Heating",
            },
        ),
        ClivetSensorEntity(
            address=4304,
            name="Fan speed",
            unit=None,
            coordinator=coordinator,
            device=ClivetDevice.COMPRESSOR,
            scale=0.1,
        ),
        ClivetTemperatureSensorEntity(
            address=4305,
            name="Condenser output temperature T3",
            coordinator=coordinator,
            device=ClivetDevice.COMPRESSOR,
        ),
        ClivetTemperatureSensorEntity(
            address=4306,
            name="Outdoor Temperature T4",
            coordinator=coordinator,
            device=ClivetDevice.COMPRESSOR,
        ),
        ClivetTemperatureSensorEntity(
            address=4307,
            name="Compressor discharge temperature Tp",
            coordinator=coordinator,
            device=ClivetDevice.COMPRESSOR,
        ),
        ClivetSensorEntity(
            address=4308,
            name="Inverter protection code",
            unit=None,
            coordinator=coordinator,
            device=ClivetDevice.COMPRESSOR,
        ),
        ClivetSensorEntity(
            address=4309,
            name="M-ODU absorbed current",
            unit=UnitOfElectricCurrent.AMPERE,
            coordinator=coordinator,
            device=ClivetDevice.COMPRESSOR,
            device_class=SensorDeviceClass.CURRENT,
        ),
        ClivetSensorEntity(
            address=4310,
            name="M-ODU voltage",
            unit=UnitOfElectricPotential.VOLT,
            coordinator=coordinator,
            device=ClivetDevice.COMPRESSOR,
            device_class=SensorDeviceClass.VOLTAGE,
        ),
        ClivetTemperatureSensorEntity(
            address=4311,
            name="Thermostatic opening degrees",
            coordinator=coordinator,
            device=ClivetDevice.COMPRESSOR,
        ),
        ClivetSensorEntity(
            address=4313,
            name="Error code",
            unit=None,
            coordinator=coordinator,
            device=ClivetDevice.COMPRESSOR,
        ),
        ClivetTemperatureSensorEntity(
            address=4315,
            name="Extraction temperature",
            coordinator=coordinator,
            device=ClivetDevice.COMPRESSOR,
        ),
        ClivetSensorEntity(
            address=4316,
            name="Pressure transducer 1",
            unit=UnitOfPressure.BAR,
            scale=0.01,
            coordinator=coordinator,
            device=ClivetDevice.COMPRESSOR,
            device_class=SensorDeviceClass.PRESSURE,
        ),
        ClivetSensorEntity(
            address=4317,
            name="Pressure transducer 2",
            unit=UnitOfPressure.BAR,
            scale=0.01,
            coordinator=coordinator,
            device=ClivetDevice.COMPRESSOR,
            device_class=SensorDeviceClass.PRESSURE,
        ),
        ClivetSensorEntity(
            address=7000,
            name="Lower frequency limit",
            unit=UnitOfFrequency.HERTZ,
            coordinator=coordinator,
            device=ClivetDevice.HEAT_PUMP,
            device_class=SensorDeviceClass.FREQUENCY,
        ),
        ClivetSensorEntity(
            address=7001,
            name="Upper frequency limit",
            unit=UnitOfFrequency.HERTZ,
            coordinator=coordinator,
            device=ClivetDevice.HEAT_PUMP,
            device_class=SensorDeviceClass.FREQUENCY,
        ),
        ClivetSensorEntity(
            address=7002,
            name="Thermoregulator requested frequency",
            unit=UnitOfFrequency.HERTZ,
            coordinator=coordinator,
            device=ClivetDevice.HEAT_PUMP,
            device_class=SensorDeviceClass.FREQUENCY,
        ),
        ClivetSensorEntity(
            address=7003,
            name="Requested outdoor unit frequency",
            unit=UnitOfFrequency.HERTZ,
            coordinator=coordinator,
            device=ClivetDevice.HEAT_PUMP,
            device_class=SensorDeviceClass.FREQUENCY,
        ),
        ClivetSensorEntity(
            address=7004,
            name="Current outdoor unit frequency",
            unit=UnitOfFrequency.HERTZ,
            coordinator=coordinator,
            device=ClivetDevice.HEAT_PUMP,
            device_class=SensorDeviceClass.FREQUENCY,
        ),
        ClivetSensorEntity(
            address=7005,
            name="Defrost mode frequency",
            unit=UnitOfFrequency.HERTZ,
            coordinator=coordinator,
            device=ClivetDevice.HEAT_PUMP,
            device_class=SensorDeviceClass.FREQUENCY,
        ),
    ]
    async_add_entities(entities, True)


class ClivetSensorEntity(ClivetNumericBaseEntity, SensorEntity):
    def __init__(
        self,
        *,
        address: int,
        name: str,
        unit: str | None,
        device: ClivetDevice,
        scale: float = 1,
        signed: bool = False,
        coordinator: ClivetCoordinator,
        state_class: SensorStateClass | None = SensorStateClass.MEASUREMENT,
        device_class: SensorDeviceClass | None = None,
    ) -> None:
        self._attr_native_unit_of_measurement = unit
        self._attr_state_class = state_class
        self._attr_device_class = device_class
        self.scale = scale
        self.signed = signed
        super().__init__(
            address=address,
            name=name,
            device=device,
            coordinator=coordinator,
            signed=signed,
            scale=scale,
        )

    @callback
    def _handle_coordinator_update(self) -> None:
        data = self.coordinator.data.get(self.address)
        self._attr_native_value = (
            self.decode_numeric_value(data) if data is not None else None
        )
        self.async_write_ha_state()


class ClivetTemperatureSensorEntity(ClivetSensorEntity):
    def __init__(
        self,
        *,
        address: int,
        name: str,
        device: ClivetDevice,
        coordinator: ClivetCoordinator,
    ) -> None:
        super().__init__(
            address=address,
            name=name,
            scale=0.1,
            signed=True,
            device=device,
            unit=UnitOfTemperature.CELSIUS,
            coordinator=coordinator,
            state_class=SensorStateClass.MEASUREMENT,
            device_class=SensorDeviceClass.TEMPERATURE,
        )


class ClivetStatusSensorEntity(ClivetSensorEntity):
    def __init__(
        self,
        *,
        address: int,
        name: str,
        status_map: dict[int, str],
        device: ClivetDevice,
        coordinator: ClivetCoordinator,
    ) -> None:
        self._attr_options = list(status_map.values())
        self.status_map = status_map
        super().__init__(
            address=address,
            name=name,
            unit=None,
            device=device,
            coordinator=coordinator,
            state_class=None,
            device_class=SensorDeviceClass.ENUM,
        )

    @callback
    def _handle_coordinator_update(self) -> None:
        data = self.coordinator.data.get(self.address)
        self._attr_native_value = (
            self.status_map.get(data, None) if data is not None else None
        )
        self.async_write_ha_state()
