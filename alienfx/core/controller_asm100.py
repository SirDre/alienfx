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
    This is a compact desktop form factor with minimal lighting zones.
    """
    
    # Speed capabilities
    DEFAULT_SPEED = 200
    MIN_SPEED = 50
    
    # Zone codes for Alienware Alpha ASM100
    # The Alpha has minimal lighting compared to laptops
    ALIEN_HEAD = 0x01
    POWER_BUTTON = 0x02
    
    # Reset codes
    RESET_ALL_LIGHTS_OFF = 3
    RESET_ALL_LIGHTS_ON = 4
    
    # State codes - Alpha is a desktop so battery states are not applicable
    BOOT = 1
    AC_SLEEP = 2
    AC_CHARGED = 5
    AC_ON = 8
    
    def __init__(self):
        acpi_controller.AlienFXACPIController.__init__(self)
        self.name = "Alienware Alpha ASM100"
        
        # ACPI identification - Alpha doesn't use USB
        # Instead it uses ACPI/WMI interface
        self.acpi_path = "/sys/devices/platform/alienware-wmi"
        
        # map the zone names to their codes
        self.zone_map = {
            self.ZONE_ALIEN_HEAD: self.ALIEN_HEAD,
            self.ZONE_POWER_BUTTON: self.POWER_BUTTON,
        }
        
        # zones that have special behaviour in different power states
        self.power_zones = [
            self.ZONE_POWER_BUTTON,
        ]
        
        # map the reset names to their codes
        self.reset_types = {
            self.RESET_ALL_LIGHTS_OFF: "all-lights-off",
            self.RESET_ALL_LIGHTS_ON: "all-lights-on"
        }
        
        # map the state names to their codes
        # Desktop only has AC power states
        self.state_map = {
            self.STATE_BOOT: self.BOOT,
            self.STATE_AC_SLEEP: self.AC_SLEEP,
            self.STATE_AC_CHARGED: self.AC_CHARGED,
            self.STATE_AC_ON: self.AC_ON,
        }

acpi_controller.AlienFXACPIController.supported_controllers.append(
    AlienFXControllerASM100())
