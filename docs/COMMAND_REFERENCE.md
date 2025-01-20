# OBD-II Command Reference Guide

## Common OBD-II Commands

### Mode 01 - Show Current Data

| Name | PID | Command | Description | Units |
|------|-----|---------|-------------|-------|
| Engine RPM | 0C | 010C | Current engine RPM | RPM = (A×256+B)÷4 |
| Vehicle Speed | 0D | 010D | Current vehicle speed | km/h |
| Engine Coolant Temp | 05 | 0105 | Engine coolant temperature | °C = A-40 |
| Engine Load | 04 | 0104 | Calculated engine load | % = A×100÷255 |
| Throttle Position | 11 | 0111 | Throttle position | % = A×100÷255 |
| Fuel Level | 2F | 012F | Fuel tank level input | % = A×100÷255 |
| Distance with MIL | 21 | 0121 | Distance since MIL turned on | km |
| O2 Voltage | 14 | 0114 | O2 Sensor 1 voltage | V = A÷200 |

### Mode 03 - Show Stored DTCs
Command: 03
- Returns stored diagnostic trouble codes
- Format: P/C/B/U + 4 digits

### Mode 04 - Clear DTCs
Command: 04
- Clears stored trouble codes
- Also clears:
  - Freeze frame data
  - O2 sensor test data
  - Status since DTCs cleared
  - MIL ("Check Engine Light")

### Mode 09 - Vehicle Information
| Name | PID | Command | Description |
|------|-----|---------|-------------|
| VIN | 02 | 0902 | Vehicle Identification Number |
| Calibration ID | 04 | 0904 | Calibration ID |
| CVN | 06 | 0906 | Calibration Verification Numbers |

## Example Command Storage

### Basic Engine Monitoring
```bash
# Store RPM command
python src/tools/store_command.py --port COM3 --name "RPM" --type 0x01 --data "010C"

# Store Speed command
python src/tools/store_command.py --port COM3 --name "Speed" --type 0x01 --data "010D"

# Store Temperature command
python src/tools/store_command.py --port COM3 --name "Temp" --type 0x01 --data "0105"
```

### Diagnostic Commands
```bash
# Store Read DTCs command
python src/tools/store_command.py --port COM3 --name "Read DTCs" --type 0x03 --data "03"

# Store Clear DTCs command
python src/tools/store_command.py --port COM3 --name "Clear DTCs" --type 0x04 --data "04"
```

### Vehicle Info Commands
```bash
# Store Read VIN command
python src/tools/store_command.py --port COM3 --name "Read VIN" --type 0x09 --data "0902"
```

## Command Management

### List Stored Commands
```bash
python src/tools/store_command.py --port COM3 --list
```

### Remove Command
```bash
python src/tools/store_command.py --port COM3 --remove 1  # Remove first command
```

## Tips for Command Usage

1. **Command Priority**
   - Store most frequently used commands first
   - Keep critical diagnostic commands easily accessible
   - Group related commands together

2. **Command Naming**
   - Use short, clear names (max 12 chars)
   - Include units if relevant (e.g., "RPM" vs "Speed_KPH")
   - Use consistent naming convention

3. **Safety Considerations**
   - Test commands via PC first
   - Verify responses before storing
   - Document command functions
   - Be cautious with clearing codes

4. **Offline Usage**
   - Store essential commands before disconnecting
   - Verify all commands work standalone
   - Keep a backup of command list
   - Test in safe conditions first

## Troubleshooting

### Invalid Responses
- Verify command format
- Check vehicle support for PID
- Ensure proper connection
- Try reinitializing connection

### No Response
- Check cable connections
- Verify ignition is on
- Confirm command syntax
- Try basic commands first

### Error Messages
- Document error codes
- Check command compatibility
- Verify timing requirements
- Consider vehicle state

## Additional Resources

- [OBD-II PIDs](https://en.wikipedia.org/wiki/OBD-II_PIDs)
- [SAE J1979 Standard](https://www.sae.org/standards/content/j1979_201702/)
- [ELM327 Commands](https://www.elmelectronics.com/help/obd/commands/)
- [DTC Database](https://www.troublecodes.net/)
