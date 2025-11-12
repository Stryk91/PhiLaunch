#!/bin/bash
# Quick system status check - run from SSH

echo "=== SYSTEM STATUS ==="
echo "Hostname: $(hostname)"
echo "Uptime: $(uptime -p)"
echo ""
echo "=== CPU & MEMORY ==="
free -h | grep -E "Mem|Swap"
echo ""
echo "=== DISK USAGE ==="
df -h / | tail -1
echo ""
echo "=== TOP 5 PROCESSES ==="
ps aux --sort=-%mem | head -6
echo ""
echo "=== NETWORK ==="
echo "LAN IPs: $(hostname -I)"
echo ""
echo "=== RUNNING SERVICES ==="
systemctl list-units --type=service --state=running --no-pager | grep -E "ssh|docker" | head -5
