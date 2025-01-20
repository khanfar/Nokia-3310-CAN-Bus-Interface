# Circuit Diagrams - Nokia 3310 to OBDLink SX Direct Adapter

## 1. Power Supply Circuit
```
                                    C1                  C2
Car 12V ----[Fuse]----[D1]---+----||----[LM7805]----||----+---- 5V Out
                             |      100uF    |        10uF  |
                             |              GND            GND
                             |
                             |     C3                   C4
                             +----||----[LD1117V33]----||----+---- 3.3V Out
                                  100uF     |          10uF  |
                                          GND              GND

Components:
- Fuse: 1A fast-blow
- D1: 1N4007 reverse protection diode
- C1, C3: 100uF electrolytic
- C2, C4: 10uF electrolytic
- LM7805: 5V regulator
- LD1117V33: 3.3V regulator
```

## 2. MCU Circuit
```
                     3.3V
                      |
                      [10k]
                      |
RESET ---------------+
                     |
                   +-----------------+
              C5   |                 |
XTAL1 ----||------| XTAL1     VCC  |---- 5V
              22pF |                |
                   |                |
16MHz             |   ATmega328P   |
                   |                |
              22pF |                |
XTAL2 ----||------| XTAL2     GND  |---- GND
              C6   |                 |
                   +-----------------+

Components:
- ATmega328P-PU
- 16MHz crystal
- C5, C6: 22pF ceramic
- 10k pullup resistor
```

## 3. Level Shifter Circuit (TXB0104)
```
                    5V                     3.3V
                     |                      |
              +------------+         +------------+
Nokia TX -----| A1     B1 |---------| A1     B1 |---- MCU RX1
Nokia RX -----| A2     B2 |         | A2     B2 |---- MCU TX1
              |            |         |            |
              | TXB0104    |         | TXB0104    |
              |            |         |            |
MCU TX2 ------| A3     B3 |         | A3     B3 |---- OBD TX
MCU RX2 ------| A4     B4 |         | A4     B4 |---- OBD RX
              +------------+         +------------+
                    |                      |
                   GND                    GND

Components:
- 2x TXB0104 level shifters
- 0.1uF bypass capacitors
```

## 4. Nokia FBUS Connector
```
           3.3V
            |
            [10k]
            |
     +------+------+
     |  FBUS_TX    |
     |             |
     |  Nokia      |
     |  FBUS       |
     |  Connector  |
     |             |
     |  FBUS_RX    |
     |             |
     |  GND        |
     +-------------+

Components:
- DKU-5 cable connector
- 10k pullup resistor
```

## 5. Status LEDs
```
           5V
            |
            [330Ω]
            |
POWER ------+---->|----GND
            |
            [330Ω]
            |
STATUS -----+---->|----GND
            |
            [330Ω]
            |
ERROR ------+---->|----GND

Components:
- 3x LEDs (Green, Blue, Red)
- 3x 330Ω resistors
```

## 6. Complete Integration
```
                                         [Power Circuit]
                                               |
                                         +-----+-----+
[Nokia FBUS] <---> [Level Shifters] <--->| ATmega328P |<---> [OBDLink SX]
                                         |           |
                                         |[Status LEDs]|
                                         +-----------+
```

## PCB Layout Guidelines

### Layer 1 (Top)
```
+----------------------------------+
|    Power     |      MCU          |
| Regulators   |                   |
|              |                   |
+--------------+-------------------+
|    Level     |     Nokia        |
|  Shifters    |    Connector     |
|              |                  |
+----------------------------------+
```

### Layer 2 (Ground)
```
+----------------------------------+
|////////////////////////////////|
|////////////////////////////////|
|////////////////////////////////|
|////////////////////////////////|
+----------------------------------+
```

### Layer 3 (Power)
```
+----------------------------------+
| 12V  ----+                      |
|          |                      |
| 5V   ----+                      |
|          |                      |
| 3.3V ----+                      |
+----------------------------------+
```

### Layer 4 (Bottom)
```
+----------------------------------+
|    Signal   |     Signal         |
|   Routing   |    Routing         |
|             |                    |
+----------------------------------+
```

## Important Notes

1. Power Considerations:
   - Use proper heat sinking for regulators
   - Add thermal relief to power planes
   - Keep high current traces wide (40mil+)

2. Signal Routing:
   - Keep FBUS signals away from power
   - Use ground planes for shielding
   - Route differential pairs together

3. Component Placement:
   - Keep bypass caps close to ICs
   - Group related components
   - Allow space for heat dissipation

4. Protection:
   - Add TVS diodes on inputs
   - Use proper fusing
   - Include reverse polarity protection
