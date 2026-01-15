@echo off
REM Pallet Manager - Initial Developer Setup
REM Installs all tools needed for automatic updates and development

echo ========================================
echo Pallet Manager - Initial Setup
echo ========================================
echo.
echo This script will install the following tools:
echo - Chocolatey (package manager)
echo - Git (version control)
echo - Python 3.11+ (for building)
echo - Pip (Python package manager)
echo.
echo Administrator privileges are REQUIRED for installation.
echo.
set /p confirm="Do you want to continue? (y/N): "
if /i not "%confirm%"=="y" goto :cancel

echo.
echo Checking prerequisites...
echo.

REM Check if running as administrator
echo Checking administrator privileges...
net session >nul 2>&1
if %errorLevel% == 0 (
    echo ✓ Running with administrator privileges.
) else (
    echo ✗ ERROR: Administrator privileges required!
    echo Please right-click this script and select "Run as administrator"
    pause
    exit /b 1
)

echo.
echo Starting installation process...
echo.

echo ========================================
echo Step 1: Installing Chocolatey
echo ========================================
echo.

REM Check if Chocolatey is already installed
choco --version >nul 2>&1
if %errorLevel% == 0 (
    echo ✓ Chocolatey is already installed.
    goto :choco_done
)

echo Installing Chocolatey...

REM Try the installation
powershell -NoProfile -ExecutionPolicy Bypass -Command "& { [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; try { Invoke-WebRequest -Uri 'https://chocolatey.org/install.ps1' -OutFile '%TEMP%\choco-install.ps1' -UseBasicParsing } catch { Write-Host 'Failed to download Chocolatey installer'; exit 1 } }"

if errorlevel 1 (
    echo ✗ ERROR: Failed to download Chocolatey installer.
    goto :error
)

REM Run the installer
powershell -NoProfile -ExecutionPolicy Bypass -File "%TEMP%\choco-install.ps1"

if errorlevel 1 (
    echo ✗ ERROR: Failed to run Chocolatey installer.
    goto :error
)

REM Clean up temp file
del "%TEMP%\choco-install.ps1" 2>nul

REM Add Chocolatey to PATH
set "PATH=%PATH%;%ALLUSERSPROFILE%\chocolatey\bin"

REM Verify Chocolatey installation
choco --version >nul 2>&1
if errorlevel 1 (
    echo ✗ ERROR: Chocolatey installation failed verification.
    goto :error
)

echo ✓ Chocolatey installed successfully.
echo.

:choco_done

echo ========================================
echo Step 2: Installing Git
echo ========================================
echo.

REM Check if Git is already installed
git --version >nul 2>&1
if %errorLevel% == 0 (
    echo ✓ Git is already installed.
    goto :git_done
)

echo Installing Git via Chocolatey...

REM Install Git
choco install git -y --params="/GitAndUnixToolsOnPath /WindowsTerminal /NoShellIntegration"

if errorlevel 1 (
    echo ✗ ERROR: Failed to install Git via Chocolatey.
    echo.
    echo Trying alternative: Download Git directly...
    echo Please download and install Git manually from:
    echo https://git-scm.com/download/win
    echo.
    echo Then re-run this script.
    goto :error
)

REM Verify Git installation
git --version >nul 2>&1
if errorlevel 1 (
    echo ✗ ERROR: Git installation failed verification.
    goto :error
)

echo ✓ Git installed successfully.
echo.

:git_done

echo ========================================
echo Step 3: Installing Python
echo ========================================
echo.

REM Check if Python is already installed
python --version >nul 2>&1
if %errorLevel% == 0 (
    echo ✓ Python is already installed.
    goto :python_done
)

echo Installing Python via Chocolatey...

REM Install Python
choco install python311 -y

if errorlevel 1 (
    echo ✗ ERROR: Failed to install Python via Chocolatey.
    echo.
    echo Trying alternative: Download Python directly...
    echo Please download and install Python manually from:
    echo https://python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation.
    echo.
    echo Then re-run this script.
    goto :error
)

REM Add Python to PATH for current session
set "PATH=%PATH%;C:\Python311;C:\Python311\Scripts"

REM Verify Python installation
python --version >nul 2>&1
if errorlevel 1 (
    echo ✗ ERROR: Python installation failed verification.
    goto :error
)

REM Verify Pip
python -m pip --version >nul 2>&1
if errorlevel 1 (
    echo ✗ WARNING: Pip may not be available.
) else (
    echo ✓ Pip is available.
)

echo ✓ Python installed successfully.
echo.

:python_done

echo ========================================
echo Step 4: Verifying Installations
echo ========================================
echo.

set "verification_errors=0"

echo Checking Chocolatey...
choco --version >nul 2>&1
if errorlevel 1 (
    echo ✗ Chocolatey: NOT FOUND
    set /a "verification_errors+=1"
) else (
    echo ✓ Chocolatey: OK
)

echo Checking Git...
git --version >nul 2>&1
if errorlevel 1 (
    echo ✗ Git: NOT FOUND
    set /a "verification_errors+=1"
) else (
    echo ✓ Git: OK
)

echo Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ✗ Python: NOT FOUND
    set /a "verification_errors+=1"
) else (
    echo ✓ Python: OK
)

echo Checking Pip...
python -m pip --version >nul 2>&1
if errorlevel 1 (
    echo ✗ Pip: NOT FOUND
    set /a "verification_errors+=1"
) else (
    echo ✓ Pip: OK
)

echo.
if %verification_errors% gtr 0 (
    echo ⚠️  Some tools failed verification.
    echo Please restart Command Prompt and try again.
    echo If issues persist, install manually:
    echo - Git: https://git-scm.com/download/win
    echo - Python: https://python.org/downloads/
    goto :error
) else (
    echo ✓ All tools verified successfully!
)

echo.
echo ========================================
echo 🎉 Setup Complete!
echo ========================================
echo.
echo All developer tools have been installed successfully!
echo.
echo Next steps:
echo 1. Close and reopen Command Prompt/PowerShell
echo 2. Run 'scripts\update_from_github.bat' to get latest updates
echo 3. Or run 'scripts\install_all_windows.bat' to rebuild
echo.
echo Your development environment is now ready! 🚀
echo.
pause
goto :eof

:error
echo.
echo ========================================
echo ❌ Setup Failed!
echo ========================================
echo.
echo One or more installations failed.
echo Please check the error messages above and try again.
echo.
echo Manual installation options:
echo - Chocolatey: https://chocolatey.org/install
echo - Git: https://git-scm.com/download/win
echo - Python: https://python.org/downloads/
echo.
echo After manual installation, re-run this script.
echo.
pause
exit /b 1

:cancel
echo.
echo Setup cancelled by user.
echo No tools were installed.
echo.
pause
