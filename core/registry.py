'''
This file use to load USB Drive's info and load app config
'''

import os
import json
import time
import ctypes
from pathlib import Path
from ctypes import wintypes

from model.drive import DriveStatus


APP_NAME = 'PLM-9067'
CONFIG_DIR = Path(os.getenv('APPDATA')) / APP_NAME
DRIVE_CONFIG_DIRR = CONFIG_DIR / 'drive_config.json'
DRIVES_INFO_DIR = CONFIG_DIR / 'drives_info.json'

# Cache
drives_info_cache = None

#==================================================
#===============Get USB drives info================
#==================================================

#===============Get drives's info==================
def _load_drives_cache() -> dict:
    global drives_info_cache

    if drives_info_cache is None:
        with open(DRIVES_INFO_DIR, 'r') as f:
            drives_info_cache = json.load(f)

    return drives_info_cache

def _ensure_drive_registered(drive_path: str) -> None:
    serial = get_drive_volume_serial(drive_path)

    if serial not in drives_info_cache:
        save_drives_info(
            drive_path=drive_path,
            status=DriveStatus.FIRST_SEEN
        )

def get_drives_info(drive_path: str) -> dict:
    cache = _load_drives_cache()
    _ensure_drive_registered(drive_path)

    serial = get_drive_volume_serial(drive_path)
    return cache[serial]
    #------------------------------------------------------------

def get_drive_label(drive_path: str) -> str | None:
    if not drive_path.endswith("\\"):
        drive_path += "\\"

    volume_name_buffer = ctypes.create_unicode_buffer(261)
    fs_name_buffer = ctypes.create_unicode_buffer(261)

    serial_number = wintypes.DWORD()
    max_component_length = wintypes.DWORD()
    file_system_flags = wintypes.DWORD()

    result = ctypes.windll.kernel32.GetVolumeInformationW(
        ctypes.c_wchar_p(drive_path),
        volume_name_buffer,
        ctypes.sizeof(volume_name_buffer),
        ctypes.byref(serial_number),
        ctypes.byref(max_component_length),
        ctypes.byref(file_system_flags),
        fs_name_buffer,
        ctypes.sizeof(fs_name_buffer)
    )

    if result:
        label = volume_name_buffer.value
        return label if label else None

    return None
    #------------------------------------------------------------

def get_drive_volume_serial(drive_path: str) -> str | None:
    if not drive_path.endswith("\\"):
        drive_path += "\\"

    volume_name_buffer = ctypes.create_unicode_buffer(261)
    fs_name_buffer = ctypes.create_unicode_buffer(261)

    serial_number = wintypes.DWORD()
    max_component_length = wintypes.DWORD()
    file_system_flags = wintypes.DWORD()

    result = ctypes.windll.kernel32.GetVolumeInformationW(
        ctypes.c_wchar_p(drive_path),
        volume_name_buffer,
        ctypes.sizeof(volume_name_buffer),
        ctypes.byref(serial_number),
        ctypes.byref(max_component_length),
        ctypes.byref(file_system_flags),
        fs_name_buffer,
        ctypes.sizeof(fs_name_buffer)
    )

    if result:
        return f"{serial_number.value:08X}"
    return None
    #------------------------------------------------------------

#------------------SAVE------------------
def save_drives_info(drive_path: str, status: DriveStatus) -> None:
    '''Save on drive's volume serial number'''
    global drives_info_cache
    
    serial_number = get_drive_volume_serial(drive_path)
    label = get_drive_label(drive_path)
    last_seen = time.time()
    
    drives = drives_info_cache
    appearance_count = drives.get(serial_number, {}).get('appearance_count', 0)
    
    drive = {
        'path':  drive_path,
        'volume_serial':  serial_number,
        'label': label,
        'appearance_count': appearance_count + 1,
        'last_seen': last_seen,
        'status': status,
        }

    drives[serial_number] = drive

    # Save drives's info
    with open(DRIVES_INFO_DIR, 'w') as file:
        json.dump(drives, file)
    drives_info_cache = None
    #------------------------------------------------------------

#==================================================
#===================CONFIG=========================
#==================================================
def save_drive_config():
    pass
