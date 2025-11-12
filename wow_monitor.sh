#!/bin/bash
# @SCRIPT_LAUNCHER_LOCAL - Script written by this computer
# WoW Connection Monitor for Sydney/Oceanic Servers
# Monitors latency, jitter, and packet loss from Bullengarook (4G LTE) to Sydney

# Load PhiLaunch configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [ -f "${SCRIPT_DIR}/config/load-config.sh" ]; then
    source "${SCRIPT_DIR}/config/load-config.sh"
    WOW_SERVER="${WOW_SERVER_IP}"
    LOG_FILE="${PHILAUNCH_LOG_DIR}/wow_connection_$(date +%Y%m%d).log"
    INTERVAL="${MONITOR_INTERVAL}"
else
    # Fallback to defaults if config not found
    WOW_SERVER="103.4.115.248"
    LOG_FILE="${HOME}/wow_connection_$(date +%Y%m%d).log"
    INTERVAL=60
fi

echo "========================================" | tee -a "$LOG_FILE"
echo "WoW Connection Monitor Started" | tee -a "$LOG_FILE"
echo "Time: $(date)" | tee -a "$LOG_FILE"
echo "Server: $WOW_SERVER (Sydney/Oceanic)" | tee -a "$LOG_FILE"
echo "Location: Bullengarook, VIC (4G LTE Telstra)" | tee -a "$LOG_FILE"
echo "========================================" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

echo "Starting continuous monitoring... (Ctrl+C to stop)"
echo ""

while true; do
    TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

    # Run MTR with 20 packets for quick analysis
    MTR_OUTPUT=$(mtr -r -c 20 -n $WOW_SERVER 2>&1)

    # Extract final hop stats (last responding hop)
    FINAL_HOP=$(echo "$MTR_OUTPUT" | grep -v "???" | tail -2 | head -1)

    # Parse latency values
    AVG_LATENCY=$(echo "$FINAL_HOP" | awk '{print $6}')
    BEST_LATENCY=$(echo "$FINAL_HOP" | awk '{print $7}')
    WORST_LATENCY=$(echo "$FINAL_HOP" | awk '{print $8}')
    JITTER=$(echo "$FINAL_HOP" | awk '{print $9}')
    LOSS=$(echo "$FINAL_HOP" | awk '{print $3}')

    # Display and log
    OUTPUT="[$TIMESTAMP] Latency: Best=${BEST_LATENCY}ms Avg=${AVG_LATENCY}ms Worst=${WORST_LATENCY}ms Jitter=${JITTER}ms Loss=${LOSS}"
    echo "$OUTPUT" | tee -a "$LOG_FILE"

    # Color-coded alert for high latency/jitter
    if (( $(echo "$AVG_LATENCY > 100" | bc -l 2>/dev/null || echo "0") )); then
        echo "  ⚠️  HIGH LATENCY DETECTED" | tee -a "$LOG_FILE"
    fi
    if (( $(echo "$JITTER > 20" | bc -l 2>/dev/null || echo "0") )); then
        echo "  ⚠️  HIGH JITTER DETECTED" | tee -a "$LOG_FILE"
    fi

    sleep $INTERVAL
done
