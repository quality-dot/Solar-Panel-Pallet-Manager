# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for Pallet Manager
Build with: pyinstaller pallet_builder.spec
"""

import os
import sys
from pathlib import Path
from PyInstaller.utils.hooks import collect_submodules, collect_data_files

block_cipher = None

# Get absolute paths for data files (more reliable on Windows)
# Note: __file__ isn't available in spec file context, use SPECPATH instead
project_root = Path(SPECPATH)
excel_dir = project_root / 'EXCEL'
icon_ico = project_root / 'icons' / 'PalletManager.ico'
icon_icns = project_root / 'icons' / 'PalletManager.icns'

# Debug output
print("\n" + "=" * 70)
print("CHECKING FOR REFERENCE WORKBOOK")
print("=" * 70)
print(f"Spec file location: {SPECPATH}")
print(f"Project root: {project_root}")
print(f"EXCEL directory: {excel_dir}")
print(f"EXCEL exists: {excel_dir.exists()}")
if excel_dir.exists():
    print(f"\nAll files in EXCEL directory:")
    for f in sorted(excel_dir.glob('*')):
        print(f"  - {f.name} ({f.stat().st_size} bytes)")
print("=" * 70 + "\n")

# Find a reference workbook - can be BUILD or CURRENT.xlsx
excel_file = None

# Priority 1: Look for BUILD workbook (preferred for bundling)
for pattern in ['BUILD*.xlsx', 'Build*.xlsx', 'build*.xlsx']:
    matches = list(excel_dir.glob(pattern))
    if matches:
        excel_file = matches[0]
        print(f"✓ Found BUILD workbook: {excel_file.name}")
        break

# Priority 2: Fall back to CURRENT.xlsx if no BUILD file
if not excel_file:
    current_xlsx = excel_dir / 'CURRENT.xlsx'
    if current_xlsx.exists():
        excel_file = current_xlsx
        print(f"✓ Found CURRENT.xlsx (using as reference workbook)")

# Verify we found a reference workbook
if not excel_file or not excel_file.exists():
    print("=" * 70)
    print("ERROR: No reference workbook found!")
    print("=" * 70)
    print(f"Current directory: {os.getcwd()}")
    print(f"Project root: {project_root}")
    print(f"EXCEL directory: {excel_dir}")
    print(f"EXCEL directory exists: {excel_dir.exists()}")
    if excel_dir.exists():
        print(f"\nFiles in EXCEL directory:")
        for f in excel_dir.glob('*'):
            print(f"  - {f.name}")
    print()
    print("Need at least ONE of:")
    print("  - BUILD*.xlsx (any BUILD file)")
    print("  - CURRENT.xlsx")
    print()
    print("The reference workbook is bundled in the app and copied")
    print("to the user's EXCEL folder on first launch.")
    print("=" * 70)
    sys.exit(1)

print(f"  Full path: {excel_file}")
print(f"  Size: {excel_file.stat().st_size} bytes")

# Check and collect openpyxl (REQUIRED for Excel operations)
print("\nChecking openpyxl...")
openpyxl_hiddenimports = []
openpyxl_datas = []

try:
    import openpyxl
    print(f"✓ openpyxl found: {openpyxl.__version__ if hasattr(openpyxl, '__version__') else 'unknown version'}")
    
    # Collect all openpyxl submodules and data files to ensure it's fully bundled
    openpyxl_hiddenimports = collect_submodules('openpyxl')
    openpyxl_datas = collect_data_files('openpyxl')
    print(f"✓ Collected {len(openpyxl_hiddenimports)} openpyxl modules")
    print(f"✓ Collected {len(openpyxl_datas)} openpyxl data files")
    
except ImportError as e:
    print("=" * 70)
    print("ERROR: openpyxl not found. Application cannot function without it!")
    print("=" * 70)
    print("Please install openpyxl before building:")
    print("  python -m pip install openpyxl")
    print(f"Error: {e}")
    print("=" * 70)
    sys.exit(1)

# Check if reportlab is available (required for PDF creation)
# Note: reportlab must be installed before building: pip install reportlab
HAS_REPORTLAB = False
reportlab_hiddenimports = []
reportlab_datas = []

try:
    import reportlab
    HAS_REPORTLAB = True
    print(f"✓ reportlab found: {reportlab.__version__ if hasattr(reportlab, '__version__') else 'unknown version'}")
    print(f"  Location: {reportlab.__file__ if hasattr(reportlab, '__file__') else 'unknown'}")
    
    # Collect all reportlab submodules and data files to avoid missing imports
    reportlab_hiddenimports = collect_submodules('reportlab')
    reportlab_datas = collect_data_files('reportlab')
    print(f"✓ Collected {len(reportlab_hiddenimports)} reportlab modules")
    print(f"✓ Collected {len(reportlab_datas)} reportlab data files")
    
except ImportError as e:
    HAS_REPORTLAB = False
    print("=" * 70)
    print("WARNING: reportlab not found. PDF creation will not work.")
    print("=" * 70)
    print("Please install reportlab before building:")
    print("  pip install reportlab")
    print(f"Error: {e}")
    print("=" * 70)

a = Analysis(
    ['app/pallet_builder_gui.py'],
    pathex=[],
    binaries=[],
    datas=[
        # Include reference workbook - will be copied to EXCEL folder on first run
        (str(excel_file), 'reference_workbook'),
        # Include icons for window icon (taskbar/dock)
        (str(icon_ico), 'icons'),
        (str(icon_icns), 'icons'),
    ] + openpyxl_datas + reportlab_datas,  # Add collected openpyxl and reportlab data files
    hiddenimports=[
        # App modules - must be explicitly included
        'app',
        'app.path_utils',
        'app.pallet_manager',
        'app.workbook_utils',
        'app.pallet_exporter',
        'app.pallet_history_window',
        'app.serial_database',
        'app.version',
        # Standard library modules that PyInstaller might miss
        'secrets',
        'hashlib',
        'hmac',
        # pandas - Data processing
        'pandas',
        'pandas._libs',
        'pandas._libs.tslibs',
        'pandas._libs.tslibs.timedeltas',
        'pandas._libs.tslibs.nattype',
        'pandas._libs.tslibs.np_datetime',
        'pandas._libs.tslibs.tzconversion',
        'pandas._libs.tslibs.base',
        'pandas._libs.tslibs.parsing',
        'pandas._libs.tslibs.timestamps',
        'pandas._libs.tslibs.period',
        'pandas._libs.tslibs.fields',
        'pandas._libs.tslibs.conversion',
        'pandas.io.excel',
        'pandas.io.excel._openpyxl',
        # pandas.plotting - may be imported by pandas internals
        'pandas.plotting',
        'pandas.plotting._core',
        'pandas.plotting._matplotlib',
        # python-dateutil - Date parsing
        'dateutil',
        'dateutil.parser',
        'dateutil.relativedelta',
        'dateutil.tz',
        # pyyaml - YAML config parsing
        'yaml',
        # jinja2 - Template engine (dependency of pandas/reportlab)
        'jinja2',
        'jinja2.ext',
        # email - Required by reportlab and other dependencies
        'email',
        'email.mime',
        'email.mime.text',
        'email.mime.multipart',
        # tkinter - GUI framework
        'tkinter',
        'tkinter.ttk',
        'tkinter.messagebox',
        'tkinter.filedialog',
        'tkinter.font',
        'tkinter.constants',
        # Pillow (PIL) - image support for reportlab
        'PIL',
        'PIL.Image',
    ] + openpyxl_hiddenimports + reportlab_hiddenimports,  # Add all collected openpyxl and reportlab modules
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # Exclude unnecessary modules to reduce size and improve performance
        'matplotlib',
        'numpy.distutils',
        'numpy.tests',
        'scipy',
        'pytest',
        'IPython',
        'jupyter',
        'notebook',
        'setuptools',
        'distutils',
        # Note: 'email' removed from excludes - required by reportlab
        'http',
        'urllib3',
        'requests',  # If not used
        'xmlrpc',
        'pydoc',
        'doctest',
        'unittest',
        'test',
        'tkinter.test',
        'pandas.tests',
        # Note: pandas.plotting removed from excludes - may be needed by pandas internals
        'pandas.io.clipboard',  # Not used
        'openpyxl.tests',
        'sqlite3',  # Not used
        'multiprocessing',  # Not used
        'concurrent.futures',  # Not used
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Pallet Manager',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,  # Disable strip on Windows (no strip tool available, prevents warnings)
    upx=False,  # Disable UPX compression for faster startup (size vs speed tradeoff)
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # No console window (GUI only)
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,  # Auto-detect: x86_64 for Windows
    codesign_identity=None,
    entitlements_file=None,
    icon='icons/PalletManager.ico',  # Application icon (PyInstaller handles path conversion)
)

# Output exe to project root instead of dist folder
# This is done by setting distpath when running PyInstaller

