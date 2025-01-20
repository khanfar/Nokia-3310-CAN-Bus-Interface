# Nokia 3310 FBUS Protocol Documentation

## Overview

The Nokia 3310 uses the FBUS (Fast Bus) protocol for communication. This document details the protocol implementation used in this project for interfacing with the Nokia 3310 display and keypad.

## Protocol Specifications

### Frame Format
```
+----------------+--------+---------+--------+----------+------+----------+
| Frame Sync (2) | Dest   | Source  | Type   | Length   | Data | Checksum |
+----------------+--------+---------+--------+----------+------+----------+
| 0x1E, 0x0C     | 1 byte | 1 byte | 1 byte | 2 bytes  | var  | 1 byte   |
```

### Frame Fields

1. Frame Sync (2 bytes)
   - Start: 0x1E
   - Device: 0x0C (Nokia 3310)

2. Destination Address (1 byte)
   - Phone: 0x00
   - PC/Device: 0x0C

3. Source Address (1 byte)
   - Phone: 0x00
   - PC/Device: 0x0C

4. Message Type (1 byte)
   ```
   0x01: Display Text
   0x02: Key Press
   0x03: Menu Navigation
   0x04: Status Update
   0x05: Memory Access
   0x06: Command Response
   ```

5. Length (2 bytes)
   - Big-endian format
   - Data length only (excludes header/checksum)

6. Data (variable length)
   - Command-specific payload
   - Max 120 bytes for display text

7. Checksum (1 byte)
   - XOR of all bytes except sync
   - Including dest, source, type, length, data

## Command Types

### 1. Display Commands (0x01)
```
Data Format:
[Row (1)] [Col (1)] [Flags (1)] [Text (...)]

Flags:
0x00: Normal text
0x01: Inverse video
0x02: Bold
0x04: Large font
```

### 2. Key Press Events (0x02)
```
Data Format:
[Key Code (1)] [Press Type (1)]

Key Codes:
0x01-0x0C: Numeric keys (1-9, *, 0, #)
0x0D: Menu
0x0E: Up
0x0F: Down
0x10: OK
0x11: Back

Press Types:
0x00: Press
0x01: Release
0x02: Long Press
```

### 3. Menu Navigation (0x03)
```
Data Format:
[Menu ID (1)] [Item Count (1)] [Selected (1)] [Items (...)]

Menu Items:
[Length (1)] [Text (...)] for each item
```

### 4. Status Updates (0x04)
```
Data Format:
[Status Type (1)] [Value (1)]

Status Types:
0x01: Battery Level (0-100)
0x02: Signal Strength (0-5)
0x03: Error Code
```

### 5. Memory Access (0x05)
```
Data Format:
[Operation (1)] [Address (2)] [Length (1)] [Data (...)]

Operations:
0x01: Read Request
0x02: Read Response
0x03: Write Request
0x04: Write Response
```

### 6. Command Response (0x06)
```
Data Format:
[Command Ref (1)] [Status (1)] [Data (...)]

Status:
0x00: Success
0x01: Error
0x02: Not Supported
0x03: Invalid Parameter
```

## Example Frames

1. Display Text "Hello"
```
1E 0C 00 0C 01 00 06 00 00 48 65 6C 6C 6F 7E
│  │  │  │  │  │  │  │  └─┴─┴─┴─┴─┴── "Hello"
│  │  │  │  │  │  │  └── Row 0
│  │  │  │  │  │  └── Length (6)
│  │  │  │  │  └── High byte of length
│  │  │  │  └── Type (Display)
│  │  │  └── Source (PC)
│  │  └── Dest (Phone)
│  └── Device ID
└── Start
```

2. Key Press (5 key)
```
1E 0C 0C 00 02 00 02 05 00 11
│  │  │  │  │  │  │  │  │  └── Checksum
│  │  │  │  │  │  │  │  └── Press type
│  │  │  │  │  │  │  └── Key code (5)
│  │  │  │  │  │  └── Length
│  │  │  │  │  └── High byte of length
│  │  │  │  └── Type (Key)
│  │  │  └── Source (Phone)
│  │  └── Dest (PC)
│  └── Device ID
└── Start
```

## Implementation Notes

1. Timing Requirements
   - Minimum 2ms between frames
   - 5ms timeout for response
   - 100ms retry interval

2. Error Handling
   - Retry up to 3 times
   - Reset connection if no response
   - Validate all checksums

3. Buffer Sizes
   - Input buffer: 256 bytes
   - Display buffer: 84x48 pixels
   - Command buffer: 128 bytes

4. Power Management
   - Keep communication minimal
   - Close connection when idle
   - Monitor phone battery status

## Code Examples

### Frame Construction
```c
typedef struct {
    uint8_t type;
    uint8_t *data;
    uint16_t length;
} fbus_frame_t;

uint8_t calculate_checksum(uint8_t *data, uint16_t len) {
    uint8_t sum = 0;
    for(uint16_t i = 0; i < len; i++) {
        sum ^= data[i];
    }
    return sum;
}

void send_frame(fbus_frame_t *frame) {
    uint8_t header[6] = {0x1E, 0x0C, 0x00, 0x0C, frame->type};
    header[5] = frame->length >> 8;
    header[6] = frame->length & 0xFF;
    
    // Send header
    uart_write(header, 6);
    
    // Send data
    uart_write(frame->data, frame->length);
    
    // Calculate and send checksum
    uint8_t checksum = calculate_checksum(&header[1], 5);
    checksum ^= calculate_checksum(frame->data, frame->length);
    uart_write(&checksum, 1);
}
```

### Display Text
```c
void display_text(const char *text, uint8_t row, uint8_t col) {
    uint8_t data[128];
    data[0] = row;
    data[1] = col;
    data[2] = 0x00; // Normal text
    
    uint8_t text_len = strlen(text);
    memcpy(&data[3], text, text_len);
    
    fbus_frame_t frame = {
        .type = 0x01,
        .data = data,
        .length = text_len + 3
    };
    
    send_frame(&frame);
}
```

### Process Key Press
```c
void process_key_frame(uint8_t *data, uint16_t len) {
    if(len < 2) return;
    
    uint8_t key = data[0];
    uint8_t type = data[1];
    
    switch(key) {
        case 0x0D: // Menu key
            show_menu();
            break;
        case 0x0E: // Up
            menu_navigate(-1);
            break;
        case 0x0F: // Down
            menu_navigate(1);
            break;
        case 0x10: // OK
            menu_select();
            break;
        default:
            if(key >= 0x01 && key <= 0x0C) {
                handle_numeric_key(key);
            }
            break;
    }
}
```

## References

1. Nokia FBUS Protocol Specification
2. Nokia 3310 LCD Controller Documentation
3. Nokia 3310 Service Manual
4. FBUS Protocol Analysis Tools

## Safety Notes

1. Memory Access
   - Validate all addresses
   - Respect memory boundaries
   - Backup critical data

2. Display Updates
   - Limit update frequency
   - Check screen boundaries
   - Clear partial updates

3. Error Recovery
   - Implement watchdog
   - Handle timeout gracefully
   - Log communication errors

## Support

For technical questions about the FBUS protocol implementation:
- Check project documentation
- Submit issues on GitHub
- Review example code

---
Copyright (c) 2025 Khanfar - Educational Project  
https://github.com/khanfar/Nokia-3310-CAN-Bus-Interface
