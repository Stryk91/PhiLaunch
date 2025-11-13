#!/bin/bash
# Generate system info JSON

HOSTNAME=$(hostname 2>/dev/null || echo "unknown")
OS=$(cat /etc/os-release 2>/dev/null | grep "PRETTY_NAME" | cut -d'"' -f2 || uname -s)
KERNEL=$(uname -r 2>/dev/null || echo "unknown")
IP=$(hostname -I 2>/dev/null | awk '{print $1}' || echo "unknown")

# Output JSON
cat <<EOF
{
  "hostname": "$HOSTNAME",
  "os": "$OS",
  "kernel": "$KERNEL",
  "ip": "$IP",
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
}
EOF
