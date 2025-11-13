#!/bin/bash
# Generate recent logs JSON

# Load config if available
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [ -f "$SCRIPT_DIR/../../config/load-config.sh" ]; then
    source "$SCRIPT_DIR/../../config/load-config.sh" 2>/dev/null || true
fi

LOG_DIR="${PHILAUNCH_LOG_DIR:-$HOME/PhiLaunch/logs}"

# Find recent log files
LOG_FILES=$(find "$LOG_DIR" -type f -name "*.log" 2>/dev/null | head -5)

echo '{"logs": ['

if [ -n "$LOG_FILES" ]; then
    FIRST=true

    # Get last 10 lines from each log file
    while IFS= read -r logfile; do
        if [ -f "$logfile" ]; then
            while IFS= read -r line; do
                if [ -n "$line" ]; then
                    if [ "$FIRST" = true ]; then
                        FIRST=false
                    else
                        echo ","
                    fi

                    # Extract timestamp and message
                    TIMESTAMP=$(echo "$line" | grep -oP '\[\K[^\]]+' | head -1 || date '+%Y-%m-%d %H:%M:%S')
                    MESSAGE=$(echo "$line" | sed 's/\[.*\]//; s/^[[:space:]]*//' | sed 's/"/\\"/g')

                    cat <<EOF
    {
      "timestamp": "$TIMESTAMP",
      "message": "$MESSAGE"
    }
EOF
                fi
            done < <(tail -5 "$logfile" 2>/dev/null)
        fi
    done <<< "$LOG_FILES"
fi

echo '],'
echo '"timestamp": "'$(date -u +%Y-%m-%dT%H:%M:%SZ)'"'
echo '}'
