#!/bin/bash
# SSH Tunnel Helper - Common tunneling scenarios
# This runs on the CLIENT side (your phone/other device)

# Load PhiLaunch configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [ -f "${SCRIPT_DIR}/../config/load-config.sh" ]; then
    source "${SCRIPT_DIR}/../config/load-config.sh"
else
    # Fallback to defaults if config not found
    PHILAUNCH_SSH_CONN="user@192.168.1.100"
    PHILAUNCH_SSH_PORT="2222"
fi

echo "=== SSH TUNNEL HELPER ==="
echo ""
echo "Run these commands from your PHONE/CLIENT device:"
echo ""
echo "1. FORWARD LOCAL PORT TO REMOTE SERVICE"
echo "   Access a service running on your PC from your phone"
echo "   ssh -L 8080:localhost:8080 ${PHILAUNCH_SSH_CONN} -p ${PHILAUNCH_SSH_PORT}"
echo "   Then browse to: http://localhost:8080 on your phone"
echo ""
echo "2. REVERSE TUNNEL (Access phone FROM PC)"
echo "   ssh -R 9000:localhost:8080 ${PHILAUNCH_SSH_CONN} -p ${PHILAUNCH_SSH_PORT}"
echo "   Your PC can now access phone's port 8080 via localhost:9000"
echo ""
echo "3. DYNAMIC SOCKS PROXY"
echo "   Use your PC as a proxy for all traffic"
echo "   ssh -D 8080 ${PHILAUNCH_SSH_CONN} -p ${PHILAUNCH_SSH_PORT}"
echo "   Configure phone to use SOCKS5 proxy: localhost:8080"
echo ""
echo "4. KEEP TUNNEL ALIVE"
echo "   Add -N flag to keep connection without shell"
echo "   ssh -N -L 8080:localhost:8080 ${PHILAUNCH_SSH_CONN} -p ${PHILAUNCH_SSH_PORT}"
