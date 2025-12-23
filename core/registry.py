'''
This file use to load USB Drive's info and load app config
'''

import os
import json
import time
import ctypes
from pathlib import Path
from ctypes import wintypes

from typing import List, Dict
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
'''
Description:
The "get_drives_info" function will be called when new USB drives plugged in.
Therefore, high performance for this function need to be ensured!.
'''
#===============Get drives's info==================
def _get_drive_volume_serial(drive_path: str) -> str | None:
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

def _get_drive_label(drive_path: str) -> str | None:
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

def _load_drives_info_cache() -> dict:
    global drives_info_cache

    if drives_info_cache is None:
        with open(DRIVES_INFO_DIR, 'r') as f:
            drives_info_cache = json.load(f)

    return drives_info_cache
    #------------------------------------------------------------
'''
How does this function work?
When new USB drives plugged in, this function will be called like this:
    "get_drives_info(["e:\\", "g:\\"].
    This function will iterate through drives in the list, on each drive
    it will:
    If this is new drives(First time seen), it will save
    this drive in DRIVES_INFO_DIR.
    
    Else if this drive has been seen before, get the info of this drive then
    prepare to update the info(If the drive's info had changed).

    Finally, return the list of drives's info with the format
          [{drive info key1: drive info key2,etc}]
    
'''
def get_drives_info(drive_paths: list) -> List[Dict]:
    '''Get dirve's info on drive's volume serial

        return the list of drives's info with the format
          [{drive info key1: drive info key2,etc}]'''
    cache = _load_drives_info_cache()
    result = []

    first_time_seens = set(drive_paths) - set(cache) 
    #------------------------------------------------------------

#------------------SAVE------------------
def save_drives_info(drive_paths: list, status: DriveStatus) -> None:
    '''
    Save on drive;s serial number.
    This function can add new drive's info or just update the info.
'''
    global drives_info_cache
    result = []
    for path in drive_paths:
        serial_number = _get_drive_volume_serial(path)
        label = _get_drive_label(path)
        last_seen = time.time()
        appearance_count = drives.get(serial_number, {}).get('appearance_count', 0)
        drives = drives_info_cache
        
        drive = {
            'path': path,
            'volume_serial':  serial_number,
            'label': label,
            'appearance_count': appearance_count + 1,
            'last_seen': last_seen,
            'status': status,
            }
        drives[serial_number] = drive
        result.append(drive)
    # Save drives's info
    with open(DRIVES_INFO_DIR, 'w') as file:
        json.dump(drives, file, indent= 4)
    drives_info_cache = None

    return result # Return saved drive info
    #------------------------------------------------------------

#==================================================
#===================CONFIG=========================
#==================================================
def save_drive_config():
    pass
