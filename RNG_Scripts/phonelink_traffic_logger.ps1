# Phone Link Traffic Logger
# Monitors and logs network traffic for Phone Link apps
# Run as Administrator for full details

$outputFile = "$env:USERPROFILE\Desktop\phonelink_traffic_log.txt"

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "   PHONE LINK TRAFFIC LOGGER" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Logging to: $outputFile" -ForegroundColor Yellow
Write-Host "Press Ctrl+C to stop" -ForegroundColor Yellow
Write-Host ""

# Initialize log file
"Phone Link Traffic Log - $(Get-Date)" | Out-File $outputFile
"=" * 60 | Out-File $outputFile -Append
"" | Out-File $outputFile -Append

while ($true) {
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

    Write-Host "[$timestamp] Capturing..." -ForegroundColor Green

    # Log section header
    "`n[$timestamp]" | Out-File $outputFile -Append
    "-" * 60 | Out-File $outputFile -Append

    # Get Phone Link processes
    $phoneProcesses = Get-Process -Name "*Phone*", "*Link*" -ErrorAction SilentlyContinue

    if ($phoneProcesses) {
        Write-Host "  Found Phone Link processes:" -ForegroundColor Cyan

        foreach ($proc in $phoneProcesses) {
            $procInfo = "Process: $($proc.Name) (PID: $($proc.Id))"
            Write-Host "    $procInfo" -ForegroundColor White
            $procInfo | Out-File $outputFile -Append

            # Get network connections for this process
            $connections = Get-NetTCPConnection -OwningProcess $proc.Id -ErrorAction SilentlyContinue

            if ($connections) {
                foreach ($conn in $connections) {
                    $connInfo = "  -> $($conn.LocalAddress):$($conn.LocalPort) -> $($conn.RemoteAddress):$($conn.RemotePort) [$($conn.State)]"
                    Write-Host "      $connInfo" -ForegroundColor Yellow
                    $connInfo | Out-File $outputFile -Append

                    # Get bandwidth stats if available
                    $stats = Get-NetAdapterStatistics | Where-Object { $_.Name -like "*" }
                    if ($stats) {
                        $bandwidth = "     Sent: $([math]::Round($stats.SentBytes/1MB, 2)) MB | Received: $([math]::Round($stats.ReceivedBytes/1MB, 2)) MB"
                        $bandwidth | Out-File $outputFile -Append
                    }
                }
            } else {
                "  No active connections" | Out-File $outputFile -Append
            }
        }
    } else {
        Write-Host "  No Phone Link processes found" -ForegroundColor Red
        "No Phone Link processes running" | Out-File $outputFile -Append
    }

    # Check for large data transfers
    Write-Host "`n  Checking network adapters..." -ForegroundColor Cyan
    $adapters = Get-NetAdapter | Where-Object Status -eq "Up"

    foreach ($adapter in $adapters) {
        $stats = Get-NetAdapterStatistics -Name $adapter.Name
        $sent = [math]::Round($stats.SentBytes / 1GB, 3)
        $received = [math]::Round($stats.ReceivedBytes / 1GB, 3)

        $adapterInfo = "Adapter: $($adapter.Name) | Sent: ${sent} GB | Received: ${received} GB"
        Write-Host "    $adapterInfo" -ForegroundColor Magenta
        $adapterInfo | Out-File $outputFile -Append
    }

    "" | Out-File $outputFile -Append

    Start-Sleep -Seconds 5
}
