#!/bin/bash
# PhiLaunch Dependency Checker
# Verifies all required tools and dependencies are installed

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# CI mode flag
CI_MODE=false
if [ "$1" = "--ci" ]; then
    CI_MODE=true
fi

# Track status
MISSING_REQUIRED=()
MISSING_OPTIONAL=()
ALL_GOOD=true

# Print functions
print_header() {
    if [ "$CI_MODE" = false ]; then
        echo -e "${BLUE}================================${NC}"
        echo -e "${BLUE}PhiLaunch Dependency Checker${NC}"
        echo -e "${BLUE}================================${NC}"
        echo ""
    else
        echo "=== PhiLaunch Dependency Check ==="
        echo ""
    fi
}

print_section() {
    if [ "$CI_MODE" = false ]; then
        echo -e "${BLUE}▶ $1${NC}"
    else
        echo "▶ $1"
    fi
}

print_success() {
    if [ "$CI_MODE" = false ]; then
        echo -e "  ${GREEN}✓${NC} $1"
    else
        echo "  ✓ $1"
    fi
}

print_warning() {
    if [ "$CI_MODE" = false ]; then
        echo -e "  ${YELLOW}⚠${NC} $1"
    else
        echo "  ⚠ $1"
    fi
}

print_error() {
    if [ "$CI_MODE" = false ]; then
        echo -e "  ${RED}✗${NC} $1"
    else
        echo "  ✗ $1"
    fi
}

# Check if command exists
check_command() {
    local cmd="$1"
    local required="$2"
    local min_version="$3"

    if command -v "$cmd" &> /dev/null; then
        local version=""
        case "$cmd" in
            git)
                version=$(git --version 2>/dev/null | awk '{print $3}')
                ;;
            bash)
                version=$(bash --version 2>/dev/null | head -1 | awk '{print $4}')
                ;;
            python3)
                version=$(python3 --version 2>/dev/null | awk '{print $2}')
                ;;
            node)
                version=$(node --version 2>/dev/null | sed 's/v//')
                ;;
            docker)
                version=$(docker --version 2>/dev/null | awk '{print $3}' | sed 's/,//')
                ;;
            tmux)
                version=$(tmux -V 2>/dev/null | awk '{print $2}')
                ;;
            *)
                version="installed"
                ;;
        esac

        print_success "$cmd ($version)"
        return 0
    else
        if [ "$required" = "yes" ]; then
            print_error "$cmd (required, not found)"
            MISSING_REQUIRED+=("$cmd")
            ALL_GOOD=false
        else
            print_warning "$cmd (optional, not found)"
            MISSING_OPTIONAL+=("$cmd")
        fi
        return 1
    fi
}

# Main checks
print_header

print_section "Required Dependencies"
check_command "bash" "yes"
check_command "git" "yes"
check_command "ssh" "yes"
check_command "tmux" "yes"

echo ""
print_section "Shell Utilities"
check_command "grep" "yes"
check_command "sed" "yes"
check_command "awk" "yes"
check_command "curl" "yes"

echo ""
print_section "Optional Tools"
check_command "docker" "no"
check_command "python3" "no"
check_command "node" "no"
check_command "jq" "no"
check_command "mtr" "no"
check_command "shellcheck" "no"
check_command "bats" "no"

echo ""
print_section "Configuration Check"

# Check if setup has been run
if [ -f "config/philaunch.conf" ]; then
    print_success "Config file exists (setup.sh has been run)"
elif [ -f "config/philaunch.conf.example" ]; then
    print_warning "Config template exists but setup.sh not run yet"
else
    print_error "Config system not found"
    ALL_GOOD=false
fi

# Check key directories
if [ -d "automation" ]; then
    print_success "automation/ directory present"
else
    print_error "automation/ directory missing"
    ALL_GOOD=false
fi

if [ -d "config" ]; then
    print_success "config/ directory present"
else
    print_error "config/ directory missing"
    ALL_GOOD=false
fi

echo ""
print_section "Testing Infrastructure"

if [ -d "tests" ]; then
    print_success "tests/ directory present"
else
    print_warning "tests/ directory not found"
fi

if [ -f ".github/workflows/ci.yml" ]; then
    print_success "CI/CD workflow configured"
else
    print_warning "CI/CD workflow not found"
fi

# Summary
echo ""
if [ "$CI_MODE" = false ]; then
    echo -e "${BLUE}================================${NC}"
    echo -e "${BLUE}Summary${NC}"
    echo -e "${BLUE}================================${NC}"
else
    echo "=== Summary ==="
fi
echo ""

if [ ${#MISSING_REQUIRED[@]} -gt 0 ]; then
    if [ "$CI_MODE" = false ]; then
        echo -e "${RED}Missing Required Dependencies:${NC}"
    else
        echo "Missing Required Dependencies:"
    fi
    for dep in "${MISSING_REQUIRED[@]}"; do
        echo "  - $dep"
    done
    echo ""
fi

if [ ${#MISSING_OPTIONAL[@]} -gt 0 ]; then
    if [ "$CI_MODE" = false ]; then
        echo -e "${YELLOW}Missing Optional Dependencies:${NC}"
    else
        echo "Missing Optional Dependencies:"
    fi
    for dep in "${MISSING_OPTIONAL[@]}"; do
        echo "  - $dep"
    done
    echo ""
fi

if [ "$ALL_GOOD" = true ] && [ ${#MISSING_REQUIRED[@]} -eq 0 ]; then
    if [ "$CI_MODE" = false ]; then
        echo -e "${GREEN}✓ All required dependencies are installed!${NC}"
    else
        echo "✓ All required dependencies are installed!"
    fi

    if [ ${#MISSING_OPTIONAL[@]} -gt 0 ]; then
        echo ""
        echo "Optional dependencies are missing but PhiLaunch will work without them."
        echo "Install them for additional features:"
        echo ""
        echo "  Ubuntu/Debian:"
        echo "    sudo apt install docker.io python3 nodejs jq mtr-tiny shellcheck bats"
        echo ""
        echo "  macOS:"
        echo "    brew install docker python3 node jq mtr shellcheck bats-core"
    fi

    exit 0
else
    if [ "$CI_MODE" = false ]; then
        echo -e "${RED}✗ Some required dependencies are missing${NC}"
    else
        echo "✗ Some required dependencies are missing"
    fi
    echo ""
    echo "Install missing dependencies:"
    echo ""
    echo "  Ubuntu/Debian:"
    echo "    sudo apt update"
    echo "    sudo apt install git openssh-client tmux grep sed gawk curl"
    echo ""
    echo "  macOS:"
    echo "    brew install git openssh tmux grep gnu-sed gawk curl"
    echo ""

    exit 1
fi
