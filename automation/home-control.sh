#!/bin/bash
# Home Automation Control Center
# Quick access to common automation tasks

# Load PhiLaunch configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/../config/load-config.sh"

ACTION="$1"

case "$ACTION" in
    status)
        bash "${PHILAUNCH_REMOTE_SCRIPTS_DIR}/quick-status.sh"
        ;;

    list-scripts)
        echo "=== Available PhiLaunch Scripts ==="
        ls -lh "${PHILAUNCH_HOME}"/*.sh 2>/dev/null | awk '{print $9, "(" $5 ")"}'
        ;;

    list-tasks)
        echo "=== Running tmux sessions ==="
        tmux list-sessions 2>/dev/null || echo "No active sessions"
        ;;

    kill-task)
        SESSION="$2"
        if [ -z "$SESSION" ]; then
            echo "Usage: $0 kill-task <session-name>"
            exit 1
        fi
        tmux kill-session -t "$SESSION"
        echo "✓ Killed session: $SESSION"
        ;;

    logs)
        echo "=== Recent System Logs ==="
        journalctl -n 20 --no-pager
        ;;

    restart-ssh)
        echo "Restarting SSH server..."
        sudo systemctl restart ssh
        echo "✓ SSH restarted"
        ;;

    *)
        echo "=== HOME AUTOMATION CONTROL ==="
        echo ""
        echo "Usage: $0 <command>"
        echo ""
        echo "Commands:"
        echo "  status        - System status overview"
        echo "  list-scripts  - Show all available scripts"
        echo "  list-tasks    - Show running background tasks"
        echo "  kill-task     - Kill a background task"
        echo "  logs          - View recent system logs"
        echo "  restart-ssh   - Restart SSH server"
        echo ""
        echo "Examples:"
        echo "  ssh ${PHILAUNCH_SSH_CONN} -p ${PHILAUNCH_SSH_PORT} 'bash ~/automation/home-control.sh status'"
        echo "  ssh ${PHILAUNCH_SSH_CONN} -p ${PHILAUNCH_SSH_PORT} 'bash ~/automation/home-control.sh list-tasks'"
        ;;
esac
