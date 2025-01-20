/**
 * Nokia 3310 to OBDLink SX Direct Adapter Firmware
 * 
 * MCU: ATmega328P
 * Clock: 16MHz
 * 
 * Copyright (c) 2025 Khanfar
 * https://github.com/khanfar/Nokia-3310-CAN-Bus-Interface
 * For educational purposes - see LICENSE file for details
 */

#include <avr/io.h>
#include <avr/interrupt.h>
#include <avr/eeprom.h>
#include <util/delay.h>
#include <string.h>
#include "fbus.h"
#include "obd.h"

// Pin definitions
#define LED_POWER   PB0
#define LED_STATUS  PB1
#define LED_ERROR   PB2

// UART settings
#define UART_BAUD 9600
#define UART_BAUD_PRESCALE (((F_CPU / (UART_BAUD * 16UL))) - 1)

// Command storage
#define MAX_COMMANDS 10
#define CMD_NAME_LEN 12
#define CMD_DATA_LEN 16

typedef struct {
    char name[CMD_NAME_LEN];
    uint8_t type;
    uint8_t data[CMD_DATA_LEN];
    uint8_t data_len;
} stored_command_t;

// Global variables
static stored_command_t EEMEM stored_commands[MAX_COMMANDS];
static uint8_t command_count EEMEM;
static uint8_t current_menu = 0;
static uint8_t error_state = 0;

// Function prototypes
void system_init(void);
void uart_init(void);
void led_init(void);
void process_fbus_frame(uint8_t *data, uint16_t len);
void process_obd_response(uint8_t *data, uint16_t len);
void execute_command(uint8_t index);
void send_menu_to_phone(void);
uint8_t store_command(const char *name, uint8_t type, const uint8_t *data, uint8_t len);

// Initialization
void system_init(void) {
    // Disable interrupts during init
    cli();
    
    // Initialize ports
    led_init();
    uart_init();
    
    // Enable interrupts
    sei();
    
    // Power LED on
    PORTB |= (1 << LED_POWER);
}

void uart_init(void) {
    // UART0 for Nokia FBUS
    UBRR0H = (UART_BAUD_PRESCALE >> 8);
    UBRR0L = UART_BAUD_PRESCALE;
    UCSR0B = (1 << RXEN0) | (1 << TXEN0) | (1 << RXCIE0);
    UCSR0C = (1 << UCSZ01) | (1 << UCSZ00);
    
    // UART1 for OBDLink SX
    UBRR1H = (UART_BAUD_PRESCALE >> 8);
    UBRR1L = UART_BAUD_PRESCALE;
    UCSR1B = (1 << RXEN1) | (1 << TXEN1) | (1 << RXCIE1);
    UCSR1C = (1 << UCSZ11) | (1 << UCSZ10);
}

void led_init(void) {
    // Set LED pins as outputs
    DDRB |= (1 << LED_POWER) | (1 << LED_STATUS) | (1 << LED_ERROR);
    // All LEDs off
    PORTB &= ~((1 << LED_POWER) | (1 << LED_STATUS) | (1 << LED_ERROR));
}

// UART receive interrupts
ISR(USART0_RX_vect) {
    static uint8_t fbus_buffer[256];
    static uint16_t fbus_pos = 0;
    
    uint8_t data = UDR0;
    
    // FBUS frame processing
    if (fbus_pos < sizeof(fbus_buffer)) {
        fbus_buffer[fbus_pos++] = data;
        
        // Check for complete frame
        if (is_fbus_frame_complete(fbus_buffer, fbus_pos)) {
            process_fbus_frame(fbus_buffer, fbus_pos);
            fbus_pos = 0;
        }
    } else {
        fbus_pos = 0; // Buffer overflow protection
    }
}

ISR(USART1_RX_vect) {
    static uint8_t obd_buffer[256];
    static uint16_t obd_pos = 0;
    
    uint8_t data = UDR1;
    
    // OBD response processing
    if (obd_pos < sizeof(obd_buffer)) {
        obd_buffer[obd_pos++] = data;
        
        // Check for complete response
        if (is_obd_response_complete(obd_buffer, obd_pos)) {
            process_obd_response(obd_buffer, obd_pos);
            obd_pos = 0;
        }
    } else {
        obd_pos = 0; // Buffer overflow protection
    }
}

// Process FBUS frame from phone
void process_fbus_frame(uint8_t *data, uint16_t len) {
    PORTB |= (1 << LED_STATUS); // Activity indicator
    
    fbus_frame_t frame;
    if (parse_fbus_frame(data, len, &frame)) {
        switch (frame.type) {
            case FBUS_TYPE_MENU_SELECT:
                if (frame.data[0] < MAX_COMMANDS) {
                    execute_command(frame.data[0]);
                }
                break;
                
            case FBUS_TYPE_MENU_REQUEST:
                send_menu_to_phone();
                break;
                
            default:
                // Unknown frame type
                error_state = 1;
                PORTB |= (1 << LED_ERROR);
                break;
        }
    }
    
    PORTB &= ~(1 << LED_STATUS);
}

// Process OBD response
void process_obd_response(uint8_t *data, uint16_t len) {
    PORTB |= (1 << LED_STATUS);
    
    obd_response_t response;
    if (parse_obd_response(data, len, &response)) {
        // Format response for Nokia display
        uint8_t display_data[32];
        uint8_t display_len = format_obd_response(&response, display_data);
        
        // Send to phone
        send_fbus_frame(FBUS_TYPE_DISPLAY, display_data, display_len);
    } else {
        error_state = 1;
        PORTB |= (1 << LED_ERROR);
    }
    
    PORTB &= ~(1 << LED_STATUS);
}

// Execute stored command
void execute_command(uint8_t index) {
    stored_command_t cmd;
    
    // Read command from EEPROM
    eeprom_read_block(&cmd, &stored_commands[index], sizeof(stored_command_t));
    
    // Send to OBD
    send_obd_command(cmd.type, cmd.data, cmd.data_len);
}

// Send menu to phone
void send_menu_to_phone() {
    uint8_t count;
    eeprom_read_block(&count, &command_count, sizeof(uint8_t));
    
    // Format menu data
    uint8_t menu_data[256];
    uint8_t pos = 0;
    
    // Add header
    const char header[] = "Stored Commands:";
    memcpy(&menu_data[pos], header, sizeof(header)-1);
    pos += sizeof(header)-1;
    
    // Add commands
    for (uint8_t i = 0; i < count && i < MAX_COMMANDS; i++) {
        stored_command_t cmd;
        eeprom_read_block(&cmd, &stored_commands[i], sizeof(stored_command_t));
        
        menu_data[pos++] = '\n';
        menu_data[pos++] = i + '1';
        menu_data[pos++] = '.';
        menu_data[pos++] = ' ';
        
        uint8_t name_len = strnlen(cmd.name, CMD_NAME_LEN);
        memcpy(&menu_data[pos], cmd.name, name_len);
        pos += name_len;
    }
    
    // Send menu frame
    send_fbus_frame(FBUS_TYPE_MENU, menu_data, pos);
}

// Store new command
uint8_t store_command(const char *name, uint8_t type, const uint8_t *data, uint8_t len) {
    uint8_t count;
    eeprom_read_block(&count, &command_count, sizeof(uint8_t));
    
    if (count >= MAX_COMMANDS) {
        return 0; // Storage full
    }
    
    stored_command_t cmd;
    strncpy(cmd.name, name, CMD_NAME_LEN-1);
    cmd.name[CMD_NAME_LEN-1] = '\0';
    cmd.type = type;
    memcpy(cmd.data, data, len);
    cmd.data_len = len;
    
    // Store in EEPROM
    eeprom_write_block(&cmd, &stored_commands[count], sizeof(stored_command_t));
    count++;
    eeprom_write_byte(&command_count, count);
    
    return 1;
}

int main(void) {
    // Initialize system
    system_init();
    
    // Main loop
    while (1) {
        // Check for errors
        if (error_state) {
            PORTB |= (1 << LED_ERROR);
            _delay_ms(100);
            PORTB &= ~(1 << LED_ERROR);
            _delay_ms(100);
            error_state = 0;
        }
        
        // Power saving
        set_sleep_mode(SLEEP_MODE_IDLE);
        sleep_mode();
    }
    
    return 0;
}
