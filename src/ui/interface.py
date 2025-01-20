"""
User Interface for Nokia 3310 CAN Bus Interface
Handles communication between FBUS and CAN bus interfaces

Developed by Khanfar Systems 2025
"""

import time
import logging
from typing import Dict, Any
from threading import Thread, Event

from src.fbus.protocol import FBUSProtocol
from src.canbus.interface import CANBusInterface
from src.storage.commands import CommandStorage

logger = logging.getLogger(__name__)

class UserInterface:
    """User interface handling communication between FBUS and CAN bus."""
    
    # Nokia 3310 display constraints
    DISPLAY_WIDTH = 14  # characters
    DISPLAY_HEIGHT = 5  # lines
    
    # FBUS message types
    MSG_DISPLAY = 0x20
    MSG_KEYPRESS = 0x21
    MSG_MENU = 0x22
    
    def __init__(self, fbus: FBUSProtocol, canbus: CANBusInterface):
        """Initialize user interface.
        
        Args:
            fbus: FBUS protocol handler
            canbus: CAN bus interface
        """
        self.fbus = fbus
        self.canbus = canbus
        self.command_storage = CommandStorage(fbus)
        self.running = False
        self.current_menu = "main"
        self.monitoring_thread = None
        self.stop_monitoring = Event()
    
    def _format_display(self, text: str) -> bytes:
        """Format text for Nokia 3310 display.
        
        Args:
            text: Text to format
            
        Returns:
            Formatted text as bytes
        """
        # Split into lines and truncate/pad to display width
        lines = text.split('\n')[:self.DISPLAY_HEIGHT]
        formatted = []
        
        for line in lines:
            # Truncate line if too long
            if len(line) > self.DISPLAY_WIDTH:
                line = line[:self.DISPLAY_WIDTH-1] + '>'
            # Pad line if too short
            else:
                line = line.ljust(self.DISPLAY_WIDTH)
            formatted.append(line)
        
        # Pad to display height
        while len(formatted) < self.DISPLAY_HEIGHT:
            formatted.append(' ' * self.DISPLAY_WIDTH)
        
        return '\n'.join(formatted).encode('ascii')
    
    def _handle_keypress(self, key: int) -> None:
        """Handle keypress from Nokia 3310.
        
        Args:
            key: Key code from phone
        """
        if self.current_menu == "main":
            self._handle_main_menu(key)
        elif self.current_menu == "sensors":
            self._handle_sensor_menu(key)
        elif self.current_menu == "dtc":
            self._handle_dtc_menu(key)
        elif self.current_menu == "commands":
            self._handle_command_menu(key)
        elif self.current_menu == "run_command":
            self._handle_run_command_menu(key)
    
    def _handle_main_menu(self, key: int) -> None:
        """Handle main menu keypresses.
        
        Args:
            key: Key code from phone
        """
        if key == 1:  # Up
            self._show_sensor_menu()
        elif key == 2:  # Down
            self._show_dtc_menu()
        elif key == 3:  # Select
            self._show_vehicle_info()
        elif key == 4:  # Custom commands
            self._show_command_menu()
    
    def _handle_sensor_menu(self, key: int) -> None:
        """Handle sensor menu keypresses.
        
        Args:
            key: Key code from phone
        """
        if key == 0:  # Back
            self._show_main_menu()
        elif key in [1, 2, 3, 4]:  # Sensor selection
            sensors = ['RPM', 'SPEED', 'TEMP', 'LOAD']
            self._monitor_sensor(sensors[key-1])
    
    def _handle_dtc_menu(self, key: int) -> None:
        """Handle DTC menu keypresses.
        
        Args:
            key: Key code from phone
        """
        if key == 0:  # Back
            self._show_main_menu()
        elif key == 1:  # Read DTCs
            self._show_dtc_codes()
        elif key == 2:  # Clear DTCs
            self._clear_dtc_codes()
    
    def _handle_command_menu(self, key: int) -> None:
        """Handle command menu keypresses."""
        if key == 0:  # Back
            self._show_main_menu()
        elif key == 1:  # List commands
            self._list_commands()
        elif key == 2:  # Add command
            self._add_command_menu()
        elif key == 3:  # Run command
            self._run_command_menu()

    def _handle_run_command_menu(self, key: int) -> None:
        """Handle run command menu keypresses."""
        if key == 0:  # Back
            self._show_command_menu()
        elif 1 <= key <= len(self.command_storage.get_commands()):
            self._execute_command(key - 1)

    def _show_main_menu(self) -> None:
        """Display main menu on phone."""
        menu_text = (
            "Main Menu:\n"
            "1.Sensors\n"
            "2.DTCs\n"
            "3.Info 4.Cmd"
        )
        self.fbus.send_command(self.MSG_DISPLAY, self._format_display(menu_text))
        self.current_menu = "main"

    def _show_sensor_menu(self) -> None:
        """Display sensor selection menu on phone."""
        menu_text = (
            "Select Sensor:\n"
            "1.RPM  2.Speed\n"
            "3.Temp 4.Load\n"
            "0.Back"
        )
        self.fbus.send_command(self.MSG_DISPLAY, self._format_display(menu_text))
        self.current_menu = "sensors"

    def _show_dtc_menu(self) -> None:
        """Display DTC menu on phone."""
        menu_text = (
            "DTCs:\n"
            "1.Read\n"
            "2.Clear\n"
            "0.Back"
        )
        self.fbus.send_command(self.MSG_DISPLAY, self._format_display(menu_text))
        self.current_menu = "dtc"

    def _show_command_menu(self) -> None:
        """Display custom command menu."""
        menu_text = (
            "Commands:\n"
            "1.List\n"
            "2.Add 3.Run\n"
            "0.Back"
        )
        self.fbus.send_command(self.MSG_DISPLAY, self._format_display(menu_text))
        self.current_menu = "commands"

    def _show_vehicle_info(self) -> None:
        """Display vehicle information on phone."""
        info = self.canbus.get_vehicle_info()
        
        if 'VIN' in info:
            info_text = f"VIN:{info['VIN'][:10]}...\n"
        else:
            info_text = "VIN: N/A\n"
            
        if 'ENGINE_LOAD' in info:
            info_text += f"Load:{info['ENGINE_LOAD']}%\n"
        
        self.fbus.send_command(self.MSG_DISPLAY, self._format_display(info_text))

    def _monitor_sensor(self, sensor_name: str) -> None:
        """Start monitoring a sensor.
        
        Args:
            sensor_name: Name of sensor to monitor
        """
        # Stop any existing monitoring
        self._stop_monitoring()
        
        # Start new monitoring thread
        self.stop_monitoring.clear()
        self.monitoring_thread = Thread(
            target=self._monitoring_loop,
            args=(sensor_name,)
        )
        self.monitoring_thread.start()

    def _monitoring_loop(self, sensor_name: str) -> None:
        """Background loop for sensor monitoring.
        
        Args:
            sensor_name: Name of sensor to monitor
        """
        while not self.stop_monitoring.is_set():
            value = self.canbus.read_sensor(sensor_name)
            if value is not None:
                display_text = f"{sensor_name}:\n{value:.1f}"
                self.fbus.send_command(
                    self.MSG_DISPLAY,
                    self._format_display(display_text)
                )
            time.sleep(0.5)  # Update every 500ms

    def _stop_monitoring(self) -> None:
        """Stop current sensor monitoring."""
        if self.monitoring_thread and self.monitoring_thread.is_alive():
            self.stop_monitoring.set()
            self.monitoring_thread.join()

    def _show_dtc_codes(self) -> None:
        """Display DTC codes on phone."""
        codes = self.canbus.get_dtc_codes()
        
        if not codes:
            display_text = "No DTCs found"
        else:
            display_text = "\n".join(codes[:4])
            if len(codes) > 4:
                display_text += f"\n+{len(codes)-4} more"
        
        self.fbus.send_command(
            self.MSG_DISPLAY,
            self._format_display(display_text)
        )

    def _clear_dtc_codes(self) -> None:
        """Clear DTC codes and show result."""
        if self.canbus.clear_dtc_codes():
            display_text = "DTCs cleared"
        else:
            display_text = "Clear failed"
            
        self.fbus.send_command(
            self.MSG_DISPLAY,
            self._format_display(display_text)
        )

    def _list_commands(self) -> None:
        """Display list of stored commands."""
        commands = self.command_storage.get_commands()
        if not commands:
            display_text = "No commands\nstored"
        else:
            display_text = "\n".join(
                f"{i+1}.{cmd['name']}"
                for i, cmd in enumerate(commands[:4])
            )
            if len(commands) > 4:
                display_text += f"\n+{len(commands)-4} more"
        
        self.fbus.send_command(
            self.MSG_DISPLAY,
            self._format_display(display_text)
        )

    def _add_command_menu(self) -> None:
        """Show add command menu."""
        # This would need a more complex UI implementation
        # for text input on Nokia 3310
        display_text = (
            "Add Command:\n"
            "Use PC to add\n"
            "new commands\n"
            "0.Back"
        )
        self.fbus.send_command(
            self.MSG_DISPLAY,
            self._format_display(display_text)
        )

    def _run_command_menu(self) -> None:
        """Show run command menu."""
        commands = self.command_storage.get_commands()
        if not commands:
            display_text = (
                "No commands\n"
                "Press 0 for\n"
                "main menu"
            )
        else:
            display_text = "Select cmd:\n" + "\n".join(
                f"{i+1}.{cmd['name']}"
                for i, cmd in enumerate(commands[:3])
            )
            display_text += "\n0.Back"
        
        self.fbus.send_command(
            self.MSG_DISPLAY,
            self._format_display(display_text)
        )
        self.current_menu = "run_command"

    def _execute_command(self, index: int) -> None:
        """Execute stored command and display result."""
        response = self.command_storage.execute_command(index)
        if response is not None:
            display_text = "Command sent\nsuccessfully"
        else:
            display_text = "Command\nfailed"
        
        self.fbus.send_command(
            self.MSG_DISPLAY,
            self._format_display(display_text)
        )

    def run(self) -> None:
        """Start the user interface."""
        self.running = True
        self._show_main_menu()
        
        try:
            while self.running:
                # Wait for and handle keypresses
                response = self.fbus.send_command(self.MSG_KEYPRESS, b'')
                if response:
                    self._handle_keypress(response[0])
                    
        except KeyboardInterrupt:
            self.running = False
            self._stop_monitoring()
        
        finally:
            self.fbus.close()
            self.canbus.close()
