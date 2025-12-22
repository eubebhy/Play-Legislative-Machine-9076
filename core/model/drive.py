# play legislative machine\core\model\drive.py
from enum import Enum
from dataclasses import dataclass


class DriveStatus(Enum):
    TRUSTED = "trusted"
    UNTRUSTED = "untrusted"
    FIRST_SEEN = "first_seen"
    BLACKLISTED = "blacklisted"


@dataclass
class USBDrive:
    path: str                  
    volume_serial: str          # ID 
    label: str                 # drive's name
    appearance_count: int
    last_seen: int             # unix timestamp (seconds)
    status: DriveStatus

