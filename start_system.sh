#!/bin/bash
# @SCRIPT_LAUNCHER_LOCAL - Script written by this computer
# PhiGEN System Starter - WSL/Linux
# Convenience wrapper for scripts/linux/start_phigen_bot.sh

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
"$SCRIPT_DIR/scripts/linux/start_phigen_bot.sh" "$@"
