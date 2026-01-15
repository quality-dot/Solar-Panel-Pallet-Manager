# Comprehensive Windows Debugging Guide

## Overview
This guide provides debugging strategies for the entire Pallet Manager application on Windows, covering startup, UI, database operations, file I/O, and common issues.

---

## Quick Debug Mode Setup

### Enable Console Window (See All Output)

Edit `pallet_builder.spec` line 181:
```python
console=True,  # Change from False to True
```

Then rebuild:
```cmd
pyinstaller pallet_builder.spec
```

**Result:** Console window will appear showing all print statements, errors, and debug output.

---

## Startup Debugging

### Test 1: Basic Launch
```cmd
cd C:\PalletManagerTest
"Pallet Manager.exe"
```

**Watch for:**
- ✅ Splash screen appears
- ✅ Progress bar animates
- ✅ Main window opens
- ✅ No error dialogs

**Debug Output to Check:**
```
======================================================================
DEBUG: _ensure_reference_workbook() called
======================================================================
Excel directory: C:\PalletManagerTest\EXCEL
Is packaged: True
sys.executable: C:\Users\...\AppData\Local\Temp\_MEI...\Pallet Manager.exe
sys._MEIPASS: C:\Users\...\AppData\Local\Temp\_MEI...
```

### Test 2: First-Time Setup
```cmd
# Fresh directory
mkdir C:\PalletManagerFirstRun
cd C:\PalletManagerFirstRun
copy "path\to\Pallet Manager.exe" .
"Pallet Manager.exe"
```

**Expected Behavior:**
1. Splash screen with "Setting up for first time..."
2. Creates folder structure:
   - EXCEL/
   - PALLETS/
   - LOGS/
   - CUSTOMERS/
   - IMPORTED DATA/
   - SUN SIMULATOR DATA/
   - ARCHIVE/
3. Copies reference workbook
4. Creates CURRENT.xlsx
5. Creates .initialized marker
6. Main window appears

**Verify:**
```cmd
dir /s
```

### Test 3: Subsequent Launches
```cmd
# Same directory as Test 2
"Pallet Manager.exe"
```

**Expected:**
- No first-time setup screen
- Faster startup
- Loads existing data

---

## UI Component Debugging

### Customer Management Window

**Test:**
```cmd
# Launch app, click "Customer Management"
```

**Watch for:**
1. Window opens quickly (< 1 second)
2. Customer list loads
3. No white-on-white text issues
4. Buttons are readable
5. Dark mode detection works (if applicable)

**Debug Output:**
```python
# Should see in console:
Loading customers from: C:\PalletManagerTest\CUSTOMERS\customers.xlsx
Found X customers
```

**Common Issues:**
- **Slow to open:** Check if CustomerManager is loading synchronously
- **White text:** Dark mode detection may not work on Windows
- **Crash on open:** Check for file permission issues

**Manual Test:**
1. Add new customer
2. Edit existing customer
3. Remove customer
4. Close and reopen window

### History Window

**Test:**
```cmd
# Launch app, click "History"
```

**Watch for:**
1. Window opens without spinning wheel
2. History data loads
3. Filter dropdown works
4. No infinite loops

**Debug Output:**
```python
# Should see:
Loading history from: C:\PalletManagerTest\PALLETS\
Found X pallet files
```

**Common Issues:**
- **Infinite loop:** Check customer filter trace callback
- **High RAM usage:** Check if load_history() is being called recursively
- **Slow loading:** Check if file operations are synchronous

### Import Data Dialog

**Test:**
```cmd
# Launch app, click "Import Data"
```

**Watch for:**
1. Status message appears: "Opening file dialog..."
2. File dialog opens quickly
3. Can select file
4. Import completes without errors

**Debug Output:**
```python
# Should see:
Opening file dialog...
Selected file: C:\path\to\file.xlsx
Importing data...
Import complete: X rows processed
```

---

## Database Operations Debugging

### Serial Database

**Test:**
```cmd
# Launch app, try scanning a barcode or validating a serial
```

**Debug Checks:**
```python
# Add to app/serial_database.py if needed:
print(f"SerialDatabase initialized: {self.db_file}")
print(f"Database exists: {self.db_file.exists()}")
print(f"Loading {len(self.df)} records from database")
```

**Verify:**
```cmd
dir PALLETS\serial_database.xlsx
```

**Expected:** File exists and is not empty

### Workbook Operations

**Test:**
```cmd
# Launch app, create a pallet
```

**Debug Checks:**
```python
# Should see:
Workbook path: C:\PalletManagerTest\EXCEL\CURRENT.xlsx
Workbook exists: True
Loading workbook...
Workbook loaded successfully
```

**Common Issues:**
- **"Workbook not found":** Check if CURRENT.xlsx was created
- **Permission denied:** Check file permissions or if file is open in Excel
- **Corrupted file:** Verify file size is ~23-24 KB

---

## File I/O Debugging

### Excel File Operations

**Test Read:**
```python
# Add debug output to workbook_utils.py:
print(f"Reading Excel file: {file_path}")
print(f"File exists: {file_path.exists()}")
print(f"File size: {file_path.stat().st_size} bytes")
```

**Test Write:**
```python
# Add debug output:
print(f"Writing Excel file: {file_path}")
print(f"Backup created: {backup_path}")
print(f"Write successful: {file_path.exists()}")
```

**Common Issues:**
- **PermissionError:** File is open in Excel
- **FileNotFoundError:** Path is incorrect or file was deleted
- **Corrupted file:** Check if write completed successfully

### Path Resolution

**Test:**
```python
# Add to app/path_utils.py get_base_dir():
base_dir = Path.cwd()
print(f"Base directory: {base_dir}")
print(f"Base dir exists: {base_dir.exists()}")
print(f"Is writable: {os.access(base_dir, os.W_OK)}")
```

**Expected on Windows:**
```
Base directory: C:\PalletManagerTest
Base dir exists: True
Is writable: True
```

---

## Performance Debugging

### Startup Time

**Measure:**
```python
# Add to app/pallet_builder_gui.py __init__:
import time
start_time = time.time()

# At end of __init__:
print(f"Startup time: {time.time() - start_time:.2f} seconds")
```

**Targets:**
- First launch: < 5 seconds
- Subsequent launches: < 2 seconds

### Memory Usage

**Monitor:**
```cmd
# Windows Task Manager
Ctrl+Shift+Esc
# Look for "Pallet Manager.exe"
```

**Expected:**
- Initial: 100-200 MB
- After operations: < 500 MB
- No continuous growth (memory leaks)

**If High Memory:**
1. Check for unclosed file handles
2. Check for large data structures not being cleared
3. Check for infinite loops

### UI Responsiveness

**Test:**
```cmd
# Launch app, try clicking buttons rapidly
```

**Expected:**
- No freezing
- Buttons respond immediately
- No "Not Responding" in title bar

**If Unresponsive:**
1. Check for synchronous file operations
2. Check for blocking UI updates
3. Check for infinite loops in callbacks

---

## Error Handling Debugging

### Catch All Exceptions

**Add to app/pallet_builder_gui.py:**
```python
def __init__(self, root):
    try:
        # ... existing code ...
    except Exception as e:
        print(f"\n{'='*70}")
        print(f"FATAL ERROR during initialization:")
        print(f"{'='*70}")
        print(f"Exception type: {type(e).__name__}")
        print(f"Exception message: {e}")
        import traceback
        print(f"Traceback:\n{traceback.format_exc()}")
        print(f"{'='*70}\n")
        raise
```

### Log to File

**Add logging:**
```python
# At top of pallet_builder_gui.py:
import logging
from pathlib import Path

log_file = Path.cwd() / "LOGS" / "debug.log"
log_file.parent.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()  # Also print to console
    ]
)
logger = logging.getLogger(__name__)

# Then use throughout code:
logger.debug("Debug message")
logger.info("Info message")
logger.warning("Warning message")
logger.error("Error message", exc_info=True)  # Includes traceback
```

**View logs:**
```cmd
type LOGS\debug.log
```

---

## Platform-Specific Issues

### Windows Path Issues

**Test:**
```python
# Check path separators:
print(f"Path separator: {os.sep}")  # Should be '\\'
print(f"Path: {Path('EXCEL/CURRENT.xlsx')}")  # Should work with forward slashes
```

### Windows Permissions

**Test:**
```python
# Check write permissions:
import os
test_file = Path.cwd() / "test_write.txt"
try:
    test_file.write_text("test")
    test_file.unlink()
    print("✅ Write permissions OK")
except PermissionError as e:
    print(f"❌ Permission denied: {e}")
```

### Windows Antivirus

**Common Issue:** Antivirus blocks file operations

**Test:**
1. Temporarily disable antivirus
2. Run app
3. If it works, add exception for Pallet Manager

**Whitelist:**
- `Pallet Manager.exe`
- Working directory (e.g., `C:\PalletManager\`)

### Windows Firewall

**Not typically an issue** (app doesn't use network), but if using network features:
```cmd
# Check firewall status:
netsh advfirewall show allprofiles
```

---

## Common Error Messages

### "Failed to start pallet manager expected boolean value got """

**Cause:** Tkinter boolean compatibility issue

**Debug:**
```python
# Check all Tkinter boolean calls:
# WRONG:
window.overrideredirect(True)
window.resizable(False, False)

# CORRECT:
window.overrideredirect(1)
window.resizable(0, 0)
```

**Fix:** Use integers (0/1) instead of booleans (False/True) for Tkinter

### "ModuleNotFoundError: No module named 'X'"

**Cause:** Module not included in PyInstaller bundle

**Debug:**
```cmd
# Check if module is in hiddenimports:
notepad pallet_builder.spec
# Look for module in hiddenimports list
```

**Fix:** Add to `hiddenimports` in `pallet_builder.spec`

### "Permission denied" / "Access is denied"

**Cause:** File is locked or insufficient permissions

**Debug:**
```python
# Check if file is open:
import psutil
for proc in psutil.process_iter(['name', 'open_files']):
    try:
        if proc.info['name'] == 'EXCEL.EXE':
            print(f"Excel is open with files: {proc.info['open_files']}")
    except:
        pass
```

**Fix:**
1. Close Excel
2. Run as Administrator
3. Check antivirus

### "Workbook not found"

**Cause:** CURRENT.xlsx not created or wrong path

**Debug:**
```python
# Check paths:
print(f"Looking for: {current_workbook}")
print(f"Exists: {current_workbook.exists()}")
print(f"EXCEL dir: {list(excel_dir.glob('*.xlsx'))}")
```

**Fix:** Verify reference workbook was bundled and copied

---

## Automated Testing Script

Save as `comprehensive_test.bat`:

```batch
@echo off
setlocal enabledelayedexpansion

echo ========================================
echo Comprehensive Windows Test Suite
echo ========================================
echo.

REM Set test directory
set TEST_DIR=C:\PalletManagerComprehensiveTest
set EXE_PATH=%~dp0Pallet Manager.exe

REM Clean previous test
if exist "%TEST_DIR%" (
    echo Cleaning previous test...
    rmdir /s /q "%TEST_DIR%"
)

REM Create test directory
mkdir "%TEST_DIR%"
cd /d "%TEST_DIR%"

echo Test directory: %TEST_DIR%
echo.

REM Copy EXE
echo [1/8] Copying EXE...
copy "%EXE_PATH%" . >nul 2>&1
if errorlevel 1 (
    echo ❌ FAILED: Could not copy EXE
    echo    Check path: %EXE_PATH%
    pause
    exit /b 1
)
echo ✅ PASSED

REM Test 1: First launch (with console output)
echo.
echo [2/8] Testing first launch...
start /wait "Pallet Manager" "Pallet Manager.exe"
timeout /t 2 >nul

REM Check folder structure
echo.
echo [3/8] Checking folder structure...
set FOLDERS=EXCEL PALLETS LOGS CUSTOMERS "IMPORTED DATA" "SUN SIMULATOR DATA" ARCHIVE
set FOLDER_PASS=1
for %%F in (%FOLDERS%) do (
    if not exist "%%~F" (
        echo ❌ FAILED: %%~F not created
        set FOLDER_PASS=0
    )
)
if !FOLDER_PASS!==1 echo ✅ PASSED

REM Check CURRENT.xlsx
echo.
echo [4/8] Checking CURRENT.xlsx...
if exist "EXCEL\CURRENT.xlsx" (
    echo ✅ PASSED
    dir "EXCEL\CURRENT.xlsx" | findstr /C:"CURRENT.xlsx"
) else (
    echo ❌ FAILED: CURRENT.xlsx not found
)

REM Check .initialized marker
echo.
echo [5/8] Checking initialization marker...
if exist ".initialized" (
    echo ✅ PASSED
) else (
    echo ❌ FAILED: .initialized not found
)

REM Test 2: Second launch (should be faster)
echo.
echo [6/8] Testing second launch...
start /wait "Pallet Manager" "Pallet Manager.exe"
timeout /t 2 >nul
echo ✅ PASSED (if app opened without errors)

REM Check memory usage
echo.
echo [7/8] Checking memory usage...
tasklist /FI "IMAGENAME eq Pallet Manager.exe" /FO CSV | findstr /C:"Pallet Manager.exe"
if errorlevel 1 (
    echo ℹ️  App not running (already closed)
) else (
    echo ℹ️  App is running - check Task Manager for memory usage
)

REM Summary
echo.
echo [8/8] Test summary...
echo.
echo ========================================
echo Test Results Summary
echo ========================================
echo.
echo Folder structure:
dir /b
echo.
echo EXCEL contents:
dir /b EXCEL
echo.
echo File sizes:
dir EXCEL\*.xlsx
echo.
echo ========================================
echo.
echo Manual tests needed:
echo 1. Customer Management button
echo 2. History button
echo 3. Import Data button
echo 4. Create a pallet
echo 5. Export pallet
echo.
echo Test directory: %TEST_DIR%
echo.
pause
```

Run with:
```cmd
comprehensive_test.bat
```

---

## Debug Checklist

### Before Testing:
- [ ] Build with `console=True` for debug output
- [ ] Verify reference workbook in source: `dir EXCEL\BUILD*.xlsx`
- [ ] Clean previous builds: `rmdir /s /q build dist`

### During Testing:
- [ ] Watch console output for errors
- [ ] Check Task Manager for memory usage
- [ ] Test all UI buttons
- [ ] Try creating/editing/deleting data

### After Testing:
- [ ] Check LOGS\debug.log for errors
- [ ] Verify all folders created
- [ ] Verify CURRENT.xlsx exists and is correct size
- [ ] Check for any error dialogs

### Report Issues With:
- [ ] Full console output
- [ ] Contents of LOGS\debug.log
- [ ] Windows version: `ver`
- [ ] Screenshots of errors
- [ ] Steps to reproduce

---

## Performance Benchmarks

| Operation | Target Time | Acceptable | Slow |
|-----------|-------------|------------|------|
| First launch | < 3s | < 5s | > 5s |
| Subsequent launch | < 1s | < 2s | > 2s |
| Open Customer Mgmt | < 0.5s | < 1s | > 1s |
| Open History | < 1s | < 2s | > 2s |
| Import Data | < 2s | < 5s | > 5s |
| Create Pallet | < 1s | < 2s | > 2s |

| Resource | Normal | Warning | Critical |
|----------|--------|---------|----------|
| RAM Usage | < 200 MB | < 500 MB | > 1 GB |
| Startup Size | 80-120 MB | 120-150 MB | > 150 MB |
| Disk Usage | < 500 MB | < 1 GB | > 1 GB |

---

## Getting Help

If issues persist after debugging:

1. **Collect Debug Info:**
   ```cmd
   # Create debug package
   mkdir debug_package
   copy LOGS\*.log debug_package\
   copy EXCEL\*.xlsx debug_package\
   dir /s > debug_package\file_list.txt
   systeminfo > debug_package\system_info.txt
   ```

2. **Document Issue:**
   - What were you trying to do?
   - What happened instead?
   - What error messages appeared?
   - What does the console output show?

3. **Include:**
   - Windows version
   - Debug package files
   - Screenshots
   - Steps to reproduce

---

**Last Updated:** January 9, 2026
**For:** Pallet Manager v1.1
**Platform:** Windows (Primary Target)






