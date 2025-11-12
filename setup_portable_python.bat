@echo off
REM Portable Python Setup for JPG Cataloger
REM Creates self-contained Python environment

setlocal enabledelayedexpansion

set PYTHON_VERSION=3.11.9
set INSTALL_DIR=%~dp0python_portable
set PYTHON_URL=https://www.python.org/ftp/python/%PYTHON_VERSION%/python-%PYTHON_VERSION%-embed-amd64.zip

echo ========================================
echo PORTABLE PYTHON INSTALLER
echo ========================================
echo.
echo Installing Python %PYTHON_VERSION% portable
echo Target: %INSTALL_DIR%
echo.

REM Create install directory
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"
cd /d "%INSTALL_DIR%"

REM Download Python embeddable
echo [1/5] Downloading Python embeddable...
curl -L -o python.zip "%PYTHON_URL%"
if errorlevel 1 (
    echo ERROR: Download failed
    pause
    exit /b 1
)

REM Extract
echo [2/5] Extracting Python...
tar -xf python.zip
del python.zip

REM Enable pip by uncommenting import site in pth file
echo [3/5] Enabling pip...
for %%f in (python*._pth) do (
    powershell -Command "(Get-Content '%%f') -replace '#import site', 'import site' | Set-Content '%%f'"
)

REM Download get-pip
echo [4/5] Installing pip...
curl -L -o get-pip.py https://bootstrap.pypa.io/get-pip.py
python.exe get-pip.py --no-warn-script-location
del get-pip.py

REM Install Pillow
echo [5/5] Installing Pillow...
python.exe -m pip install --no-warn-script-location Pillow

echo.
echo ========================================
echo INSTALLATION COMPLETE
echo ========================================
echo.
echo Python location: %INSTALL_DIR%
echo.
pause
