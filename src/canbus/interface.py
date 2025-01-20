"""
CAN Bus Interface for OBDLink SX
Handles communication with vehicle through OBD-II port

Developed by Khanfar Systems © 2025
"""

import obd
import logging
from typing import Dict, Any, Optional
from obd import OBDCommand, OBDResponse

logger = logging.getLogger(__name__)

class CANBusInterface:
    """Interface for communicating with vehicle CAN bus through OBDLink SX."""
    
    def __init__(self):
        """Initialize CAN bus interface."""
        self.connection = None
        self.supported_commands = {}
        self._connect()
    
    def _connect(self):
        """Establish connection with OBDLink SX and vehicle."""
        try:
            # Auto-connect to OBDLink SX
            self.connection = obd.OBD(fast=False)
            
            if not self.connection.is_connected():
                raise ConnectionError("Failed to connect to OBDLink SX")
            
            # Query available commands
            self.supported_commands = self._get_supported_commands()
            logger.info("Connected to vehicle through OBDLink SX")
            
        except Exception as e:
            logger.error(f"Failed to connect to OBDLink SX: {e}")
            raise
    
    def _get_supported_commands(self) -> Dict[str, OBDCommand]:
        """Get dictionary of supported OBD commands.
        
        Returns:
            Dictionary of command name to OBDCommand object
        """
        supported = {}
        for command in self.connection.supported_commands:
            supported[command.name] = command
        return supported
    
    def read_sensor(self, sensor_name: str) -> Optional[float]:
        """Read value from specified sensor.
        
        Args:
            sensor_name: Name of sensor to read (e.g., 'RPM', 'SPEED')
            
        Returns:
            Sensor value if successful, None otherwise
        """
        if sensor_name not in self.supported_commands:
            logger.warning(f"Unsupported sensor: {sensor_name}")
            return None
        
        try:
            response = self.connection.query(self.supported_commands[sensor_name])
            if response.is_null():
                return None
                
            return response.value.magnitude
            
        except Exception as e:
            logger.error(f"Error reading sensor {sensor_name}: {e}")
            return None
    
    def get_dtc_codes(self) -> list[str]:
        """Read Diagnostic Trouble Codes (DTCs).
        
        Returns:
            List of DTC codes
        """
        try:
            response = self.connection.query(obd.commands.GET_DTC)
            if response.is_null():
                return []
                
            return [dtc for dtc, _ in response.value]
            
        except Exception as e:
            logger.error(f"Error reading DTCs: {e}")
            return []
    
    def clear_dtc_codes(self) -> bool:
        """Clear all Diagnostic Trouble Codes.
        
        Returns:
            True if successful, False otherwise
        """
        try:
            response = self.connection.query(obd.commands.CLEAR_DTC)
            return not response.is_null()
            
        except Exception as e:
            logger.error(f"Error clearing DTCs: {e}")
            return False
    
    def get_vehicle_info(self) -> Dict[str, Any]:
        """Get basic vehicle information.
        
        Returns:
            Dictionary of vehicle information
        """
        info = {}
        info_commands = [
            ('VIN', obd.commands.VIN),
            ('ECU_NAME', obd.commands.ECU_NAME),
            ('FUEL_STATUS', obd.commands.FUEL_STATUS),
            ('ENGINE_LOAD', obd.commands.ENGINE_LOAD)
        ]
        
        for name, command in info_commands:
            try:
                response = self.connection.query(command)
                if not response.is_null():
                    info[name] = response.value
            except:
                continue
                
        return info
    
    def monitor_sensor(self, sensor_name: str, callback) -> None:
        """Start monitoring a sensor in real-time.
        
        Args:
            sensor_name: Name of sensor to monitor
            callback: Function to call with each new value
        """
        if sensor_name not in self.supported_commands:
            logger.warning(f"Unsupported sensor: {sensor_name}")
            return
        
        try:
            self.connection.watch(self.supported_commands[sensor_name], callback)
            self.connection.start()
            logger.info(f"Started monitoring {sensor_name}")
            
        except Exception as e:
            logger.error(f"Error setting up monitoring for {sensor_name}: {e}")
    
    def stop_monitoring(self) -> None:
        """Stop all sensor monitoring."""
        try:
            self.connection.stop()
            self.connection.unwatch_all()
            logger.info("Stopped all monitoring")
            
        except Exception as e:
            logger.error(f"Error stopping monitoring: {e}")
    
    def close(self):
        """Close connection to OBDLink SX."""
        if self.connection:
            self.stop_monitoring()
            self.connection.close()
            logger.info("Closed connection to OBDLink SX")
