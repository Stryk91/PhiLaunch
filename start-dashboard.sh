#!/bin/bash
# PhiLaunch Dashboard Launcher
# Convenience script to start the dashboard

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Load config if available
if [ -f "$SCRIPT_DIR/config/load-config.sh" ]; then
    source "$SCRIPT_DIR/config/load-config.sh" 2>/dev/null || true
fi

echo "Starting PhiLaunch Dashboard..."
echo ""

# Start dashboard server
exec "$SCRIPT_DIR/dashboard/serve.sh"
