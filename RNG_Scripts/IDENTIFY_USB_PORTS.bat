@echo off
REM USB Port Identifier - Find which physical port is which controller

echo ================================================
echo    USB PORT IDENTIFIER
echo ================================================
echo.
echo This tool helps you find which physical USB port
echo is connected to which controller.
echo.
echo ================================================
echo YOUR CONTROLLERS:
echo ================================================
echo.
echo [1] Intel USB 3.0 - 5 Gbps (SLOW)
echo     Color: Usually BLUE ports
echo     Label: May say "USB 3.0" or "SS"
echo.
echo [2] ASMedia USB 3.1 - 10 Gbps (FAST!)
echo     Color: Usually RED or CYAN ports
echo     Label: May say "USB 3.1" or "10G" or "SS+"
echo.
echo ================================================
echo IDENTIFICATION PROCESS:
echo ================================================
echo.
echo 1. This will open Device Manager
echo 2. Expand "Universal Serial Bus controllers"
echo 3. Unplug your phone/device
echo 4. Plug it into DIFFERENT USB ports on your PC
echo 5. Watch which controller lights up each time:
echo    - "Intel" = USB 3.0 (slower)
echo    - "ASMedia" = USB 3.1 (faster) ✓ REMEMBER THIS ONE
echo.
echo 6. Mark the ASMedia port with tape or sticker
echo 7. Always use that port for large file transfers!
echo.
pause

echo Opening Device Manager...
devmgmt.msc

echo.
echo ================================================
echo TIP: Physical Location Hints
echo ================================================
echo.
echo ASMedia USB 3.1 ports are usually:
echo.
echo  • On the MOTHERBOARD I/O (back of PC)
echo  • Color: RED, CYAN, or TURQUOISE
echo  • Near the network port
echo  • Labeled "USB 3.1", "10G", or "SS+"
echo  • Usually only 1-2 ports
echo.
echo Intel USB 3.0 ports are usually:
echo  • Also on motherboard I/O (back of PC)
echo  • Color: BLUE
echo  • More common (4-6 ports)
echo  • Labeled "USB 3.0" or "SS"
echo.
echo Front panel USB ports are usually:
echo  • Connected to motherboard headers
echo  • Often USB 2.0 or USB 3.0
echo  • Rarely USB 3.1 (unless high-end case)
echo.
echo ================================================
echo.

echo Do you want to see currently connected devices? (Y/N)
set /p show_devices=

if /i "%show_devices%"=="Y" (
    echo.
    echo Current USB Devices:
    echo ================================================
    powershell -Command "Get-PnpDevice | Where-Object { $_.InstanceId -like 'USB\VID*' -and $_.FriendlyName -notlike '*Hub*' -and $_.FriendlyName -notlike '*Controller*' } | Select-Object -First 10 FriendlyName, Status | Format-Table -AutoSize"
    echo.
)

echo.
echo ================================================
echo NEXT STEPS:
echo ================================================
echo.
echo 1. Find the ASMedia USB 3.1 port (RED/CYAN color)
echo 2. Mark it with tape or sticker
echo 3. Plug your Samsung phone into THAT port
echo 4. Use File Transfer mode
echo 5. Get 10 Gbps speeds!
echo.
pause
