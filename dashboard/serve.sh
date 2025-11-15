#!/bin/bash
# PhiLaunch Dashboard Server
# Serves the dashboard on http://localhost:8080

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Configuration
PORT="${DASHBOARD_PORT:-8080}"
UPDATE_INTERVAL=5  # Seconds between API updates

echo -e "${BLUE}╔════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║  PhiLaunch Dashboard Server           ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════╝${NC}"
echo ""

# Check if port is available
if lsof -Pi :"$PORT" -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo -e "${YELLOW}⚠ Port $PORT is already in use${NC}"
    echo "  Kill the process or use a different port:"
    echo "  DASHBOARD_PORT=8081 ./serve.sh"
    exit 1
fi

# Start API update loop in background
echo -e "${GREEN}▶${NC} Starting API update loop..."

update_api_data() {
    while true; do
        # Generate JSON files
        api/status.sh > api/status.json 2>/dev/null || echo '{"error": "Failed to generate status"}' > api/status.json
        api/metrics.sh > api/metrics.json 2>/dev/null || echo '{"error": "Failed to generate metrics"}' > api/metrics.json
        api/tasks.sh > api/tasks.json 2>/dev/null || echo '{"error": "Failed to generate tasks"}' > api/tasks.json
        api/wow.sh > api/wow.json 2>/dev/null || echo '{"error": "Failed to generate wow stats"}' > api/wow.json
        api/logs.sh > api/logs.json 2>/dev/null || echo '{"error": "Failed to generate logs"}' > api/logs.json
        api/info.sh > api/info.json 2>/dev/null || echo '{"error": "Failed to generate info"}' > api/info.json

        sleep $UPDATE_INTERVAL
    done
}

# Start update loop in background
update_api_data &
UPDATE_PID=$!

# Cleanup function
cleanup() {
    echo ""
    echo -e "${YELLOW}▶${NC} Stopping dashboard server..."
    kill $UPDATE_PID 2>/dev/null || true
    rm -f api/*.json 2>/dev/null || true
    echo -e "${GREEN}✓${NC} Dashboard stopped"
    exit 0
}

trap cleanup SIGINT SIGTERM EXIT

# Generate initial data
echo -e "${GREEN}▶${NC} Generating initial data..."
api/status.sh > api/status.json 2>/dev/null || true
api/metrics.sh > api/metrics.json 2>/dev/null || true
api/tasks.sh > api/tasks.json 2>/dev/null || true
api/wow.sh > api/wow.json 2>/dev/null || true
api/logs.sh > api/logs.json 2>/dev/null || true
api/info.sh > api/info.json 2>/dev/null || true

# Start HTTP server
echo -e "${GREEN}▶${NC} Starting HTTP server on port $PORT..."
echo ""
echo -e "${GREEN}✓${NC} Dashboard ready!"
echo ""
echo -e "  ${BLUE}Local:${NC}   http://localhost:$PORT"
echo -e "  ${BLUE}Network:${NC} http://$(hostname -I | awk '{print $1}'):$PORT"
echo ""
echo -e "Press ${YELLOW}Ctrl+C${NC} to stop"
echo ""

# Start Python HTTP server
if command -v python3 &> /dev/null; then
    python3 -m http.server "$PORT" --bind 0.0.0.0
elif command -v python &> /dev/null; then
    python -m SimpleHTTPServer "$PORT"
else
    echo -e "${YELLOW}⚠ Python not found${NC}"
    echo "  Install Python to run the dashboard server"
    exit 1
fi
