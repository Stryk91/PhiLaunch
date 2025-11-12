# PhiLaunch Phone Shortcuts

**Connection**: `ssh stryk@192.168.254.73 -p 2222`

---

## Quick Status & Monitoring

### System Status
```
ssh stryk@192.168.254.73 -p 2222 'bash ~/automation/home-control.sh status'
```

### List Available Scripts
```
ssh stryk@192.168.254.73 -p 2222 'bash ~/automation/home-control.sh list-scripts'
```

### List Running Tasks
```
ssh stryk@192.168.254.73 -p 2222 'tmux list-sessions'
```

### View Recent Logs
```
ssh stryk@192.168.254.73 -p 2222 'bash ~/automation/home-control.sh logs'
```

---

## Run PhiLaunch Scripts

### WoW Monitor
```
ssh stryk@192.168.254.73 -p 2222 'bash ~/automation/launch-script.sh wow_monitor.sh'
```

### WoW Quick Check
```
ssh stryk@192.168.254.73 -p 2222 'bash ~/automation/launch-script.sh wow_quick_check.sh'
```

### System Info Check
```
ssh stryk@192.168.254.73 -p 2222 'bash ~/automation/launch-script.sh system_info_checker.sh'
```

### Status Monitor
```
ssh stryk@192.168.254.73 -p 2222 'bash ~/automation/launch-script.sh status_monitor.sh'
```

---

## Background Tasks

### Start Background Task
```
ssh stryk@192.168.254.73 -p 2222
~/automation/start-long-task.sh TASKNAME 'command here'
exit
```

### Check Background Tasks
```
ssh stryk@192.168.254.73 -p 2222 'tmux list-sessions'
```

### Attach to Task (interactive)
```
ssh stryk@192.168.254.73 -p 2222
tmux attach -t TASKNAME
# Ctrl+B then D to detach
```

### Kill Background Task
```
ssh stryk@192.168.254.73 -p 2222 'bash ~/automation/home-control.sh kill-task TASKNAME'
```

---

## System Commands

### Restart SSH Server
```
ssh stryk@192.168.254.73 -p 2222 'bash ~/automation/home-control.sh restart-ssh'
```

### Free Memory Info
```
ssh stryk@192.168.254.73 -p 2222 'free -h'
```

### Disk Usage
```
ssh stryk@192.168.254.73 -p 2222 'df -h /'
```

### Uptime
```
ssh stryk@192.168.254.73 -p 2222 'uptime -p'
```

### Network Info
```
ssh stryk@192.168.254.73 -p 2222 'hostname -I'
```

### Process List (top 10)
```
ssh stryk@192.168.254.73 -p 2222 'ps aux --sort=-%mem | head -11'
```

---

## File Operations

### Download File
```
scp -P 2222 stryk@192.168.254.73:/home/STRYK/file.txt ~/Downloads/
```

### Upload File
```
scp -P 2222 ~/file.txt stryk@192.168.254.73:/home/STRYK/
```

### List Files
```
ssh stryk@192.168.254.73 -p 2222 'ls -lh /home/STRYK/'
```

### View File Content
```
ssh stryk@192.168.254.73 -p 2222 'cat /home/STRYK/file.txt'
```

---

## Git Operations

### Git Status
```
ssh stryk@192.168.254.73 -p 2222 'cd /home/STRYK && git status'
```

### Git Pull Latest
```
ssh stryk@192.168.254.73 -p 2222 'cd /home/STRYK && git pull origin main'
```

### Git Commit All
```
ssh stryk@192.168.254.73 -p 2222 'cd /home/STRYK && git add . && git commit -m "Update from phone" && git push'
```

---

## Port Forwarding

### Forward Web Service (8080)
```
ssh -L 8080:localhost:8080 stryk@192.168.254.73 -p 2222
```

### Forward Multiple Ports
```
ssh -L 8080:localhost:8080 -L 3000:localhost:3000 stryk@192.168.254.73 -p 2222
```

### Background Tunnel
```
ssh -N -f -L 8080:localhost:8080 stryk@192.168.254.73 -p 2222
```

---

## Suggested Shortcuts/Keywords

Copy these to your phone's text replacement or shortcut app:

| Keyword | Expands to |
|---------|------------|
| `pcstatus` | `ssh stryk@192.168.254.73 -p 2222 'bash ~/automation/home-control.sh status'` |
| `pctasks` | `ssh stryk@192.168.254.73 -p 2222 'tmux list-sessions'` |
| `pcscripts` | `ssh stryk@192.168.254.73 -p 2222 'bash ~/automation/home-control.sh list-scripts'` |
| `pcwow` | `ssh stryk@192.168.254.73 -p 2222 'bash ~/automation/launch-script.sh wow_monitor.sh'` |
| `pclogs` | `ssh stryk@192.168.254.73 -p 2222 'bash ~/automation/home-control.sh logs'` |
| `pckill` | `ssh stryk@192.168.254.73 -p 2222 'bash ~/automation/home-control.sh kill-task '` |
| `pcgit` | `ssh stryk@192.168.254.73 -p 2222 'cd /home/STRYK && git status'` |
| `pcssh` | `ssh stryk@192.168.254.73 -p 2222` |
| `pcmem` | `ssh stryk@192.168.254.73 -p 2222 'free -h'` |
| `pcdisk` | `ssh stryk@192.168.254.73 -p 2222 'df -h /'` |
| `pcup` | `ssh stryk@192.168.254.73 -p 2222 'uptime -p'` |

---

## iOS Shortcuts App Examples

### Quick Status Check
```
Run Script Over SSH
  Host: 192.168.254.73
  Port: 2222
  User: stryk
  Script: bash ~/automation/home-control.sh status
```

### Launch WoW Monitor
```
Run Script Over SSH
  Host: 192.168.254.73
  Port: 2222
  User: stryk
  Script: bash ~/automation/launch-script.sh wow_monitor.sh
```

---

## Android Termux Aliases

Add to `~/.bashrc` in Termux:

```bash
alias pc='ssh stryk@192.168.254.73 -p 2222'
alias pcstatus='ssh stryk@192.168.254.73 -p 2222 "bash ~/automation/home-control.sh status"'
alias pctasks='ssh stryk@192.168.254.73 -p 2222 "tmux list-sessions"'
alias pcscripts='ssh stryk@192.168.254.73 -p 2222 "bash ~/automation/home-control.sh list-scripts"'
alias pcwow='ssh stryk@192.168.254.73 -p 2222 "bash ~/automation/launch-script.sh wow_monitor.sh"'
```

Then just type: `pcstatus`, `pcwow`, etc.

---

**Last Updated**: 2025-11-12
