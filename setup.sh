#!/bin/bash
# PhiLaunch Interactive Setup Wizard
# Generates personalized configuration for your environment

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_FILE="${SCRIPT_DIR}/config/philaunch.conf"
EXAMPLE_FILE="${SCRIPT_DIR}/config/philaunch.conf.example"

# ============================================================================
# Helper Functions
# ============================================================================

print_header() {
    echo -e "${CYAN}"
    echo "╔════════════════════════════════════════════════════════════════╗"
    echo "║                                                                ║"
    echo "║              PhiLaunch Setup Wizard v1.0                       ║"
    echo "║         Remote Automation Configuration Generator              ║"
    echo "║                                                                ║"
    echo "╚════════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
    echo ""
}

print_step() {
    echo -e "${BLUE}▶ $1${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

prompt_input() {
    local prompt="$1"
    local default="$2"
    local result

    if [ -n "$default" ]; then
        echo -ne "${CYAN}$prompt${NC} [${YELLOW}$default${NC}]: "
    else
        echo -ne "${CYAN}$prompt${NC}: "
    fi

    read -r result

    if [ -z "$result" ] && [ -n "$default" ]; then
        result="$default"
    fi

    echo "$result"
}

confirm() {
    local prompt="$1"
    local response

    echo -ne "${CYAN}$prompt${NC} [y/N]: "
    read -r response

    case "$response" in
        [yY][eE][sS]|[yY])
            return 0
            ;;
        *)
            return 1
            ;;
    esac
}

# ============================================================================
# Detection Functions
# ============================================================================

detect_current_user() {
    echo "$USER"
}

detect_hostname() {
    # Try to get LAN IP
    local ip=$(hostname -I 2>/dev/null | awk '{print $1}')
    if [ -z "$ip" ]; then
        ip=$(ip addr show | grep 'inet ' | grep -v '127.0.0.1' | awk '{print $2}' | cut -d/ -f1 | head -1)
    fi
    echo "$ip"
}

check_ssh_server() {
    if systemctl is-active --quiet ssh || systemctl is-active --quiet sshd; then
        return 0
    else
        return 1
    fi
}

detect_ssh_port() {
    # Try to detect SSH port from config
    local port=$(grep "^Port " /etc/ssh/sshd_config 2>/dev/null | awk '{print $2}')
    if [ -z "$port" ]; then
        port="22"
    fi
    echo "$port"
}

# ============================================================================
# Main Setup Flow
# ============================================================================

main() {
    print_header

    # Check if config already exists
    if [ -f "$CONFIG_FILE" ]; then
        print_warning "Configuration file already exists: $CONFIG_FILE"
        echo ""
        if ! confirm "Do you want to reconfigure (this will backup the old config)?"; then
            echo "Setup cancelled."
            exit 0
        fi

        # Backup existing config
        BACKUP_FILE="${CONFIG_FILE}.backup.$(date +%Y%m%d_%H%M%S)"
        cp "$CONFIG_FILE" "$BACKUP_FILE"
        print_success "Backed up existing config to: $BACKUP_FILE"
        echo ""
    fi

    # ========================================================================
    # Step 1: Detect Environment
    # ========================================================================

    print_step "Step 1: Detecting your environment..."
    echo ""

    DETECTED_USER=$(detect_current_user)
    DETECTED_HOST=$(detect_hostname)
    DETECTED_PORT=$(detect_ssh_port)
    DETECTED_HOME="$HOME"

    print_success "Current user: $DETECTED_USER"
    print_success "Detected IP: ${DETECTED_HOST:-"(not found)"}"
    print_success "SSH port: $DETECTED_PORT"
    print_success "Home directory: $DETECTED_HOME"
    echo ""

    # Check SSH server
    if check_ssh_server; then
        print_success "SSH server is running"
    else
        print_warning "SSH server is not running or not detected"
        echo "  You may need to install and start SSH server:"
        echo "    sudo apt install openssh-server"
        echo "    sudo systemctl start ssh"
    fi
    echo ""

    # ========================================================================
    # Step 2: Get User Input
    # ========================================================================

    print_step "Step 2: Configure connection settings..."
    echo ""

    CONFIG_USER=$(prompt_input "SSH username" "$DETECTED_USER")
    CONFIG_HOST=$(prompt_input "Server IP address (LAN)" "$DETECTED_HOST")
    CONFIG_PORT=$(prompt_input "SSH port" "$DETECTED_PORT")
    CONFIG_HOME=$(prompt_input "PhiLaunch directory" "${DETECTED_HOME}/PhiLaunch")

    echo ""

    # ========================================================================
    # Step 3: Optional Settings
    # ========================================================================

    print_step "Step 3: Optional settings..."
    echo ""

    if confirm "Configure WoW monitoring? (optional)"; then
        WOW_IP=$(prompt_input "WoW server IP" "103.4.115.248")
        MONITOR_INT=$(prompt_input "Monitoring interval (seconds)" "60")
    else
        WOW_IP="103.4.115.248"
        MONITOR_INT="60"
    fi

    echo ""

    if confirm "Enable WAN access warnings? (reminds you to use VPN)"; then
        WAN_WARNINGS="true"
    else
        WAN_WARNINGS="false"
    fi

    echo ""

    if confirm "Enable debug mode? (verbose logging)"; then
        DEBUG="true"
    else
        DEBUG="false"
    fi

    echo ""

    # ========================================================================
    # Step 4: Generate Config
    # ========================================================================

    print_step "Step 4: Generating configuration..."
    echo ""

    cat > "$CONFIG_FILE" << EOF
# PhiLaunch Configuration
# Generated by setup wizard on $(date)
# DO NOT commit this file to version control

# ============================================================================
# SERVER CONNECTION SETTINGS
# ============================================================================

PHILAUNCH_USER="$CONFIG_USER"
PHILAUNCH_HOST="$CONFIG_HOST"
PHILAUNCH_SSH_PORT="$CONFIG_PORT"
PHILAUNCH_SSH_CONN="\${PHILAUNCH_USER}@\${PHILAUNCH_HOST}"

# ============================================================================
# DIRECTORY PATHS
# ============================================================================

PHILAUNCH_HOME="$CONFIG_HOME"
PHILAUNCH_USER_HOME="$HOME"
PHILAUNCH_AUTOMATION_DIR="\${PHILAUNCH_HOME}/automation"
PHILAUNCH_REMOTE_SCRIPTS_DIR="\${PHILAUNCH_HOME}/remote-scripts"
PHILAUNCH_LOG_DIR="\${PHILAUNCH_HOME}/logs"

# ============================================================================
# MONITORING SETTINGS
# ============================================================================

WOW_SERVER_IP="$WOW_IP"
MONITOR_INTERVAL="$MONITOR_INT"

# ============================================================================
# NETWORK SETTINGS
# ============================================================================

WIREGUARD_INTERFACE="wg0"
ENABLE_WAN_WARNINGS="$WAN_WARNINGS"

# ============================================================================
# ADVANCED SETTINGS
# ============================================================================

TMUX_SESSION_PREFIX="philaunch"
ENABLE_COLOR_OUTPUT="true"
DEBUG_MODE="$DEBUG"
EOF

    chmod 600 "$CONFIG_FILE"  # Protect config file
    print_success "Configuration file created: $CONFIG_FILE"
    echo ""

    # ========================================================================
    # Step 5: Update .gitignore
    # ========================================================================

    print_step "Step 5: Protecting sensitive files..."
    echo ""

    GITIGNORE_FILE="${SCRIPT_DIR}/.gitignore"

    if [ -f "$GITIGNORE_FILE" ]; then
        if ! grep -q "config/philaunch.conf" "$GITIGNORE_FILE"; then
            echo "" >> "$GITIGNORE_FILE"
            echo "# PhiLaunch personal configuration (contains sensitive info)" >> "$GITIGNORE_FILE"
            echo "config/philaunch.conf" >> "$GITIGNORE_FILE"
            echo "config/*.backup.*" >> "$GITIGNORE_FILE"
            print_success "Added config to .gitignore"
        else
            print_success ".gitignore already protects config file"
        fi
    else
        print_warning ".gitignore not found - consider creating one"
    fi
    echo ""

    # ========================================================================
    # Step 6: Create Log Directory
    # ========================================================================

    print_step "Step 6: Creating directories..."
    echo ""

    mkdir -p "${CONFIG_HOME}/logs"
    print_success "Created logs directory"
    echo ""

    # ========================================================================
    # Step 7: Test Configuration
    # ========================================================================

    print_step "Step 7: Testing configuration..."
    echo ""

    # Source the config
    if source "$CONFIG_FILE"; then
        print_success "Configuration loads successfully"
    else
        print_error "Failed to load configuration"
        exit 1
    fi

    # Test SSH (optional)
    if confirm "Test SSH connection now?"; then
        echo ""
        echo "Testing: ssh -p $CONFIG_PORT $CONFIG_USER@$CONFIG_HOST 'echo Connection successful'"
        echo ""

        if ssh -p "$CONFIG_PORT" -o ConnectTimeout=5 -o BatchMode=yes "$CONFIG_USER@$CONFIG_HOST" 'echo "✓ SSH connection successful"' 2>/dev/null; then
            print_success "SSH connection works!"
        else
            print_warning "SSH connection failed"
            echo "  This could mean:"
            echo "    - SSH server is not running"
            echo "    - SSH keys not set up (try: ssh-copy-id -p $CONFIG_PORT $CONFIG_USER@$CONFIG_HOST)"
            echo "    - Firewall blocking port $CONFIG_PORT"
            echo "    - Incorrect IP address or port"
            echo ""
            echo "  You can test manually with:"
            echo "    ssh -p $CONFIG_PORT $CONFIG_USER@$CONFIG_HOST"
        fi
    fi

    echo ""

    # ========================================================================
    # Step 8: Summary
    # ========================================================================

    echo -e "${GREEN}"
    echo "╔════════════════════════════════════════════════════════════════╗"
    echo "║                                                                ║"
    echo "║                  Setup Complete! 🚀                            ║"
    echo "║                                                                ║"
    echo "╚════════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
    echo ""

    print_step "Configuration Summary:"
    echo ""
    echo "  Connection: ssh -p $CONFIG_PORT $CONFIG_USER@$CONFIG_HOST"
    echo "  Home:       $CONFIG_HOME"
    echo "  Config:     $CONFIG_FILE"
    echo ""

    print_step "Next Steps:"
    echo ""
    echo "  1. Set up SSH keys (if not already done):"
    echo "     ${YELLOW}ssh-copy-id -p $CONFIG_PORT $CONFIG_USER@$CONFIG_HOST${NC}"
    echo ""
    echo "  2. Test the connection:"
    echo "     ${YELLOW}ssh -p $CONFIG_PORT $CONFIG_USER@$CONFIG_HOST${NC}"
    echo ""
    echo "  3. Try running a script:"
    echo "     ${YELLOW}bash automation/home-control.sh status${NC}"
    echo ""
    echo "  4. Update your phone shortcuts:"
    echo "     ${YELLOW}./tools/generate-phone-shortcuts.sh${NC} (coming soon)"
    echo ""

    print_warning "Remember: Never commit config/philaunch.conf to git!"
    echo ""

}

# Run main function
main "$@"
