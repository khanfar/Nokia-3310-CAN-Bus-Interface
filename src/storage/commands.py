"""
Command Storage Module for Nokia 3310 CAN Bus Interface
Handles saving and loading custom commands in phone's memory

Developed by Khanfar Systems © 2025
"""

import struct
from typing import List, Dict, Optional

class CommandStorage:
    """Handles storage and retrieval of custom commands in phone memory."""
    
    # FBUS memory commands
    CMD_READ_MEM = 0x23
    CMD_WRITE_MEM = 0x24
    
    # Memory locations (using phone's free memory area)
    MEM_START = 0x1000  # Starting address for command storage
    MAX_COMMANDS = 10   # Maximum number of stored commands
    
    def __init__(self, fbus_protocol):
        """Initialize command storage.
        
        Args:
            fbus_protocol: FBUS protocol instance for memory access
        """
        self.fbus = fbus_protocol
        self.commands = self._load_commands()
    
    def _load_commands(self) -> List[Dict]:
        """Load saved commands from phone memory.
        
        Returns:
            List of command dictionaries
        """
        try:
            # Read command count
            count_data = self._read_memory(self.MEM_START, 1)
            if not count_data:
                return []
            
            count = count_data[0]
            commands = []
            
            # Read each command
            addr = self.MEM_START + 1
            for _ in range(count):
                # Read command length
                len_data = self._read_memory(addr, 1)
                if not len_data:
                    break
                    
                length = len_data[0]
                addr += 1
                
                # Read command data
                cmd_data = self._read_memory(addr, length)
                if not cmd_data:
                    break
                
                # Parse command data
                try:
                    name_len = cmd_data[0]
                    name = cmd_data[1:name_len+1].decode('ascii')
                    cmd_type = cmd_data[name_len+1]
                    cmd_bytes = bytes(cmd_data[name_len+2:])
                    
                    commands.append({
                        'name': name,
                        'type': cmd_type,
                        'command': cmd_bytes
                    })
                except:
                    continue
                    
                addr += length
            
            return commands
            
        except Exception as e:
            print(f"Error loading commands: {e}")
            return []
    
    def _save_commands(self) -> bool:
        """Save commands to phone memory.
        
        Returns:
            True if successful, False otherwise
        """
        try:
            # Prepare data
            data = bytearray([len(self.commands)])  # Command count
            
            for cmd in self.commands:
                name_bytes = cmd['name'].encode('ascii')
                cmd_data = bytes([
                    len(name_bytes),  # Name length
                    *name_bytes,      # Name
                    cmd['type'],      # Command type
                    *cmd['command']   # Command bytes
                ])
                data.extend([len(cmd_data)])  # Command length
                data.extend(cmd_data)
            
            # Write to memory
            return self._write_memory(self.MEM_START, data)
            
        except Exception as e:
            print(f"Error saving commands: {e}")
            return False
    
    def _read_memory(self, address: int, length: int) -> Optional[bytes]:
        """Read data from phone memory.
        
        Args:
            address: Memory address to read from
            length: Number of bytes to read
            
        Returns:
            Read data if successful, None otherwise
        """
        cmd = struct.pack('>HB', address, length)
        response = self.fbus.send_command(self.CMD_READ_MEM, cmd)
        
        if response and len(response) >= length:
            return response[:length]
        return None
    
    def _write_memory(self, address: int, data: bytes) -> bool:
        """Write data to phone memory.
        
        Args:
            address: Memory address to write to
            data: Data to write
            
        Returns:
            True if successful, False otherwise
        """
        cmd = struct.pack('>H', address) + data
        response = self.fbus.send_command(self.CMD_WRITE_MEM, cmd)
        return response is not None
    
    def add_command(self, name: str, cmd_type: int, command: bytes) -> bool:
        """Add new command to storage.
        
        Args:
            name: Command name (max 12 chars)
            cmd_type: Command type
            command: Command bytes
            
        Returns:
            True if successful, False otherwise
        """
        if len(self.commands) >= self.MAX_COMMANDS:
            return False
            
        # Truncate name if too long
        name = name[:12]
        
        self.commands.append({
            'name': name,
            'type': cmd_type,
            'command': command
        })
        
        return self._save_commands()
    
    def remove_command(self, index: int) -> bool:
        """Remove command at specified index.
        
        Args:
            index: Command index to remove
            
        Returns:
            True if successful, False otherwise
        """
        if 0 <= index < len(self.commands):
            self.commands.pop(index)
            return self._save_commands()
        return False
    
    def get_commands(self) -> List[Dict]:
        """Get list of stored commands.
        
        Returns:
            List of command dictionaries
        """
        return self.commands.copy()
    
    def execute_command(self, index: int) -> Optional[bytes]:
        """Execute stored command.
        
        Args:
            index: Index of command to execute
            
        Returns:
            Command response if successful, None otherwise
        """
        if 0 <= index < len(self.commands):
            cmd = self.commands[index]
            return self.fbus.send_command(cmd['type'], cmd['command'])
        return None
