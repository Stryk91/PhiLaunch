@echo off
REM INSTANT PHONE LINK CONNECTION CHECK
REM Run this while the 50GB file is transferring

echo ================================================
echo   PHONE LINK - QUICK CONNECTION CHECK
echo ================================================
echo.

echo [1/4] Finding Phone Link process...
for /f "tokens=2" %%a in ('tasklist ^| findstr /i "PhoneExperienceHost"') do set PID=%%a
if "%PID%"=="" (
    for /f "tokens=2" %%a in ('tasklist ^| findstr /i "YourPhone"') do set PID=%%a
)

if "%PID%"=="" (
    echo ERROR: Phone Link is not running!
    echo Start the file transfer first, then run this script.
    pause
    exit /b 1
)

echo Found Phone Link (PID: %PID%)
echo.

echo [2/4] Active connections:
echo.
netstat -ano | findstr %PID% | findstr ESTABLISHED
echo.

echo [3/4] Remote IPs (where data is going):
echo.
for /f "tokens=3" %%a in ('netstat -ano ^| findstr %PID% ^| findstr ESTABLISHED') do (
    echo %%a
) | findstr /v "127.0.0.1 [::1]" | sort | uniq
echo.

echo [4/4] Checking if it's local or cloud transfer...
echo.
netstat -ano | findstr %PID% | findstr ESTABLISHED | findstr "192.168"
if %errorlevel%==0 (
    echo ^=^> LOCAL TRANSFER DETECTED!
    echo File is being sent directly over your WiFi network.
    echo This is FAST - no internet needed.
) else (
    netstat -ano | findstr %PID% | findstr ESTABLISHED | findstr /v "192.168 127.0.0"
    if %errorlevel%==0 (
        echo ^=^> CLOUD RELAY DETECTED!
        echo File is going through Microsoft servers.
        echo This is SLOWER - uses your internet connection.
    ) else (
        echo ^=^> UNKNOWN - No established connections found yet.
        echo Wait for the transfer to start, then run this again.
    )
)

echo.
echo ================================================
echo DETAILED ANALYSIS
echo ================================================
echo.
echo Full connection list for Phone Link (PID: %PID%):
echo.
netstat -ano | findstr %PID%
echo.

echo ================================================
echo.
pause
