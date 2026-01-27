#
# controller_asm100.py
#
# Alienfx is free software.
#
# You may redistribute it and/or modify it under the terms of the
# GNU General Public License, as published by the Free Software
# Foundation; either version 3 of the License, or (at your option)
# any later version.
#
# Alienfx is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
""" Specialization of the AlienFxController class for the Alienware Alpha ASM100 controller.

This module provides the following classes:
AlienFXControllerASM100 : Alienware Alpha ASM100 ACPI-based controller
"""

import alienfx.core.acpi_controller as acpi_controller

class AlienFXControllerASM100(acpi_controller.AlienFXACPIController):
    
    """ Specialization of the AlienFXACPIController class for the Alpha ASM100.
    
    The Alienware Alpha ASM100 uses ACPI/WMI for lighting control rather than USB.
    This is a compact desktop form factor (Chassis deviceTypeID: 1) with two lighting zones.
    
    Device Information from AWCC:
    - VID: 187C
    - PID: ASM100
    - Device Type: Chassis (deviceTypeID: 1)
    - LED Zones: 2 (Alienhead - LED 0, Side Left - LED 1)
    - Actions per Zone: 1
    """
    
    # Speed capabilities (tempo from theme)
    DEFAULT_SPEED = 200
    MIN_SPEED = 50
    
    # Zone codes for Alienware Alpha ASM100
    # Based on the JSON theme structure:
    # LED 0 - Alienhead (Group01)
    # LED 1 - Side Left (Group02)
    ALIEN_HEAD = 0x00  # ledID: 0
    SIDE_LEFT = 0x01   # ledID: 1
    
    # Legacy compatibility (POWER_BUTTON may not exist as separate zone)
    POWER_BUTTON = 0x00  # Map to Alienhead for backward compatibility
    
    # Reset codes
    RESET_ALL_LIGHTS_OFF = 3
    RESET_ALL_LIGHTS_ON = 4
    
    # State codes - Alpha is a desktop so battery states are not applicable
    # These correspond to visualization types in the JSON
    BOOT = 1                # Default visualization (visualizationTypeID: 1)
    AC_SLEEP = 2           # Sleep Mode visualization (visualizationTypeID: 2)
    AC_CHARGED = 5         # Not applicable for desktop
    AC_ON = 8              # Active state
    
    # Action types from JSON theme
    ACTION_MORPH = 1
    ACTION_PULSE = 2
    ACTION_SET_COLOR = 3
    ACTION_LOOP = 4
    ACTION_PLAY_POWER_STATUS = 15
    
    # Device identification
    DEVICE_VID = "187C"
    DEVICE_PID = "ASM100"
    DEVICE_TYPE_CHASSIS = 1
    
    def __init__(self):
        acpi_controller.AlienFXACPIController.__init__(self)
        self.name = "Alienware Alpha ASM100"
        
        # ACPI/WMI identification
        # The Alpha uses the alienware-wmi kernel module
        self.acpi_path = "/sys/devices/platform/alienware-wmi"
        self.device_vid = self.DEVICE_VID
        self.device_pid = self.DEVICE_PID
        self.device_type = self.DEVICE_TYPE_CHASSIS
        
        # Map zone names to their LED IDs (based on JSON leds array)
        self.zone_map = {
            self.ZONE_ALIEN_HEAD: self.ALIEN_HEAD,      # LED 0 - Alienhead
            self.ZONE_POWER_BUTTON: self.POWER_BUTTON,  # LED 0 - Mapped to Alienhead
            "SIDE_LEFT": self.SIDE_LEFT,                # LED 1 - Side Left
        }
        
        # LED groups mapping (from JSON groups and zonesGroups)
        self.led_groups = {
            1: "Alienhead",     # Group01 - groupID: 1
            2: "Side Left",     # Group02 - groupID: 2
        }
        
        # LED definitions (from JSON leds array)
        self.leds = {
            0: {
                "name": "Led 0",
                "description": "Alienhead",
                "groupID": 1
            },
            1: {
                "name": "Led 1",
                "description": "Side Left",
                "groupID": 2
            }
        }
        
        # Zones that have special behaviour in different power states
        # Based on visualization types
        self.power_zones = [
            self.ZONE_ALIEN_HEAD,
            "SIDE_LEFT",
        ]
        
        # Map reset names to their codes
        self.reset_types = {
            self.RESET_ALL_LIGHTS_OFF: "all-lights-off",
            self.RESET_ALL_LIGHTS_ON: "all-lights-on"
        }
        
        # Map state names to their codes
        # Desktop only has AC power states
        # Corresponds to visualizationTypes in JSON
        self.state_map = {
            self.STATE_BOOT: self.BOOT,           # Default (visualizationTypeID: 1)
            self.STATE_AC_SLEEP: self.AC_SLEEP,   # Sleep Mode (visualizationTypeID: 2)
            self.STATE_AC_CHARGED: self.AC_CHARGED,
            self.STATE_AC_ON: self.AC_ON,
        }
        
        # Action types mapping (from JSON actionTypes)
        self.action_types = {
            self.ACTION_MORPH: "Morph",
            self.ACTION_PULSE: "Pulse",
            self.ACTION_SET_COLOR: "SetColor",
            self.ACTION_LOOP: "Loop",
            self.ACTION_PLAY_POWER_STATUS: "PlayPowerStatus"
        }
        
        # Theme configuration defaults (from JSON theme)
        self.theme_config = {
            "mode": 0,
            "actionDuration": 3,
            "tempo": 200,
            "actionsPerZone": 1
        }
    
    def get_led_by_id(self, led_id):
        """Get LED information by LED ID.
        
        Args:
            led_id: The LED identifier (0 for Alienhead, 1 for Side Left)
            
        Returns:
            Dictionary containing LED information or None if not found
        """
        return self.leds.get(led_id)
    
    def get_group_name(self, group_id):
        """Get group name by group ID.
        
        Args:
            group_id: The group identifier (1 or 2)
            
        Returns:
            String containing group name or None if not found
        """
        return self.led_groups.get(group_id)
    
    def get_zone_by_group(self, group_id):
        """Get zone code by group ID.
        
        Args:
            group_id: The group identifier (1 for Alienhead, 2 for Side Left)
            
        Returns:
            Zone code corresponding to the group
        """
        if group_id == 1:
            return self.ALIEN_HEAD
        elif group_id == 2:
            return self.SIDE_LEFT
        return None

acpi_controller.AlienFXACPIController.supported_controllers.append(
    AlienFXControllerASM100())
