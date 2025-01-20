# Circuit Diagrams

[📚 Documentation](INDEX.md) > Circuit Diagrams

## Navigation
- Previous: [Hardware Guide](HARDWARE_GUIDE.md)
- Next: [Assembly Guide](ASSEMBLY_GUIDE.md)
- Related: 
  - [Direct Connection Guide](DIRECT_CONNECTION_GUIDE.md)
  - [Nokia Protocol](NOKIA_PROTOCOL.md)

## Overview

This document contains the circuit diagrams and schematics for the Nokia 3310 CAN Bus Interface adapter.

## Main Components

### 1. MCU Section
```
                  ATmega328P
                 +----------+
        +--XTAL1-|1  ▢   28|-VCC--+
        |  XTAL2-|2      27|-PC4   |
+5V-----+--RESET-|3      26|-PC3   |
        |     PD-|4      25|-PC2   |
        |     PD-|5      24|-PC1   |
        |     PD-|6      23|-PC0   |
VCC-----+--VCC--|7      22|-GND----+
GND-----+--GND--|8      21|-AREF   |
   16MHz|  XTAL1-|9      20|-VCC   |
        |  XTAL2-|10     19|-PB5   |
        |     PD-|11     18|-PB4   |
        |     PD-|12     17|-PB3   |
        |     PD-|13     16|-PB2   |
        |     PD-|14     15|-PB1   |
        +--------+----------+
```

### 2. FBUS Interface
```
       Nokia 3310
      FBUS Socket
     +------------+
     |  1 2 3 4  |    1: GND
     +------------+    2: FBUS TX
                      3: FBUS RX
                      4: VCC (3.3V)

     Level Shifter
    +-------------+
    |    3.3V    |
    |  +---------+
TX--+--|HV1  LV1|--FBUS_TX
RX--+--|HV2  LV2|--FBUS_RX
    |  |GND  GND|
    |  +---------+
    |    5V      |
    +-------------+
```

### 3. OBD-II Interface
```
     OBD-II Socket (DB9)
    +-------------------+
    |  1 2 3 4 5       |
    |   6 7 8 9        |
    +-------------------+
    1: NC         6: CAN_H
    2: NC         7: ISO_K
    3: NC         8: NC
    4: GND        9: CAN_L
    5: GND

     CAN Transceiver
    +--------------+
    |   MCP2551    |
    |  +---------+ |
    |  |1  ▢   8| |
    |  |2      7| |
    |  |3      6| |
    |  |4      5| |
    |  +---------+ |
    +--------------+
    1: TXD    5: CAN_L
    2: VSS    6: VDD
    3: VDD    7: CAN_H
    4: RXD    8: RS
```

### 4. Power Supply
```
    Input Protection
    +-------------+     Voltage Regulator
    |  Polarity   |    +---------------+
    | Protection  |    |    LM7805     |
    |  +------+  |    |  +---------+  |
12V-+--|D1  D2|--+----|IN  OUT    |--+--5V
    |  +------+  |    |  |         |  |
    |    TVS     |    |  +---------+  |
    +------------+    +---------------+

    3.3V Regulator
    +---------------+
    |    LM1117     |
    |  +---------+  |
5V--+--|IN  OUT  |--+--3.3V
    |  |         |  |
    |  +---------+  |
    +---------------+
```

## Complete Schematic

### Main Board
```
                                        +------------------+
                                        |    ATmega328P   |
                    +--------+          |                 |
    Nokia 3310      | Level  |     +---|TX           CAN |    OBD-II
    FBUS Port       | Shift  |     |   |RX          TXD |    Port
    +---------+     +--------+     |   |            RXD |    +--------+
    |   TX  1 |-----|LV1 HV1|-----+   |                |    |  CAN_H |
    |   RX  2 |-----|LV2 HV2|---------|                |    |  CAN_L |
    |   GND 3 |--+  +--------+         |                |    |   GND  |
    |   VCC 4 |----|3.3V REG|---------|VCC         GND |    |   NC   |
    +---------+    +---------+     +---|RST            |    +--------+
                                   |   +------------------+
                   +---------+     |   +------------------+
    12V Input      |  5V REG |     |   |   MCP2551 CAN  |
    +---------+    +---------+     |   |    Transceiver  |
    |   12V  |-----|IN  OUT |--+---+   |                |
    |   GND  |-----|GND GND |  |       |TXD         CANH|----+
    +---------+    +---------+  |       |RXD         CANL|----+
                                |       |                |
                                +-------|VCC         GND |
                                        +------------------+
```

## PCB Layout

### Top Layer
```
    +----------------------------------------+
    |  +-----------------+                   |
    |  |   ATmega328P    |   +----------+   |
    |  |                 |   | MCP2551  |   |
    |  +-----------------+   +----------+   |
    |                                       |
    |  +---------+           +----------+   |
    |  |  Level  |           |  5V REG  |   |
    |  | Shifter |           +----------+   |
    |  +---------+                          |
    |                        +----------+   |
    |  +---------+          | 3.3V REG |   |
    |  |  FBUS   |          +----------+   |
    |  |  Port   |                         |
    |  +---------+          +----------+   |
    |                       |  OBD-II  |   |
    |                       |   Port   |   |
    |                       +----------+   |
    +----------------------------------------+
```

## Component List

### Core Components
```
MCU:
- ATmega328P (TQFP-32)
- 16MHz Crystal
- 2x 22pF Capacitors

Level Shifter:
- TXB0102 or equivalent
- 4x 10kΩ Pull-up Resistors

CAN Interface:
- MCP2551 CAN Transceiver
- 120Ω Termination Resistor
- 100nF Bypass Capacitor
```

### Power Components
```
Regulators:
- LM7805 (5V)
- LM1117-3.3 (3.3V)
- Input Protection Diode
- TVS Diode
- 470µF Input Capacitor
- 100µF Output Capacitors
```

### Connectors
```
FBUS:
- 4-pin Female Header
- 2.54mm Pitch

OBD:
- DB9 Female Connector
- Mounting Hardware

Power:
- DC Barrel Jack
- Screw Terminal (optional)
```

## Assembly Notes

### Critical Areas
1. Power Supply
   - Check polarity protection
   - Verify voltage levels
   - Test regulation

2. Level Shifting
   - Match voltage levels
   - Check direction
   - Verify signals

3. CAN Bus
   - Proper termination
   - Shield connections
   - Signal integrity

### Test Points
```
Required:
TP1: 12V Input
TP2: 5V Rail
TP3: 3.3V Rail
TP4: FBUS TX
TP5: FBUS RX
TP6: CAN_H
TP7: CAN_L
```

## Test Procedures

### 1. Power Supply Testing
```
Test Sequence:
1. Initial Power Check
   □ Input voltage: 12V ±0.5V
   □ No load 5V: 5.0V ±0.1V
   □ No load 3.3V: 3.3V ±0.1V
   
2. Load Testing
   □ 5V with 100mA load: >4.9V
   □ 3.3V with 50mA load: >3.2V
   □ Ripple voltage: <50mV
   
3. Protection Tests
   □ Reverse polarity protection
   □ Overvoltage protection (15V)
   □ Short circuit recovery
```

### 2. MCU Testing
```
Test Sequence:
1. Basic Functions
   □ Clock frequency: 16MHz ±0.1%
   □ Reset circuit operation
   □ Power-on reset timing
   
2. I/O Testing
   □ All pins high: 4.8V-5.2V
   □ All pins low: 0-0.2V
   □ Pull-up resistors: 20-50kΩ
   
3. Programming
   □ ISP connection
   □ Fuse verification
   □ Bootloader upload
```

### 3. FBUS Interface Testing
```
Test Sequence:
1. Signal Levels
   □ TX idle: 3.3V
   □ RX idle: 3.3V
   □ TX active: 0-3.3V swing
   □ RX active: 0-3.3V swing

2. Communication Test
   □ Loopback test
   □ Frame integrity
   □ Error detection
   
3. Timing Analysis
   □ Bit rate: 115200 baud
   □ Frame timing: ±2% tolerance
   □ Response delay: <10ms
```

### 4. CAN Bus Testing
```
Test Sequence:
1. Physical Layer
   □ CAN_H idle: 2.5V
   □ CAN_L idle: 2.5V
   □ Differential voltage: 0V
   □ Termination: 60Ω ±10%

2. Signal Quality
   □ Rise time: <250ns
   □ Fall time: <250ns
   □ Common mode range
   □ Signal integrity at 1Mbps

3. Protocol Tests
   □ Message transmission
   □ Message reception
   □ Error handling
   □ Bit stuffing
```

### 5. Level Shifter Testing
```
Test Sequence:
1. Voltage Levels
   □ High side: 5V ±0.1V
   □ Low side: 3.3V ±0.1V
   □ Direction control

2. Signal Integrity
   □ Propagation delay: <20ns
   □ Edge transitions
   □ No signal distortion
   
3. Load Testing
   □ Maximum current: 20mA
   □ Heat dissipation
   □ Continuous operation
```

### 6. System Integration Tests
```
Test Sequence:
1. Full Power Test
   □ Current draw idle: <50mA
   □ Current draw active: <200mA
   □ Thermal stability
   
2. Communication Chain
   □ FBUS → MCU → CAN
   □ CAN → MCU → FBUS
   □ End-to-end latency
   
3. EMC/EMI Testing
   □ Interference immunity
   □ Emissions testing
   □ Ground bounce check
```

### 7. Environmental Testing
```
Test Sequence:
1. Temperature Range
   □ Cold start: 0°C
   □ Hot operation: 50°C
   □ Thermal cycling
   
2. Vibration Testing
   □ Connection integrity
   □ Component stability
   □ PCB flex test
   
3. Long-term Testing
   □ 24-hour burn-in
   □ Power cycling
   □ Stress testing
```

### Test Equipment Required
```
Basic Equipment:
□ Digital Multimeter
□ Oscilloscope (50MHz+)
□ Power Supply (0-30V, 3A)
□ Logic Analyzer
□ CAN Bus Analyzer

Specialized Tools:
□ FBUS Protocol Analyzer
□ Temperature Chamber
□ Current Probe
□ EMC/EMI Scanner
□ Signal Generator
```

### Test Documentation
```
For each test:
1. Record Setup
   □ Test conditions
   □ Equipment used
   □ Software version
   
2. Measurements
   □ Raw data
   □ Calculated values
   □ Pass/fail criteria
   
3. Results
   □ Test outcomes
   □ Observations
   □ Failure analysis
```

### Safety Procedures
```
Before Testing:
□ ESD protection
□ Current limiting
□ Voltage verification
□ Tool calibration

During Testing:
□ Monitor temperature
□ Watch current draw
□ Check for shorts
□ Regular pauses

After Testing:
□ Power down sequence
□ Component inspection
□ Results backup
□ Equipment storage
```

## Test Results Template
```
Test Report ID: TR-[DATE]-[SERIAL]

1. Device Information
   Model: Nokia 3310 CAN Bus Interface
   Serial: [SERIAL]
   Firmware: [VERSION]
   Build Date: [DATE]

2. Test Environment
   Temperature: [XX]°C
   Humidity: [XX]%
   Power Supply: [XX]V
   Test Duration: [XX] hours

3. Power Supply Results
   □ Input Voltage: [XX]V
   □ 5V Rail: [XX]V
   □ 3.3V Rail: [XX]V
   □ Ripple: [XX]mV
   Status: [PASS/FAIL]

4. MCU Results
   □ Clock: [XX]MHz
   □ Reset: [PASS/FAIL]
   □ I/O Test: [PASS/FAIL]
   □ Programming: [PASS/FAIL]
   Status: [PASS/FAIL]

5. FBUS Results
   □ Signal Levels: [PASS/FAIL]
   □ Communication: [PASS/FAIL]
   □ Timing: [PASS/FAIL]
   Status: [PASS/FAIL]

6. CAN Bus Results
   □ Physical Layer: [PASS/FAIL]
   □ Signal Quality: [PASS/FAIL]
   □ Protocol Tests: [PASS/FAIL]
   Status: [PASS/FAIL]

7. System Integration
   □ Power Draw: [XX]mA
   □ Communication: [PASS/FAIL]
   □ EMC/EMI: [PASS/FAIL]
   Status: [PASS/FAIL]

8. Environmental Tests
   □ Temperature: [PASS/FAIL]
   □ Vibration: [PASS/FAIL]
   □ Long-term: [PASS/FAIL]
   Status: [PASS/FAIL]

9. Notes & Observations
   [Enter detailed notes here]

10. Final Result
    □ Overall Status: [PASS/FAIL]
    □ Tested By: [NAME]
    □ Date: [DATE]
    □ Signature: _____________
```

### Quick Test Checklist
```
Pre-Test Setup
□ ESD strap worn
□ Equipment calibrated
□ Power supply checked
□ Test area cleared

Basic Tests (5 min)
□ Visual inspection
□ Power rails check
□ Basic communication
□ LED indicators

Full Tests (30 min)
□ All voltage rails
□ Communication tests
□ Protocol checks
□ Load testing

Extended Tests (24h)
□ Burn-in period
□ Temperature cycle
□ Stress testing
□ Final inspection
```

### Common Test Points Reference
```
Voltage Test Points
TP1 (12V): 11.5-12.5V
TP2 (5V):  4.9-5.1V
TP3 (3.3V): 3.25-3.35V

Signal Test Points
TP4 (FBUS TX): 0-3.3V swing
TP5 (FBUS RX): 0-3.3V swing
TP6 (CAN_H): 2.5-3.5V
TP7 (CAN_L): 1.5-2.5V

Ground References
GND1: Power ground
GND2: Digital ground
GND3: CAN ground
```

### Test Equipment Setup
```
Oscilloscope Settings
Channel 1: FBUS (1V/div)
Channel 2: CAN_H (2V/div)
Channel 3: CAN_L (2V/div)
Channel 4: MCU Clock (2V/div)
Timebase: 500ns/div
Trigger: Channel 1, Rising Edge

Logic Analyzer
Channel 0-7: MCU I/O
Channel 8: FBUS TX
Channel 9: FBUS RX
Sample Rate: 50MHz
Trigger: Pattern Match

Power Supply
Channel 1: 12V/1A (Main)
Channel 2: 5V/500mA (Aux)
Current Limit: Enabled
OVP: Set to 13V
```

---
## Related Documentation
- [Assembly Guide](ASSEMBLY_GUIDE.md) - Building instructions
- [Hardware Guide](HARDWARE_GUIDE.md) - Setup guide
- [Direct Connection Guide](DIRECT_CONNECTION_GUIDE.md) - Usage
- [Back to Index](INDEX.md)

---
Copyright (c) 2025 Khanfar - Educational Project  
https://github.com/khanfar/Nokia-3310-CAN-Bus-Interface
