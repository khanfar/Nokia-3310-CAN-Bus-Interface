"""
FBUS Protocol Implementation for Nokia 3310
Handles communication with Nokia phone using FBUS protocol

Developed by Khanfar Systems © 2025
"""

import time
import serial
import logging
from typing import List, Optional, Tuple

logger = logging.getLogger(__name__)

class FBUSProtocol:
    """Implementation of Nokia FBUS protocol."""
    
    # FBUS Constants
    FRAME_ID = 0x1E  # Serial FBUS
    PHONE_DEV = 0x00
    PC_DEV = 0x0C
    
    def __init__(self, port: str, baudrate: int = 9600):
        """Initialize FBUS protocol handler.
        
        Args:
            port: Serial port for FBUS communication
            baudrate: Baud rate (default: 9600)
        """
        self.port = port
        self.baudrate = baudrate
        self.serial = None
        self.sequence = 0x08  # Initial sequence number for PC
        self._connect()
    
    def _connect(self):
        """Establish serial connection with Nokia phone."""
        try:
            self.serial = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                bytesize=serial.EIGHTBITS,
                parity=serial.PARITY_ODD,
                stopbits=serial.STOPBITS_ONE,
                timeout=1
            )
            logger.info(f"Connected to {self.port} at {self.baudrate} baud")
        except serial.SerialException as e:
            logger.error(f"Failed to connect to {self.port}: {e}")
            raise
    
    def _calculate_checksum(self, data: bytes) -> Tuple[int, int]:
        """Calculate FBUS checksums.
        
        Args:
            data: Data bytes to calculate checksums for
            
        Returns:
            Tuple of (odd checksum, even checksum)
        """
        odd_sum = 0
        even_sum = 0
        
        for i, byte in enumerate(data):
            if i % 2:
                odd_sum ^= byte
            else:
                even_sum ^= byte
        
        return odd_sum, even_sum
    
    def _create_frame(self, msg_type: int, payload: bytes) -> bytes:
        """Create FBUS frame with proper structure.
        
        Args:
            msg_type: Type of message
            payload: Message payload bytes
            
        Returns:
            Complete FBUS frame as bytes
        """
        # Basic frame structure
        frame = bytes([
            self.FRAME_ID,      # Frame ID
            self.PHONE_DEV,     # Destination (phone)
            self.PC_DEV,        # Source (PC)
            msg_type,           # Message type
            0x00,              # Command
            len(payload)        # Length
        ])
        
        # Add payload
        frame += payload
        
        # Add sequence number
        frame += bytes([0x01, self.sequence])  # 0x01 = last frame
        
        # Calculate and add checksums
        odd_sum, even_sum = self._calculate_checksum(frame)
        frame += bytes([odd_sum, even_sum])
        
        # Update sequence number for next frame
        self.sequence = (self.sequence + 1) & 0x07 | 0x08
        
        return frame
    
    def send_command(self, msg_type: int, payload: bytes) -> Optional[bytes]:
        """Send command to phone and wait for response.
        
        Args:
            msg_type: Type of message to send
            payload: Command payload
            
        Returns:
            Response payload if successful, None otherwise
        """
        if not self.serial or not self.serial.is_open:
            raise ConnectionError("Serial port not open")
        
        # Create and send frame
        frame = self._create_frame(msg_type, payload)
        
        try:
            # Wait for bus to be free (3ms)
            time.sleep(0.003)
            
            # Send frame
            self.serial.write(frame)
            logger.debug(f"Sent frame: {frame.hex()}")
            
            # Wait for acknowledgment (200ms timeout)
            ack = self.serial.read(2)
            if len(ack) != 2 or ack[0] != 0x7F:
                logger.warning("No acknowledgment received")
                return None
            
            # Read response
            response = self._read_response()
            return response
            
        except serial.SerialException as e:
            logger.error(f"Serial communication error: {e}")
            return None
    
    def _read_response(self) -> Optional[bytes]:
        """Read and parse response from phone.
        
        Returns:
            Response payload if valid, None otherwise
        """
        # Read header (6 bytes)
        header = self.serial.read(6)
        if len(header) != 6:
            logger.warning("Invalid response header")
            return None
        
        # Get payload length
        payload_len = header[5]
        
        # Read payload and footer
        payload = self.serial.read(payload_len + 4)  # payload + seq + checksums
        if len(payload) != payload_len + 4:
            logger.warning("Invalid response payload")
            return None
        
        return payload[:-4]  # Remove sequence and checksums
    
    def close(self):
        """Close serial connection."""
        if self.serial and self.serial.is_open:
            self.serial.close()
            logger.info("Serial connection closed")
