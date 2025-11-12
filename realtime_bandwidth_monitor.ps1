# Real-Time Phone Link Bandwidth Monitor
# Shows live transfer speed and destination

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  PHONE LINK - REAL-TIME BANDWIDTH MONITOR" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Find Phone Link process
$phoneProc = Get-Process -Name "*PhoneExperienceHost*", "*YourPhone*" -ErrorAction SilentlyContinue | Select-Object -First 1

if (-not $phoneProc) {
    Write-Host "ERROR: Phone Link is not running!" -ForegroundColor Red
    Write-Host "Start the file transfer first, then run this script." -ForegroundColor Yellow
    pause
    exit 1
}

Write-Host "Found: $($phoneProc.Name) (PID: $($phoneProc.Id))" -ForegroundColor Green
Write-Host ""

# Get initial network stats
$initialStats = Get-NetAdapterStatistics

Write-Host "Monitoring bandwidth... Press Ctrl+C to stop" -ForegroundColor Yellow
Write-Host ""

$lastSent = 0
$lastReceived = 0
$iteration = 0

while ($true) {
    $iteration++

    # Get current connections
    $connections = Get-NetTCPConnection -OwningProcess $phoneProc.Id -State Established -ErrorAction SilentlyContinue

    # Get current network stats
    $currentStats = Get-NetAdapterStatistics

    # Calculate bandwidth
    $totalSent = ($currentStats | Measure-Object -Property SentBytes -Sum).Sum
    $totalReceived = ($currentStats | Measure-Object -Property ReceivedBytes -Sum).Sum

    if ($lastSent -gt 0) {
        $sentDiff = $totalSent - $lastSent
        $recvDiff = $totalReceived - $lastReceived

        $sentSpeed = [math]::Round($sentDiff / 1MB, 2)
        $recvSpeed = [math]::Round($recvDiff / 1MB, 2)

        $timestamp = Get-Date -Format "HH:mm:ss"

        Write-Host "[$timestamp]" -NoNewline -ForegroundColor Gray
        Write-Host " Upload: " -NoNewline
        Write-Host "$sentSpeed MB/s" -NoNewline -ForegroundColor $(if ($sentSpeed -gt 10) { "Green" } else { "Yellow" })
        Write-Host " | Download: " -NoNewline
        Write-Host "$recvSpeed MB/s" -NoNewline -ForegroundColor $(if ($recvSpeed -gt 10) { "Green" } else { "Yellow" })

        # Show connections every 5 iterations
        if ($iteration % 5 -eq 0 -and $connections) {
            Write-Host ""
            Write-Host "  Active connections:" -ForegroundColor Cyan

            foreach ($conn in $connections) {
                $remote = "$($conn.RemoteAddress):$($conn.RemotePort)"

                # Determine if local or cloud
                if ($conn.RemoteAddress -match "^192\.168\." -or $conn.RemoteAddress -match "^10\." -or $conn.RemoteAddress -match "^172\.(1[6-9]|2[0-9]|3[0-1])\.") {
                    $type = "[LOCAL]"
                    $color = "Green"
                } elseif ($conn.RemoteAddress -match "^(20\.|13\.|40\.|52\.)") {
                    $type = "[MICROSOFT CLOUD]"
                    $color = "Yellow"
                } else {
                    $type = "[EXTERNAL]"
                    $color = "Red"
                }

                Write-Host "    $type $remote" -ForegroundColor $color
            }
        } else {
            Write-Host ""
        }
    }

    $lastSent = $totalSent
    $lastReceived = $totalReceived

    Start-Sleep -Seconds 1
}
