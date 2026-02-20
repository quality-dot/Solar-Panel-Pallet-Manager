@echo off
REM Simple Windows build script - minimal approach
REM Run this script to create Pallet Manager.exe

cd /d "%~dp0.."

echo Building Pallet Manager for Windows...
echo.

REM Check Python availability early
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found on PATH.
    echo Install Python and ensure "python" command is available.
    pause
    exit /b 1
)

REM Install dependencies only if missing (avoid repeated upgrades/churn)
echo Checking required dependencies...
echo.

REM Check if openpyxl is installed (REQUIRED - Excel operations)
python -c "import openpyxl" 2>nul
if errorlevel 1 (
    echo ERROR: openpyxl is not installed and is REQUIRED!
    echo Installing openpyxl...
    python -m pip install openpyxl
    if errorlevel 1 (
        echo ERROR: Failed to install openpyxl. Please install manually:
        echo   python -m pip install openpyxl
        pause
        exit /b 1
    )
)

REM Check if pandas is installed (REQUIRED - Data processing)
python -c "import pandas" 2>nul
if errorlevel 1 (
    echo ERROR: pandas is not installed and is REQUIRED!
    echo Installing pandas...
    python -m pip install pandas
    if errorlevel 1 (
        echo ERROR: Failed to install pandas. Please install manually:
        echo   python -m pip install pandas
        pause
        exit /b 1
    )
)

REM Check if reportlab is installed (required for PDF creation)
python -c "import reportlab" 2>nul
if errorlevel 1 (
    echo WARNING: reportlab is not installed. PDF creation will not work.
    echo Installing reportlab...
    python -m pip install reportlab
    if errorlevel 1 (
        echo ERROR: Failed to install reportlab. Please install manually:
        echo   python -m pip install reportlab
        pause
        exit /b 1
    )
)

REM Check if jinja2 is installed (dependency of pandas/reportlab)
python -c "import jinja2" 2>nul
if errorlevel 1 (
    echo Installing jinja2...
    python -m pip install jinja2
    if errorlevel 1 (
        echo ERROR: Failed to install jinja2. Please install manually:
        echo   python -m pip install jinja2
        pause
        exit /b 1
    )
)

REM Check if Pillow is installed (dependency of reportlab for image support)
python -c "import PIL" 2>nul
if errorlevel 1 (
    echo Installing Pillow...
    python -m pip install Pillow
    if errorlevel 1 (
        echo WARNING: Failed to install Pillow. PDF creation may have limited functionality.
        echo   python -m pip install Pillow
    )
)

REM Check if pywin32 is installed (REQUIRED - Windows integrations)
python -c "import win32com" 2>nul
if errorlevel 1 (
    echo Installing pywin32...
    python -m pip install pywin32
    if errorlevel 1 (
        echo ERROR: Failed to install pywin32. Please install manually:
        echo   python -m pip install pywin32
        pause
        exit /b 1
    )
)

REM Check if PyPDF2 is installed (REQUIRED - PDF handling)
python -c "import PyPDF2" 2>nul
if errorlevel 1 (
    echo Installing PyPDF2...
    python -m pip install PyPDF2
    if errorlevel 1 (
        echo ERROR: Failed to install PyPDF2. Please install manually:
        echo   python -m pip install PyPDF2
        pause
        exit /b 1
    )
)

REM Check if PyInstaller is installed
echo Checking PyInstaller...
python -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo Installing PyInstaller and hooks...
    python -m pip install pyinstaller pyinstaller-hooks-contrib
    if errorlevel 1 (
        echo ERROR: Failed to install PyInstaller. Please install manually:
        echo   python -m pip install pyinstaller pyinstaller-hooks-contrib
        pause
        exit /b 1
    )
)

REM Check for SumatraPDF and download if missing
echo.
echo Checking for SumatraPDF...
if not exist "external_tools\SumatraPDF\SumatraPDF.exe" (
    echo SumatraPDF not found. Downloading automatically...
    echo.
    
    REM Use Python to download (more reliable than PowerShell)
    python scripts\download_sumatrapdf.py
    
    if errorlevel 1 (
        echo.
        echo WARNING: Failed to download SumatraPDF automatically.
        echo Build will continue without it, but automatic print dialog won't work.
        echo.
        echo To enable automatic print dialog:
        echo 1. Download from: https://www.sumatrapdfreader.org/download-free-pdf-viewer
        echo 2. Download the latest 64-bit portable ZIP
        echo 3. Extract and place SumatraPDF.exe in: external_tools\SumatraPDF\
        echo 4. Rebuild
        echo.
    )
) else (
    echo ✓ SumatraPDF found: external_tools\SumatraPDF\SumatraPDF.exe
    echo   Will bundle for automatic print dialog support.
    echo.
)

REM Check if spec file exists
if not exist "pallet_builder.spec" (
    echo ERROR: pallet_builder.spec not found!
    echo Please ensure the spec file exists in the project root.
    pause
    exit /b 1
)

REM Clean up old build artifacts to ensure fresh build
echo.
echo Cleaning old build artifacts...
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"
if exist "Pallet Manager.exe" del /f /q "Pallet Manager.exe"
if exist "__pycache__" rmdir /s /q "__pycache__"
if exist "app\__pycache__" rmdir /s /q "app\__pycache__"
echo Done cleaning!
echo.

REM Try building without spec file first to isolate the issue
echo Building executable without spec file...
python -m PyInstaller launch_app.py --onefile --windowed --name="Pallet Manager" --hidden-import=http --hidden-import=http.client --hidden-import=http.server --hidden-import=http.cookies --hidden-import=http.cookiejar --hidden-import=urllib --hidden-import=urllib.parse --hidden-import=urllib.error --hidden-import=socket --hidden-import=email --hidden-import=email.utils --hidden-import=email.header --hidden-import=email.mime --hidden-import=secrets --hidden-import=ssl --hidden-import=urllib.request --clean --noconfirm --log-level=INFO

if errorlevel 1 (
    echo.
    echo Basic build failed, trying with spec file...
    python -m PyInstaller pallet_builder.spec --clean --noconfirm --log-level=INFO --hidden-import=http --hidden-import=http.client --hidden-import=http.server --hidden-import=http.cookies --hidden-import=http.cookiejar --hidden-import=urllib --hidden-import=urllib.parse --hidden-import=urllib.error --hidden-import=socket
)

if errorlevel 1 (
    echo.
    echo Build failed!
    pause
    exit /b 1
)

echo.
echo Build Complete!
echo Executable: Pallet Manager.exe
echo.
pause

