# Windows Build - Missing reportlab

## Issue

The application is telling you to install reportlab with pip. This means the Windows .exe was built **without reportlab installed**, so PDF creation features won't work.

## Why This Happened

During the Windows build:
1. The build script tried to install reportlab
2. reportlab failed to install or wasn't available
3. PyInstaller showed a WARNING but continued building
4. The .exe was created without reportlab bundled

## Solution

**You need to rebuild the .exe with reportlab properly installed.**

### Step 1: Install reportlab on Windows

```cmd
python -m pip install reportlab
```

If that fails, try:

```cmd
python -m pip install --upgrade pip
python -m pip install reportlab
```

If it STILL fails, you might need Visual C++ Build Tools (reportlab has C extensions):
- Download from: https://visualstudio.microsoft.com/visual-cpp-build-tools/
- Install "Desktop development with C++"
- Restart Command Prompt
- Try `python -m pip install reportlab` again

### Step 2: Verify reportlab is installed

```cmd
python -c "import reportlab; print(reportlab.__version__)"
```

You should see a version number (e.g., `4.4.7`).

### Step 3: Rebuild the application

```cmd
cd C:\Users\grant.schlarb\Downloads\Solar-Panel-Pallet-Manager-main\Solar-Panel-Pallet-Manager-main
scripts\build_windows.bat
```

You should now see during the build:

```
✓ reportlab found: 4.4.7
✓ Collected XXX reportlab modules
✓ Collected XX reportlab data files
```

### Step 4: Test the application

Run `Pallet Manager.exe` and:
1. Go to History
2. Select a pallet
3. Click "Export to PDF"
4. Should work without errors!

## Alternative: Use Without PDF Export

If you can't install reportlab, the application will still work fine for:
- ✅ Scanning barcodes
- ✅ Building pallets
- ✅ Exporting to Excel
- ✅ Viewing history
- ✅ Customer management
- ✅ Import simulator data

Only **PDF export from History** won't work. Everything else functions normally!

## Notes

- reportlab is **optional** - the app won't crash without it
- The app will show a clear error if you try to create PDFs without it
- Excel export (the main export feature) works fine without reportlab
- PDF export is just a convenience feature for printing pallet history

## Status

- ✅ All other features work
- ❌ PDF export requires reportlab
- ✅ App handles missing reportlab gracefully





