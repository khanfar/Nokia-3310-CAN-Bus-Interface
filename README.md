# Nokia 3310 CAN Bus Interface

Turn your Nokia 3310 into a powerful car diagnostic tool! This project allows you to use a Nokia 3310 phone to send CAN bus commands to your car through an OBDLink SX adapter, either via PC or standalone with our custom adapter.

**Educational Project by Khanfar**  
Project: https://github.com/khanfar/Nokia-3310-CAN-Bus-Interface

This project is designed for educational purposes to help people learn about:
- Vehicle diagnostics and OBD-II protocols
- Embedded systems and microcontroller programming
- Hardware interface design
- Classic Nokia phone protocols

See [LICENSE](LICENSE) for usage terms and conditions.

## 🌟 Features

- Store and execute custom OBD-II commands
- Real-time vehicle data monitoring
- DTC reading and clearing
- Standalone operation (with custom adapter)
- Simple Nokia 3310 menu interface
- Command storage in phone memory

## 📁 Project Structure

```
nokia3310-canbus/
├── src/                    # Source code
│   ├── fbus/              # Nokia FBUS protocol
│   ├── canbus/            # CAN bus interface
│   ├── storage/           # Command storage
│   ├── ui/                # User interface
│   └── tools/             # Utility tools
├── firmware/              # Custom adapter firmware
│   └── adapter/           # Direct connection adapter
├── hardware/              # Hardware designs
│   └── schematics/        # Circuit diagrams
└── docs/                  # Documentation
```

## 📚 Documentation

### [Documentation Index](docs/INDEX.md)

### User Guides
- [User Guide](docs/USER_GUIDE.md) - Getting started and basic usage
- [Hardware Guide](docs/HARDWARE_GUIDE.md) - Hardware setup and connections
- [Nokia Protocol](docs/NOKIA_PROTOCOL.md) - FBUS protocol details
- [Command Reference](docs/COMMAND_REFERENCE.md) - OBD-II commands and usage
- [Compatibility Guide](docs/COMPATIBILITY.md) - Supported devices and vehicles
- [Troubleshooting Guide](docs/TROUBLESHOOTING.md) - Common issues and solutions

### Technical Documentation
- [Circuit Diagrams](docs/CIRCUIT_DIAGRAMS.md) - Detailed schematics
- [Direct Connection Guide](docs/DIRECT_CONNECTION_GUIDE.md) - Standalone adapter
- [Assembly Guide](docs/ASSEMBLY_GUIDE.md) - Building instructions
- [Alternative Access](docs/ALTERNATIVE_ACCESS.md) - Alternative CAN bus connection points
- [Immobilizer Guide](docs/IMMOBILIZER.md) - Key programming procedures

## 🛠️ Setup

### PC Mode Setup
1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Connect hardware:
- Nokia 3310 via FBUS cable
- OBDLink SX to car's OBD-II port

3. Run the software:
```bash
python src/main.py --port COM3
```

### Direct Connection Setup
1. Build custom adapter following [Assembly Guide](docs/ASSEMBLY_GUIDE.md)
2. Flash firmware using AVR programmer
3. Store commands via PC
4. Use standalone in garage

## 🔧 Tools

### Command Storage Utility
```bash
# Store a new command
python src/tools/store_command.py --port COM3 --name "RPM" --type 0x01 --data "010C"

# List stored commands
python src/tools/store_command.py --port COM3 --list
```

## 🚗 Compatible Vehicles

- Works with all OBD-II compliant vehicles (1996 and newer)
- Tested with major manufacturers:
  - Toyota
  - Honda
  - Ford
  - Volkswagen
  - BMW
  - Mercedes-Benz

## 📱 Hardware Requirements

### PC Mode
- Nokia 3310 phone
- DKU-5 or compatible FBUS cable
- OBDLink SX adapter
- USB to Serial adapter (if needed)

### Direct Connection Mode
- Nokia 3310 phone
- Custom adapter (DIY or purchased)
- OBDLink SX adapter
- Components listed in [Circuit Diagrams](docs/CIRCUIT_DIAGRAMS.md)

## 🔐 Safety Notes

- Always connect to OBD-II port with ignition off
- Don't disconnect while engine running
- Test commands in safe conditions first
- Keep backup of stored commands
- Follow vehicle manufacturer guidelines

## 🆘 Troubleshooting

Common issues and solutions:
1. Connection Problems
   - Check cable connections
   - Verify COM port settings
   - Ensure proper power supply

2. Command Issues
   - Verify command format
   - Check vehicle compatibility
   - Test basic commands first

3. Display Problems
   - Check phone battery
   - Verify FBUS connection
   - Reset if necessary

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Open pull request

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file.

## 👥 Support

- GitHub Issues: Report bugs and feature requests
- Documentation: Check guides and references
- Project Link: https://github.com/khanfar/Nokia-3310-CAN-Bus-Interface
- Contact: Through GitHub issues

## 🙏 Acknowledgments

- Nokia for the legendary 3310
- OBDLink for the SX adapter
- All contributors and testers
- The car hacking community

## 🔗 Related Projects

### By Same Developer
- [OBD2-PYTHON](https://github.com/khanfar/OBD2-PYTHON) - Python library for OBD-II diagnostics
  - Pure Python implementation
  - Supports multiple adapters
  - Real-time data logging
  - Compatible with this project

### Recommended Tools
- [python-obd](https://github.com/brendan-w/python-obd)
- [pyserial](https://github.com/pyserial/pyserial)
- [python-can](https://github.com/hardbyte/python-can)

---
Copyright (c) 2025 Khanfar - Educational Project  
https://github.com/khanfar/Nokia-3310-CAN-Bus-Interface
