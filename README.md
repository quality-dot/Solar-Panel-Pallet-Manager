# Pallet Manager

**Version 1.1.0**

A professional application for managing solar panel pallets with automated barcode scanning, Excel integration, and comprehensive pallet tracking.

## 🚀 Quick Start

### For End Users

**macOS:**
1. Download `PalletManager-Installer.pkg` or `PalletManager-Installer.dmg`
2. Double-click to install
3. Follow the installation wizard
4. Launch from Applications folder

**Windows:**
1. Download `Pallet Manager-Setup.exe`
2. Double-click to install
3. Follow the installation wizard
4. Launch from Start Menu or Desktop

**First Run:**
- The app automatically creates required folders
- Place Excel workbooks in `EXCEL/` folder
- Drop sun simulator files in `SUN SIMULATOR DATA/` folder
- Start scanning barcodes to build pallets!

### For Developers

**Prerequisites:**
- Python 3.11+
- Required packages (see `requirements.txt`)

**Setup:**
```bash
# Install dependencies
pip install -r requirements.txt

# Verify dependencies
python verify_dependencies.py
```

**Run from Source:**
```bash
python app/pallet_builder_gui.py
```

**Build Installers:**
```bash
# macOS
./scripts/install_all.sh

# Windows
scripts\install_all_windows.bat
```

**Release New Version:**
```bash
./scripts/release.sh 1.0.1
```

---

## 📚 Documentation

### 📘 [Complete Application Overview](APP_OVERVIEW.md) ⭐ **START HERE**
**Comprehensive guide explaining what the app does and how it works:**
- What is Pallet Manager?
- What problem does it solve?
- Who uses it and why?
- Complete workflow explanation
- Technical architecture
- Data flow and processes
- File structure and organization

### 📖 [Complete User Guide](docs/USER_GUIDE.md)
**Everything users need to know:**
- Installation instructions (macOS & Windows)
- First-time setup
- Using the application
- Troubleshooting common issues
- FAQ

### 🛠️ [Developer Guide](docs/DEVELOPER_GUIDE.md)
**Everything developers need:**
- Project structure
- Build and packaging instructions
- Scripts reference
- Deployment guide
- Update distribution
- Performance optimizations

### 📋 Quick References
- **[Scripts Guide](SCRIPTS_GUIDE.md)** - All available scripts and their usage
- **[Project Structure](PROJECT_STRUCTURE.md)** - Directory organization
- **[Troubleshooting](docs/USER_GUIDE.md#troubleshooting)** - Common issues and solutions

---

## 📁 Project Structure

```
.
├── app/                    # Application source code
├── scripts/                # Build and installer scripts
├── docs/                   # Documentation
├── assets/                 # Application icons and assets
├── tools/                  # External tools and dependencies
├── data/                   # User data and runtime files
│   ├── CUSTOMERS/          # Customer data
│   ├── EXCEL/              # Excel workbooks
│   ├── PALLETS/            # Exported pallets
│   ├── IMPORTED DATA/      # Processed simulator data
│   ├── SUN SIMULATOR DATA/ # Drop new simulator files here
│   └── LOGS/               # Application logs
├── tests/                  # Test suite
└── [other files]           # Build configs, requirements, etc.
```

See [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) for detailed structure.

---

## ✨ Features

- ✅ **Barcode Scanning** - Scan panel barcodes to build pallets
- ✅ **Excel Integration** - Automatic workbook updates
- ✅ **Pallet History** - Track all pallets with search and export
- ✅ **Export to Excel** - Date-organized pallet exports
- ✅ **Sun Simulator Import** - Import and process simulator data
- ✅ **Professional Installers** - Easy installation wizards
- ✅ **Cross-Platform** - Works on macOS & Windows
- ✅ **Standalone** - No Python installation required for end users

---

## 🛠️ Development

### Common Tasks

**Build installers:**
```bash
./scripts/install_all.sh          # macOS
scripts\install_all_windows.bat   # Windows
```

**Release new version:**
```bash
./scripts/release.sh 1.0.1
```

**Run tests:**
```bash
python test_bugs.py
```

**Create icons:**
```bash
./scripts/create_icons.sh icons/Pallet\ icon.png
```

See [SCRIPTS_GUIDE.md](SCRIPTS_GUIDE.md) for complete scripts reference.

---

## 📦 Building Installers

### macOS

```bash
# Complete installer (recommended)
./scripts/install_all.sh

# Or step by step:
./scripts/build_macos.sh
./scripts/create_macos_installer.sh
./scripts/create_dmg.sh
```

**Output:**
- `dist/Pallet Manager.app` - Application bundle
- `dist/PalletManager-Installer.pkg` - Professional installer
- `dist/PalletManager-Installer.dmg` - DMG file

### Windows

```bash
# Complete installer (recommended)
scripts\install_all_windows.bat

# Or step by step:
scripts\setup_windows.bat
scripts\build_windows.bat
scripts\create_windows_installer.bat
```

**Output:**
- `dist/Pallet Manager.exe` - Standalone executable
- `dist/Pallet Manager-Setup.exe` - Installer

**Note:** Windows installer requires NSIS (Nullsoft Scriptable Install System)

---

## 🆘 Support

**For Users:**
- See [Complete User Guide](docs/USER_GUIDE.md) for installation and usage help
- Check [Troubleshooting](docs/USER_GUIDE.md#troubleshooting) for common issues

**For Developers:**
- See [Developer Guide](docs/DEVELOPER_GUIDE.md) for build and deployment
- Check [Scripts Guide](SCRIPTS_GUIDE.md) for available scripts

---

## 📝 License

Copyright (c) 2024 Crossroads Solar. All rights reserved.

---

## 📊 Version

**Current Version:** 1.1.0

### Version History

- **[Version 1.1.0 Changelog](VERSION_1.1_CHANGELOG.md)** - Latest release
  - Enhanced Pallet History interface
  - Customer filtering and barcode search
  - Sortable table headers
  - Delete pallet functionality
  - Improved data import handling
  - Bug fixes and performance improvements

- **Version 1.0.0** - Initial release
  - Core pallet building functionality
  - Barcode scanning and validation
  - Excel export and integration
  - Pallet history tracking
  - PDF creation and printing

### Version Information

Current version details: See `app/version.py`

To update version:
```bash
python scripts/update_version.py 1.1.1
```
