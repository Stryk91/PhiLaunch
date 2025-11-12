@echo off
REM Quick USB Port Check - Simple Version

echo ================================================
echo    USB PORT QUICK CHECK
echo ================================================
echo.

echo [1/3] USB Controllers:
echo ================================================
wmic path Win32_USBController get Name,Status,Protocol
echo.

echo [2/3] USB Devices Connected:
echo ================================================
wmic path Win32_PnPEntity where "PNPClass='USB'" get Name,Status
echo.

echo [3/3] USB Hub Info:
echo ================================================
wmic path Win32_USBHub get Name,DeviceID
echo.

echo ================================================
echo THEORETICAL USB SPEEDS:
echo ================================================
echo.
echo USB 1.0 Low Speed:     1.5 Mbps   (~187 KB/s)
echo USB 1.1 Full Speed:    12 Mbps    (~1.5 MB/s)
echo USB 2.0 High Speed:    480 Mbps   (~60 MB/s)
echo USB 3.0 SuperSpeed:    5 Gbps     (~625 MB/s)
echo USB 3.1 Gen 2:         10 Gbps    (~1,250 MB/s)
echo USB 3.2 Gen 2x2:       20 Gbps    (~2,500 MB/s)
echo USB4 / Thunderbolt:    40 Gbps    (~5,000 MB/s)
echo.
echo ================================================
echo.

echo Opening Device Manager USB section...
echo Check "Universal Serial Bus controllers" for details
echo.
pause

REM Open Device Manager to USB section
devmgmt.msc

echo.
pause
