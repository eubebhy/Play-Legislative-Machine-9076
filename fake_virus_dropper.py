import os
import zipfile
import base64
import random
import string
import shutil

# EICAR test string (harmless, for AV testing only)
EICAR = "X5O!P%@AP[4\\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*"

def create_random_string(length=10):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def create_fake_image_file(path):
    # Create a text file disguised as image
    with open(path, 'w') as f:
        f.write("This is a fake image file containing: " + EICAR)

def create_shortcut(target_path, shortcut_path):
    # Simple batch file mimicking a shortcut behavior
    with open(shortcut_path, 'w') as f:
        f.write(f'@echo off\nstart "" "{target_path}"')

def create_encrypted_file(path, content):
    # Simple base64 "encryption"
    encoded = base64.b64encode(content.encode()).decode()
    with open(path, 'w') as f:
        f.write(encoded)

def create_nested_zip(root_dir, levels=3):
    current_dir = root_dir
    for i in range(levels):
        zip_name = os.path.join(current_dir, f'nested_{i}.zip')
        with zipfile.ZipFile(zip_name, 'w') as zf:
            # Add EICAR file inside
            eicar_path = os.path.join(current_dir, 'eicar.txt')
            with open(eicar_path, 'w') as f:
                f.write(EICAR)
            zf.write(eicar_path)
            os.remove(eicar_path)
        # Move to next "directory" level (simulate nesting)
        next_dir = os.path.join(current_dir, f'dir_{i+1}')
        os.makedirs(next_dir, exist_ok=True)
        current_dir = next_dir

def main(output_dir='fake_malware_test'):
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir)

    # Create complex directory structure
    dirs = [
        os.path.join(output_dir, 'Documents'),
        os.path.join(output_dir, 'Pictures'),
        os.path.join(output_dir, 'Downloads'),
        os.path.join(output_dir, 'System'),
        os.path.join(output_dir, 'Hidden', '.secret')
    ]
    for d in dirs:
        os.makedirs(d, exist_ok=True)

    # Place EICAR in various places
    with open(os.path.join(output_dir, 'important.doc'), 'w') as f:
        f.write(EICAR)
    
    create_fake_image_file(os.path.join(output_dir, 'Pictures', 'vacation.jpg'))
    
    create_encrypted_file(os.path.join(output_dir, 'Downloads', 'encrypted.dat'), EICAR)
    
    # Create shortcuts pointing to EICAR files
    eicar_bat = os.path.join(output_dir, 'run.bat')
    with open(eicar_bat, 'w') as f:
        f.write(EICAR)  # Batch file with EICAR
    create_shortcut(eicar_bat, os.path.join(output_dir, 'Documents', 'open_me.lnk.bat'))  # Disguised shortcut
    
    # Random files with dumb extensions
    dumb_exts = ['.exe.txt', '.pdf.exe', '.jpg.bat', '.scr']
    for i in range(5):
        file_path = os.path.join(output_dir, 'System', f'file_{i}{random.choice(dumb_exts)}')
        with open(file_path, 'w') as f:
            if random.random() > 0.5:
                f.write(EICAR)
            else:
                f.write(create_random_string(100))

    # Nested zips with EICAR
    create_nested_zip(os.path.join(output_dir, 'Hidden'))

    # Social engineering mimic: Innocent looking file that "executes" EICAR
    se_file = os.path.join(output_dir, 'free_gift.exe.bat')
    with open(se_file, 'w') as f:
        f.write(f'@echo off\necho {EICAR}\npause')

    print(f"Fake malware test structure created in: {output_dir}")

if __name__ == "__main__":
    main()
