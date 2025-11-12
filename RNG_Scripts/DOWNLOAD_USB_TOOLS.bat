@echo off
REM Download USB Analysis Tools

echo ================================================
echo    DOWNLOAD USB ANALYSIS TOOLS
echo ================================================
echo.

set TOOLS_DIR=%~dp0USB_Tools
if not exist "%TOOLS_DIR%" mkdir "%TOOLS_DIR%"

echo Installing advanced USB analysis tools...
echo.

echo [1/2] Downloading USBDeview (NirSoft)...
echo ================================================
echo.
echo USBDeview shows:
echo - All USB devices ever connected
echo - Current connection speed
echo - USB version and port info
echo - Serial numbers and timestamps
echo.

curl -L -o "%TOOLS_DIR%\usbdeview.zip" "https://www.nirsoft.net/utils/usbdeview-x64.zip"

if exist "%TOOLS_DIR%\usbdeview.zip" (
    echo Extracting...
    tar -xf "%TOOLS_DIR%\usbdeview.zip" -C "%TOOLS_DIR%"
    del "%TOOLS_DIR%\usbdeview.zip"
    echo ✓ USBDeview installed to %TOOLS_DIR%
) else (
    echo ✗ Download failed
)

echo.
echo [2/2] Downloading USB Device Tree Viewer (Microsoft)...
echo ================================================
echo.
echo USB Device Tree Viewer shows:
echo - Complete USB topology
echo - Connection speeds per device
echo - USB descriptors
echo - Power consumption
echo.

echo Visit: https://learn.microsoft.com/en-us/windows-hardware/drivers/debugger/usbview
echo Download manually if automatic download fails.
echo.

REM Try to download from Microsoft
curl -L -o "%TOOLS_DIR%\UsbTreeView.exe" "https://ftdichip.com/wp-content/uploads/2021/11/UsbTreeView.zip" 2>nul

if exist "%TOOLS_DIR%\UsbTreeView.exe" (
    echo ✓ USB Tree Viewer installed
) else (
    echo ⚠ Auto-download not available
    echo   Visit Microsoft docs to download manually
)

echo.
echo ================================================
echo INSTALLATION COMPLETE
echo ================================================
echo.

if exist "%TOOLS_DIR%\USBDeview.exe" (
    echo Tools installed in: %TOOLS_DIR%
    echo.
    echo Run USBDeview.exe to see all USB port details!
    echo.

    set /p launch="Launch USBDeview now? (Y/N): "
    if /i "%launch%"=="Y" (
        start "" "%TOOLS_DIR%\USBDeview.exe"
    )
) else (
    echo Some tools failed to download.
    echo.
    echo Manual download links:
    echo.
    echo USBDeview:
    echo   https://www.nirsoft.net/utils/usb_devices_view.html
    echo.
    echo USB Device Tree Viewer:
    echo   https://learn.microsoft.com/en-us/windows-hardware/drivers/debugger/usbview
    echo.
)

echo.
pause
