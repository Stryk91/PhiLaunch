# USB Speed Test - Real Transfer Speed Measurement
# Creates test files and measures actual USB transfer speeds

param(
    [string]$TargetDrive = "",
    [int]$TestSizeMB = 1000
)

Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "              USB TRANSFER SPEED TEST" -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""

# List available drives
Write-Host "Available Drives:" -ForegroundColor Yellow
Get-PSDrive -PSProvider FileSystem | Where-Object { $_.Root -match "^[A-Z]:\\" } | ForEach-Object {
    $drive = $_
    $volumeInfo = Get-Volume -DriveLetter $drive.Name -ErrorAction SilentlyContinue

    if ($volumeInfo) {
        $freeGB = [math]::Round($volumeInfo.SizeRemaining / 1GB, 2)
        $totalGB = [math]::Round($volumeInfo.Size / 1GB, 2)
        $label = if ($volumeInfo.FileSystemLabel) { $volumeInfo.FileSystemLabel } else { "No Label" }

        Write-Host "  [$($drive.Name):] $label" -ForegroundColor White
        Write-Host "      Free: $freeGB GB / $totalGB GB" -ForegroundColor Gray
        Write-Host "      Type: $($volumeInfo.FileSystemType)" -ForegroundColor Gray
    }
}

Write-Host ""

# Prompt for drive if not specified
if (-not $TargetDrive) {
    $TargetDrive = Read-Host "Enter drive letter to test (e.g., D)"
    $TargetDrive = $TargetDrive.TrimEnd(':')
}

$testPath = "${TargetDrive}:\USB_SPEED_TEST"

# Validate drive
if (-not (Test-Path "${TargetDrive}:\")) {
    Write-Host "ERROR: Drive ${TargetDrive}: not found!" -ForegroundColor Red
    pause
    exit 1
}

# Check free space
$volume = Get-Volume -DriveLetter $TargetDrive
$freeGB = [math]::Round($volume.SizeRemaining / 1GB, 2)

if ($freeGB -lt ($TestSizeMB / 1000)) {
    Write-Host "ERROR: Not enough free space! Need $TestSizeMB MB, have $freeGB GB" -ForegroundColor Red
    pause
    exit 1
}

Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "TEST CONFIGURATION" -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "  Target Drive: ${TargetDrive}:" -ForegroundColor White
Write-Host "  Test Size: $TestSizeMB MB" -ForegroundColor White
Write-Host "  Test Path: $testPath" -ForegroundColor White
Write-Host ""

$confirm = Read-Host "Start test? (Y/N)"
if ($confirm -ne "Y" -and $confirm -ne "y") {
    Write-Host "Test cancelled." -ForegroundColor Yellow
    exit 0
}

Write-Host ""
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "STARTING SPEED TEST" -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""

# Create test directory
if (-not (Test-Path $testPath)) {
    New-Item -Path $testPath -ItemType Directory -Force | Out-Null
}

# Generate random test file
$testFile = "$env:TEMP\usb_test_$TestSizeMB.tmp"
$targetFile = "$testPath\test_$TestSizeMB.tmp"

Write-Host "[1/3] Generating ${TestSizeMB}MB test file..." -ForegroundColor Yellow

$sw = [System.Diagnostics.Stopwatch]::StartNew()

# Create test file with random data (faster than using fsutil for large files)
$buffer = New-Object byte[] (1MB)
$rng = [System.Security.Cryptography.RNGCryptoServiceProvider]::Create()
$stream = [System.IO.File]::OpenWrite($testFile)

for ($i = 0; $i -lt $TestSizeMB; $i++) {
    $rng.GetBytes($buffer)
    $stream.Write($buffer, 0, $buffer.Length)

    if ($i % 100 -eq 0) {
        Write-Host "  Progress: $i / $TestSizeMB MB" -ForegroundColor Gray
    }
}

$stream.Close()
$sw.Stop()

Write-Host "  ✓ Test file created in $($sw.Elapsed.TotalSeconds) seconds" -ForegroundColor Green
Write-Host ""

# Test WRITE speed
Write-Host "[2/3] Testing WRITE speed to ${TargetDrive}:..." -ForegroundColor Yellow

$sw.Restart()
Copy-Item -Path $testFile -Destination $targetFile -Force
$sw.Stop()

$writeSeconds = $sw.Elapsed.TotalSeconds
$writeMBps = [math]::Round($TestSizeMB / $writeSeconds, 2)
$writeGbps = [math]::Round(($writeMBps * 8) / 1000, 2)

Write-Host "  ✓ WRITE Speed: $writeMBps MB/s ($writeGbps Gbps)" -ForegroundColor Green
Write-Host ""

# Clear cache before read test
[System.GC]::Collect()
[System.GC]::WaitForPendingFinalizers()

# Test READ speed
Write-Host "[3/3] Testing READ speed from ${TargetDrive}:..." -ForegroundColor Yellow

$readDestination = "$env:TEMP\usb_read_test_$TestSizeMB.tmp"

$sw.Restart()
Copy-Item -Path $targetFile -Destination $readDestination -Force
$sw.Stop()

$readSeconds = $sw.Elapsed.TotalSeconds
$readMBps = [math]::Round($TestSizeMB / $readSeconds, 2)
$readGbps = [math]::Round(($readMBps * 8) / 1000, 2)

Write-Host "  ✓ READ Speed: $readMBps MB/s ($readGbps Gbps)" -ForegroundColor Green
Write-Host ""

# Cleanup
Write-Host "Cleaning up test files..." -ForegroundColor Gray
Remove-Item $testFile -Force -ErrorAction SilentlyContinue
Remove-Item $targetFile -Force -ErrorAction SilentlyContinue
Remove-Item $readDestination -Force -ErrorAction SilentlyContinue
Remove-Item $testPath -Force -ErrorAction SilentlyContinue

Write-Host ""
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "                    TEST RESULTS" -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "  Drive: ${TargetDrive}: ($($volume.FileSystemLabel))" -ForegroundColor White
Write-Host "  Filesystem: $($volume.FileSystemType)" -ForegroundColor White
Write-Host ""
Write-Host "  WRITE Speed: $writeMBps MB/s ($writeGbps Gbps)" -ForegroundColor Cyan
Write-Host "  READ Speed:  $readMBps MB/s ($readGbps Gbps)" -ForegroundColor Cyan
Write-Host ""

# Determine USB version based on speed
$avgSpeed = ($writeMBps + $readMBps) / 2

Write-Host "ANALYSIS:" -ForegroundColor Yellow

if ($avgSpeed -gt 1000) {
    Write-Host "  ✓ USB 3.1 Gen 2 (10 Gbps) performance detected!" -ForegroundColor Green
    Write-Host "    Drive is running at full USB 3.1 speed." -ForegroundColor Green
} elseif ($avgSpeed -gt 400) {
    Write-Host "  ✓ USB 3.0 (5 Gbps) performance detected" -ForegroundColor Green
    Write-Host "    Drive is running at USB 3.0 speed." -ForegroundColor Green
} elseif ($avgSpeed -gt 200) {
    Write-Host "  ~ Good USB 3.0 performance" -ForegroundColor Yellow
    Write-Host "    Close to USB 3.0 maximum (625 MB/s)" -ForegroundColor Yellow
} elseif ($avgSpeed -gt 50) {
    Write-Host "  ⚠ USB 2.0 speed detected!" -ForegroundColor Red
    Write-Host "    Drive is only running at USB 2.0 (480 Mbps) speed." -ForegroundColor Red
    Write-Host "    Expected: 60 MB/s max for USB 2.0" -ForegroundColor Red
    Write-Host "    ISSUE: Drive may be in USB 2.0 port or using USB 2.0 cable" -ForegroundColor Red
} else {
    Write-Host "  ✗ Very slow speed!" -ForegroundColor Red
    Write-Host "    Possible issues:" -ForegroundColor Red
    Write-Host "      - Bad cable" -ForegroundColor Red
    Write-Host "      - USB 1.1 port" -ForegroundColor Red
    Write-Host "      - Drive performance issue" -ForegroundColor Red
}

Write-Host ""
Write-Host "THEORETICAL MAXIMUMS:" -ForegroundColor Yellow
Write-Host "  USB 2.0:        ~60 MB/s" -ForegroundColor Gray
Write-Host "  USB 3.0:        ~625 MB/s" -ForegroundColor Gray
Write-Host "  USB 3.1 Gen 2:  ~1,250 MB/s" -ForegroundColor Gray
Write-Host "  USB 3.2:        ~2,500 MB/s" -ForegroundColor Gray
Write-Host ""

Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press any key to exit..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
