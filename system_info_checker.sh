#!/bin/bash
# @SCRIPT_LAUNCHER_LOCAL - Script written by this computer
#
# System Info Checker
# Purpose: Display comprehensive system information
# Dependencies: python3, df, uname, free, uptime
# Sudo: Not required
#

echo "========================================"
echo "   SYSTEM INFORMATION CHECKER v1.0"
echo "========================================"
echo ""

# OS Information
echo "📋 Operating System:"
echo "  - OS Type: $(uname -s)"
echo "  - Kernel: $(uname -r)"
echo "  - Architecture: $(uname -m)"
echo "  - Hostname: $(hostname)"
echo ""

# Python Version
echo "🐍 Python Information:"
if command -v python3 &> /dev/null; then
    echo "  - Python3: $(python3 --version)"
    echo "  - Location: $(which python3)"
else
    echo "  - Python3: NOT FOUND"
fi
echo ""

# Memory Information
echo "💾 Memory Information:"
if command -v free &> /dev/null; then
    free -h | grep -E "Mem:|Swap:"
else
    echo "  - free command not available"
fi
echo ""

# Disk Usage
echo "💿 Disk Usage:"
df -h | grep -E "Filesystem|/dev/|tmpfs" | head -5
echo ""

# System Uptime
echo "⏱️  System Uptime:"
uptime
echo ""

# Current User
echo "👤 Current User:"
echo "  - Username: $USER"
echo "  - Home: $HOME"
echo "  - Shell: $SHELL"
echo ""

# Network Info (basic)
echo "🌐 Network:"
if command -v ip &> /dev/null; then
    echo "  - IP Addresses:"
    ip -4 addr show | grep inet | awk '{print "    " $2}' | head -3
else
    echo "  - ip command not available"
fi
echo ""

# Environment
echo "🔧 Environment Variables (sample):"
echo "  - PATH entries: $(echo $PATH | tr ':' '\n' | wc -l)"
echo "  - TERM: $TERM"
echo "  - PWD: $PWD"
echo ""

echo "========================================"
echo "✅ System check complete!"
echo "========================================"
