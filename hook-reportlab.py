# PyInstaller hook for reportlab
# This ensures all reportlab dependencies are properly included

from PyInstaller.utils.hooks import collect_submodules, collect_data_files

# Collect all reportlab submodules
hiddenimports = collect_submodules('reportlab')

# Add specific modules that reportlab needs
hiddenimports += [
    'email',
    'email.utils',
    'email.header',
    'email.message',
    'email.parser',
    'email.generator',
    'email.encoders',
    'email.base64mime',
    'email.quoprimime',
    'email.mime',
    'email.mime.base',
    'email.mime.multipart',
    'email.mime.text',
    'smtplib',
    'imaplib',
    'calendar',
    'gzip',
    'base64',
    'uu',
    'binascii',
    'hashlib',
    'ssl',
    'urllib.request',
    'json',
    'csv',
    'xml.etree.ElementTree',
    'secrets',  # For numpy compatibility
]

# Collect any data files reportlab might need
datas = collect_data_files('reportlab')