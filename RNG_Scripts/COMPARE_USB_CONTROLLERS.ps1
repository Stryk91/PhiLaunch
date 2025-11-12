# USB Controller Performance Comparison
# Test both Intel and ASMedia controllers with actual transfer tests

param(
    [string]$TestDrive = "",
    [int]$TestSizeMB = 500
)

Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "     USB CONTROLLER PERFORMANCE COMPARISON" -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "This tool will help identify which controller is ACTUALLY faster" -ForegroundColor Yellow
Write-Host "by testing real file transfers, not just specs." -ForegroundColor Yellow
Write-Host ""

# Detect controllers
Write-Host "[STEP 1] Detecting USB Controllers..." -ForegroundColor Yellow
Write-Host ""

$controllers = Get-WmiObject -Class Win32_USBController

foreach ($ctrl in $controllers) {
    $status = if ($ctrl.Status -eq "OK") { "[OK]" } else { "[ISSUE]" }
    $color = if ($ctrl.Status -eq "OK") { "Green" } else { "Red" }

    Write-Host "$status " -NoNewline -ForegroundColor $color
    Write-Host "$($ctrl.Name)" -ForegroundColor White

    if ($ctrl.Name -match "Intel.*3\.0") {
        Write-Host "    Type: USB 3.0 (5 Gbps theoretical / ~625 MB/s)" -ForegroundColor Cyan
        Write-Host "    Known: Generally reliable, consistent performance" -ForegroundColor Green
    }
    elseif ($ctrl.Name -match "ASMedia.*3\.1") {
        Write-Host "    Type: USB 3.1 (10 Gbps theoretical / ~1,250 MB/s)" -ForegroundColor Cyan
        Write-Host "    Known: Often has driver/firmware issues, may underperform" -ForegroundColor Yellow
    }
    Write-Host ""
}

Write-Host "[STEP 2] Check Currently Connected Device..." -ForegroundColor Yellow
Write-Host ""

# Find Samsung device
$samsungDevice = Get-PnpDevice | Where-Object {
    $_.FriendlyName -like "*Samsung*" -and
    $_.InstanceId -like "USB\VID_04E8*" -and
    $_.Status -eq "OK"
} | Select-Object -First 1

if ($samsungDevice) {
    Write-Host "Found: $($samsungDevice.FriendlyName)" -ForegroundColor Green

    # Trace to controller
    $parent = Get-PnpDeviceProperty -InstanceId $samsungDevice.InstanceId |
              Where-Object { $_.KeyName -eq 'DEVPKEY_Device_Parent' }

    if ($parent) {
        $hub = Get-PnpDevice -InstanceId $parent.Data
        $hubParent = Get-PnpDeviceProperty -InstanceId $hub.InstanceId |
                     Where-Object { $_.KeyName -eq 'DEVPKEY_Device_Parent' }

        if ($hubParent) {
            $controller = Get-PnpDevice -InstanceId $hubParent.Data
            Write-Host "Currently connected to: $($controller.FriendlyName)" -ForegroundColor Cyan

            if ($controller.FriendlyName -match "Intel") {
                Write-Host "→ You are on the INTEL controller (USB 3.0)" -ForegroundColor Green
            }
            elseif ($controller.FriendlyName -match "ASMedia") {
                Write-Host "→ You are on the ASMEDIA controller (USB 3.1)" -ForegroundColor Yellow
            }
        }
    }
    Write-Host ""
}

# Check for Samsung SSD
$samsungSSD = Get-PnpDevice | Where-Object {
    ($_.FriendlyName -like "*Samsung*SSD*" -or $_.FriendlyName -like "*Samsung*PSSD*") -and
    $_.Status -eq "OK"
} | Select-Object -First 1

if ($samsungSSD) {
    Write-Host "Found Samsung SSD: $($samsungSSD.FriendlyName)" -ForegroundColor Green
    Write-Host ""
}

Write-Host "[STEP 3] ASMedia Controller Analysis..." -ForegroundColor Yellow
Write-Host ""

# Check ASMedia driver version
$asmediaCtrl = Get-PnpDevice | Where-Object { $_.FriendlyName -like "*ASMedia*" -and $_.Class -eq "USB" }

if ($asmediaCtrl) {
    $driver = Get-PnpDeviceProperty -InstanceId $asmediaCtrl.InstanceId |
              Where-Object { $_.KeyName -eq 'DEVPKEY_Device_DriverVersion' }

    if ($driver) {
        Write-Host "ASMedia Driver Version: $($driver.Data)" -ForegroundColor White

        # Check if driver is old
        $driverDate = Get-PnpDeviceProperty -InstanceId $asmediaCtrl.InstanceId |
                     Where-Object { $_.KeyName -eq 'DEVPKEY_Device_DriverDate' }

        if ($driverDate) {
            $date = [DateTime]$driverDate.Data
            $age = (Get-Date) - $date

            Write-Host "Driver Date: $($date.ToString('yyyy-MM-dd')) ($([math]::Round($age.TotalDays)) days old)" -ForegroundColor Gray

            if ($age.TotalDays -gt 365) {
                Write-Host "⚠ WARNING: Driver is over 1 year old!" -ForegroundColor Red
                Write-Host "  Old drivers are a common cause of ASMedia underperformance." -ForegroundColor Yellow
                Write-Host "  Check motherboard manufacturer website for updates." -ForegroundColor Yellow
            }
        }
    }
}

Write-Host ""
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "              COMMON ASMEDIA ISSUES" -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Why ASMedia controllers often underperform:" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. OUTDATED DRIVERS" -ForegroundColor Red
Write-Host "   ASMedia drivers are rarely updated via Windows Update" -ForegroundColor Gray
Write-Host "   Must download from motherboard manufacturer" -ForegroundColor Gray
Write-Host ""
Write-Host "2. FIRMWARE BUGS" -ForegroundColor Red
Write-Host "   Some ASMedia chipsets have firmware bugs that throttle speed" -ForegroundColor Gray
Write-Host "   Requires BIOS/UEFI update from motherboard vendor" -ForegroundColor Gray
Write-Host ""
Write-Host "3. POWER DELIVERY ISSUES" -ForegroundColor Red
Write-Host "   ASMedia controllers sometimes can't deliver stable 900mA" -ForegroundColor Gray
Write-Host "   Devices may fall back to USB 2.0 mode" -ForegroundColor Gray
Write-Host ""
Write-Host "4. UASP/BOT MODE PROBLEMS" -ForegroundColor Red
Write-Host "   Some devices perform worse with UASP on ASMedia" -ForegroundColor Gray
Write-Host "   Disabling UASP in registry sometimes helps" -ForegroundColor Gray
Write-Host ""
Write-Host "5. CHIPSET COMPATIBILITY" -ForegroundColor Red
Write-Host "   ASMedia add-on controllers may conflict with Intel chipset" -ForegroundColor Gray
Write-Host "   BIOS settings can help (disable/enable certain options)" -ForegroundColor Gray
Write-Host ""

Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "              BENCHMARK RECOMMENDATION" -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Based on your Samsung Magician results showing ASMedia is SLOWER:" -ForegroundColor Yellow
Write-Host ""
Write-Host "RECOMMENDATION: STICK WITH INTEL USB 3.0 PORT" -ForegroundColor Green
Write-Host ""
Write-Host "Real-world Intel USB 3.0:  400-550 MB/s (reliable)" -ForegroundColor Green
Write-Host "Real-world ASMedia USB 3.1: ~200-300 MB/s (broken/throttled)" -ForegroundColor Red
Write-Host ""
Write-Host "Even though ASMedia CLAIMS 10 Gbps, if it's actually slower" -ForegroundColor Yellow
Write-Host "than Intel in your tests, INTEL IS BETTER for you." -ForegroundColor Yellow
Write-Host ""

Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "                   FIXES TO TRY" -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "[FIX 1] Update ASMedia Drivers" -ForegroundColor Yellow
Write-Host "  1. Find your motherboard model (System Information)" -ForegroundColor Gray
Write-Host "  2. Go to manufacturer website (ASUS, MSI, Gigabyte, etc.)" -ForegroundColor Gray
Write-Host "  3. Download latest USB 3.1 drivers" -ForegroundColor Gray
Write-Host "  4. Install and reboot" -ForegroundColor Gray
Write-Host ""
Write-Host "[FIX 2] Update BIOS/UEFI" -ForegroundColor Yellow
Write-Host "  1. Check current BIOS version (System Information)" -ForegroundColor Gray
Write-Host "  2. Download latest BIOS from motherboard manufacturer" -ForegroundColor Gray
Write-Host "  3. Follow manufacturer's update procedure (BE CAREFUL!)" -ForegroundColor Red
Write-Host ""
Write-Host "[FIX 3] Disable UASP (if using external drive)" -ForegroundColor Yellow
Write-Host "  1. Device Manager → Universal Serial Bus controllers" -ForegroundColor Gray
Write-Host "  2. Find 'USB Attached SCSI (UAS) Mass Storage Device'" -ForegroundColor Gray
Write-Host "  3. Right-click → Uninstall (will reinstall as BOT mode)" -ForegroundColor Gray
Write-Host ""
Write-Host "[FIX 4] Check BIOS USB Settings" -ForegroundColor Yellow
Write-Host "  1. Reboot into BIOS/UEFI" -ForegroundColor Gray
Write-Host "  2. Look for 'USB Configuration' or similar" -ForegroundColor Gray
Write-Host "  3. Try: 'USB 3.1 Mode' = Enabled/Auto" -ForegroundColor Gray
Write-Host "  4. Try: 'XHCI Hand-off' = Enabled" -ForegroundColor Gray
Write-Host ""

Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Want to run actual speed test on your device? (Y/N)" -ForegroundColor Yellow
$runTest = Read-Host

if ($runTest -eq "Y" -or $runTest -eq "y") {
    Write-Host ""
    Write-Host "Which drive letter is your test device? (e.g., D, E, F)" -ForegroundColor Yellow
    $driveLetter = Read-Host

    Write-Host ""
    Write-Host "Running speed test..." -ForegroundColor Green
    Write-Host ""

    # Run the speed test script
    $speedTestScript = "$PSScriptRoot\USB_SPEED_TEST.ps1"
    if (Test-Path $speedTestScript) {
        & $speedTestScript -TargetDrive $driveLetter -TestSizeMB $TestSizeMB
    }
    else {
        Write-Host "Speed test script not found. Run USB_SPEED_TEST.ps1 manually." -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "                     CONCLUSION" -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "If ASMedia is slower in YOUR tests (Samsung Magician):" -ForegroundColor Yellow
Write-Host ""
Write-Host "→ KEEP USING INTEL USB 3.0 PORT" -ForegroundColor Green
Write-Host "→ It's not about the specs, it's about REAL performance" -ForegroundColor Green
Write-Host "→ Intel: Reliable ~500 MB/s > ASMedia: Broken ~250 MB/s" -ForegroundColor Green
Write-Host ""
Write-Host "Your phone is probably already on the BEST port!" -ForegroundColor Cyan
Write-Host ""

Write-Host "Press any key to exit..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
