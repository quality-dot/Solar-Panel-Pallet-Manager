# Windows Build Troubleshooting

## Common Build Errors and Solutions

### Error 1: "ModuleNotFoundError" during build

**Symptoms:**
```
ModuleNotFoundError: No module named 'X'
```

**Causes:**
- Missing dependency
- Module not installed in build environment

**Solutions:**

1. **Install missing dependencies:**
   ```cmd
   pip install -r requirements.txt
   ```

2. **Verify all required packages:**
   ```cmd
   pip list | findstr /I "openpyxl pandas pyyaml tkinter reportlab pillow"
   ```

3. **Add to hiddenimports in pallet_builder.spec if needed**

---

### Error 2: "FileNotFoundError: EXCEL/BUILD 10-12-25.xlsx"

**Symptoms:**
```
FileNotFoundError: [Errno 2] No such file or directory: 'EXCEL/BUILD 10-12-25.xlsx'
```

**Cause:**
- Reference workbook file missing from source

**Solution:**

1. **Verify file exists:**
   ```cmd
   dir "EXCEL\BUILD 10-12-25.xlsx"
   ```

2. **If missing, create or restore it:**
   - Check if file was accidentally deleted
   - Restore from git: `git checkout EXCEL/BUILD\ 10-12-25.xlsx`
   - Or copy from backup

---

### Error 3: "ImportError: cannot import name 'X' from 'Y'"

**Symptoms:**
```
ImportError: cannot import name 'something' from 'module'
```

**Causes:**
- Version mismatch
- Circular import
- Missing __init__.py

**Solutions:**

1. **Check package versions:**
   ```cmd
   pip show openpyxl pandas pyyaml
   ```

2. **Update packages:**
   ```cmd
   pip install --upgrade openpyxl pandas pyyaml
   ```

3. **Check for circular imports in app/ modules**

---

### Error 4: "PermissionError" or "Access is denied"

**Symptoms:**
```
PermissionError: [WinError 5] Access is denied
```

**Causes:**
- Previous build files locked
- Antivirus blocking
- Running from protected directory

**Solutions:**

1. **Clean build directories:**
   ```cmd
   rmdir /s /q build dist
   del "Pallet Manager.exe"
   ```

2. **Run as Administrator:**
   - Right-click Command Prompt → "Run as administrator"
   - Navigate to project directory
   - Run build again

3. **Temporarily disable antivirus:**
   - Disable real-time protection
   - Run build
   - Re-enable protection

4. **Move project to user directory:**
   ```cmd
   REM Avoid C:\Program Files or C:\Windows
   REM Use C:\Users\YourName\Documents\Projects\
   ```

---

### Error 5: "UnicodeDecodeError"

**Symptoms:**
```
UnicodeDecodeError: 'charmap' codec can't decode byte...
```

**Cause:**
- File encoding issue

**Solution:**

1. **Set environment variable:**
   ```cmd
   set PYTHONIOENCODING=utf-8
   pyinstaller pallet_builder.spec
   ```

2. **Or add to spec file:**
   ```python
   # At top of pallet_builder.spec
   import sys
   sys.stdout.reconfigure(encoding='utf-8')
   sys.stderr.reconfigure(encoding='utf-8')
   ```

---

### Error 6: "RecursionError: maximum recursion depth exceeded"

**Symptoms:**
```
RecursionError: maximum recursion depth exceeded
```

**Cause:**
- Circular imports
- Deep module nesting

**Solution:**

1. **Increase recursion limit in spec file:**
   ```python
   # At top of pallet_builder.spec
   import sys
   sys.setrecursionlimit(5000)
   ```

2. **Check for circular imports in app/ modules**

---

### Error 7: "OSError: [WinError 193] %1 is not a valid Win32 application"

**Symptoms:**
```
OSError: [WinError 193] %1 is not a valid Win32 application
```

**Cause:**
- 32-bit/64-bit mismatch
- Corrupted DLL

**Solution:**

1. **Check Python architecture:**
   ```cmd
   python -c "import struct; print(struct.calcsize('P') * 8)"
   ```
   Should output: `64` (for 64-bit)

2. **Reinstall PyInstaller:**
   ```cmd
   pip uninstall pyinstaller
   pip install pyinstaller
   ```

3. **Use matching architecture throughout**

---

### Error 8: "RuntimeError: No metadata path found for distribution 'X'"

**Symptoms:**
```
RuntimeError: No metadata path found for distribution 'package-name'
```

**Cause:**
- Package installed in editable mode
- Missing metadata

**Solution:**

1. **Reinstall package normally:**
   ```cmd
   pip uninstall package-name
   pip install package-name
   ```

2. **Or add to hiddenimports in spec file**

---

### Error 9: "AttributeError: module 'X' has no attribute 'Y'"

**Symptoms:**
```
AttributeError: module 'winreg' has no attribute 'ConnectRegistry'
```

**Cause:**
- Wrong Python version
- Module not available on platform

**Solution:**

1. **Check Python version:**
   ```cmd
   python --version
   ```
   Should be: `Python 3.8+`

2. **Verify module availability:**
   ```cmd
   python -c "import winreg; print(dir(winreg))"
   ```

3. **If module is platform-specific, ensure it's in try-except block**

---

### Error 10: "Failed to execute script 'pyi_rth_pkgres'"

**Symptoms:**
```
Failed to execute script 'pyi_rth_pkgres' due to unhandled exception
```

**Cause:**
- PyInstaller version issue
- Conflicting packages

**Solution:**

1. **Update PyInstaller:**
   ```cmd
   pip install --upgrade pyinstaller
   ```

2. **Try specific version:**
   ```cmd
   pip install pyinstaller==5.13.0
   ```

3. **Clean install:**
   ```cmd
   pip uninstall pyinstaller
   pip cache purge
   pip install pyinstaller
   ```

---

## Build Environment Checklist

Before building, verify:

### Python Environment:
```cmd
REM Check Python version (should be 3.8+)
python --version

REM Check pip
pip --version

REM Check architecture (should be 64-bit)
python -c "import struct; print(struct.calcsize('P') * 8)"
```

### Required Packages:
```cmd
pip install openpyxl pandas python-dateutil pyyaml pillow reportlab pyinstaller
```

### Project Files:
```cmd
REM Verify reference workbook exists
dir "EXCEL\BUILD 10-12-25.xlsx"

REM Verify icon files exist
dir "icons\PalletManager.ico"

REM Verify spec file exists
dir pallet_builder.spec

REM Verify app modules exist
dir app\*.py
```

### Clean State:
```cmd
REM Remove old build artifacts
rmdir /s /q build dist __pycache__
del "Pallet Manager.exe"

REM Remove .pyc files
for /r %%i in (*.pyc) do del "%%i"
```

---

## Step-by-Step Build Process

### 1. Prepare Environment

```cmd
REM Navigate to project directory
cd "C:\path\to\Pallet Manager 1.1"

REM Activate virtual environment (if using)
venv\Scripts\activate

REM Update pip
python -m pip install --upgrade pip

REM Install/update dependencies
pip install -r requirements.txt
```

### 2. Verify Prerequisites

```cmd
REM Check all dependencies
pip list

REM Verify critical files
dir EXCEL\BUILD*.xlsx
dir icons\*.ico
dir app\*.py
```

### 3. Clean Previous Builds

```cmd
rmdir /s /q build dist
del "Pallet Manager.exe"
```

### 4. Run Build

```cmd
pyinstaller pallet_builder.spec
```

### 5. Verify Build Output

```cmd
REM Check if EXE was created
dir "Pallet Manager.exe"

REM Check file size (should be 80-120 MB)
dir "Pallet Manager.exe" | findstr "Pallet Manager"
```

---

## Debug Build (Verbose Output)

If build fails, run with verbose output:

```cmd
pyinstaller --log-level=DEBUG pallet_builder.spec > build_log.txt 2>&1
```

Then review `build_log.txt` for detailed error information.

---

## Alternative: Build with Console Window

For debugging, temporarily enable console:

1. **Edit `pallet_builder.spec` line 181:**
   ```python
   console=True,  # Change from False
   ```

2. **Rebuild:**
   ```cmd
   pyinstaller pallet_builder.spec
   ```

3. **Run and see errors:**
   ```cmd
   "Pallet Manager.exe"
   ```

4. **After fixing, change back to:**
   ```python
   console=False,
   ```

---

## Common Windows-Specific Issues

### Issue: Antivirus Blocks Build

**Symptoms:**
- Build hangs
- Files disappear after creation
- "Access denied" errors

**Solution:**
1. Add exclusion for project directory
2. Add exclusion for Python installation
3. Temporarily disable real-time protection

### Issue: Long Path Names

**Symptoms:**
- "Path too long" errors
- Files not found

**Solution:**
1. Enable long paths in Windows:
   ```cmd
   REM Run as Administrator
   reg add HKLM\SYSTEM\CurrentControlSet\Control\FileSystem /v LongPathsEnabled /t REG_DWORD /d 1 /f
   ```

2. Or move project to shorter path:
   ```cmd
   C:\PM\  instead of  C:\Users\...\Documents\...\Pallet Manager 1.1\
   ```

### Issue: Windows Defender SmartScreen

**Symptoms:**
- "Windows protected your PC" message
- Can't run EXE

**Solution:**
1. Click "More info" → "Run anyway"
2. For distribution, consider code signing certificate

---

## Getting Help

If build still fails:

1. **Capture full error output:**
   ```cmd
   pyinstaller --log-level=DEBUG pallet_builder.spec > build_error.txt 2>&1
   ```

2. **Collect environment info:**
   ```cmd
   python --version > env_info.txt
   pip list >> env_info.txt
   systeminfo >> env_info.txt
   ```

3. **Document:**
   - What command you ran
   - Full error message
   - Python version
   - Windows version
   - What you've tried

4. **Check files:**
   - `build_error.txt` - Full build log
   - `env_info.txt` - Environment details
   - `build/` folder - Intermediate files

---

## Quick Fix Checklist

Try these in order:

- [ ] Clean build: `rmdir /s /q build dist`
- [ ] Update PyInstaller: `pip install --upgrade pyinstaller`
- [ ] Verify dependencies: `pip install -r requirements.txt`
- [ ] Check reference workbook: `dir EXCEL\BUILD*.xlsx`
- [ ] Run as Administrator
- [ ] Disable antivirus temporarily
- [ ] Try verbose build: `pyinstaller --log-level=DEBUG pallet_builder.spec`
- [ ] Check Python version: `python --version` (should be 3.8+)
- [ ] Check architecture: 64-bit
- [ ] Move to shorter path if needed

---

**Last Updated:** January 9, 2026  
**For:** Pallet Manager v1.1 Windows Build

