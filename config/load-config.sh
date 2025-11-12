#!/bin/bash
# PhiLaunch Configuration Loader
# Source this file at the beginning of your scripts to load config

# Determine the PhiLaunch root directory
if [ -n "$PHILAUNCH_HOME" ]; then
    # Already set, use it
    PHILAUNCH_ROOT="$PHILAUNCH_HOME"
elif [ -n "$BASH_SOURCE" ]; then
    # Get directory of this script, then go up one level
    PHILAUNCH_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
else
    # Fallback: assume we're in PhiLaunch directory
    PHILAUNCH_ROOT="$(cd "$(dirname "$0")/.." && pwd 2>/dev/null || echo "$HOME/PhiLaunch")"
fi

# Path to the config file
CONFIG_FILE="${PHILAUNCH_ROOT}/config/philaunch.conf"

# Check if config exists
if [ ! -f "$CONFIG_FILE" ]; then
    echo "ERROR: PhiLaunch config file not found: $CONFIG_FILE"
    echo ""
    echo "Please run the setup wizard first:"
    echo "  cd ${PHILAUNCH_ROOT}"
    echo "  ./setup.sh"
    echo ""
    echo "Or manually copy the example config:"
    echo "  cp config/philaunch.conf.example config/philaunch.conf"
    echo "  nano config/philaunch.conf"
    exit 1
fi

# Load the configuration
source "$CONFIG_FILE"

# Validate required variables
REQUIRED_VARS=(
    "PHILAUNCH_USER"
    "PHILAUNCH_HOST"
    "PHILAUNCH_SSH_PORT"
    "PHILAUNCH_HOME"
)

MISSING_VARS=()
for var in "${REQUIRED_VARS[@]}"; do
    if [ -z "${!var}" ]; then
        MISSING_VARS+=("$var")
    fi
done

if [ ${#MISSING_VARS[@]} -gt 0 ]; then
    echo "ERROR: Required configuration variables are missing:"
    for var in "${MISSING_VARS[@]}"; do
        echo "  - $var"
    done
    echo ""
    echo "Please update your config file: $CONFIG_FILE"
    exit 1
fi

# Export variables so they're available to child processes
export PHILAUNCH_USER
export PHILAUNCH_HOST
export PHILAUNCH_SSH_PORT
export PHILAUNCH_SSH_CONN
export PHILAUNCH_HOME
export PHILAUNCH_USER_HOME
export PHILAUNCH_AUTOMATION_DIR
export PHILAUNCH_REMOTE_SCRIPTS_DIR
export PHILAUNCH_LOG_DIR
export WOW_SERVER_IP
export MONITOR_INTERVAL
export WIREGUARD_INTERFACE
export ENABLE_WAN_WARNINGS
export TMUX_SESSION_PREFIX
export ENABLE_COLOR_OUTPUT
export DEBUG_MODE

# Debug output if enabled
if [ "$DEBUG_MODE" = "true" ]; then
    echo "[DEBUG] PhiLaunch config loaded successfully"
    echo "[DEBUG] User: $PHILAUNCH_USER"
    echo "[DEBUG] Host: $PHILAUNCH_HOST"
    echo "[DEBUG] Port: $PHILAUNCH_SSH_PORT"
    echo "[DEBUG] Home: $PHILAUNCH_HOME"
fi
