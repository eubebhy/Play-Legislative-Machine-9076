from core.models.drive import DriveStatus, USBdrive

def classify_drive(drive: USBdrive) -> DriveStatus:
    if drive.is_blacklisted:
        return DriveStatus.BLACKLISTED

    if drive.apperance_count == 1:
        return DriveStatus.FIRST_SEEN
