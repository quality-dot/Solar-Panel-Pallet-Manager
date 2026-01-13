# Windows Testing Guide for Pallet Manager

## Purpose
This guide helps test the Windows build, especially the **CURRENT.xlsx** creation on first launch.

---

## Pre-Build Checklist

### 1. Verify Reference Workbook Exists
```cmd
dir "EXCEL\BUILD 10-12-25.xlsx"
```
**Expected:** File should exist and be ~23-24 KB

### 2. Verify PyInstaller Spec Configuration
Check `pallet_builder.spec` line 46:
```python
('EXCEL/BUILD 10-12-25.xlsx', 'reference_workbook'),
```

---

## Build Process

### 1. Clean Previous Builds
```cmd
rmdir /s /q build dist
del "Pallet Manager.exe"
```

### 2. Build with PyInstaller
```cmd
pyinstaller pallet_builder.spec
```

### 3. Verify Build Output
```cmd
dir "Pallet Manager.exe"
```
**Expected:** EXE file should exist (typically 80-120 MB for onefile build)

---

## Testing First Launch

### Test 1: Fresh Install (No Data)

1. **Create Clean Test Environment:**
   ```cmd
   mkdir C:\PalletManagerTest
   cd C:\PalletManagerTest
   ```

2. **Copy EXE:**
   ```cmd
   copy "path\to\Pallet Manager.exe" .
   ```

3. **Launch and Watch Console Output:**
   ```cmd
   "Pallet Manager.exe"
   ```
   
   **Look for debug output:**
   ```
   ======================================================================
   DEBUG: _ensure_reference_workbook() called
   ======================================================================
   Excel directory: C:\PalletManagerTest\EXCEL
   Excel dir exists: True
   Is packaged: True
   sys.executable: C:\Users\...\AppData\Local\Temp\_MEI...\Pallet Manager.exe
   sys._MEIPASS: C:\Users\...\AppData\Local\Temp\_MEI...
   ======================================================================
   Found reference workbook in _MEIPASS: C:\Users\...\Temp\_MEI...\reference_workbook\BUILD 10-12-25.xlsx
   Existing workbooks in EXCEL: []
   
   Checking if we need to copy reference workbook...
     existing_workbooks: 0
     reference_workbook: C:\Users\...\Temp\_MEI...\reference_workbook\BUILD 10-12-25.xlsx
     reference exists: True
     → Copying BUILD workbook to: C:\PalletManagerTest\EXCEL\BUILD 10-12-25.xlsx
     ✅ Copied reference workbook successfully!
   
   Checking CURRENT.xlsx...
     Target: C:\PalletManagerTest\EXCEL\CURRENT.xlsx
     Exists: False
     → Creating CURRENT.xlsx from reference workbook
     ✅ Created CURRENT.xlsx successfully!
        Size: 24053 bytes
   ======================================================================
   ```

4. **Verify Files Created:**
   ```cmd
   dir EXCEL
   ```
   
   **Expected Output:**
   ```
   BUILD 10-12-25.xlsx    (23-24 KB)
   CURRENT.xlsx           (23-24 KB)
   ```

5. **Test App Functionality:**
   - Click "Customer Management" → Should open without errors
   - Click "History" → Should open without errors
   - Try creating a pallet → Should work

### Test 2: Existing EXCEL Folder (Empty)

1. **Create EXCEL folder manually:**
   ```cmd
   mkdir C:\PalletManagerTest2
   cd C:\PalletManagerTest2
   mkdir EXCEL
   copy "path\to\Pallet Manager.exe" .
   ```

2. **Launch:**
   ```cmd
   "Pallet Manager.exe"
   ```

3. **Verify CURRENT.xlsx Created:**
   ```cmd
   dir EXCEL\CURRENT.xlsx
   ```

### Test 3: Existing BUILD File (No CURRENT.xlsx)

1. **Setup:**
   ```cmd
   mkdir C:\PalletManagerTest3
   cd C:\PalletManagerTest3
   mkdir EXCEL
   echo test > EXCEL\BUILD_2025_Q1.xlsx
   copy "path\to\Pallet Manager.exe" .
   ```

2. **Launch:**
   ```cmd
   "Pallet Manager.exe"
   ```

3. **Verify:**
   - CURRENT.xlsx should be created from existing BUILD file
   - Reference workbook should NOT be copied (since BUILD file exists)

---

## Troubleshooting

### Issue: "EXCEL folder is empty!"

**Check:**
1. Look for debug output in console
2. Check if `sys._MEIPASS` is shown
3. Verify reference workbook path in debug output

**Common Causes:**
- Reference workbook not bundled in EXE
- Wrong path lookup (not checking `sys._MEIPASS`)
- File permissions issue

### Issue: "Could not create CURRENT.xlsx"

**Check:**
1. Look for exception traceback in console
2. Verify EXCEL folder permissions
3. Check if antivirus is blocking file operations

### Issue: No Debug Output

**Cause:** Console is hidden (expected for GUI app)

**Solution:** Run with console enabled temporarily:
1. Edit `pallet_builder.spec` line 181: `console=True`
2. Rebuild
3. Run and capture output

---

## Expected Behavior Summary

| Scenario | BUILD Copied? | CURRENT.xlsx Created? | Source |
|----------|---------------|----------------------|--------|
| Fresh install (no files) | ✅ Yes | ✅ Yes | Reference workbook |
| Empty EXCEL folder | ✅ Yes | ✅ Yes | Reference workbook |
| Existing BUILD file | ❌ No | ✅ Yes | Existing BUILD file |
| Existing CURRENT.xlsx | ❌ No | ❌ No | Already exists |

---

## Debug Mode

To enable detailed logging:

1. **Edit `pallet_builder.spec`:**
   ```python
   console=True,  # Line 181 - enable console window
   ```

2. **Rebuild:**
   ```cmd
   pyinstaller pallet_builder.spec
   ```

3. **Run and capture output:**
   ```cmd
   "Pallet Manager.exe" > debug_log.txt 2>&1
   ```

4. **Review log:**
   ```cmd
   type debug_log.txt
   ```

---

## Success Criteria

✅ **Build succeeds without errors**
✅ **EXE file is created**
✅ **First launch creates EXCEL folder**
✅ **CURRENT.xlsx is created on first launch**
✅ **CURRENT.xlsx is ~23-24 KB (not empty)**
✅ **App opens without crashes**
✅ **Customer Management works**
✅ **History window works**
✅ **Can create pallets**

---

## Reporting Issues

If testing fails, provide:
1. Full console output (if available)
2. Contents of EXCEL folder: `dir EXCEL`
3. Windows version: `ver`
4. Error messages or screenshots
5. Steps to reproduce

---

## Quick Test Script

Save as `test_windows_build.bat`:

```batch
@echo off
echo ========================================
echo Pallet Manager Windows Build Test
echo ========================================
echo.

REM Clean test environment
if exist PalletManagerTest rmdir /s /q PalletManagerTest
mkdir PalletManagerTest
cd PalletManagerTest

REM Copy EXE
echo Copying EXE...
copy "..\Pallet Manager.exe" . >nul
if errorlevel 1 (
    echo ERROR: Could not copy EXE
    pause
    exit /b 1
)

REM Launch app
echo.
echo Launching Pallet Manager...
echo Watch for debug output in app window
echo.
start /wait "Pallet Manager" "Pallet Manager.exe"

REM Check results
echo.
echo ========================================
echo Test Results:
echo ========================================
echo.

if exist EXCEL\CURRENT.xlsx (
    echo ✅ CURRENT.xlsx created successfully!
    dir EXCEL\CURRENT.xlsx
) else (
    echo ❌ CURRENT.xlsx NOT found!
)

echo.
if exist EXCEL\BUILD*.xlsx (
    echo ✅ BUILD workbook found!
    dir EXCEL\BUILD*.xlsx
) else (
    echo ℹ️  No BUILD workbook (might be OK if CURRENT.xlsx exists)
)

echo.
echo Full EXCEL folder contents:
dir EXCEL

echo.
echo ========================================
echo Test Complete
echo ========================================
pause
```

Run with:
```cmd
test_windows_build.bat
```


