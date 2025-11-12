#!/bin/bash
# Start a long-running task in a detached tmux session
# Usage: ./start-long-task.sh <session-name> <command>

SESSION_NAME="$1"
shift

if [ -z "$SESSION_NAME" ] || [ $# -eq 0 ]; then
    echo "Usage: $0 <session-name> <command>"
    echo ""
    echo "Active tmux sessions:"
    tmux list-sessions 2>/dev/null || echo "No active sessions"
    exit 1
fi

# Create detached tmux session and run command
tmux new-session -d -s "$SESSION_NAME" "$@"

echo "✓ Task started in tmux session: $SESSION_NAME"
echo ""
echo "To check progress:"
echo "  tmux attach -t $SESSION_NAME"
echo ""
echo "To list all sessions:"
echo "  tmux list-sessions"
