@echo off
REM Quick Phone Link Traffic Monitor
REM Run this while transferring the file

echo ================================================
echo   PHONE LINK TRAFFIC MONITOR
echo ================================================
echo.
echo Starting Resource Monitor...
echo Look for "PhoneExperienceHost.exe" or "YourPhone.exe"
echo.
pause

REM Open Resource Monitor focused on Network tab
resmon.exe

echo.
echo ================================================
echo ALTERNATIVE: Netstat Monitor
echo ================================================
echo.
echo Press any key to also monitor connections...
pause

:loop
cls
echo ================================================
echo   ACTIVE PHONE LINK CONNECTIONS
echo   Press Ctrl+C to stop
echo ================================================
echo.
date /t
time /t
echo.

REM Show connections for Phone Link processes
netstat -ano | findstr /i "PhoneExperienceHost YourPhone"

echo.
echo Checking IP connections...
netstat -n | findstr ESTABLISHED | findstr /v "127.0.0.1 ::1"

timeout /t 2 >nul
goto loop
