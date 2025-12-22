import os
import json
import time
import subprocess

from typing import List
from typing import Optional
from pathlib import Path
from dataclasses import dataclass

SUSPICIOUS_EXT = {".exe", ".bat", ".ps1", ".cmd", ".vbs", ".lnk", '.scr'}


# =========================
# Result model
# =========================
@dataclass
class ScanResult:
    safe: bool
    threats_found: int
    scanned_paths: List[str]
    suspicious_paths: List[str]
    engine: str = "Windows Defender"
    error: Optional[str] = None


# =========================
# Helpers
# =========================
def _is_hidden(path: Path) -> bool:
    try:
        import ctypes
        FILE_ATTRIBUTE_HIDDEN = 0x02
        attrs = ctypes.windll.kernel32.GetFileAttributesW(str(path))
        return attrs != -1 and bool(attrs & FILE_ATTRIBUTE_HIDDEN)
    except Exception:
        return False


def _collect_suspicious_paths(drive: Path, max_depth: int = 67) -> List[Path]:
    targets = []

    for root, dirs, files in os.walk(drive):
        depth = Path(root).relative_to(drive).parts
        if len(depth) > max_depth:
            dirs[:] = []
            continue

        for name in files:
            p = Path(root) / name
            if p.suffix.lower() in SUSPICIOUS_EXT or _is_hidden(p):
                targets.append(p)

        for d in dirs:
            dp = Path(root) / d
            if _is_hidden(dp):
                targets.append(dp)

    return list(set(targets))


def _run_defender_scan(target: Path) -> bool:
    cmd = [
        "powershell.exe",
        "-NoProfile",
        "-NonInteractive",
        "-Command",
        f'Start-MpScan -ScanType CustomScan -ScanPath "{target}"'
    ]

    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

    return subprocess.run(
        cmd,
        startupinfo=startupinfo,
        creationflags=subprocess.CREATE_NO_WINDOW,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        timeout=600
    ).returncode == 0


def _get_defender_threats(since_ts: float) -> int:
    ps_time = time.strftime(
        "%Y-%m-%dT%H:%M:%S",
        time.localtime(since_ts)
    )

    cmd = [
        "powershell.exe",
        "-NoProfile",
        "-NonInteractive",
        "-WindowStyle", "Hidden",
        "-Command",
        f"""
        $since = Get-Date "{ps_time}";
        Get-MpThreatDetection |
        Where-Object {{ $_.InitialDetectionTime -ge $since }} |
        ConvertTo-Json
        """
    ]

    r = subprocess.run(
        cmd,
        creationflags=subprocess.CREATE_NO_WINDOW,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True
    )

    out = r.stdout.strip()
    if not out:
        return 0

    try:
        data = json.loads(out)
        return len(data) if isinstance(data, list) else 1
    except Exception:
        return 0




# =========================
# Main API
# =========================
def scan_drive(drive_path: str, first_seen: bool = True) -> ScanResult:
    """
    Scan USB drive using Windows Defender.

    first_seen = True  -> quick scan
    first_seen = False -> full scan
    """

    drive = Path(os.path.abspath(drive_path))
    scanned = []
    suspicious = []
    
    scan_start = time.time() # for _get_defener_threats
    if not drive.exists():
        return ScanResult(
            safe=False,
            threats_found=0,
            scanned_paths=[],
            suspicious_paths=[],
            error="Drive path does not exist"
        )

    try:
        if not first_seen:
            suspicious = _collect_suspicious_paths(drive)

            if not suspicious:
                return ScanResult(
                    safe=True,
                    threats_found=0,
                    scanned_paths=[],
                    suspicious_paths=[],
                )

            # Scan parent folders instead of individual files
            scan_targets = {p.parent for p in suspicious}

            for target in scan_targets:
                _run_defender_scan(target)
                scanned.append(str(target))

        else:
            _run_defender_scan(drive)
            scanned.append(str(drive))

        threats = _get_defender_threats(scan_start)

        return ScanResult(
            safe=threats == 0,
            threats_found=threats,
            scanned_paths=scanned,
            suspicious_paths=[str(p) for p in suspicious]
        )

    except Exception as e:
        return ScanResult(
            safe=False,
            threats_found=0,
            scanned_paths=scanned,
            suspicious_paths=[str(p) for p in suspicious],
            error=str(e)
        )
