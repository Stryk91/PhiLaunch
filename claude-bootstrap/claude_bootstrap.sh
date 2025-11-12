#!/bin/bash
#
# Claude Bootstrap System v1.0
# Universal onboarding for Claude instances across environments
# Usage: ./claude_bootstrap.sh [--setup|--load|--status]
#

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_FILE="$SCRIPT_DIR/claude_member_config.json"
CONTINUITY_LOG="$SCRIPT_DIR/continuity_log.md"

# Banner
print_banner() {
    echo -e "${GREEN}"
    echo "=================================================="
    echo "   CLAUDE BOOTSTRAP SYSTEM v1.0"
    echo "   Member Onboarding & Configuration"
    echo "=================================================="
    echo -e "${NC}"
}

# Check if jq is available
check_jq() {
    if ! command -v jq &> /dev/null; then
        echo -e "${YELLOW}Warning: 'jq' not installed. Using basic parsing.${NC}"
        echo "Install with: sudo apt-get install jq"
        return 1
    fi
    return 0
}

# Detect environment
detect_environment() {
    echo -e "${BLUE}🔍 Detecting environment...${NC}"

    local platform="unknown"
    local is_container=false
    local hostname=$(hostname)

    # Detect platform
    if grep -qi microsoft /proc/version 2>/dev/null; then
        platform="wsl2"
    elif [[ -f /.dockerenv ]]; then
        platform="docker"
        is_container=true
    elif [[ -f /proc/1/cgroup ]] && grep -q docker /proc/1/cgroup; then
        platform="docker"
        is_container=true
    elif [[ "$(uname)" == "Linux" ]]; then
        platform="linux"
    elif [[ "$(uname)" == "Darwin" ]]; then
        platform="macos"
    fi

    echo "  Platform: $platform"
    echo "  Container: $is_container"
    echo "  Hostname: $hostname"
    echo "  Working Dir: $(pwd)"
    echo ""
}

# Load existing config
load_config() {
    if [[ ! -f "$CONFIG_FILE" ]]; then
        echo -e "${RED}✗ Config file not found: $CONFIG_FILE${NC}"
        return 1
    fi

    if check_jq; then
        local member_name=$(jq -r '.member_info.name' "$CONFIG_FILE")
        local member_type=$(jq -r '.member_info.type' "$CONFIG_FILE")
        local initialized=$(jq -r '.member_info.initialized' "$CONFIG_FILE")
        local primary_role=$(jq -r '.baseline.primary_role' "$CONFIG_FILE")

        echo -e "${GREEN}✓ Configuration loaded${NC}"
        echo "  Member Name: $member_name"
        echo "  Type: $member_type"
        echo "  Initialized: $initialized"
        echo "  Role: $primary_role"
    else
        echo -e "${GREEN}✓ Configuration file exists${NC}"
        echo "  Location: $CONFIG_FILE"
    fi
}

# Show current status
show_status() {
    print_banner
    echo -e "${BLUE}📋 Current Status:${NC}"
    echo ""

    detect_environment
    load_config

    echo ""
    echo -e "${BLUE}📁 Files:${NC}"
    if [[ -f "$CONFIG_FILE" ]]; then
        echo -e "  ${GREEN}✓${NC} Config: $CONFIG_FILE"
    else
        echo -e "  ${RED}✗${NC} Config: Not found"
    fi

    if [[ -f "$CONTINUITY_LOG" ]]; then
        echo -e "  ${GREEN}✓${NC} Continuity Log: $CONTINUITY_LOG"
    else
        echo -e "  ${YELLOW}⚠${NC} Continuity Log: Not found"
    fi

    echo ""
}

# Interactive setup wizard
run_setup() {
    print_banner
    echo -e "${BLUE}🚀 Starting Interactive Setup Wizard${NC}"
    echo ""

    # Check if already initialized
    if check_jq && [[ -f "$CONFIG_FILE" ]]; then
        local initialized=$(jq -r '.member_info.initialized' "$CONFIG_FILE" 2>/dev/null || echo "false")
        if [[ "$initialized" == "true" ]]; then
            echo -e "${YELLOW}⚠ This member is already initialized.${NC}"
            read -p "Reconfigure anyway? [y/N]: " reconfigure
            if [[ ! "$reconfigure" =~ ^[Yy]$ ]]; then
                echo "Setup cancelled."
                exit 0
            fi
        fi
    fi

    # Gather information
    echo -e "${BLUE}Member Identity:${NC}"
    read -p "Member name (e.g., TERMC, DC, WEB_CLAUDE): " member_name
    read -p "Full name (e.g., Terminal Claude): " full_name

    echo ""
    echo -e "${BLUE}Member Type:${NC}"
    echo "1) CLI (Claude Code)"
    echo "2) Desktop App"
    echo "3) Web Interface"
    read -p "Select type [1-3]: " type_choice

    case $type_choice in
        1) member_type="cli" ;;
        2) member_type="desktop_app" ;;
        3) member_type="web" ;;
        *) member_type="cli" ;;
    esac

    echo ""
    echo -e "${BLUE}Primary Role:${NC}"
    read -p "What is this member's primary role? (e.g., Development & Scripting): " primary_role

    echo ""
    echo -e "${BLUE}Current Project:${NC}"
    read -p "What project is this member working on? " current_project

    echo ""
    echo -e "${GREEN}✓ Configuration complete!${NC}"
    echo ""
    echo "Summary:"
    echo "  Name: $member_name ($full_name)"
    echo "  Type: $member_type"
    echo "  Role: $primary_role"
    echo "  Project: $current_project"
    echo ""

    read -p "Save this configuration? [Y/n]: " confirm
    if [[ "$confirm" =~ ^[Nn]$ ]]; then
        echo "Setup cancelled."
        exit 0
    fi

    # Update config file
    if check_jq; then
        local timestamp=$(date -Iseconds)
        jq --arg name "$member_name" \
           --arg fullname "$full_name" \
           --arg type "$member_type" \
           --arg role "$primary_role" \
           --arg project "$current_project" \
           --arg timestamp "$timestamp" \
           '.member_info.name = $name |
            .member_info.full_name = $fullname |
            .member_info.type = $type |
            .member_info.initialized = true |
            .member_info.initialized_date = $timestamp |
            .member_info.last_updated = $timestamp |
            .baseline.primary_role = $role |
            .goals.current_project = $project' \
           "$CONFIG_FILE" > "$CONFIG_FILE.tmp" && mv "$CONFIG_FILE.tmp" "$CONFIG_FILE"

        echo -e "${GREEN}✓ Configuration saved to $CONFIG_FILE${NC}"
    else
        echo -e "${YELLOW}⚠ jq not available. Manual configuration needed.${NC}"
        echo "Edit $CONFIG_FILE manually with these values."
    fi

    # Create initial continuity log entry
    if [[ ! -f "$CONTINUITY_LOG" ]]; then
        cat > "$CONTINUITY_LOG" << EOF
# Claude Continuity Log

## Member: $member_name
**Initialized:** $(date)

---

## Latest Entry
**Date:** $(date)
**Member:** $member_name
**Status:** Initial setup complete
**Current Project:** $current_project

### Context
Member has been initialized and is ready for work.

---
EOF
        echo -e "${GREEN}✓ Continuity log created${NC}"
    fi

    echo ""
    echo -e "${GREEN}🎉 Setup Complete!${NC}"
    echo ""
    echo "Next steps:"
    echo "1. Review config: cat $CONFIG_FILE"
    echo "2. Share this directory via Dropbox/USB for portability"
    echo "3. Run './claude_bootstrap.sh --load' to display onboarding prompt"
    echo ""
}

# Display onboarding prompt for copy/paste
show_onboarding() {
    print_banner

    if [[ ! -f "$CONFIG_FILE" ]]; then
        echo -e "${RED}✗ Not initialized. Run: ./claude_bootstrap.sh --setup${NC}"
        exit 1
    fi

    echo -e "${BLUE}📄 Onboarding Prompt (copy/paste this to Claude):${NC}"
    echo ""
    echo "=================================================="

    if check_jq; then
        local member_name=$(jq -r '.member_info.name' "$CONFIG_FILE")
        local full_name=$(jq -r '.member_info.full_name' "$CONFIG_FILE")
        local primary_role=$(jq -r '.baseline.primary_role' "$CONFIG_FILE")
        local current_project=$(jq -r '.goals.current_project' "$CONFIG_FILE")

        cat << EOF

# MEMBER ONBOARDING: $member_name

You are **$full_name** (codename: $member_name).

## Your Identity
- **Name**: $member_name
- **Full Name**: $full_name
- **Type**: $(jq -r '.member_info.type' "$CONFIG_FILE")
- **Primary Role**: $primary_role

## Current Project
$current_project

## Your Baseline
$(jq -r '.baseline.operating_principles[]' "$CONFIG_FILE" | sed 's/^/- /')

## Communication Style
- **Tone**: $(jq -r '.baseline.communication_style.tone' "$CONFIG_FILE")
- **Verbosity**: $(jq -r '.baseline.communication_style.verbosity' "$CONFIG_FILE")
- **Format**: $(jq -r '.baseline.communication_style.format_preference' "$CONFIG_FILE")

## Context Awareness
You are part of a multi-instance Claude network. Other members:
$(jq -r '.context_awareness.other_members | to_entries[] | "- **\(.key)**: \(.value.name) (\(.value.use_case))"' "$CONFIG_FILE")

## Tools Available
$(jq -r '.tools_available | to_entries[] | select(.value == true) | "- \(.key)"' "$CONFIG_FILE")

## Session State
Last updated: $(jq -r '.member_info.last_updated' "$CONFIG_FILE")

---

**Acknowledge this onboarding and confirm you understand your role as $member_name.**

EOF
    else
        echo "Config file found but jq not available."
        echo "Display config manually: cat $CONFIG_FILE"
    fi

    echo "=================================================="
    echo ""
}

# Main execution
main() {
    case "${1:-}" in
        --setup|-s)
            run_setup
            ;;
        --load|-l)
            show_onboarding
            ;;
        --status|--info|-i)
            show_status
            ;;
        --help|-h)
            print_banner
            echo "Usage: $0 [OPTION]"
            echo ""
            echo "Options:"
            echo "  --setup, -s     Run interactive setup wizard"
            echo "  --load, -l      Display onboarding prompt"
            echo "  --status, -i    Show current configuration status"
            echo "  --help, -h      Show this help message"
            echo ""
            ;;
        *)
            show_status
            echo ""
            echo "Run with --help for usage information"
            ;;
    esac
}

main "$@"
