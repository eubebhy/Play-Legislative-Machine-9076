from core.scanner import scan_drive
from core.model.drive import DriveStatus, USBDrive

def block(drive, config):
    pass

def apply_policy(drive: USBDrive, config):
    if drive.status == DriveStatus.BLACKLISTED:
        block(drive, config)

    else:
        scan_drive(drive)
