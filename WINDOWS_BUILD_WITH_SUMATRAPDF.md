# Windows Build with SumatraPDF Integration

This guide explains how to build Pallet Manager with bundled SumatraPDF for automatic print dialog support.

## Why Bundle SumatraPDF?

**Problem:** Windows default PDF viewer (Edge) doesn't support direct print dialog launching
- Users have to manually navigate and print
- Multiple pallets require opening each PDF separately
- Poor user experience

**Solution:** Bundle SumatraPDF (free, lightweight, perfect command-line support)
- ✅ Opens print dialog automatically with `-print-dialog` flag
- ✅ Only ~5MB added to build
- ✅ Handles batch printing elegantly
- ✅ No installation required for end users

## Setup Instructions (AUTOMATIC!)

### Just Build - That's It!

Run the Windows build:

```cmd
cd "C:\path\to\Pallet Manager 1.1"
scripts\build_windows.bat
```

**The build script automatically:**
1. ✅ Checks if SumatraPDF is present
2. ✅ Downloads it from GitHub if missing (portable version)
3. ✅ Extracts it to the correct location
4. ✅ Bundles it into your .exe
5. ✅ Configures the app to use it

**No manual steps required!** 🎉

### What You'll See:

**First build (no SumatraPDF yet):**
```
Checking for SumatraPDF...
SumatraPDF not found. Downloading automatically...
Downloading SumatraPDF 3.5.2 (64-bit portable)...
Extracting SumatraPDF...

✓ SumatraPDF downloaded and extracted successfully!
  Automatic print dialog will be enabled.
```

**Subsequent builds:**
```
Checking for SumatraPDF...
✓ SumatraPDF found: external_tools\SumatraPDF\SumatraPDF.exe
  Will bundle for automatic print dialog support.
```

### Manual Download (If Auto-Download Fails)

If the automatic download fails (firewall/proxy):

1. Go to: https://www.sumatrapdfreader.org/download-free-pdf-viewer
2. Download the **64-bit portable version**: `SumatraPDF-3.5.2-64.zip`
3. Extract and place `SumatraPDF.exe` in: `external_tools\SumatraPDF\SumatraPDF.exe`
4. Rebuild

## What Happens at Runtime?

### With Bundled SumatraPDF (Best Experience):
1. User exports pallet(s)
2. PDF created and saved to HISTORY
3. **Print dialog opens automatically** ✨
4. User adjusts settings and clicks Print
5. Done!

### Without SumatraPDF (Fallback):
1. User exports pallet(s)
2. PDF created and saved to HISTORY
3. App checks for:
   - Installed SumatraPDF
   - Adobe Reader
   - Microsoft Edge
4. Opens PDF with best available viewer
5. Shows instructions if auto-print not available

## User Experience Comparison

### Before (No SumatraPDF):
```
1. Export 5 pallets
2. PDFs created
3. Opens in Edge browser
4. Each PDF in separate tab
5. User manually navigates tabs
6. Ctrl+P on each one
7. 😩 Tedious for multiple pallets
```

### After (With SumatraPDF):
```
1. Export 5 pallets
2. PDFs created
3. Print dialog opens for each PDF automatically
4. User clicks Print (or adjusts settings)
5. ✅ Clean, fast workflow
```

## Licensing

**SumatraPDF License:** AGPL/GPLv3
- ✅ Free to redistribute
- ✅ Free for commercial use
- ✅ No attribution required in UI
- ✅ Source available at: https://github.com/sumatrapdfreader/sumatrapdf

**Compliance:**
- We bundle the unmodified portable executable
- We don't modify the source code
- License file included in external_tools/SumatraPDF/

## If SumatraPDF is NOT Included

The app will still work! It just falls back to:
1. Checking for installed SumatraPDF
2. Checking for Adobe Reader
3. Using Microsoft Edge
4. Default PDF viewer + manual print instructions

## File Size Impact

- **Without SumatraPDF:** ~180 MB
- **With SumatraPDF:** ~185 MB (+5 MB)

Worth it for the dramatically better UX! 🎯

## Troubleshooting

### Build says "SumatraPDF not found"

Check the path:
```cmd
dir "external_tools\SumatraPDF\SumatraPDF.exe"
```

Should show the file. If not, extract the portable version correctly.

### Print dialog still doesn't open

1. Check build output - did it bundle SumatraPDF?
2. Look for message: `✓ Found SumatraPDF`
3. If not found, re-download and place in correct location

### Can I use a different version?

Yes! Any SumatraPDF 3.x portable version works. Just:
1. Download the portable ZIP
2. Extract SumatraPDF.exe
3. Place in external_tools/SumatraPDF/
4. Rebuild

## Summary

**For end users:** Zero installation, zero config - print dialog just works!
**For developers:** 5 MB trade-off for massively better UX
**For deployment:** Single .exe with everything bundled

🎉 Professional-grade PDF printing, batteries included!

