@echo off
title Phone Link Traffic Monitor - Menu

:menu
cls
echo.
echo ================================================
echo    PHONE LINK TRAFFIC MONITOR
echo ================================================
echo.
echo Choose a monitoring method:
echo.
echo  [1] Quick Check - Instant analysis
echo      ^(Shows if transfer is local or cloud^)
echo.
echo  [2] Real-Time Monitor - Live bandwidth
echo      ^(PowerShell - Shows MB/s upload/download^)
echo.
echo  [3] Detailed Logger - Continuous logging
echo      ^(PowerShell - Logs to Desktop^)
echo.
echo  [4] Windows Resource Monitor
echo      ^(Built-in GUI tool^)
echo.
echo  [5] Wireshark Instructions
echo      ^(Advanced packet capture guide^)
echo.
echo  [6] Exit
echo.
echo ================================================
echo.

set /p choice="Enter your choice (1-6): "

if "%choice%"=="1" goto quick
if "%choice%"=="2" goto realtime
if "%choice%"=="3" goto logger
if "%choice%"=="4" goto resmon
if "%choice%"=="5" goto wireshark
if "%choice%"=="6" goto end

echo Invalid choice. Try again.
timeout /t 2 >nul
goto menu

:quick
cls
echo.
echo Running Quick Check...
echo.
call "%~dp0quick_check_phonelink.bat"
goto menu

:realtime
cls
echo.
echo Starting Real-Time Monitor...
echo.
echo NOTE: This requires PowerShell
echo Press Ctrl+C to stop monitoring
echo.
pause
powershell -ExecutionPolicy Bypass -File "%~dp0realtime_bandwidth_monitor.ps1"
goto menu

:logger
cls
echo.
echo Starting Traffic Logger...
echo.
echo NOTE: This requires PowerShell
echo Logs will be saved to your Desktop
echo Press Ctrl+C to stop logging
echo.
pause
powershell -ExecutionPolicy Bypass -File "%~dp0phonelink_traffic_logger.ps1"
goto menu

:resmon
cls
echo.
echo Opening Resource Monitor...
echo.
echo INSTRUCTIONS:
echo 1. Click the "Network" tab
echo 2. Look for "PhoneExperienceHost.exe" or "YourPhone.exe"
echo 3. Check "Processes with Network Activity"
echo 4. See live send/receive rates
echo.
pause
start resmon.exe
goto menu

:wireshark
cls
echo.
echo ================================================
echo    WIRESHARK SETUP GUIDE
echo ================================================
echo.
echo Full instructions are in:
echo %~dp0WIRESHARK_PHONELINK_GUIDE.txt
echo.
echo QUICK STEPS:
echo 1. Install Wireshark from wireshark.org
echo 2. Run as Administrator
echo 3. Select your network adapter
echo 4. Use filter: ip.addr == [YOUR_PHONE_IP]
echo.
echo Opening guide...
echo.
pause
notepad "%~dp0WIRESHARK_PHONELINK_GUIDE.txt"
goto menu

:end
echo.
echo Exiting...
timeout /t 1 >nul
exit /b 0
