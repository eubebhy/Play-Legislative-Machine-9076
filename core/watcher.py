'''API chinh la wating_until_new_drives'''
import os
import time
import string

def _get_drives() -> list :
    '''Tra ve list cac drive dang ton tai'''
    
    active_drives = []
    for letter in string.ascii_uppercase:
        drive = f'{letter}:\\'
        if os.path.exists(drive):
            active_drives.append(drive)
    return active_drives

def waiting_until_new_drives(intervals: float = 0.2) -> list:
    '''Tao loop lien tuc kiem tra su suat hien cua drive moi
    moi interval giay. Tra ve danh sach ten cua drive moi'''
    
    old_drives = _get_drives()
   
    while True:
        new_drives = _get_drives()
        if len(new_drives) > len(old_drives):
            return list(set(new_drives) ^ set(old_drives))
        else:
            old_drives = new_drives
        time.sleep(intervals)

        
if __name__ == '__main__':
    print("Dang lang nghe phat hien usb")

    
    print(waiting_until_new_drives(intervals = 0.2))
    print("da phat hien usb")
