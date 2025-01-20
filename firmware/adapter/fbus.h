/**
 * FBUS Protocol Implementation for Nokia 3310
 * 
 * Handles communication with Nokia 3310 phone
 * Based on FBUS protocol specification
 */

#ifndef FBUS_H
#define FBUS_H

#include <stdint.h>

// FBUS frame types
#define FBUS_TYPE_MENU_SELECT  0x01
#define FBUS_TYPE_MENU_REQUEST 0x02
#define FBUS_TYPE_MENU         0x03
#define FBUS_TYPE_DISPLAY      0x04

// FBUS frame structure
typedef struct {
    uint8_t type;
    uint8_t *data;
    uint16_t length;
    uint8_t sequence;
} fbus_frame_t;

// Function prototypes
uint8_t is_fbus_frame_complete(uint8_t *buffer, uint16_t len);
uint8_t parse_fbus_frame(uint8_t *buffer, uint16_t len, fbus_frame_t *frame);
void send_fbus_frame(uint8_t type, uint8_t *data, uint16_t len);
uint8_t calculate_fbus_checksum(uint8_t *data, uint16_t len);

#endif /* FBUS_H */
