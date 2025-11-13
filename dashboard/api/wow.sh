#!/bin/bash
# Generate WoW monitor JSON

# Load config if available
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [ -f "$SCRIPT_DIR/../../config/load-config.sh" ]; then
    source "$SCRIPT_DIR/../../config/load-config.sh" 2>/dev/null || true
    WOW_SERVER="${WOW_SERVER_IP:-103.4.115.248}"
else
    WOW_SERVER="103.4.115.248"
fi

# Check if log file exists
LOG_DIR="${PHILAUNCH_LOG_DIR:-$HOME/PhiLaunch/logs}"
LOG_FILE=$(find "$LOG_DIR" -name "wow_connection_*.log" -type f 2>/dev/null | sort | tail -1)

if [ -z "$LOG_FILE" ] || [ ! -f "$LOG_FILE" ]; then
    echo '{"enabled": false, "message": "No log file found"}'
    exit 0
fi

# Get latest stats from log
LATEST=$(tail -1 "$LOG_FILE" 2>/dev/null)

if [ -z "$LATEST" ]; then
    echo '{"enabled": false, "message": "No data in log"}'
    exit 0
fi

# Parse stats
AVG=$(echo "$LATEST" | grep -oP 'Avg=\K[0-9.]+' || echo "0")
BEST=$(echo "$LATEST" | grep -oP 'Best=\K[0-9.]+' || echo "0")
WORST=$(echo "$LATEST" | grep -oP 'Worst=\K[0-9.]+' || echo "0")
JITTER=$(echo "$LATEST" | grep -oP 'Jitter=\K[0-9.]+' || echo "0")
LOSS=$(echo "$LATEST" | grep -oP 'Loss=\K[0-9.]+' || echo "0.0")

# Output JSON
cat <<EOF
{
  "enabled": true,
  "server": "$WOW_SERVER",
  "stats": {
    "avg_latency": "$AVG",
    "best_latency": "$BEST",
    "worst_latency": "$WORST",
    "jitter": "$JITTER",
    "loss": "$LOSS"
  },
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
}
EOF
