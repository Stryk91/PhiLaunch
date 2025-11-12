@echo off
REM Fix ASMedia USB 3.1 Performance Issues

title ASMedia USB Fix Tool

:menu
cls
echo.
echo ================================================
echo    ASMEDIA USB 3.1 PERFORMANCE FIX
echo ================================================
echo.
echo Your ASMedia controller claims 10 Gbps but tests
echo show it's SLOWER than Intel USB 3.0. This is a
echo common ASMedia problem.
echo.
echo ================================================
echo CHOOSE A FIX:
echo ================================================
echo.
echo  [1] Check Driver Version
echo      See if drivers are outdated
echo.
echo  [2] Find Motherboard Info
echo      Identify your board for driver downloads
echo.
echo  [3] Disable UASP Mode
echo      Force BOT mode (sometimes faster)
echo.
echo  [4] Open Device Manager
echo      Manual driver update
echo.
echo  [5] Check BIOS Info
echo      See current BIOS version
echo.
echo  [6] ASMedia Known Issues Guide
echo      Common problems and solutions
echo.
echo  [7] Exit
echo.
echo ================================================
echo.

set /p choice="Enter your choice (1-7): "

if "%choice%"=="1" goto checkdriver
if "%choice%"=="2" goto motherboard
if "%choice%"=="3" goto disableuasp
if "%choice%"=="4" goto devmgr
if "%choice%"=="5" goto biosinfo
if "%choice%"=="6" goto guide
if "%choice%"=="7" goto end

echo Invalid choice.
timeout /t 2 >nul
goto menu

:checkdriver
cls
echo.
echo ================================================
echo    ASMEDIA DRIVER CHECK
echo ================================================
echo.

echo Checking ASMedia controller driver...
echo.

powershell -Command "Get-PnpDevice | Where-Object { $_.FriendlyName -like '*ASMedia*USB*' } | ForEach-Object { $props = Get-PnpDeviceProperty -InstanceId $_.InstanceId; Write-Host \"Device: $($_.FriendlyName)\"; Write-Host \"Status: $($_.Status)\"; $driverVer = $props | Where-Object { $_.KeyName -eq 'DEVPKEY_Device_DriverVersion' }; if ($driverVer) { Write-Host \"Driver Version: $($driverVer.Data)\" }; $driverDate = $props | Where-Object { $_.KeyName -eq 'DEVPKEY_Device_DriverDate' }; if ($driverDate) { $date = [DateTime]$driverDate.Data; Write-Host \"Driver Date: $($date.ToString('yyyy-MM-dd'))\" ; $age = (Get-Date) - $date; Write-Host \"Age: $([math]::Round($age.TotalDays)) days old\"; if ($age.TotalDays -gt 365) { Write-Host \"WARNING: Driver over 1 year old!\" -ForegroundColor Red } }; Write-Host \"\" }"

echo.
echo ================================================
echo.
echo If driver is over 1 year old, you should update it.
echo.
echo To update:
echo   1. Find your motherboard model (option 2)
echo   2. Go to manufacturer website
echo      (ASUS, MSI, Gigabyte, ASRock, etc.)
echo   3. Download "USB 3.1 Driver" or "ASMedia USB Driver"
echo   4. Install and reboot
echo.
pause
goto menu

:motherboard
cls
echo.
echo ================================================
echo    MOTHERBOARD INFORMATION
echo ================================================
echo.

echo System Information:
echo.
wmic baseboard get manufacturer,product,version
echo.

echo Computer Model:
echo.
wmic computersystem get manufacturer,model
echo.

echo BIOS Version:
echo.
wmic bios get smbiosbiosversion,releasedate
echo.

echo ================================================
echo.
echo Take note of your motherboard model above.
echo.
echo Then visit your manufacturer website:
echo.
echo   ASUS:      https://www.asus.com/support/
echo   MSI:       https://www.msi.com/support
echo   Gigabyte:  https://www.gigabyte.com/Support
echo   ASRock:    https://www.asrock.com/support/
echo.
echo Search for your motherboard model and download:
echo   - Latest USB 3.1 / ASMedia drivers
echo   - Latest BIOS/UEFI (if drivers don't help)
echo.
pause
goto menu

:disableuasp
cls
echo.
echo ================================================
echo    DISABLE UASP MODE
echo ================================================
echo.
echo UASP (USB Attached SCSI Protocol) sometimes
echo causes performance issues on ASMedia controllers.
echo.
echo This will force your device to use BOT (Bulk-Only
echo Transport) mode instead, which may be faster.
echo.
echo WARNING: This requires uninstalling a device!
echo It will reinstall automatically when you replug.
echo.
echo ================================================
echo.

set /p confirm="Continue? (Y/N): "
if /i not "%confirm%"=="Y" goto menu

echo.
echo Opening Device Manager...
echo.
echo Steps:
echo   1. Expand "Universal Serial Bus controllers"
echo   2. Find "USB Attached SCSI (UAS) Mass Storage Device"
echo   3. Right-click it
echo   4. Select "Uninstall device"
echo   5. Check "Delete the driver software" if option appears
echo   6. Click OK
echo   7. Unplug and replug your device
echo   8. It will reinstall in BOT mode
echo.
pause

devmgmt.msc

echo.
echo After uninstalling and replugging, test speed again
echo with Samsung Magician or CrystalDiskMark.
echo.
pause
goto menu

:devmgr
cls
echo.
echo Opening Device Manager...
echo.
echo To manually update ASMedia driver:
echo.
echo   1. Expand "Universal Serial Bus controllers"
echo   2. Find "ASMedia USB3.1 eXtensible Host Controller"
echo   3. Right-click it
echo   4. Select "Update driver"
echo   5. Choose "Browse my computer for drivers"
echo   6. Point to downloaded driver folder
echo.
pause

devmgmt.msc

pause
goto menu

:biosinfo
cls
echo.
echo ================================================
echo    BIOS/UEFI INFORMATION
echo ================================================
echo.

systeminfo | findstr /i "bios"

echo.
echo ================================================
echo.
echo Check your motherboard manufacturer website for
echo BIOS updates. Newer BIOS versions often include:
echo.
echo   - Improved USB controller firmware
echo   - Better power delivery
echo   - USB compatibility fixes
echo.
echo IMPORTANT: BIOS updates can be risky!
echo Only update if you're comfortable with the process.
echo.
pause
goto menu

:guide
cls
echo.
echo ================================================
echo    ASMEDIA USB KNOWN ISSUES GUIDE
echo ================================================
echo.
echo COMMON PROBLEMS WITH ASMEDIA USB 3.1:
echo ================================================
echo.
echo 1. LOWER REAL-WORLD SPEED THAN INTEL USB 3.0
echo    - ASMedia claims 10 Gbps (1,250 MB/s)
echo    - Real performance often 200-400 MB/s
echo    - Intel USB 3.0: 400-550 MB/s (more reliable)
echo.
echo    FIX: Update drivers or just use Intel ports
echo.
echo 2. DEVICE NOT RECOGNIZED / KEEPS DISCONNECTING
echo    - Power delivery issues
echo    - Firmware bugs
echo.
echo    FIX: Update BIOS, use different port
echo.
echo 3. UASP MODE CAUSES SLOW SPEEDS
echo    - Some devices perform worse with UASP
echo    - Especially external SSDs
echo.
echo    FIX: Disable UASP (option 3)
echo.
echo 4. DRIVER CONFLICTS WITH INTEL CHIPSET
echo    - ASMedia is add-on controller
echo    - May conflict with Intel xHCI
echo.
echo    FIX: Update both drivers, check BIOS settings
echo.
echo 5. OLD FIRMWARE IN CONTROLLER CHIP
echo    - ASMedia 1042/1142/1143/1242 have known bugs
echo    - Can only be fixed via BIOS update
echo.
echo    FIX: Update motherboard BIOS/UEFI
echo.
echo ================================================
echo RECOMMENDATION FOR YOUR SITUATION:
echo ================================================
echo.
echo Since Samsung Magician showed ASMedia is SLOWER:
echo.
echo   → IGNORE ASMedia USB 3.1 ports
echo   → USE Intel USB 3.0 ports instead
echo   → Real performance matters more than specs
echo.
echo Intel USB 3.0:     Reliable 400-550 MB/s ✓
echo ASMedia USB 3.1:   Broken 200-300 MB/s ✗
echo.
echo Your phone is probably already on the BEST port!
echo.
echo ================================================
echo.
pause
goto menu

:end
cls
echo.
echo Exiting...
timeout /t 1 >nul
exit /b 0
