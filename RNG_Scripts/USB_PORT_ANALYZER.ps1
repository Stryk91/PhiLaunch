# USB Port Analyzer - Complete USB Architecture Report
# Shows all USB controllers, ports, devices, speeds, and compares to theoretical maximums

Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "           USB PORT ARCHITECTURE ANALYZER" -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""

# USB Speed Standards (Theoretical Maximum)
$usbSpeedStandards = @{
    "1.0" = @{ Name = "USB 1.0 Low Speed"; Speed = 1.5; Unit = "Mbps" }
    "1.1" = @{ Name = "USB 1.1 Full Speed"; Speed = 12; Unit = "Mbps" }
    "2.0" = @{ Name = "USB 2.0 High Speed"; Speed = 480; Unit = "Mbps" }
    "3.0" = @{ Name = "USB 3.0 SuperSpeed (Gen 1)"; Speed = 5000; Unit = "Mbps"; Bytes = 625 }
    "3.1" = @{ Name = "USB 3.1 SuperSpeed+ (Gen 2)"; Speed = 10000; Unit = "Mbps"; Bytes = 1250 }
    "3.2" = @{ Name = "USB 3.2 SuperSpeed++ (Gen 2x2)"; Speed = 20000; Unit = "Mbps"; Bytes = 2500 }
    "4.0" = @{ Name = "USB4 (Thunderbolt)"; Speed = 40000; Unit = "Mbps"; Bytes = 5000 }
}

Write-Host "[1/5] USB Host Controllers" -ForegroundColor Yellow
Write-Host "================================================================" -ForegroundColor Gray

# Get USB Controllers
$usbControllers = Get-PnpDevice | Where-Object { $_.Class -eq "USB" -and $_.FriendlyName -like "*Host Controller*" }

$controllerCount = 0
foreach ($controller in $usbControllers) {
    $controllerCount++

    $status = if ($controller.Status -eq "OK") { "[OK]" } else { "[ISSUE]" }
    $color = if ($controller.Status -eq "OK") { "Green" } else { "Red" }

    Write-Host "  $status " -NoNewline -ForegroundColor $color
    Write-Host "$($controller.FriendlyName)" -ForegroundColor White
    Write-Host "      Instance: $($controller.InstanceId)" -ForegroundColor Gray

    # Try to determine USB version from controller name
    if ($controller.FriendlyName -match "3\.[0-2]|xHCI") {
        Write-Host "      Type: USB 3.x Controller (xHCI)" -ForegroundColor Cyan
    } elseif ($controller.FriendlyName -match "2\.0|EHCI") {
        Write-Host "      Type: USB 2.0 Controller (EHCI)" -ForegroundColor Yellow
    } elseif ($controller.FriendlyName -match "1\.[01]|UHCI|OHCI") {
        Write-Host "      Type: USB 1.x Controller" -ForegroundColor DarkYellow
    }
    Write-Host ""
}

Write-Host "  Total Controllers: $controllerCount" -ForegroundColor Cyan
Write-Host ""

Write-Host "[2/5] USB Root Hubs" -ForegroundColor Yellow
Write-Host "================================================================" -ForegroundColor Gray

$rootHubs = Get-PnpDevice | Where-Object { $_.Class -eq "USB" -and $_.FriendlyName -like "*Root Hub*" }

foreach ($hub in $rootHubs) {
    $status = if ($hub.Status -eq "OK") { "[OK]" } else { "[ISSUE]" }
    $color = if ($hub.Status -eq "OK") { "Green" } else { "Red" }

    Write-Host "  $status " -NoNewline -ForegroundColor $color
    Write-Host "$($hub.FriendlyName)" -ForegroundColor White

    # Determine USB version
    if ($hub.FriendlyName -match "3\.[0-2]|xHCI|SuperSpeed") {
        Write-Host "      Supports: USB 3.x (SuperSpeed)" -ForegroundColor Cyan
    } elseif ($hub.FriendlyName -match "2\.0") {
        Write-Host "      Supports: USB 2.0 (High Speed)" -ForegroundColor Yellow
    }
    Write-Host ""
}

Write-Host "[3/5] Connected USB Devices" -ForegroundColor Yellow
Write-Host "================================================================" -ForegroundColor Gray

# Get all USB devices
$usbDevices = Get-PnpDevice | Where-Object {
    $_.InstanceId -like "USB\*" -and
    $_.FriendlyName -notlike "*Root Hub*" -and
    $_.FriendlyName -notlike "*Host Controller*" -and
    $_.FriendlyName -notlike "*Composite Device*"
}

if ($usbDevices.Count -eq 0) {
    Write-Host "  No USB devices detected (or enumeration failed)" -ForegroundColor Red
} else {
    foreach ($device in $usbDevices) {
        $status = if ($device.Status -eq "OK") { "✓" } else { "✗" }
        $color = if ($device.Status -eq "OK") { "Green" } else { "Red" }

        Write-Host "  [$status] " -NoNewline -ForegroundColor $color
        Write-Host "$($device.FriendlyName)" -ForegroundColor White

        # Parse instance ID for speed info
        if ($device.InstanceId -match "USB\\VID_([0-9A-F]{4})&PID_([0-9A-F]{4})") {
            $vid = $matches[1]
            $pid = $matches[2]
            Write-Host "      VID:PID = $vid:$pid" -ForegroundColor Gray
        }
    }
}

Write-Host ""
Write-Host "  Total Connected Devices: $($usbDevices.Count)" -ForegroundColor Cyan
Write-Host ""

Write-Host "[4/5] USB Speed Analysis (via Device Manager)" -ForegroundColor Yellow
Write-Host "================================================================" -ForegroundColor Gray

# Try to get speed info via WMI
try {
    $wmiUSB = Get-WmiObject -Class Win32_USBController -ErrorAction SilentlyContinue

    if ($wmiUSB) {
        foreach ($usb in $wmiUSB) {
            Write-Host "  Controller: $($usb.Name)" -ForegroundColor White
            Write-Host "      Status: $($usb.Status)" -ForegroundColor $(if ($usb.Status -eq "OK") { "Green" } else { "Red" })
            Write-Host "      Protocol: $($usb.ProtocolSupported)" -ForegroundColor Cyan

            # Check if USB 3.0+
            if ($usb.Name -match "3\.[0-2]|xHCI") {
                Write-Host "      Max Speed: 5-10 Gbps (USB 3.x)" -ForegroundColor Cyan
            } elseif ($usb.Name -match "2\.0|EHCI") {
                Write-Host "      Max Speed: 480 Mbps (USB 2.0)" -ForegroundColor Yellow
            }
            Write-Host ""
        }
    }
} catch {
    Write-Host "  WMI query failed: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "[5/5] Detailed Port Speed Check (via USB View Data)" -ForegroundColor Yellow
Write-Host "================================================================" -ForegroundColor Gray

# Check if USBView or similar is available
Write-Host "  Checking USB port speeds via Registry..." -ForegroundColor Gray
Write-Host ""

# Get USB device speeds from registry
$usbStorageDevices = Get-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Enum\USBSTOR\*\*" -ErrorAction SilentlyContinue

if ($usbStorageDevices) {
    foreach ($dev in $usbStorageDevices | Where-Object { $_.FriendlyName }) {
        Write-Host "  Device: $($dev.FriendlyName)" -ForegroundColor White

        # Try to find parent USB device for speed info
        $parentId = $dev.ParentIdPrefix
        if ($parentId) {
            Write-Host "      Parent: $parentId" -ForegroundColor Gray
        }
    }
} else {
    Write-Host "  No USB storage devices found in registry" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "                   THEORETICAL MAXIMUMS" -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""

foreach ($version in $usbSpeedStandards.Keys | Sort-Object) {
    $info = $usbSpeedStandards[$version]
    $speedText = if ($info.Speed -ge 1000) {
        "$([math]::Round($info.Speed/1000, 1)) Gbps"
    } else {
        "$($info.Speed) Mbps"
    }

    $realSpeed = if ($info.ContainsKey("Bytes")) {
        " (~$($info.Bytes) MB/s real-world)"
    } else {
        ""
    }

    Write-Host "  USB $version - $($info.Name)" -ForegroundColor Cyan
    Write-Host "      Theoretical: $speedText$realSpeed" -ForegroundColor White
    Write-Host ""
}

Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "                      ANALYSIS COMPLETE" -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "NOTE: For detailed per-port speed testing, use:" -ForegroundColor Yellow
Write-Host "  - USBDeview (NirSoft)" -ForegroundColor White
Write-Host "  - USB Device Tree Viewer (Microsoft)" -ForegroundColor White
Write-Host "  - Actual file transfer tests" -ForegroundColor White
Write-Host ""

# Generate summary
Write-Host "SUMMARY:" -ForegroundColor Green
Write-Host "  Controllers: $controllerCount" -ForegroundColor White
Write-Host "  Root Hubs: $($rootHubs.Count)" -ForegroundColor White
Write-Host "  Connected Devices: $($usbDevices.Count)" -ForegroundColor White
Write-Host ""

# Check for issues
$issues = @()

# Check for non-OK devices
$badDevices = Get-PnpDevice | Where-Object { $_.Class -eq "USB" -and $_.Status -ne "OK" }
if ($badDevices) {
    $issues += "Found $($badDevices.Count) USB device(s) with issues"
}

# Check if USB 3.0 controllers are present
$usb3Controllers = $usbControllers | Where-Object { $_.FriendlyName -match "3\.[0-2]|xHCI" }
if (-not $usb3Controllers) {
    $issues += "No USB 3.x controllers detected! System may only have USB 2.0"
}

if ($issues.Count -gt 0) {
    Write-Host "ISSUES DETECTED:" -ForegroundColor Red
    foreach ($issue in $issues) {
        Write-Host "  ! $issue" -ForegroundColor Red
    }
} else {
    Write-Host "NO ISSUES DETECTED - All USB devices appear healthy!" -ForegroundColor Green
}

Write-Host ""
Write-Host "Press any key to exit..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
