#!/usr/bin/env python3
"""
Nokia 3310 CAN Bus Interface
Main entry point for the application

Copyright (c) 2025 Khanfar
https://github.com/khanfar/Nokia-3310-CAN-Bus-Interface
For educational purposes - see LICENSE file for details
"""

import sys
import time
import logging
import argparse
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from src.fbus.protocol import FBUSProtocol
from src.canbus.interface import CANBusInterface
from src.ui.interface import UserInterface

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Nokia 3310 CAN Bus Interface')
    parser.add_argument('--port', type=str, help='FBUS serial port')
    parser.add_argument('--baud', type=int, default=9600, help='FBUS baud rate')
    parser.add_argument('--debug', action='store_true', help='Enable debug logging')
    parser.add_argument('--retry', type=int, default=3, help='Connection retry attempts')
    return parser.parse_args()

def wait_for_phone(port: str, baudrate: int, max_attempts: int = 3) -> FBUSProtocol:
    """Wait for phone to become available.
    
    Args:
        port: Serial port to connect to
        baudrate: Baud rate for connection
        max_attempts: Maximum number of connection attempts
        
    Returns:
        Connected FBUSProtocol instance
        
    Raises:
        ConnectionError: If connection fails after max attempts
    """
    attempt = 0
    while attempt < max_attempts:
        try:
            fbus = FBUSProtocol(port=port, baudrate=baudrate)
            logger.info("Successfully connected to phone")
            return fbus
        except Exception as e:
            attempt += 1
            if attempt < max_attempts:
                logger.warning(f"Connection attempt {attempt} failed: {e}")
                logger.info("Waiting 5 seconds before retry...")
                time.sleep(5)
            else:
                raise ConnectionError(f"Failed to connect after {max_attempts} attempts")

def main():
    """Main application entry point."""
    args = parse_args()
    
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
    
    while True:
        try:
            # Initialize FBUS communication with retry
            fbus = wait_for_phone(args.port, args.baud, args.retry)
            
            # Initialize CAN bus interface
            canbus = CANBusInterface()
            logger.info("CAN bus interface initialized")
            
            # Start user interface
            ui = UserInterface(fbus, canbus)
            ui.run()
            
        except KeyboardInterrupt:
            logger.info("Application terminated by user")
            sys.exit(0)
        except ConnectionError as e:
            logger.error(f"Connection error: {e}")
            response = input("Retry connection? (y/n): ")
            if response.lower() != 'y':
                sys.exit(1)
        except Exception as e:
            logger.error(f"Application error: {e}")
            response = input("Retry application? (y/n): ")
            if response.lower() != 'y':
                sys.exit(1)
        finally:
            # Ensure clean shutdown
            try:
                if 'fbus' in locals():
                    fbus.close()
                if 'canbus' in locals():
                    canbus.close()
            except:
                pass

if __name__ == '__main__':
    main()
