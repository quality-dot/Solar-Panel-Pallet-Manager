#!/usr/bin/env python3
"""
Download SumatraPDF portable for bundling with Pallet Manager
Fallback script if PowerShell download fails in build_windows.bat
"""

import sys
import urllib.request
import zipfile
import ssl
from pathlib import Path

SUMATRA_VERSION = "3.5.2"
SUMATRA_URL = f"https://github.com/sumatrapdfreader/sumatrapdf/releases/download/{SUMATRA_VERSION}rel/SumatraPDF-{SUMATRA_VERSION}-64.zip"
TARGET_DIR = Path("external_tools/SumatraPDF")
ZIP_PATH = TARGET_DIR / "SumatraPDF.zip"
EXE_PATH = TARGET_DIR / "SumatraPDF.exe"

def download_sumatra():
    """Download and extract SumatraPDF"""
    try:
        # Create directory if needed
        TARGET_DIR.mkdir(parents=True, exist_ok=True)
        
        # Check if already downloaded
        if EXE_PATH.exists():
            print(f"✓ SumatraPDF already exists: {EXE_PATH}")
            return True
        
        print(f"Downloading SumatraPDF {SUMATRA_VERSION}...")
        print(f"URL: {SUMATRA_URL}")
        
        # Download with progress
        def show_progress(block_num, block_size, total_size):
            downloaded = block_num * block_size
            if total_size > 0:
                percent = min(100, (downloaded / total_size) * 100)
                sys.stdout.write(f"\r  Progress: {percent:.1f}% ({downloaded}/{total_size} bytes)")
                sys.stdout.flush()
        
        # Create SSL context that doesn't verify certificates (for corporate proxies/firewalls)
        ssl_context = ssl._create_unverified_context()
        
        # Create opener with unverified SSL context
        opener = urllib.request.build_opener(urllib.request.HTTPSHandler(context=ssl_context))
        urllib.request.install_opener(opener)
        
        # Download with progress
        urllib.request.urlretrieve(SUMATRA_URL, ZIP_PATH, show_progress)
        print("\n")
        
        # Extract
        print("Extracting SumatraPDF...")
        with zipfile.ZipFile(ZIP_PATH, 'r') as zip_ref:
            zip_ref.extractall(TARGET_DIR)
        
        # Clean up zip
        ZIP_PATH.unlink()
        
        # Verify
        if EXE_PATH.exists():
            print(f"✓ SumatraPDF downloaded successfully!")
            print(f"  Location: {EXE_PATH}")
            return True
        else:
            print("✗ SumatraPDF.exe not found after extraction")
            # List what we got
            print("Files extracted:")
            for f in TARGET_DIR.glob("*"):
                print(f"  - {f.name}")
            return False
            
    except Exception as e:
        print(f"✗ Error downloading SumatraPDF: {e}")
        print("\nPlease download manually:")
        print(f"1. Go to: https://www.sumatrapdfreader.org/download-free-pdf-viewer")
        print(f"2. Download the 64-bit portable version")
        print(f"3. Extract SumatraPDF.exe to: {TARGET_DIR}")
        return False

if __name__ == "__main__":
    success = download_sumatra()
    sys.exit(0 if success else 1)

