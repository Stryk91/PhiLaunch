#!/bin/bash
# @SCRIPT_LAUNCHER_LOCAL - Script written by this computer
# Ultimate Hack Launch - Split Screen Edition

# Check if tmux is installed
if ! command -v tmux &> /dev/null; then
    echo "Installing tmux..."
    sudo apt update && sudo apt install -y tmux
fi

# Kill any existing tmux session named 'hack'
tmux kill-session -t hack 2>/dev/null

# Create new tmux session with split panes
tmux new-session -d -s hack -x "$(tput cols)" -y "$(tput lines)"

# Split vertically (left and right panes)
tmux split-window -h -t hack

# Left pane (60% width) - Run the main hack script
tmux send-keys -t hack:0.0 "bash ~/fake_hack_matrix.sh" C-m

# Right pane (40% width) - Run complementary effects
tmux send-keys -t hack:0.1 "bash ~/hack_right_pane.sh" C-m

# Attach to the session
tmux attach-session -t hack
