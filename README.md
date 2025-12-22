# PLM 9076 – Play Legislative Machine

**Play Legislative Machine 9076 (PLM)** is a project designed to manage and secure removable drives, especially USB drives, on Windows systems.

The project focuses on **USB classification, policy-based actions, and basic malware protection**, using a lightweight terminal-based interface.

---

## ✨ Features

- Create USB groups and apply different actions for each group
- Protect your computer from malicious USB drives  
  _(Does NOT include Rubber Ducky or HID-based attack protection)_
- Anti-malware scanning for removable drives
- Create **autorun-enabled USB drives**, with PLM acting as the launcher
- Block, scan, autorun, or restrict files for specific USB drives or groups
- Automatically handle USB drives based on classification

---

## 🧠 USB Classification System

Each USB drive can be registered and classified.

### Default Categories

- Trusted
- Untrusted
- First Seen
- Blacklisted

You can also create **custom groups**, such as:
- Home
- Work
- Tools

---

## 🔒 USB Drive Actions

PLM supports the following actions:

- Block specific file types (`.exe`, `.scr`, `.txt`, etc.)
- Read and execute `autorun.inf`
- Automatically scan USB drives when plugged in
- Apply different policies per drive or group
