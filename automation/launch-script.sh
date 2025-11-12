#!/bin/bash
# Home Automation - Launch any PhiLaunch script remotely
# Usage: ./launch-script.sh <script-name>

SCRIPTS_DIR="/home/STRYK"
SCRIPT_NAME="$1"

if [ -z "$SCRIPT_NAME" ]; then
    echo "Available scripts:"
    ls -1 "$SCRIPTS_DIR"/*.sh | xargs -n 1 basename
    exit 1
fi

SCRIPT_PATH="$SCRIPTS_DIR/$SCRIPT_NAME"

if [ ! -f "$SCRIPT_PATH" ]; then
    echo "Error: Script not found: $SCRIPT_PATH"
    exit 1
fi

echo "Launching: $SCRIPT_NAME"
chmod +x "$SCRIPT_PATH"
"$SCRIPT_PATH"
