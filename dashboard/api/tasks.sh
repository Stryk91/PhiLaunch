#!/bin/bash
# Generate background tasks JSON

if ! command -v tmux &> /dev/null; then
    echo '{"tasks": [], "count": 0}'
    exit 0
fi

# Get tmux sessions
SESSIONS=$(tmux list-sessions 2>/dev/null | awk -F: '{print $1}' || echo "")

if [ -z "$SESSIONS" ]; then
    echo '{"tasks": [], "count": 0}'
    exit 0
fi

# Build JSON array
echo '{"tasks": ['

FIRST=true
while IFS= read -r session; do
    if [ -n "$session" ]; then
        if [ "$FIRST" = true ]; then
            FIRST=false
        else
            echo ","
        fi

        # Get session info
        WINDOWS=$(tmux list-windows -t "$session" 2>/dev/null | wc -l || echo 0)

        cat <<EOF
    {
      "name": "$session",
      "status": "running",
      "windows": $WINDOWS
    }
EOF
    fi
done <<< "$SESSIONS"

echo '],'
echo '"count": '"$(echo "$SESSIONS" | grep -c '^')"','
echo '"timestamp": "'"$(date -u +%Y-%m-%dT%H:%M:%SZ)"'"'
echo '}'
