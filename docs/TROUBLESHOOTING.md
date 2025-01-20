# Troubleshooting Guide

## Quick Reference

### LED Status Indicators
```
Power LED (Green):
✅ Solid: Normal operation
❌ Off: No power
🟡 Blinking: Low voltage

Status LED (Blue):
✅ Blinking: Active communication
❌ Off: No communication
🟡 Solid: Initializing

Error LED (Red):
✅ Off: No errors
❌ Solid: Critical error
🟡 Blinking: Recoverable error
```

## Common Issues

### 1. Connection Problems

#### No Communication with Phone
```
Symptoms:
- Status LED not blinking
- Phone not responding
- "No Device" error

Steps:
1. Check Connections
   - Verify FBUS cable is firmly connected
   - Inspect cable for damage
   - Try different USB port

2. Check Phone
   - Ensure battery is charged
   - Remove and reinsert battery
   - Check phone display works

3. Software Check
   - Verify COM port number
   - Run as administrator
   - Check USB drivers

4. Hardware Test
   ❯ Test cable continuity
   ❯ Measure FBUS voltage (should be 3.3V)
   ❯ Check USB power
```

#### OBD Connection Failed
```
Symptoms:
- "No OBD Response" error
- Can't read vehicle data
- Error LED blinking

Steps:
1. Vehicle Setup
   - Key in ON position
   - Engine may need to be running
   - Wait 5 seconds after power

2. Connection Check
   - Verify OBD adapter is secure
   - Check for bent pins
   - Try removing/reinserting

3. Protocol Issues
   - Try manual protocol selection
   - Check vehicle compatibility
   - Verify baud rate settings

4. Voltage Check
   ❯ Battery voltage > 11V
   ❯ OBD port power present
   ❯ Adapter LED indicators
```

### 2. Display Problems

#### Garbled Text
```
Symptoms:
- Unreadable characters
- Missing lines
- Screen artifacts

Solutions:
1. Reset Display
   - Exit to main menu
   - Power cycle phone
   - Clear display buffer

2. Check Settings
   - Verify character encoding
   - Check display timing
   - Reset to defaults

3. Hardware Issues
   - Check cable shielding
   - Verify voltage levels
   - Look for interference
```

#### No Display Update
```
Symptoms:
- Screen frozen
- No response to input
- Blank sections

Solutions:
1. Software Reset
   - Force refresh display
   - Restart application
   - Clear command queue

2. Communication Check
   - Verify data flow
   - Check frame timing
   - Reset FBUS connection

3. Memory Issues
   - Clear stored commands
   - Reset phone memory
   - Check buffer overflow
```

### 3. Command Execution

#### Commands Not Working
```
Symptoms:
- No response from car
- Error messages
- Timeout errors

Debug Steps:
1. Basic Tests
   - Try simple commands first (RPM)
   - Verify command format
   - Check timing requirements

2. Protocol Check
   - Confirm OBD protocol
   - Verify PID support
   - Check message timing

3. Advanced Tests
   - Monitor communication
   - Log all transactions
   - Analyze timing patterns
```

#### Stored Commands Lost
```
Symptoms:
- Missing commands
- Reset to defaults
- Memory errors

Solutions:
1. Memory Check
   - Verify storage space
   - Check for corruption
   - Backup current commands

2. Storage Issues
   - Reformat memory
   - Reload commands
   - Update firmware

3. Prevention
   - Regular backups
   - Verify saves
   - Use checksums
```

### 4. Performance Issues

#### Slow Response
```
Symptoms:
- Long delays
- Missed updates
- Laggy interface

Optimization:
1. Software
   - Reduce polling rate
   - Optimize queries
   - Clear old data

2. Hardware
   - Check CPU usage
   - Monitor memory
   - Verify timing

3. Connection
   - Test different speeds
   - Check for errors
   - Optimize protocol
```

#### Battery Drain
```
Symptoms:
- Quick battery depletion
- Phone shutdowns
- Voltage warnings

Solutions:
1. Power Settings
   - Enable power saving
   - Reduce update frequency
   - Optimize display

2. Hardware Check
   - Measure current draw
   - Check for shorts
   - Verify regulators

3. Software
   - Implement sleep modes
   - Batch commands
   - Reduce polling
```

## Advanced Troubleshooting

### Diagnostic Mode
```
Access:
1. Power on while holding '1'
2. Enter code: *#0000#
3. Select 'Diagnostic Mode'

Tests Available:
- Communication test
- Memory check
- Display test
- Keypad test
```

### Debug Logging
```bash
# Enable detailed logging
python src/main.py --debug --log-level=DEBUG

# Monitor communication
python src/main.py --monitor --port=COM3

# Test specific command
python src/tools/test_command.py --cmd="010C"
```

### Hardware Diagnostics

#### Voltage Test Points
```
1. FBUS Connection
   - Pin 1: GND
   - Pin 2: 3.3V
   - Pin 3: TX
   - Pin 4: RX

2. OBD Connection
   - Pin 16: +12V
   - Pin 4: GND
   - Pin 6: CAN High
   - Pin 14: CAN Low
```

#### Signal Analysis
```
Oscilloscope Settings:
- FBUS: 2V/div, 100µs/div
- CAN: 1V/div, 10µs/div
- Trigger: Rising edge
- Coupling: DC
```

## Recovery Procedures

### Emergency Reset
```
1. Soft Reset
   - Hold power button 10s
   - Remove battery 30s
   - Clear all buffers

2. Hard Reset
   - Disconnect all cables
   - Clear stored commands
   - Reflash firmware
```

### Data Recovery
```
1. Backup Commands
   - Export to file
   - Save configurations
   - Document settings

2. Restore Procedure
   - Verify backup
   - Import commands
   - Test functionality
```

## Prevention Tips

### Regular Maintenance
```
Daily:
- Check connections
- Verify operation
- Monitor errors

Weekly:
- Backup commands
- Clean connections
- Test all functions

Monthly:
- Full system test
- Update firmware
- Deep cleaning
```

### Best Practices
```
1. Operation
   - Connect in correct order
   - Wait for initialization
   - Verify before commands

2. Storage
   - Keep dry and clean
   - Protect from EMI
   - Proper temperature

3. Updates
   - Check for updates
   - Test new features
   - Maintain backups
```

## Support Resources

### Documentation
- User Guide
- Hardware Manual
- Protocol Specs
- Command Reference

### Community Help
- GitHub Issues
- Project Wiki
- User Forums
- Email Support

### Tools
- Diagnostic Software
- Test Scripts
- Logging Utilities
- Analysis Tools

---
Copyright (c) 2025 Khanfar - Educational Project  
https://github.com/khanfar/Nokia-3310-CAN-Bus-Interface
