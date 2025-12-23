# PLM - Play Legislative Machine 9076

This is a project helps users manage removable drives such as USB drives.

## Features

- Create USB groups and apply different actions to different USB drives.
- Protect your computer from malicious USB  
  (Does not include Rubber Ducky USB or malicious HID tools).
- Anti-malware protection for USB drives.
- Create autorun-enable USB and this application acting as the launcher.
- Block, scan for viruses, autorun, etc for target USB drives or target group.
- Handle and process different USB drives based on their classification. You can register classifications for each USB drive.

### Default Categories

- Trusted
- Untrusted
- First Seen
- Blacklisted
- And you can create your own groups and types for USB drives such as Home, Work or Tools

## Options for USB drives

- Block files (.exe, .txt, .scr, etc)
- Autorun the target file in the USB by reading the autorun.inf
- Auto scan for viruses when new USB drives are plugged in.

## Project files structure

PLay Legislative Machine/
│
├── PLM_autorun_creator.py
│ Create autorun.inf for target USB drives.
│
├── PLM_policy.py
│ Do action for USB drive.
│
├── PLM-9076.py / PLM-9076.exe
│ The entry point of the project.
│ Use watcher.py to listen for new USB drive then call
│ PLM_autorun_creator.py and PLM_policy.py's functions
│ for logic.
│
├── fake_virus_dropper.py
│ Generate fake virus for scan virus feature testing.
│
├── legal_viewer.py
│ Legal view GUI app.
│
└── core/
├── policies.py
│ Policies function for PLM_policy.py
│
├── watcher.py
│ Listen for new USB drives
│
└── classifier/
├── scanner.py
│ Scan for viruses
│
└── autorun_runner.py
Autorun for USB drive



## How does it work?

USB plugged
->
core/watcher.py -> drive path
->
core/registry.py -> Load USB drive's info
->
core/classifier.py -> drive's status
->
core/policies/init.py -> action
->
core/registry.py -> Update USB drive's info
->
core/log.py -> save work log


## USAGE

1. Run the PLM-9076.exe to start, it uses terminal UI.
2. Plug in your USB drives and enjoy.

## Disclaimer

This software is provided for educational and personal use only.

PLM is NOT a replacement for professional antivirus or enterprise-grade security solutions.  
The author makes no guarantees regarding security, stability, or data safety.

Use this software at your own risk.

## Limitations

PLM does NOT protect against:

- HID-based attacks (Rubber Ducky, BadUSB)
- Firmware-level USB attacks
- Physical hardware tampering

## Author

eubebhy - 2025-12-19  
Email: thienle6a1@gmail.com  
https://social.mtdv.me/contactme-DEV-info-python
