from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .coordinator import ClivetCoordinator
from .entity import ClivetBooleanBaseEntity, ClivetDevice


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    coordinator = config_entry.runtime_data
    entity_lists: list[list[ClivetBinarySensorEntity]] = [
        [
            ClivetBinarySensorEntity(
                address=4222,
                name="Boiler control / Auxiliary heater",
                coordinator=coordinator,
                device=ClivetDevice.HEAT_PUMP,
            ),
            ClivetStatusMapSplitSensorEntity(
                address=4263,
                bit=1,
                bit_value=False,
                name="Cooling mode",
                coordinator=coordinator,
                device=ClivetDevice.HEAT_PUMP,
                device_class=BinarySensorDeviceClass.COLD,
            ),
            ClivetStatusMapSplitSensorEntity(
                address=4263,
                bit=1,
                bit_value=True,
                name="Heating mode",
                coordinator=coordinator,
                device=ClivetDevice.HEAT_PUMP,
                device_class=BinarySensorDeviceClass.HEAT,
            ),
        ],
        ClivetStatusMapSensorEntity.from_status_map(
            address=2801,
            status_map={
                3: ("Anti-legionella", BinarySensorDeviceClass.RUNNING),
            },
            coordinator=coordinator,
            device=ClivetDevice.DHW,
        ),
        ClivetStatusMapSensorEntity.from_status_map(
            address=2803,
            status_map={
                0: "Resistance",
                1: ("Pump", BinarySensorDeviceClass.RUNNING),
            },
            coordinator=coordinator,
            device=ClivetDevice.DHW,
        ),
        ClivetStatusMapSensorEntity.from_status_map(
            address=3000,
            coordinator=coordinator,
            device=ClivetDevice.HEAT_PUMP,
            status_map={
                0: ("Alarm: ALL_TIMEOUT_TAST_e00", BinarySensorDeviceClass.PROBLEM),
                1: ("Alarm: ERR_SONDA_IN_E01", BinarySensorDeviceClass.PROBLEM),
                2: ("Alarm: ERR_SONDA_OUT_E02", BinarySensorDeviceClass.PROBLEM),
                3: ("Alarm: ERR_SONDA_EXT_E03", BinarySensorDeviceClass.PROBLEM),
                4: ("Alarm: ERR_SONDA_BATTERIA_E04", BinarySensorDeviceClass.PROBLEM),
                8: ("Alarm: ERR_SONDA_PRESS1_E08", BinarySensorDeviceClass.PROBLEM),
                14: ("Alarm: ALL_HP1_CIRC1_F01", BinarySensorDeviceClass.PROBLEM),
                15: ("Alarm: ALL_LP1_CIRC1_F02", BinarySensorDeviceClass.PROBLEM),
            },
        ),
        ClivetStatusMapSensorEntity.from_status_map(
            address=3001,
            coordinator=coordinator,
            device=ClivetDevice.HEAT_PUMP,
            status_map={
                0: ("Alarm: ALL_TERMICA1_E26", BinarySensorDeviceClass.PROBLEM),
                4: (
                    "Alarm: ALL_TERMICO_VENTIL_CIRC1_E23",
                    BinarySensorDeviceClass.PROBLEM,
                ),
                15: ("Alarm: ALL_FLUSSO_POMPA_UT_I01", BinarySensorDeviceClass.PROBLEM),
            },
        ),
        ClivetStatusMapSensorEntity.from_status_map(
            address=3002,
            coordinator=coordinator,
            device=ClivetDevice.HEAT_PUMP,
            status_map={
                3: ("Alarm: ALL_GELO_UT_I03", BinarySensorDeviceClass.PROBLEM),
                6: ("Alarm: ALL_CARICO_I06", BinarySensorDeviceClass.PROBLEM),
                7: ("Alarm: ALL_DELTA_T_INC_I07", BinarySensorDeviceClass.PROBLEM),
                9: ("Alarm: PREALL_ANTIGELO_i09", BinarySensorDeviceClass.PROBLEM),
                11: ("Alarm: ALL_TIN_FUORI_NORM_i11", BinarySensorDeviceClass.PROBLEM),
                12: (
                    "Alarm: SCAMB_INS_SEC/PRIM (LATO ACS)_i12",
                    BinarySensorDeviceClass.PROBLEM,
                ),
                13: ("Alarm: ALL_GELO_AMBIENTE_I13", BinarySensorDeviceClass.PROBLEM),
                15: ("Alarm: ALL_TIMEOUT_POTENZA_e14", BinarySensorDeviceClass.PROBLEM),
            },
        ),
        ClivetStatusMapSensorEntity.from_status_map(
            address=3003,
            coordinator=coordinator,
            device=ClivetDevice.HEAT_PUMP,
            status_map={1: ("Alarm: ALL_MAX_TS_F10", BinarySensorDeviceClass.PROBLEM)},
        ),
        ClivetStatusMapSensorEntity.from_status_map(
            address=3004,
            coordinator=coordinator,
            device=ClivetDevice.HEAT_PUMP,
            status_map={
                0: ("Alarm: ERR_SONDA_SOLARE_E15", BinarySensorDeviceClass.PROBLEM),
                2: ("Alarm: ERR_SONDA_ACS_SUP_E16", BinarySensorDeviceClass.PROBLEM),
                6: ("Alarm: ERR_SONDA_SCARICO_E18", BinarySensorDeviceClass.PROBLEM),
                7: ("Alarm: ERR_SONDA_ASP_E19", BinarySensorDeviceClass.PROBLEM),
                14: ("Alarm: ALL_CARICO_ACS_I15", BinarySensorDeviceClass.PROBLEM),
            },
        ),
        ClivetStatusMapSensorEntity.from_status_map(
            address=3006,
            coordinator=coordinator,
            device=ClivetDevice.HEAT_PUMP,
            status_map={
                2: ("Alarm: ALLARME_INVERTER_E32", BinarySensorDeviceClass.PROBLEM),
                3: (
                    "Alarm: ERR_SONDA_IN_SCA_ACS_IMP_Sol_E58",
                    BinarySensorDeviceClass.PROBLEM,
                ),
                6: ("Alarm: ALL_CALDAIA_E46", BinarySensorDeviceClass.PROBLEM),
                7: ("Alarm: ALL_TIMEOUT_IO_E47", BinarySensorDeviceClass.PROBLEM),
                9: ("Alarm: ALL_HT_IMPIANTO (I22)", BinarySensorDeviceClass.PROBLEM),
                10: ("Alarm: ALL_OUT_ENVELOPE (F22)", BinarySensorDeviceClass.PROBLEM),
            },
        ),
        ClivetStatusMapSensorEntity.from_status_map(
            address=3007,
            coordinator=coordinator,
            device=ClivetDevice.HEAT_PUMP,
            status_map={
                0: (
                    "Alarm: CONDENSER_OUTLET_HT_PROTECTION_E59",
                    BinarySensorDeviceClass.PROBLEM,
                ),
                1: ("Alarm: ERR_ODU_POWER_SUPPLY_E60", BinarySensorDeviceClass.PROBLEM),
                2: (
                    "Alarm: FAN_SPEED_IN_A_AREA_10MIN_F22",
                    BinarySensorDeviceClass.PROBLEM,
                ),
                3: ("Alarm: ERR_ODU_EEPROM_E61", BinarySensorDeviceClass.PROBLEM),
                4: ("Alarm: ALL_FAN_E62", BinarySensorDeviceClass.PROBLEM),
                5: ("Alarm: LP_PROTECTION_F23", BinarySensorDeviceClass.PROBLEM),
                6: ("Alarm: DC_GEN_VOLT_TOO_LOW_E63", BinarySensorDeviceClass.PROBLEM),
            },
        ),
        ClivetStatusMapSensorEntity.from_status_map(
            address=4263,
            status_map={
                0: "Status",
                3: "Only boiler",
                4: "Only DHW",
                5: "Defrosting",
                6: "Cycle reverse",
                7: ("Any alarm", BinarySensorDeviceClass.PROBLEM),
                8: "DHW valve",
                10: "Boiler / additional heating element",
                11: "Oil return",
            },
            coordinator=coordinator,
            device=ClivetDevice.HEAT_PUMP,
        ),
        ClivetStatusMapSensorEntity.from_status_map(
            address=4264,
            status_map={
                4: "Production (HP)",
                5: "Production (boiler)",
                7: "In anti-legionella",
                8: "Pump status",
            },
            coordinator=coordinator,
            device=ClivetDevice.DHW,
        ),
        ClivetStatusMapSensorEntity.from_status_map(
            address=4314,
            status_map={
                0: "Status",
                1: "Defrosting",
                3: "Oil return",
                5: "Test mode",
            },
            coordinator=coordinator,
            device=ClivetDevice.COMPRESSOR,
        ),
    ]
    async_add_entities(
        [entity for entity_list in entity_lists for entity in entity_list], True
    )


class ClivetBinarySensorEntity(ClivetBooleanBaseEntity, BinarySensorEntity):
    def __init__(
        self,
        *,
        address: int,
        name: str,
        device: ClivetDevice,
        coordinator: ClivetCoordinator,
        device_class: BinarySensorDeviceClass | None = None,
        bit: int | None = None,
    ) -> None:
        self._attr_device_class = device_class
        super().__init__(
            address=address, name=name, device=device, coordinator=coordinator, bit=bit
        )

    @callback
    def _handle_coordinator_update(self) -> None:
        data = self.coordinator.data.get(self.address)
        self._attr_is_on = self.decode_bool_value(data) if data is not None else None
        self.async_write_ha_state()


class ClivetStatusMapSensorEntity(ClivetBinarySensorEntity):
    def __init__(
        self,
        address: int,
        bit: int,
        name: str,
        device: ClivetDevice,
        coordinator: ClivetCoordinator,
        device_class: BinarySensorDeviceClass | None = None,
    ) -> None:
        self._attr_device_class = device_class
        super().__init__(
            address=address, name=name, device=device, coordinator=coordinator, bit=bit
        )

    @classmethod
    def from_status_map(
        cls,
        address: int,
        status_map: dict[int, str | tuple[str, BinarySensorDeviceClass]],
        device: ClivetDevice,
        coordinator: ClivetCoordinator,
    ) -> list[ClivetBinarySensorEntity]:
        return [
            cls(
                address=address,
                name=val if isinstance(val, str) else val[0],
                bit=bit,
                device=device,
                coordinator=coordinator,
                device_class=val[1] if isinstance(val, tuple) else None,
            )
            for bit, val in status_map.items()
        ]


class ClivetStatusMapSplitSensorEntity(ClivetStatusMapSensorEntity):
    def __init__(
        self,
        address: int,
        bit: int,
        bit_value: bool,
        name: str,
        device: ClivetDevice,
        coordinator: ClivetCoordinator,
        device_class: BinarySensorDeviceClass | None = None,
    ) -> None:
        self.bit_value = bit_value
        super().__init__(
            address=address,
            name=name,
            coordinator=coordinator,
            device=device,
            bit=bit,
            device_class=device_class,
        )
        self._attr_unique_id = f"{super().unique_id}_{int(bit_value)}"

    def decode_bool_value(self, register: int) -> bool | None:
        return super().decode_bool_value(register) == self.bit_value
