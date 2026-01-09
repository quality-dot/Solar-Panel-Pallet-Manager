"""
Setup script for py2app (macOS packaging)
Build with: python setup.py py2app
"""

from setuptools import setup

APP = ['app/pallet_builder_gui.py']
DATA_FILES = [
    # Include any data files needed
    # ('app', ['app/config.yaml']),
]

# Check if reportlab is available (optional dependency)
try:
    import reportlab
    HAS_REPORTLAB = True
except ImportError:
    HAS_REPORTLAB = False

# Build packages list
packages_list = [
    'openpyxl',
    'pandas',
    'dateutil',
    'yaml',
    'tkinter',
]

# Build includes list
includes_list = [
    # openpyxl
    'openpyxl',
    'openpyxl.styles',
    'openpyxl.utils',
    'openpyxl.cell.cell',
    # pandas - include all necessary submodules
    'pandas',
    'pandas._libs',
    'pandas._libs.tslibs',
    'pandas._libs.tslibs.timedeltas',
    'pandas._libs.tslibs.nattype',
    'pandas._libs.tslibs.np_datetime',
    'pandas._libs.tslibs.tzconversion',
    'pandas._libs.tslibs.base',
    'pandas._libs.tslibs.parsing',
    'pandas._libs.testing',
    'pandas._testing',
    'pandas._testing.asserters',
    'pandas.io.excel',
    'pandas.io.excel._openpyxl',
    # python-dateutil
    'dateutil',
    'dateutil.parser',
    'dateutil.relativedelta',
    # pyyaml
    'yaml',
    # Standard library modules that pandas needs
    'cmath',
    'math',
    'decimal',
    'fractions',
]

# Add reportlab only if available
if HAS_REPORTLAB:
    packages_list.append('reportlab')
    includes_list.extend([
        'reportlab',
        'reportlab.lib.pagesizes',
        'reportlab.pdfgen.canvas',
    ])

OPTIONS = {
    'argv_emulation': False,  # Disable for faster startup
    'packages': packages_list,
    'includes': includes_list,
    'excludes': [
        # Exclude unnecessary modules to reduce size and improve performance
        'matplotlib',
        'scipy',
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
        'numpy.tests',
        'pandas.tests',
        'pandas.plotting',  # Not used in this app
        'pandas.io.clipboard',  # Not used
        'openpyxl.tests',
        'sqlite3',  # Not used
        'multiprocessing',  # Not used
        'concurrent.futures',  # Not used
    ],
    'site_packages': True,  # Include site-packages to ensure all dependencies
    'semi_standalone': False,  # Fully standalone bundle (better performance)
    'use_pythonpath': True,  # Use Python path
    'strip': True,  # Strip debug symbols for smaller size and faster loading
    'iconfile': 'icons/PalletManager.icns',  # Application icon
    'plist': {
        'CFBundleName': 'Pallet Manager',
        'CFBundleDisplayName': 'Pallet Manager',
        'CFBundleGetInfoString': 'Pallet Builder for Solar Panel Management',
        'CFBundleIdentifier': 'com.crossroads.palletmanager',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0.0',
        'NSHighResolutionCapable': True,
        'LSMinimumSystemVersion': '10.13',  # macOS High Sierra or later
        'LSRequiresNativeExecution': True,  # Prefer native execution (ARM64)
    },
    'optimize': 2,  # Maximum bytecode optimization
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)

