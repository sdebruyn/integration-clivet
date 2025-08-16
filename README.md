# Clivet Integration for Home Assistant

[![GitHub Release][releases-shield]][releases]
[![License][license-shield]](LICENSE)

[![HACS][hacsbadge]][hacs]

A Home Assistant integration for Clivet Sphera-T heat pumps that provides comprehensive monitoring and control via Modbus communication.

## Features

This integration exposes your Clivet heat pump as multiple devices in Home Assistant:

### 🔥 Heat Pump Control

- **Water Heater Entity**: Full control with multiple operation modes (Heat Pump, Electric, Performance, Eco)
- **Temperature Control**: Set target temperatures for both storage and boost modes
- **System Status**: Monitor and control overall system operation
- **Operating Modes**: Switch between heating/cooling, DHW-only mode, and more
- **Thermoregulation**: Enable/disable the heat pump for heating/cooling your home

### 📊 Comprehensive Monitoring

- **Temperature Sensors**: Indoor/outdoor temperatures, water temperatures, setpoints
- **Performance Metrics**: Compressor operation hours, electrical power consumption, flow rates
- **System Status**: Real-time operating modes, defrost cycles, alarms
- **DHW (Domestic Hot Water)**: Storage temperature, resistance operation, anti-legionella status

### ⚙️ Advanced Controls

- **Configurable Parameters**: Demand limits, sanitary bands, anti-legionella settings
- **Remote Control**: Enable/disable various remote control functions
- **Safety Features**: Multiple alarm and error monitoring

### 🔧 Technical Monitoring

- **Compressor Data**: Frequencies, pressures, temperatures, electrical parameters
- **Flow Management**: Primary and DHW circuit flow rates, total consumption
- **Diagnostics**: Comprehensive error codes and system status information

## Installation

### HACS (Recommended)

1. Open HACS in your Home Assistant instance
2. Go to "Integrations"
3. Click the three dots in the top right corner and select "Custom repositories"
4. Add `https://github.com/sdebruyn/integration-clivet` as an Integration repository
5. Click "Install" on the Clivet integration
6. Restart Home Assistant

### Manual Installation

1. Download the latest release from the [releases page][releases]
2. Extract the contents to your `custom_components/clivet` directory
3. Restart Home Assistant

## Configuration

### Prerequisites

**Important**: You must manually connect your heat pump to your Home Assistant server over Modbus. This integration requires a direct Modbus connection to the heat pump's main board.

#### Connection Options

1. **USB to RS485 Adapter**: Connect a USB to RS485 stick directly to your Home Assistant server, then wire it to the heat pump's Modbus terminals on the main board.

2. **Networked Modbus Server**: Use a network-based Modbus gateway/server (such as a Modbus TCP/IP converter) connected to the heat pump's main board, then connect to it over your network.

#### Important Limitations

- **Only one Modbus connection is supported**: It is impossible to have the thermostat or other Modbus devices connected to the heat pump at the same time as this integration.
- **Exclusive access required**: The integration needs exclusive access to the Modbus connection points.
- **Consult your manual**: All Modbus connection points and wiring details are indicated in your heat pump's manual.

### Setup

1. Go to **Settings** → **Devices & Services** in Home Assistant
2. Click **Add Integration** and search for "Clivet"
3. Choose your connection type:
   - **Network**: For TCP/UDP Modbus over network
   - **Serial/USB**: For direct serial connection

#### Network Configuration

- **Host**: IP address of your Modbus device/gateway
- **Port**: Modbus port (default: 502)
- **Protocol**: TCP or UDP (default: TCP)
- **Slave ID**: Device address (default: 2)

#### Serial Configuration

- **Port**: Serial port path (e.g., `/dev/ttyUSB0`)
- **Baudrate**: Communication speed (default: 9600)
- **Parity**: Parity setting (default: N)
- **Slave ID**: Device address (default: 2)

## Usage

Once configured, the integration will create several device entities:

### Water Heater

The main water heater entity supports:

- **Operation Modes**: Off, Heat Pump, Electric, Performance, Eco
- **Temperature Control**: Adjustable target temperatures
- **Status Monitoring**: Current temperature, operation state

#### Operation Mode Mapping

The Home Assistant operation modes correspond to the heat pump's internal terminology:

- **Eco** = Maintenance mode
- **Heat Pump** = Storage mode  
- **Electric** = Resistance only mode
- **Performance** = Boost mode

### Sensors

Numerous sensors provide real-time data:

- Temperature sensors (°C)
- Power consumption (kW)
- Flow rates (L/min)
- Operating hours and cycles
- Pressure readings (bar)
- Electrical parameters (V, A, Hz)

### Controls

Configurable number entities for:

- Demand limits
- Temperature setpoints
- Anti-legionella settings
- Time intervals

### Binary Sensors

Status indicators for:

- Heating/cooling modes
- Alarms and errors
- Operation states
- Safety features

## Requirements

- **Home Assistant**: 2025.8.0 or later

## Troubleshooting

### Connection Issues

1. Verify network connectivity to your heat pump
2. Check Modbus settings and slave ID
3. Ensure firewall rules allow Modbus communication (port 502)
4. For serial connections, verify port permissions and settings

### Missing Entities

- Some entities may not appear if the corresponding features aren't available on your model
- Check the integration logs for any communication errors

### Logs

Enable debug logging by adding to your `configuration.yaml`:

```yaml
logger:
  logs:
    custom_components.clivet: debug
    pymodbus: debug
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Development Setup

1. Clone this repository
2. Install dependencies: `uv sync`
3. Run linting: `uv run ruff check`
4. Run formatting: `uv run ruff format`

## Support

- **Issues**: [GitHub Issues][issues]
- **Documentation**: [GitHub Repository][repository]

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

[releases-shield]: https://img.shields.io/github/release/sdebruyn/integration-clivet.svg?style=for-the-badge
[releases]: https://github.com/sdebruyn/integration-clivet/releases
[license-shield]: https://img.shields.io/github/license/sdebruyn/integration-clivet.svg?style=for-the-badge
[hacsbadge]: https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge
[hacs]: https://github.com/hacs/integration
[issues]: https://github.com/sdebruyn/integration-clivet/issues
[repository]: https://github.com/sdebruyn/integration-clivet
