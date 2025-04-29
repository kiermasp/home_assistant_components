# External Blinds Integration for Home Assistant

This integration allows you to control external blinds in Home Assistant using switch entities and binary sensors.

## Features

- Control external blinds using switch entities
- Trigger blind movement using binary sensors
- Configurable open and close durations
- Support for both manual configuration and config flow

## Installation

1. Copy the `custom_components/external_blinds` directory to your Home Assistant's `custom_components` directory
2. Restart Home Assistant
3. Add the integration through the UI or configuration.yaml

## Configuration

### Config Flow (Recommended)

1. Go to Home Assistant's Configuration > Integrations
2. Click the "+ Add Integration" button
3. Search for "External Blinds"
4. Follow the configuration steps:
   - Select the switch entity for moving the blind up
   - Select the switch entity for moving the blind down
   - Select the binary sensor that triggers the blind to move up
   - Select the binary sensor that triggers the blind to move down
   - (Optional) Set the time in seconds for the blind to fully close
   - (Optional) Set the time in seconds for the blind to fully open

### Configuration.yaml

```yaml
external_blinds:
  up_switch: switch.blind_up
  down_switch: switch.blind_down
  up_trigger: binary_sensor.blind_up_trigger
  down_trigger: binary_sensor.blind_down_trigger
  close_time: 30  # Optional, default is 30 seconds
  open_time: 30   # Optional, default is 30 seconds
```

## How it Works

1. When the up trigger binary sensor turns on, the up switch is activated for the specified duration
2. When the down trigger binary sensor turns on, the down switch is activated for the specified duration
3. The switches are automatically turned off after the specified duration

## Requirements

- Home Assistant 2023.1.0 or newer
- Switch entities to control the blind motors
- Binary sensor entities to trigger the blind movement
