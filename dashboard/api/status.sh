#!/bin/bash
# Generate system status JSON

# Load config if available
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [ -f "$SCRIPT_DIR/../../config/load-config.sh" ]; then
    source "$SCRIPT_DIR/../../config/load-config.sh" 2>/dev/null || true
fi

# Check system status
check_system() {
    if [ -f /proc/uptime ]; then
        echo "true"
    else
        echo "false"
    fi
}

# Check services
check_services() {
    if command -v systemctl &> /dev/null; then
        if systemctl is-active --quiet ssh || systemctl is-active --quiet sshd; then
            echo "true"
        else
            echo "false"
        fi
    else
        echo "true"  # Assume OK if systemctl not available
    fi
}

# Check tasks
check_tasks() {
    if command -v tmux &> /dev/null; then
        if tmux list-sessions &>/dev/null; then
            echo "true"
        else
            echo "false"
        fi
    else
        echo "false"
    fi
}

# Get uptime
get_uptime() {
    if command -v uptime &> /dev/null; then
        uptime -p 2>/dev/null | sed 's/up //' || echo "unknown"
    else
        echo "unknown"
    fi
}

SYSTEM_ONLINE=$(check_system)
SERVICES_ONLINE=$(check_services)
TASKS_ONLINE=$(check_tasks)
UPTIME=$(get_uptime)

# Output JSON
cat <<EOF
{
  "system": {
    "online": $SYSTEM_ONLINE,
    "warning": false
  },
  "services": {
    "online": $SERVICES_ONLINE,
    "warning": false
  },
  "tasks": {
    "online": $TASKS_ONLINE,
    "warning": false
  },
  "uptime": "$UPTIME",
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
}
EOF
