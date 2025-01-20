#!/usr/bin/env python3
"""
Command Storage Utility for Nokia 3310 CAN Bus Interface
Allows storing custom commands in phone memory when connected to PC

Developed by Khanfar Systems © 2025
"""

import sys
import argparse
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

from src.fbus.protocol import FBUSProtocol
from src.storage.commands import CommandStorage

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='Store custom commands in Nokia 3310 memory'
    )
    parser.add_argument(
        '--port',
        type=str,
        required=True,
        help='FBUS serial port'
    )
    parser.add_argument(
        '--name',
        type=str,
        required=True,
        help='Command name (max 12 chars)'
    )
    parser.add_argument(
        '--type',
        type=str,
        required=True,
        help='Command type in hex (e.g., 0x01)'
    )
    parser.add_argument(
        '--data',
        type=str,
        required=True,
        help='Command data in hex (e.g., 010C for RPM)'
    )
    parser.add_argument(
        '--list',
        action='store_true',
        help='List stored commands'
    )
    parser.add_argument(
        '--remove',
        type=int,
        help='Remove command at index'
    )
    return parser.parse_args()

def validate_hex(hex_str: str) -> bytes:
    """Validate and convert hex string to bytes.
    
    Args:
        hex_str: Hex string to validate
        
    Returns:
        Converted bytes
        
    Raises:
        ValueError: If hex string is invalid
    """
    # Remove 0x prefix if present
    if hex_str.startswith('0x'):
        hex_str = hex_str[2:]
    
    # Validate hex string
    if not all(c in '0123456789ABCDEFabcdef' for c in hex_str):
        raise ValueError(f"Invalid hex string: {hex_str}")
    
    # Ensure even length
    if len(hex_str) % 2 != 0:
        hex_str = '0' + hex_str
    
    try:
        return bytes.fromhex(hex_str)
    except ValueError as e:
        raise ValueError(f"Invalid hex string: {hex_str}") from e

def main():
    """Main entry point."""
    args = parse_args()
    
    try:
        # Initialize FBUS communication
        fbus = FBUSProtocol(port=args.port)
        storage = CommandStorage(fbus)
        
        if args.list:
            # List stored commands
            commands = storage.get_commands()
            if not commands:
                print("No commands stored")
            else:
                print("\nStored Commands:")
                print("-" * 40)
                for i, cmd in enumerate(commands):
                    print(f"{i+1}. {cmd['name']}")
                    print(f"   Type: 0x{cmd['type']:02X}")
                    print(f"   Data: {cmd['command'].hex().upper()}")
                    print("-" * 40)
            return
        
        if args.remove is not None:
            # Remove command
            if storage.remove_command(args.remove - 1):
                print(f"Removed command at index {args.remove}")
            else:
                print(f"Failed to remove command at index {args.remove}")
            return
        
        # Validate command type
        try:
            cmd_type = int(args.type, 16)
            if not 0 <= cmd_type <= 255:
                raise ValueError
        except ValueError:
            print(f"Invalid command type: {args.type}")
            return
        
        # Validate command data
        try:
            cmd_data = validate_hex(args.data)
        except ValueError as e:
            print(f"Invalid command data: {e}")
            return
        
        # Add command
        if storage.add_command(args.name, cmd_type, cmd_data):
            print(f"Successfully stored command: {args.name}")
            
            # Show updated command list
            print("\nUpdated Command List:")
            print("-" * 40)
            for i, cmd in enumerate(storage.get_commands()):
                print(f"{i+1}. {cmd['name']}")
            print("-" * 40)
        else:
            print("Failed to store command")
    
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
