# -*- mode: python ; coding: utf-8 -*-

import os
import sys
from pathlib import Path

# Get the project root directory
project_root = Path(__file__).parent

# Define data files to include
datas = [
    # Include the entire data directory (contains templates, configurations, etc.)
    (str(project_root / 'data'), 'data'),
    # Include assets
    (str(project_root / 'assets'), 'assets'),
    # Include docs if needed
    (str(project_root / 'docs'), 'docs'),
]

# Define binaries (external tools like SumatraPDF)
binaries = []
sumatra_path = project_root / 'tools' / 'SumatraPDF' / 'SumatraPDF.exe'
if sumatra_path.exists():
    binaries.append((str(sumatra_path), 'tools/SumatraPDF/'))

# Define hidden imports (modules that PyInstaller might miss)
hiddenimports = [
    # pandas and related
    'pandas',
    'pandas._libs.tslibs',
    'pandas._libs.tslibs.timedeltas',
    'pandas._libs.tslibs.nattype',
    'pandas._libs.tslibs.np_datetime',
    'pandas._libs.tslibs.tzconversion',
    'pandas._libs.tslibs.base',
    'pandas._libs.tslibs.parsing',
    'pandas.io.excel',
    'pandas.io.excel._openpyxl',
    'pandas.io.excel._base',
    # openpyxl
    'openpyxl',
    'openpyxl.styles',
    'openpyxl.utils',
    'openpyxl.cell.cell',
    'openpyxl.worksheet',
    'openpyxl.workbook',
    # dateutil
    'dateutil',
    'dateutil.parser',
    'dateutil.relativedelta',
    # yaml
    'yaml',
    # tkinter
    'tkinter',
    'tkinter.ttk',
    'tkinter.filedialog',
    'tkinter.messagebox',
    # app modules
    'app.pallet_builder_gui',
    'app.serial_database',
    'app.pallet_manager',
    'app.workbook_utils',
    'app.pallet_exporter',
    'app.pallet_history_window',
    'app.customer_manager',
    'app.version',
    'app.path_utils',
    'app.debug_logger',
    'app.archive_manager',
    'app.tool_runner',
    'app.import_sunsim',
    'app.resource_manager',
    'app.update_checker',
    # Optional modules (handle gracefully if not available)
    'reportlab',
    'reportlab.lib.pagesizes',
    'reportlab.pdfgen.canvas',
    'PIL',
    'PIL.Image',
    'jinja2',
]

# Define what to exclude to reduce size
excludes = [
    # Large unused packages
    'matplotlib',
    'scipy',
    'numpy.testing',
    'pandas.tests',
    'openpyxl.tests',
    'pytest',
    'IPython',
    'jupyter',
    'notebook',
    'setuptools',
    'distutils',
    'email',
    'http',
    'urllib3',
    'xmlrpc',
    'pydoc',
    'doctest',
    'unittest',
    'test',
    'sqlite3',
    'multiprocessing',
    'concurrent.futures',
    'PyQt5',
    'PyQt6',
    'PySide6',
    'PySide2',
    'wx',
    'kivy',
]

a = Analysis(
    ['launch_app.py'],
    pathex=[str(project_root)],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=excludes,
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

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
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Hide console window
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/PalletManager.ico',
)