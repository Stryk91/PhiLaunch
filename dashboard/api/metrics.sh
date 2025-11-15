#!/bin/bash
# Generate system metrics JSON

# Get CPU usage
get_cpu_usage() {
    if command -v top &> /dev/null; then
        top -bn1 | grep "Cpu(s)" | sed "s/.*, *\([0-9.]*\)%* id.*/\1/" | awk '{print 100 - $1}'
    elif command -v mpstat &> /dev/null; then
        mpstat 1 1 | awk '/Average/ {print 100-$NF}'
    else
        echo "0"
    fi
}

# Get memory usage
get_memory_usage() {
    if command -v free &> /dev/null; then
        free | grep Mem | awk '{printf "%.1f", ($3/$2) * 100.0}'
    else
        echo "0"
    fi
}

# Get disk usage
get_disk_usage() {
    if command -v df &> /dev/null; then
        df -h / | awk 'NR==2 {print $5}' | sed 's/%//'
    else
        echo "0"
    fi
}

# Get network status
get_network_status() {
    if ping -c 1 -W 1 8.8.8.8 &>/dev/null; then
        echo '{"status": "Connected", "connected": true}'
    else
        echo '{"status": "Disconnected", "connected": false}'
    fi
}

CPU=$(get_cpu_usage)
MEMORY=$(get_memory_usage)
DISK=$(get_disk_usage)
NETWORK=$(get_network_status)

# Output JSON
cat <<EOF
{
  "cpu": {
    "percent": $CPU,
    "cores": $(nproc 2>/dev/null || echo 1)
  },
  "memory": {
    "percent": $MEMORY,
    "total": "$(free -h 2>/dev/null | awk '/^Mem:/ {print $2}' || echo 'N/A')",
    "used": "$(free -h 2>/dev/null | awk '/^Mem:/ {print $3}' || echo 'N/A')"
  },
  "disk": {
    "percent": $DISK,
    "total": "$(df -h / 2>/dev/null | awk 'NR==2 {print $2}' || echo 'N/A')",
    "used": "$(df -h / 2>/dev/null | awk 'NR==2 {print $3}' || echo 'N/A')"
  },
  "network": $NETWORK,
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
}
EOF
