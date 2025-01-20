# User Guide - Nokia 3310 CAN Bus Interface

## Overview

The Nokia 3310 CAN Bus Interface allows you to use your Nokia 3310 phone as a car diagnostic tool. This guide will walk you through the setup and usage of the system.

## Installation

1. Install Python Requirements:
```bash
pip install -r requirements.txt
```

2. Connect Hardware:
   - Connect Nokia 3310 using FBUS cable
   - Connect OBDLink SX to USB port
   - Connect OBDLink SX to car's OBD-II port

3. Start the Software:
```bash
python src/main.py --port COM3  # Replace COM3 with your FBUS port
```

## Using the Interface

### Main Menu
The Nokia 3310 display shows the main menu with these options:
```
Main Menu:
1.Sensors
2.DTCs
3.Info 4.Cmd
```

Use the phone's keypad to navigate:
- Press 1 for Sensors
- Press 2 for DTCs (Diagnostic Trouble Codes)
- Press 3 for Vehicle Info
- Press 4 for Custom Commands

### Sensor Menu
```
Select Sensor:
1.RPM  2.Speed
3.Temp 4.Load
0.Back
```

- Press 1-4 to select a sensor to monitor
- Press 0 to return to main menu
- Values update every 500ms

### DTC Menu
```
DTCs:
1.Read
2.Clear
0.Back
```

- Press 1 to read current DTCs
- Press 2 to clear all DTCs
- Press 0 to return to main menu

### Vehicle Info
Displays basic vehicle information:
- VIN (Vehicle Identification Number)
- Engine Load
- Fuel Status
- ECU Information

### Custom Commands Menu
```
Commands:
1.List
2.Add 3.Run
0.Back
```

#### Storing Commands
You can store up to 10 custom commands for quick access:
1. Connect phone to computer
2. Use the command storage utility:
   ```bash
   python src/tools/store_command.py --port COM3 --name "Read RPM" --type 0x01 --data "010C"
   ```
3. Commands are saved in phone's memory

#### Using Stored Commands
1. From main menu, press 4 for Commands
2. Choose an option:
   - Press 1 to list stored commands
   - Press 2 to add new command (requires PC)
   - Press 3 to run a command
3. When running commands:
   - Select command by number (1-3)
   - View result on display
   - Press 0 to go back

#### Command Types
Common command examples:
- Read RPM: 010C
- Read Speed: 010D
- Read Temperature: 0105
- Read DTCs: 03
- Clear DTCs: 04

#### Offline Usage
Once commands are stored:
1. Disconnect from computer
2. Connect FBUS cable to OBDLink SX
3. Access stored commands from phone menu
4. Execute commands directly from phone

## Features

### Real-time Monitoring
- Engine RPM
- Vehicle Speed
- Engine Temperature
- Engine Load
- Custom sensors (if supported)

### Diagnostic Functions
- Read DTCs
- Clear DTCs
- View freeze frame data
- Monitor sensor data

### Vehicle Information
- Read VIN
- ECU information
- System status
- Supported sensors

## Troubleshooting

### Connection Issues
1. Check FBUS cable connection
2. Verify COM port number
3. Ensure car is in ACC or ON position
4. Check OBDLink SX connection

### Display Problems
1. Check phone battery
2. Verify FBUS protocol
3. Reset phone if necessary
4. Check cable integrity

### Data Reading Issues
1. Verify sensor support
2. Check vehicle compatibility
3. Update OBDLink firmware
4. Try reconnecting OBD-II

## Best Practices

1. Safety First:
   - Don't use while driving
   - Follow vehicle guidelines
   - Handle equipment carefully

2. Data Collection:
   - Note important readings
   - Track changes over time
   - Document error codes

3. Maintenance:
   - Keep connections clean
   - Update software regularly
   - Check cable condition
   - Backup important data

## Advanced Usage

### Custom Commands
To create effective custom commands:
1. Identify needed PIDs
2. Format command properly:
   - First byte: Mode (01-0A)
   - Second byte: PID
   - Additional data if needed
3. Test command via PC first
4. Store working commands
5. Label clearly for easy use

### Command Management
Best practices:
1. Keep names short (12 chars max)
2. Group related commands
3. Test before storing
4. Document command functions
5. Update as needed

### Custom Sensors
To monitor custom sensors:
1. Find sensor PID
2. Add to supported list
3. Use manual entry mode
4. Monitor response

### Data Logging
The system can log data to files:
1. Use --log option
2. Specify log file
3. Set logging interval
4. Analyze data later

### Multiple Vehicles
When using with different vehicles:
1. Save vehicle profiles
2. Note compatibility
3. Track separate issues
4. Compare data

## Support

If you encounter issues:
1. Check documentation
2. Search known issues
3. Contact support
4. Report bugs

## Updates

Stay current with:
1. Software updates
2. Firmware updates
3. Protocol changes
4. New features

## Safety Notes

 **IMPORTANT:**
- Don't modify car systems
- Follow safety protocols
- Keep backups of data
- Use appropriate tools

## Additional Resources

- [Hardware Guide](HARDWARE_GUIDE.md)
- [Protocol Documentation](NOKIA_PROTOCOL.md)
- [Compatibility List](COMPATIBILITY.md)
- [FAQ](FAQ.md)
