#!/bin/bash
# Generate personalized phone shortcuts based on your configuration

# Load PhiLaunch configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/../config/load-config.sh"

OUTPUT_FILE="${PHILAUNCH_HOME}/PHONE-SHORTCUTS-PERSONAL.md"

echo "Generating personalized phone shortcuts..."
echo "Using configuration:"
echo "  User: $PHILAUNCH_USER"
echo "  Host: $PHILAUNCH_HOST"
echo "  Port: $PHILAUNCH_SSH_PORT"
echo ""

cat > "$OUTPUT_FILE" << EOF
# PhiLaunch Phone Shortcuts (Personalized)
# Auto-generated from your configuration on $(date)

**Connection**: \`ssh ${PHILAUNCH_SSH_CONN} -p ${PHILAUNCH_SSH_PORT}\`

---

## Quick Status & Monitoring

### System Status
\`\`\`
ssh ${PHILAUNCH_SSH_CONN} -p ${PHILAUNCH_SSH_PORT} 'bash ~/automation/home-control.sh status'
\`\`\`

### List Available Scripts
\`\`\`
ssh ${PHILAUNCH_SSH_CONN} -p ${PHILAUNCH_SSH_PORT} 'bash ~/automation/home-control.sh list-scripts'
\`\`\`

### List Running Tasks
\`\`\`
ssh ${PHILAUNCH_SSH_CONN} -p ${PHILAUNCH_SSH_PORT} 'tmux list-sessions'
\`\`\`

### View Recent Logs
\`\`\`
ssh ${PHILAUNCH_SSH_CONN} -p ${PHILAUNCH_SSH_PORT} 'bash ~/automation/home-control.sh logs'
\`\`\`

---

## Run PhiLaunch Scripts

### WoW Monitor
\`\`\`
ssh ${PHILAUNCH_SSH_CONN} -p ${PHILAUNCH_SSH_PORT} 'bash ~/automation/launch-script.sh wow_monitor.sh'
\`\`\`

### WoW Quick Check
\`\`\`
ssh ${PHILAUNCH_SSH_CONN} -p ${PHILAUNCH_SSH_PORT} 'bash ~/automation/launch-script.sh wow_quick_check.sh'
\`\`\`

### System Info Check
\`\`\`
ssh ${PHILAUNCH_SSH_CONN} -p ${PHILAUNCH_SSH_PORT} 'bash ~/automation/launch-script.sh system_info_checker.sh'
\`\`\`

---

## Background Tasks

### Start Background Task
\`\`\`
ssh ${PHILAUNCH_SSH_CONN} -p ${PHILAUNCH_SSH_PORT}
~/automation/start-long-task.sh TASKNAME 'command here'
exit
\`\`\`

### Check Background Tasks
\`\`\`
ssh ${PHILAUNCH_SSH_CONN} -p ${PHILAUNCH_SSH_PORT} 'tmux list-sessions'
\`\`\`

### Kill Background Task
\`\`\`
ssh ${PHILAUNCH_SSH_CONN} -p ${PHILAUNCH_SSH_PORT} 'bash ~/automation/home-control.sh kill-task TASKNAME'
\`\`\`

---

## System Commands

### Free Memory Info
\`\`\`
ssh ${PHILAUNCH_SSH_CONN} -p ${PHILAUNCH_SSH_PORT} 'free -h'
\`\`\`

### Disk Usage
\`\`\`
ssh ${PHILAUNCH_SSH_CONN} -p ${PHILAUNCH_SSH_PORT} 'df -h /'
\`\`\`

### Uptime
\`\`\`
ssh ${PHILAUNCH_SSH_CONN} -p ${PHILAUNCH_SSH_PORT} 'uptime -p'
\`\`\`

---

## File Operations

### Download File
\`\`\`
scp -P ${PHILAUNCH_SSH_PORT} ${PHILAUNCH_SSH_CONN}:${PHILAUNCH_HOME}/file.txt ~/storage/downloads/
\`\`\`

### Upload File
\`\`\`
scp -P ${PHILAUNCH_SSH_PORT} ~/storage/downloads/file.txt ${PHILAUNCH_SSH_CONN}:${PHILAUNCH_HOME}/
\`\`\`

---

## Termux Aliases

Add these to your \`~/.bashrc\` in Termux:

\`\`\`bash
# PhiLaunch PC Shortcuts
alias pc='ssh ${PHILAUNCH_SSH_CONN} -p ${PHILAUNCH_SSH_PORT}'
alias pcstatus='ssh ${PHILAUNCH_SSH_CONN} -p ${PHILAUNCH_SSH_PORT} "bash ~/automation/home-control.sh status"'
alias pctasks='ssh ${PHILAUNCH_SSH_CONN} -p ${PHILAUNCH_SSH_PORT} "tmux list-sessions"'
alias pcscripts='ssh ${PHILAUNCH_SSH_CONN} -p ${PHILAUNCH_SSH_PORT} "bash ~/automation/home-control.sh list-scripts"'
alias pclogs='ssh ${PHILAUNCH_SSH_CONN} -p ${PHILAUNCH_SSH_PORT} "bash ~/automation/home-control.sh logs"'
alias pcwow='ssh ${PHILAUNCH_SSH_CONN} -p ${PHILAUNCH_SSH_PORT} "bash ~/automation/launch-script.sh wow_monitor.sh"'
alias pcmem='ssh ${PHILAUNCH_SSH_CONN} -p ${PHILAUNCH_SSH_PORT} "free -h"'
alias pcdisk='ssh ${PHILAUNCH_SSH_CONN} -p ${PHILAUNCH_SSH_PORT} "df -h /"'
alias pcup='ssh ${PHILAUNCH_SSH_CONN} -p ${PHILAUNCH_SSH_PORT} "uptime -p"'
\`\`\`

---

## Termux:Widget Shortcuts

Create these in \`~/.shortcuts/\`:

### PC Status (\`pc-status.sh\`)
\`\`\`bash
#!/data/data/com.termux/files/usr/bin/bash
ssh ${PHILAUNCH_SSH_CONN} -p ${PHILAUNCH_SSH_PORT} 'bash ~/automation/home-control.sh status'
\`\`\`

### WoW Monitor (\`wow-monitor.sh\`)
\`\`\`bash
#!/data/data/com.termux/files/usr/bin/bash
ssh ${PHILAUNCH_SSH_CONN} -p ${PHILAUNCH_SSH_PORT} 'bash ~/automation/start-long-task.sh wow "./wow_monitor.sh"'
echo "WoW monitor started in background"
\`\`\`

### Check Tasks (\`check-tasks.sh\`)
\`\`\`bash
#!/data/data/com.termux/files/usr/bin/bash
ssh ${PHILAUNCH_SSH_CONN} -p ${PHILAUNCH_SSH_PORT} 'tmux list-sessions'
\`\`\`

Make them executable:
\`\`\`bash
chmod +x ~/.shortcuts/*.sh
\`\`\`

---

**Generated**: $(date)
**Configuration**: ${PHILAUNCH_HOME}/config/philaunch.conf
EOF

echo "✓ Generated: $OUTPUT_FILE"
echo ""
echo "Next steps:"
echo "  1. Review the file: cat $OUTPUT_FILE"
echo "  2. Copy commands to your phone (Termux)"
echo "  3. Set up Termux aliases and widgets"
echo ""
