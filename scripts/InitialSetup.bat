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
echo Administrator privileges may be required.
echo.
set /p confirm="Do you want to continue? (y/N): "
if /i not "%confirm%"=="y" goto :cancel

echo.
echo Starting installation process...
echo.

REM Check if running as administrator
net session >nul 2>&1
if %errorLevel% == 0 (
    echo Running with administrator privileges.
) else (
    echo WARNING: Not running as administrator.
    echo Some installations may fail. Please run as admin if possible.
    echo.
)

echo ========================================
echo Step 1: Installing Chocolatey
echo ========================================
echo.

REM Install Chocolatey
powershell -Command "Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))"

if errorlevel 1 (
    echo ERROR: Failed to install Chocolatey.
    goto :error
)

REM Refresh environment for Chocolatey
call refreshenv.cmd 2>nul
set "PATH=%PATH%;%ALLUSERSPROFILE%\chocolatey\bin"

echo Chocolatey installed successfully.
echo.

echo ========================================
echo Step 2: Installing Git
echo ========================================
echo.

REM Install Git via Chocolatey
choco install git -y --params="/GitAndUnixToolsOnPath /WindowsTerminal /NoShellIntegration"

if errorlevel 1 (
    echo ERROR: Failed to install Git.
    goto :error
)

echo Git installed successfully.
echo.

echo ========================================
echo Step 3: Installing Python
echo ========================================
echo.

REM Install Python via Chocolatey (latest stable version)
choco install python -y --params="/InstallDir:C:\Python311"

if errorlevel 1 (
    echo ERROR: Failed to install Python.
    goto :error
)

REM Refresh environment for Python
call refreshenv.cmd 2>nul

REM Add Python to PATH if not already there
python --version >nul 2>&1
if errorlevel 1 (
    echo Adding Python to PATH...
    setx PATH "%PATH%;C:\Python311;C:\Python311\Scripts" /M
    set "PATH=%PATH%;C:\Python311;C:\Python311\Scripts"
)

echo Python installed successfully.
echo.

echo ========================================
echo Step 4: Verifying Installations
echo ========================================
echo.

echo Checking Git...
git --version
if errorlevel 1 (
    echo WARNING: Git may not be in PATH. Try restarting command prompt.
) else (
    echo Git: OK
)

echo.
echo Checking Python...
python --version
if errorlevel 1 (
    echo WARNING: Python may not be in PATH. Try restarting command prompt.
) else (
    echo Python: OK
)

echo.
echo Checking Pip...
python -m pip --version
if errorlevel 1 (
    echo WARNING: Pip may not be available.
) else (
    echo Pip: OK
)

echo.
echo Checking Chocolatey...
choco --version
if errorlevel 1 (
    echo WARNING: Chocolatey may not be in PATH. Try restarting command prompt.
) else (
    echo Chocolatey: OK
)

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo All prerequisites have been installed.
echo.
echo Next steps:
echo 1. Close and reopen Command Prompt/PowerShell
echo 2. Run 'update_from_github.bat' to get latest updates
echo 3. Or run 'scripts\install_all_windows.bat' to rebuild
echo.
echo If any tools show warnings above, restart your terminal and try again.
echo.
pause
goto :eof

:error
echo.
echo ========================================
echo Setup Failed!
echo ========================================
echo.
echo One or more installations failed.
echo Please check the error messages above and try again.
echo.
echo You can also install tools manually:
echo - Git: https://git-scm.com/download/win
echo - Python: https://python.org/downloads/
echo - Chocolatey: https://chocolatey.org/install
echo.
pause
exit /b 1

:cancel
echo.
echo Setup cancelled by user.
echo.
pause
