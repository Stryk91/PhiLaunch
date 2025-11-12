#!/bin/bash
# Home Automation Control Center
# Quick access to common automation tasks

ACTION="$1"

case "$ACTION" in
    status)
        bash /home/STRYK/remote-scripts/quick-status.sh
        ;;

    list-scripts)
        echo "=== Available PhiLaunch Scripts ==="
        ls -lh /home/STRYK/*.sh | awk '{print $9, "(" $5 ")"}'
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
        echo "  ssh stryk@192.168.50.149 -p 2222 'bash ~/automation/home-control.sh status'"
        echo "  ssh stryk@192.168.50.149 -p 2222 'bash ~/automation/home-control.sh list-tasks'"
        ;;
esac
