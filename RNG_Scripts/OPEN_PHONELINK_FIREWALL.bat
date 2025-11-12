@echo off
REM Open Firewall Ports for Phone Link Direct Transfer
REM Run as Administrator

echo ================================================
echo   PHONE LINK - FORCE LOCAL TRANSFER
echo   Opening Firewall Ports
echo ================================================
echo.

net session >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Must run as Administrator!
    echo Right-click this file and select "Run as Administrator"
    pause
    exit /b 1
)

echo Opening TCP ports 47000-48000 for Phone Link...
netsh advfirewall firewall add rule name="Phone Link Direct Transfer (TCP)" dir=in action=allow protocol=TCP localport=47000-48000

echo Opening UDP ports 47000-48000 for Phone Link...
netsh advfirewall firewall add rule name="Phone Link Direct Transfer (UDP)" dir=in action=allow protocol=UDP localport=47000-48000

echo.
echo ================================================
echo SUCCESS!
echo ================================================
echo.
echo Firewall ports opened for direct P2P transfer.
echo.
echo NEXT STEPS:
echo 1. Restart Phone Link app
echo 2. Reconnect your phone
echo 3. Try transferring again
echo.
echo It should now use local connection instead of cloud.
echo.
pause
