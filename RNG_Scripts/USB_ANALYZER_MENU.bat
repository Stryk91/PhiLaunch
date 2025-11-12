@echo off
title USB Port Analyzer - Menu

:menu
cls
echo.
echo ================================================
echo        USB PORT ANALYZER SUITE
echo ================================================
echo.
echo Choose an analysis method:
echo.
echo  [1] Quick Check
echo      ^(Basic info, opens Device Manager^)
echo.
echo  [2] Full Architecture Report
echo      ^(PowerShell - Complete USB controller analysis^)
echo.
echo  [3] Real Speed Test
echo      ^(PowerShell - Test actual transfer speeds^)
echo.
echo  [4] Download Advanced Tools
echo      ^(USBDeview, USB Tree Viewer^)
echo.
echo  [5] Open Device Manager
echo      ^(Manual USB inspection^)
echo.
echo  [6] Exit
echo.
echo ================================================
echo.

set /p choice="Enter your choice (1-6): "

if "%choice%"=="1" goto quick
if "%choice%"=="2" goto full
if "%choice%"=="3" goto speedtest
if "%choice%"=="4" goto download
if "%choice%"=="5" goto devmgr
if "%choice%"=="6" goto end

echo Invalid choice. Try again.
timeout /t 2 >nul
goto menu

:quick
cls
call "%~dp0USB_QUICK_CHECK.bat"
goto menu

:full
cls
echo.
echo Running Full USB Architecture Report...
echo.
pause
powershell -ExecutionPolicy Bypass -File "%~dp0USB_PORT_ANALYZER.ps1"
goto menu

:speedtest
cls
echo.
echo ================================================
echo   USB SPEED TEST
echo ================================================
echo.
echo This will test actual transfer speeds to a USB drive.
echo You need a USB drive connected to test.
echo.
pause
powershell -ExecutionPolicy Bypass -File "%~dp0USB_SPEED_TEST.ps1"
goto menu

:download
cls
call "%~dp0DOWNLOAD_USB_TOOLS.bat"
goto menu

:devmgr
cls
echo.
echo Opening Device Manager...
echo.
echo Navigate to:
echo   "Universal Serial Bus controllers"
echo.
echo Look for:
echo   - "USB 3.x Extensible Host Controller" = USB 3.0+
echo   - "USB 2.0 Enhanced Host Controller" = USB 2.0
echo.
pause
devmgmt.msc
goto menu

:end
echo.
echo Exiting...
timeout /t 1 >nul
exit /b 0
