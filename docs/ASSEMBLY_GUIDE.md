# Assembly Guide - Nokia 3310 to OBDLink SX Direct Adapter

[📚 Documentation](INDEX.md) > Assembly Guide

## Navigation
- Previous: [Direct Connection Guide](DIRECT_CONNECTION_GUIDE.md)
- Next: [Troubleshooting Guide](TROUBLESHOOTING.md)
- Related: 
  - [Circuit Diagrams](CIRCUIT_DIAGRAMS.md)
  - [Hardware Guide](HARDWARE_GUIDE.md)

## Required Tools

1. Soldering Equipment:
   - Temperature-controlled soldering iron (recommended 300-350°C)
   - Solder (60/40 or lead-free)
   - Solder wick and flux
   - Helping hands or PCB holder
   - Heat gun (for SMD components)

2. Testing Equipment:
   - Multimeter
   - USB-TTL adapter (for firmware flashing)
   - Oscilloscope (optional, for debugging)

3. Hand Tools:
   - Wire strippers
   - Small screwdrivers
   - Tweezers
   - Wire cutters
   - Heat shrink tubing
   - Isopropyl alcohol for cleaning

## Assembly Steps

### 1. PCB Preparation
```
[Before soldering]
1. Inspect PCB for defects
2. Clean with isopropyl alcohol
3. Mark component positions
4. Verify all holes are clear
```

### 2. Power Supply Section
```
[Power components layout]
┌──────────────────┐
│    D1   LM7805  │
│ ┌─┐   ┌──────┐  │
│ └─┘   └──────┘  │
│    C1    C2     │
│ ┌──┐  ┌──┐     │
│ └──┘  └──┘     │
└──────────────────┘

Assembly Order:
1. Solder D1 (check polarity)
2. Mount LM7805 (with heatsink)
3. Add C1, C2 capacitors
4. Repeat for 3.3V section
5. Test voltages before proceeding
```

### 3. Microcontroller Section
```
[MCU placement]
┌────────────────┐
│    ATmega328P  │
│   ┌────────┐   │
│   │        │   │
│   │        │   │
│   └────────┘   │
│ XTAL   C5  C6  │
└────────────────┘

Steps:
1. Install IC socket
2. Solder crystal and caps
3. Add pull-up resistors
4. Don't insert MCU yet
```

### 4. Level Shifters
```
[Level shifter connections]
Nokia (3.3V) <-> TXB0104 <-> MCU (5V)
┌────────┐     ┌────────┐
│ TX ────┼─────┤ A1  B1 │
│ RX ────┼─────┤ A2  B2 │
└────────┘     └────────┘

1. Mount TXB0104 chips
2. Add bypass capacitors
3. Check orientation
4. Test continuity
```

### 5. Connectors
```
[Connector layout]
┌─────────────┐
│ FBUS   OBD  │
│ ┌───┐ ┌───┐ │
│ └───┘ └───┘ │
│ PROG   PWR  │
└─────────────┘

1. Install headers first
2. Add FBUS connector
3. Mount OBD connector
4. Secure mechanically
```

### 6. Status LEDs
```
[LED placement]
┌────────┐
│ G B R  │
│ ○ ○ ○  │
└────────┘

1. Check LED polarity
2. Solder resistors
3. Install LEDs
4. Test each color
```

## Testing Procedure

### 1. Power Supply Test
```
Voltage Check Points:
○ 12V Input
○ 5V Output
○ 3.3V Output
○ Ground continuity
```

### 2. Communication Test
```
Signal Test Points:
○ FBUS TX/RX
○ OBD TX/RX
○ MCU pins
```

### 3. Final Assembly
```
1. Install MCU
2. Upload firmware
3. Verify LEDs
4. Test all functions
```

## Common Issues and Solutions

### 1. Power Problems
```
Symptom: No power LED
Check:
- Input voltage
- Diode polarity
- Regulator output
- Solder joints
```

### 2. Communication Issues
```
Symptom: No data transfer
Check:
- Level shifter orientation
- TX/RX connections
- Signal levels
- Ground connections
```

### 3. LED Problems
```
Symptom: LEDs not working
Check:
- LED polarity
- Resistor values
- MCU pins
- Solder joints
```

## Final Testing

### 1. Bench Test
```
1. Power up test
2. LED sequence check
3. Communication test
4. Temperature check
```

### 2. Vehicle Test
```
1. OBD connection
2. Phone connection
3. Command execution
4. Response display
```

## Enclosure Assembly

### 1. Preparation
```
1. Drill mounting holes
2. Cut connector openings
3. Add ventilation holes
4. Test fit PCB
```

### 2. Final Assembly
```
1. Mount PCB
2. Secure connectors
3. Add strain relief
4. Close enclosure
```

## Quality Checks

### 1. Visual Inspection
```
□ No solder bridges
□ Components properly seated
□ No damaged traces
□ Clean PCB surface
```

### 2. Electrical Tests
```
□ Voltage levels correct
□ No shorts to ground
□ Signals present
□ Current draw normal
```

### 3. Functional Tests
```
□ LEDs working
□ Commands execute
□ Data displayed
□ No overheating
```

## Maintenance

### 1. Regular Checks
```
Monthly:
□ Check connections
□ Clean connectors
□ Verify voltages
□ Test functions
```

### 2. Troubleshooting
```
If issues occur:
1. Check power
2. Verify connections
3. Test communication
4. Update firmware
```

## Safety Notes

### 1. During Assembly
```
⚠️ CAUTION:
- Use proper ESD protection
- Verify voltages before connecting
- Don't solder with power applied
- Keep work area clean
```

### 2. During Use
```
⚠️ IMPORTANT:
- Connect OBD first
- Wait for LED sequence
- Follow power-up order
- Monitor temperature
```

## Support

For assembly support:
1. Check documentation
2. Contact Khanfar Systems
3. Visit project website
4. Join user forum
