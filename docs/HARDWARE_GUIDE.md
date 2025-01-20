# Hardware Guide

[📚 Documentation](INDEX.md) > Hardware Guide

## Navigation
- Previous: [User Guide](USER_GUIDE.md)
- Next: [Assembly Guide](ASSEMBLY_GUIDE.md)
- Related: 
  - [Circuit Diagrams](CIRCUIT_DIAGRAMS.md)
  - [Direct Connection Guide](DIRECT_CONNECTION_GUIDE.md)

## Required Components

1. Nokia 3310 Phone
   - Original Nokia 3310 or compatible model
   - Fully charged battery
   - Working display and keypad

2. FBUS Cable (DKU-5 or compatible)
   - Can be purchased or DIY (see DIY instructions below)
   - Must support FBUS protocol
   - Requires proper voltage levels (3.3V)

3. OBDLink SX
   - USB to OBD-II adapter
   - Supports all OBD-II protocols
   - Compatible with ELM327 commands

4. Computer/Laptop
   - USB ports for both adapters
   - Windows/Linux/macOS compatible
   - Python 3.8 or higher installed

## DIY FBUS Cable Instructions

If you want to build your own FBUS cable, you'll need:

### Components:
- Nokia Pop-Port or FBUS connector
- USB-to-Serial adapter (FTDI FT232RL recommended)
- 3.3V voltage regulator
- 2x 10kΩ resistors
- 2x 1kΩ resistors
- Breadboard or PCB
- Wire and solder

### Wiring Diagram:
```
Nokia FBUS      FTDI
MBUS (TX) ---[1kΩ]--- RX
MBUS (RX) ---[1kΩ]--- TX
GND -------------- GND
VCC --[3.3V reg]-- 5V
```

### Safety Notes:
- Double-check voltage levels
- Use proper ESD protection
- Test continuity before connecting
- Never connect while powered

## Connection Setup

1. Phone Connection:
   ```
   [Nokia 3310] --- FBUS Cable --- [USB Port 1]
   ```

2. OBD-II Connection:
   ```
   [OBDLink SX] --- OBD-II Port --- [Car]
                 --- USB --- [USB Port 2]
   ```

3. Power Sequence:
   1. Connect FBUS cable to computer
   2. Connect FBUS cable to phone
   3. Connect OBDLink SX to computer
   4. Start car (or turn to ACC)
   5. Connect OBDLink SX to OBD-II port

## Troubleshooting

### FBUS Connection Issues:
1. Check cable connections
2. Verify COM port assignment
3. Test with Nokia PC Suite
4. Check voltage levels

### OBDLink SX Issues:
1. Update firmware
2. Check USB drivers
3. Verify car compatibility
4. Test with OBDLink software

### General Problems:
1. Try different USB ports
2. Check system requirements
3. Update drivers
4. Test components separately

## Safety Warnings

⚠️ **IMPORTANT SAFETY NOTES:**

1. Never connect/disconnect while car is running
2. Protect against static electricity
3. Use proper voltage levels
4. Follow car manufacturer guidelines
5. Don't modify while connected
6. Keep connections secure

## Maintenance

1. Regular Checks:
   - Cable integrity
   - Connector cleanliness
   - Voltage levels
   - Software updates

2. Storage:
   - Keep in dry place
   - Avoid extreme temperatures
   - Protect connectors
   - Bundle cables properly

## Technical Specifications

### FBUS Protocol:
- Baud Rate: 9600
- Data Bits: 8
- Parity: Odd
- Stop Bits: 1
- Flow Control: None

### OBD-II Protocols:
- ISO 15765-4 (CAN)
- ISO 14230-4 (KWP2000)
- ISO 9141-2
- SAE J1850 VPW
- SAE J1850 PWM

### Voltage Levels:
- FBUS: 3.3V
- OBD-II: 12V
- USB: 5V

## Additional Resources

- [Nokia Protocol Documentation](NOKIA_PROTOCOL.md)
- [OBDLink SX Manual](https://www.obdlink.com/support)
- [Vehicle Compatibility List](COMPATIBILITY.md)
- [Troubleshooting Guide](TROUBLESHOOTING.md)

---
## Related Documentation
- [Assembly Guide](ASSEMBLY_GUIDE.md) - Building instructions
- [Circuit Diagrams](CIRCUIT_DIAGRAMS.md) - Detailed schematics
- [Nokia Protocol](NOKIA_PROTOCOL.md) - Protocol details
- [Back to Index](INDEX.md)

---
Copyright (c) 2025 Khanfar - Educational Project  
https://github.com/khanfar/Nokia-3310-CAN-Bus-Interface
