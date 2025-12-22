import os
import json

def autorun(drive_path: str):
    '''cilent fail if the target file doesn't exit'''
    
    success = True
    path = f"{drive_path}autorun.cc"
    if os.path.exists(path):
        with open(path, 'r') as file:
            data = json.load(file)
    
        target_file_path = data['target_file_path']
                

        if success:   
            os.startfile(target_file_path)
