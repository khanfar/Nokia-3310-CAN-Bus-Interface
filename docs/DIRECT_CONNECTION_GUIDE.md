# Direct Connection Guide - Nokia 3310 to OBDLink SX

## Overview
This guide explains how to create a direct connection adapter between your Nokia 3310 and OBDLink SX, allowing you to use the system without a PC.

## Required Components

1. Hardware:
   - Nokia FBUS connector (from DKU-5 cable)
   - OBDLink SX
   - ATmega328P microcontroller (or similar)
   - 3.3V voltage regulator
   - 5V voltage regulator
   - Level shifters (3.3V to 5V)
   - PCB or prototype board
   - Various resistors and capacitors
   - Project box/enclosure

2. Tools:
   - Soldering iron
   - Wire strippers
   - Multimeter
   - Basic electronic tools

## Circuit Design

### Power Section
```
Car 12V ----[5V Regulator]---- 5V (for OBDLink SX)
                |
                ----[3.3V Regulator]---- 3.3V (for Nokia)
```

### Communication Section
```
Nokia 3310    ATmega328P     OBDLink SX
(FBUS)          (MCU)         (USB)
   TX ----[LS]---> RX1          
   RX <---[LS]---- TX1    
                   RX2 <-------- TX
                   TX2 --------> RX
```
LS = Level Shifter

## Assembly Instructions

1. Power Supply:
   - Connect car 12V to 5V regulator
   - Connect 5V to 3.3V regulator
   - Add filtering capacitors

2. Microcontroller:
   - Program ATmega328P with provided firmware
   - Connect to power supplies
   - Add 16MHz crystal and caps

3. Level Shifters:
   - Connect Nokia side to 3.3V
   - Connect MCU side to 5V
   - Wire TX/RX lines

4. Connectors:
   - Wire Nokia FBUS connector
   - Wire OBDLink SX connector
   - Add power LED indicator

## Firmware Features

The ATmega328P firmware provides:
- FBUS protocol handling
- Command translation
- Menu system
- Stored command execution
- Error handling

## Using the Direct Connection

1. Initial Setup:
   - Store commands via PC first
   - Test all commands
   - Verify stored commands

2. Garage Usage:
   a. Connect adapter to car OBD-II port
   b. Connect Nokia 3310 to adapter
   c. Turn on car (or ACC)
   d. Use phone menu to send commands

3. Menu Navigation:
   - Same menu system as PC version
   - All stored commands available
   - Real-time monitoring works
   - DTC reading/clearing supported

## Safety Notes

⚠️ IMPORTANT:
1. Always connect adapter first, then phone
2. Don't disconnect while car running
3. Use proper fusing for power
4. Keep connections secure
5. Protect from water/dust
6. Follow car manufacturer guidelines

## Troubleshooting

1. No Power:
   - Check car battery voltage
   - Verify fuse condition
   - Check voltage regulators
   - Test LED indicators

2. Communication Issues:
   - Check all connections
   - Verify phone battery level
   - Reset adapter if needed
   - Check error indicators

3. Command Failures:
   - Verify command storage
   - Check timing requirements
   - Reset and try again
   - Use simpler commands first

## Parts List

### Core Components:
1. ATmega328P-PU
   - Quantity: 1
   - Purpose: Main controller

2. Voltage Regulators:
   - LM7805 (5V): 1
   - LD1117V33 (3.3V): 1

3. Level Shifters:
   - TXB0104 or similar
   - Quantity: 2

4. Passive Components:
   - 10kΩ resistors: 4
   - 100nF capacitors: 6
   - 10µF capacitors: 2
   - 16MHz crystal: 1
   - 22pF crystal caps: 2

### Connectors:
1. Nokia FBUS connector
2. OBD-II pass-through connector
3. Power LED and resistor
4. Headers for programming

### Protection:
1. TVS diodes
2. Fuse holder and fuse
3. Reverse polarity protection

## Building Tips

1. PCB Layout:
   - Keep power traces wide
   - Separate digital grounds
   - Add test points
   - Use proper clearances

2. Assembly:
   - Socket for microcontroller
   - Heat sinks on regulators
   - Strain relief on cables
   - Good ventilation

3. Testing:
   - Check voltages first
   - Verify communication
   - Test all functions
   - Monitor temperature

## Future Improvements

Possible enhancements:
1. Battery backup
2. Status display
3. Bluetooth option
4. More storage
5. Custom case design

## Support

For technical support:
- Check documentation
- Contact Khanfar Systems
- Visit project website
- Join user forum
