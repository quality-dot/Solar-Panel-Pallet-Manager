# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for Pallet Manager
Build with: pyinstaller pallet_builder.spec
"""

import os
from PyInstaller.utils.hooks import collect_submodules, collect_data_files

block_cipher = None

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
        ('EXCEL/BUILD 10-12-25.xlsx', 'reference_workbook'),
        # Include icons for window icon (taskbar/dock)
        ('icons/PalletManager.ico', 'icons'),
        ('icons/PalletManager.icns', 'icons'),
    ] + reportlab_datas,  # Add collected reportlab data files
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
        # openpyxl - Excel file operations
        'openpyxl',
        'openpyxl.cell._writer',
        'openpyxl.workbook._writer',
        'openpyxl.styles',
        'openpyxl.styles.fonts',
        'openpyxl.styles.borders',
        'openpyxl.styles.fills',
        'openpyxl.styles.alignment',
        'openpyxl.styles.protection',
        'openpyxl.utils',
        'openpyxl.cell.cell',
        'openpyxl.cell.text',
        'openpyxl.worksheet.worksheet',
        'openpyxl.workbook.workbook',
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
    ] + reportlab_hiddenimports,  # Add all collected reportlab modules
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

