@echo off
REM Simple Windows build script - minimal approach
REM Run this script to create Pallet Manager.exe

cd /d "%~dp0.."

echo Building Pallet Manager for Windows...
echo.

REM Check if reportlab is installed (required for PDF creation)
python -c "import reportlab" 2>nul
if errorlevel 1 (
    echo WARNING: reportlab is not installed. PDF creation will not work.
    echo Installing reportlab...
    pip install reportlab
    if errorlevel 1 (
        echo ERROR: Failed to install reportlab. Please install manually:
        echo   pip install reportlab
        pause
        exit /b 1
    )
)

REM Check if jinja2 is installed (dependency of pandas/reportlab)
python -c "import jinja2" 2>nul
if errorlevel 1 (
    echo Installing jinja2...
    pip install jinja2
    if errorlevel 1 (
        echo ERROR: Failed to install jinja2. Please install manually:
        echo   pip install jinja2
        pause
        exit /b 1
    )
)

REM Check if Pillow is installed (dependency of reportlab for image support)
python -c "import PIL" 2>nul
if errorlevel 1 (
    echo Installing Pillow...
    pip install Pillow
    if errorlevel 1 (
        echo WARNING: Failed to install Pillow. PDF creation may have limited functionality.
        echo   pip install Pillow
    )
)

REM Update PyInstaller and hooks to latest versions
echo Updating PyInstaller and hooks...
pip install -U pyinstaller pyinstaller-hooks-contrib

REM Build with reduced logging for cleaner output
python -m PyInstaller pallet_builder.spec --clean --noconfirm --distpath=. --log-level=WARN

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


