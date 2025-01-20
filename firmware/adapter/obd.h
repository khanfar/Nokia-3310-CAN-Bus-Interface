/**
 * OBD Protocol Implementation for OBDLink SX
 * 
 * Handles communication with OBDLink SX adapter
 * Supports standard OBD-II PIDs
 */

#ifndef OBD_H
#define OBD_H

#include <stdint.h>

// OBD response structure
typedef struct {
    uint8_t mode;
    uint8_t pid;
    uint8_t *data;
    uint8_t length;
    uint8_t status;
} obd_response_t;

// Function prototypes
uint8_t is_obd_response_complete(uint8_t *buffer, uint16_t len);
uint8_t parse_obd_response(uint8_t *buffer, uint16_t len, obd_response_t *response);
void send_obd_command(uint8_t type, uint8_t *data, uint8_t len);
uint8_t format_obd_response(obd_response_t *response, uint8_t *display_data);

// OBD Mode definitions
#define OBD_MODE_CURRENT_DATA    0x01
#define OBD_MODE_FREEZE_FRAME    0x02
#define OBD_MODE_STORED_DTC      0x03
#define OBD_MODE_CLEAR_DTC       0x04
#define OBD_MODE_TEST_RESULTS    0x05
#define OBD_MODE_LIVE_DATA       0x06
#define OBD_MODE_PENDING_DTC     0x07
#define OBD_MODE_CONTROL         0x08
#define OBD_MODE_VEHICLE_INFO    0x09

// Common PIDs
#define PID_ENGINE_RPM           0x0C
#define PID_VEHICLE_SPEED        0x0D
#define PID_COOLANT_TEMP         0x05
#define PID_ENGINE_LOAD          0x04
#define PID_THROTTLE_POS         0x11
#define PID_FUEL_LEVEL          0x2F
#define PID_O2_VOLTAGE          0x14

#endif /* OBD_H */
