# Vehicle Immobilizer Programming Guide

[📚 Documentation](INDEX.md) > Immobilizer Guide

## ⚠️ IMPORTANT SECURITY NOTICE
```
This document is for EDUCATIONAL PURPOSES ONLY.
Unauthorized access to vehicle security systems is illegal.
Only use on vehicles you own or have explicit permission to work on.
```

## Key Fob Programming Procedures

### Toyota Smart Key Programming
```
1. Enter Programming Mode
   -> Send: 31 01 00 (Start Session)
   <- Recv: 71 01 00 (Session Started)

2. Authenticate
   -> Send: 27 01 (Request Seed)
   <- Recv: 67 01 [4-byte seed]
   -> Send: 27 02 [calculated key]
   <- Recv: 67 02 00 (Success)

3. Register New Key
   -> Send: 31 02 00 (Start Registration)
   <- Recv: 71 02 01 (Waiting for Key)
   Action: Present new key to antenna
   <- Recv: 71 02 02 (Key Detected)
   -> Send: 31 03 00 (Confirm Key)
   <- Recv: 71 03 00 (Key Registered)

4. Verify Registration
   -> Send: 31 04 00 (Read Status)
   <- Recv: 71 04 [key_count][status]
```

### Honda Smart Entry
```
1. Initialize Programming
   -> Send: 72 00 (Start Session)
   <- Recv: 72 00 00 (Session OK)

2. Security Access
   -> Send: 27 11 (Programming Access)
   <- Recv: 67 11 00 (Access Granted)

3. Program Key
   Step 1: Clear Memory
   -> Send: 72 10 (Clear Keys)
   <- Recv: 72 10 00 (Memory Cleared)

   Step 2: Register Master
   -> Send: 72 20 (Register Master)
   <- Recv: 72 20 01 (Present Key)
   Action: Hold master key near antenna
   <- Recv: 72 20 00 (Master Registered)

   Step 3: Add Sub Keys
   -> Send: 72 30 (Add Key)
   <- Recv: 72 30 01 (Present Key)
   Action: Hold new key near antenna
   <- Recv: 72 30 00 (Key Added)
```

### BMW Key Programming
```
1. Access EWS Module
   -> Send: 3E 01 (Start Session)
   <- Recv: 7E 01 00 (Session OK)

2. Security Login
   -> Send: 27 01 (Request Seed)
   <- Recv: 67 01 [seed]
   -> Send: 27 02 [key]
   <- Recv: 67 02 00 (Accepted)

3. Program New Key
   Step 1: Initialize
   -> Send: 3E 10 (Start Programming)
   <- Recv: 7E 10 00 (Ready)

   Step 2: Write Key Data
   -> Send: 3E 11 [key_data]
   <- Recv: 7E 11 00 (Written)

   Step 3: Activate
   -> Send: 3E 12 (Activate Key)
   <- Recv: 7E 12 00 (Activated)
```

### Mercedes-Benz Key Programming
```
1. Start Diagnostic Session
   -> Send: A1 01 (Start Session)
   <- Recv: E1 01 00 (Session Started)

2. Security Access
   -> Send: 27 01 (Request Access)
   <- Recv: 67 01 [seed]
   -> Send: 27 02 [response]
   <- Recv: 67 02 00 (Granted)

3. Key Programming
   Step 1: Prepare System
   -> Send: A1 10 (Initialize)
   <- Recv: E1 10 00 (Ready)

   Step 2: Write Key Data
   -> Send: A1 20 [key_data]
   <- Recv: E1 20 00 (Written)

   Step 3: Validate
   -> Send: A1 30 (Test Key)
   <- Recv: E1 30 00 (Validated)
```

### VW/Audi Key Programming
```
1. Access Security
   -> Send: 10 03 (Extended Session)
   <- Recv: 50 03 00 (Session OK)

2. Login
   -> Send: 27 01 (Request Seed)
   <- Recv: 67 01 [seed]
   -> Send: 27 02 [login_key]
   <- Recv: 67 02 00 (Logged In)

3. Program Key
   Step 1: Start Programming
   -> Send: 2E 03 (Programming Mode)
   <- Recv: 6E 03 00 (Mode Active)

   Step 2: Write SKC
   -> Send: 2E 04 [skc_data]
   <- Recv: 6E 04 00 (SKC Written)

   Step 3: Adapt Key
   -> Send: 2E 05 [adaptation_data]
   <- Recv: 6E 05 00 (Key Adapted)
```

### Hyundai/Kia Smart Key Programming
```
1. Initialize System
   -> Send: 22 B0 (Start Session)
   <- Recv: 62 B0 00 (Session OK)

2. Security Access
   -> Send: 27 01 (Request Seed)
   <- Recv: 67 01 [seed_data]
   -> Send: 27 02 [calculated_key]
   <- Recv: 67 02 00 (Access OK)

3. Program Smart Key
   Step 1: Enter Program Mode
   -> Send: 22 B1 01 (Program Mode)
   <- Recv: 62 B1 00 (Mode Active)

   Step 2: Register Key
   -> Send: 22 B1 02 (Start Register)
   <- Recv: 62 B1 01 (Present Key)
   Action: Hold key near start button
   <- Recv: 62 B1 02 (Key Detected)

   Step 3: Confirm Registration
   -> Send: 22 B1 03 (Confirm)
   <- Recv: 62 B1 00 (Success)
```

### Nissan Intelligent Key
```
1. Access BCM
   -> Send: 1A 90 (Diagnostic Mode)
   <- Recv: 5A 90 00 (Mode Active)

2. Security Login
   -> Send: 27 01 (Request Access)
   <- Recv: 67 01 [seed]
   -> Send: 27 02 [response]
   <- Recv: 67 02 00 (Logged In)

3. Key Registration
   Step 1: Clear Memory
   -> Send: 1A 91 (Clear Keys)
   <- Recv: 5A 91 00 (Cleared)

   Step 2: Register Key
   -> Send: 1A 92 (Register Mode)
   <- Recv: 5A 92 01 (Ready)
   Action: Touch key to start button
   <- Recv: 5A 92 02 (Key Read)

   Step 3: Save Registration
   -> Send: 1A 93 (Save Key)
   <- Recv: 5A 93 00 (Saved)
```

### Subaru Keyless System
```
1. Start Programming
   -> Send: 27 10 (Access Request)
   <- Recv: 67 10 [seed_value]
   -> Send: 27 11 [calculated]
   <- Recv: 67 11 00 (Granted)

2. Enter Registration
   Step 1: Initialize
   -> Send: 27 20 (Start Register)
   <- Recv: 67 20 00 (Ready)

   Step 2: Add Key
   -> Send: 27 21 (Program Key)
   <- Recv: 67 21 01 (Present Key)
   Action: Place key in specified position
   <- Recv: 67 21 02 (Key Found)

   Step 3: Finalize
   -> Send: 27 22 (Complete)
   <- Recv: 67 22 00 (Success)
```

### Mazda Advanced Keyless
```
1. Enter Programming
   -> Send: 2F 01 (Start Session)
   <- Recv: 6F 01 00 (Session OK)

2. Security Access
   -> Send: 27 01 (Request Seed)
   <- Recv: 67 01 [seed]
   -> Send: 27 02 [response]
   <- Recv: 67 02 00 (Access OK)

3. Key Programming
   Step 1: Prepare System
   -> Send: 2F 10 (Initialize)
   <- Recv: 6F 10 00 (Ready)

   Step 2: Register Key
   -> Send: 2F 11 (Program Mode)
   <- Recv: 6F 11 01 (Insert Key)
   Action: Insert key into slot
   <- Recv: 6F 11 02 (Key Read)

   Step 3: Complete
   -> Send: 2F 12 (Finalize)
   <- Recv: 6F 12 00 (Complete)
```

### Volvo Keyless Entry
```
1. Access CEM
   -> Send: 3B 01 (Start Session)
   <- Recv: 7B 01 00 (Session OK)

2. Authorization
   -> Send: 27 01 (Request Access)
   <- Recv: 67 01 [seed_data]
   -> Send: 27 02 [calculated]
   <- Recv: 67 02 00 (Authorized)

3. Key Programming
   Step 1: Start Programming
   -> Send: 3B 10 (Program Mode)
   <- Recv: 7B 10 00 (Mode Active)

   Step 2: Write Key Data
   -> Send: 3B 11 [key_data]
   <- Recv: 7B 11 00 (Data Written)

   Step 3: Validate Key
   -> Send: 3B 12 (Validate)
   <- Recv: 7B 12 00 (Key Valid)
```

### Mitsubishi FAST-Key
```
1. Initialize System
   -> Send: 31 A0 (Start Session)
   <- Recv: 71 A0 00 (Session OK)

2. Security Access
   -> Send: 27 01 (Request Seed)
   <- Recv: 67 01 [seed]
   -> Send: 27 02 [response]
   <- Recv: 67 02 00 (Access OK)

3. Key Registration
   Step 1: Enter Program
   -> Send: 31 A1 (Program Mode)
   <- Recv: 71 A1 00 (Mode Active)

   Step 2: Register Key
   -> Send: 31 A2 (Register)
   <- Recv: 71 A2 01 (Present Key)
   Action: Hold key near antenna
   <- Recv: 71 A2 02 (Key Found)

   Step 3: Complete
   -> Send: 31 A3 (Finalize)
   <- Recv: 71 A3 00 (Success)
```

### Lexus Smart Access
```
1. Access Smart ECU
   -> Send: 82 F1 00 (Start Session)
   <- Recv: C2 F1 00 (Session OK)

2. Security Login
   -> Send: 27 01 (Request Seed)
   <- Recv: 67 01 [seed_data]
   -> Send: 27 02 [calculated]
   <- Recv: 67 02 00 (Login OK)

3. Key Programming
   Step 1: Initialize
   -> Send: 82 F1 10 (Program Mode)
   <- Recv: C2 F1 10 00 (Ready)

   Step 2: Register Key
   -> Send: 82 F1 11 (Register)
   <- Recv: C2 F1 11 01 (Present Key)
   Action: Place key on start button
   <- Recv: C2 F1 11 02 (Key Read)

   Step 3: Finalize
   -> Send: 82 F1 12 (Complete)
   <- Recv: C2 F1 12 00 (Success)
```

## Common Key Programming Patterns

### Security Access Flow
```
1. Request Seed
   -> Send: 27 01
   <- Recv: 67 01 [seed]

2. Calculate Response
   Algorithm varies by manufacturer:
   - XOR with secret key
   - SHA-1 hash
   - Proprietary algorithm

3. Send Response
   -> Send: 27 02 [calculated]
   <- Recv: 67 02 [result]
```

### Key Registration States
```
Common Status Codes:
00 - Success
01 - Waiting for Key
02 - Key Detected
03 - Registration Complete
7F - Error

Error Codes:
22 - Conditions Not Met
24 - Request Sequence Error
31 - Request Out of Range
33 - Security Access Denied
35 - Invalid Key
36 - Exceed Attempts
37 - Required Time Delay
```

### Programming Requirements
```
1. Vehicle State
   □ Battery voltage >12V
   □ Key in ON position
   □ Doors closed
   □ Hood closed
   □ Engine off
   □ Parking brake on

2. Equipment Needed
   □ OBD-II interface
   □ Security access codes
   □ Programming software
   □ Backup power supply

3. Safety Precautions
   □ Disable airbags
   □ Clear work area
   □ Document settings
   □ Backup existing keys
```

## Related Documentation
- [Alternative Access](ALTERNATIVE_ACCESS.md)
- [Circuit Diagrams](CIRCUIT_DIAGRAMS.md)
- [Troubleshooting Guide](TROUBLESHOOTING.md)

---
Copyright (c) 2025 Khanfar - Educational Project  
https://github.com/khanfar/Nokia-3310-CAN-Bus-Interface
