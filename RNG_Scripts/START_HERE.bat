@echo off
title RNG Scripts - Main Menu

:menu
cls
echo.
echo ================================================
echo        RNG SCRIPTS - MAIN MENU
echo    Network ^& USB Diagnostic Tools
echo ================================================
echo.
echo What do you want to do?
echo.
echo  [1] Phone Link Monitoring
echo      Check if transfer is local or cloud
echo.
echo  [2] USB Port Analysis
echo      Find fastest USB ports and controllers
echo.
echo  [3] Read Documentation
echo      README and guides
echo.
echo  [4] Exit
echo.
echo ================================================
echo.

set /p choice="Enter your choice (1-4): "

if "%choice%"=="1" goto phonelink
if "%choice%"=="2" goto usb
if "%choice%"=="3" goto docs
if "%choice%"=="4" goto end

echo Invalid choice. Try again.
timeout /t 2 >nul
goto menu

:phonelink
cls
echo.
echo Starting Phone Link Monitoring Menu...
echo.
call "%~dp0MONITOR_PHONELINK_MENU.bat"
goto menu

:usb
cls
echo.
echo Starting USB Analyzer Menu...
echo.
call "%~dp0USB_ANALYZER_MENU.bat"
goto menu

:docs
cls
echo.
echo ================================================
echo    DOCUMENTATION
echo ================================================
echo.
echo Opening README...
echo.
notepad "%~dp0README.txt"

echo.
echo Other documentation available:
echo.
echo  • USB_SITUATION_EXPLAINED.txt
echo  • USB_ANALYSIS_RESULTS.txt
echo  • FIX_PHONELINK_LOCAL_TRANSFER.txt
echo  • WIRESHARK_PHONELINK_GUIDE.txt
echo.
echo Open these files with Notepad when needed.
echo.
pause
goto menu

:end
echo.
echo Exiting...
timeout /t 1 >nul
exit /b 0
