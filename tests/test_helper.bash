#!/bin/bash
# Test helper functions for bats tests

# Get the PhiLaunch root directory
export PHILAUNCH_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
export PHILAUNCH_AUTOMATION="${PHILAUNCH_ROOT}/automation"
export PHILAUNCH_REMOTE_SCRIPTS="${PHILAUNCH_ROOT}/remote-scripts"
export PHILAUNCH_CONFIG="${PHILAUNCH_ROOT}/config"

# Setup test environment
setup_test_env() {
    # Create temporary test directory
    export TEST_TEMP_DIR="$(mktemp -d)"
    export TEST_CONFIG="${TEST_TEMP_DIR}/philaunch.conf"

    # Create mock config for tests
    cat > "$TEST_CONFIG" << EOF
PHILAUNCH_USER="testuser"
PHILAUNCH_HOST="192.168.1.100"
PHILAUNCH_SSH_PORT="2222"
PHILAUNCH_SSH_CONN="testuser@192.168.1.100"
PHILAUNCH_HOME="${TEST_TEMP_DIR}"
PHILAUNCH_USER_HOME="${TEST_TEMP_DIR}"
PHILAUNCH_AUTOMATION_DIR="${TEST_TEMP_DIR}/automation"
PHILAUNCH_REMOTE_SCRIPTS_DIR="${TEST_TEMP_DIR}/remote-scripts"
PHILAUNCH_LOG_DIR="${TEST_TEMP_DIR}/logs"
WOW_SERVER_IP="103.4.115.248"
MONITOR_INTERVAL="60"
WIREGUARD_INTERFACE="wg0"
ENABLE_WAN_WARNINGS="false"
TMUX_SESSION_PREFIX="philaunch"
ENABLE_COLOR_OUTPUT="false"
DEBUG_MODE="false"
EOF

    # Create test directories
    mkdir -p "${TEST_TEMP_DIR}"/{automation,remote-scripts,logs}
}

# Cleanup test environment
teardown_test_env() {
    if [ -n "$TEST_TEMP_DIR" ] && [ -d "$TEST_TEMP_DIR" ]; then
        rm -rf "$TEST_TEMP_DIR"
    fi
}

# Assert command succeeds
assert_success() {
    if [ "$status" -ne 0 ]; then
        echo "Expected success but got exit code: $status"
        echo "Output: $output"
        return 1
    fi
}

# Assert command fails
assert_failure() {
    if [ "$status" -eq 0 ]; then
        echo "Expected failure but got success"
        echo "Output: $output"
        return 1
    fi
}

# Assert output contains string
assert_output_contains() {
    local expected="$1"
    if [[ "$output" != *"$expected"* ]]; then
        echo "Expected output to contain: $expected"
        echo "Actual output: $output"
        return 1
    fi
}

# Assert file exists
assert_file_exists() {
    local file="$1"
    if [ ! -f "$file" ]; then
        echo "Expected file to exist: $file"
        return 1
    fi
}

# Assert file contains string
assert_file_contains() {
    local file="$1"
    local expected="$2"
    if ! grep -q "$expected" "$file"; then
        echo "Expected file $file to contain: $expected"
        return 1
    fi
}

# Skip test if command not available
require_command() {
    local cmd="$1"
    if ! command -v "$cmd" &> /dev/null; then
        skip "Command '$cmd' not available"
    fi
}

# Mock SSH for testing
mock_ssh() {
    # Create a mock ssh command that succeeds
    export PATH="${TEST_TEMP_DIR}/bin:$PATH"
    mkdir -p "${TEST_TEMP_DIR}/bin"
    cat > "${TEST_TEMP_DIR}/bin/ssh" << 'EOF'
#!/bin/bash
echo "Mock SSH: $@"
exit 0
EOF
    chmod +x "${TEST_TEMP_DIR}/bin/ssh"
}

# Mock tmux for testing
mock_tmux() {
    export PATH="${TEST_TEMP_DIR}/bin:$PATH"
    mkdir -p "${TEST_TEMP_DIR}/bin"
    cat > "${TEST_TEMP_DIR}/bin/tmux" << 'EOF'
#!/bin/bash
echo "Mock tmux: $@"
exit 0
EOF
    chmod +x "${TEST_TEMP_DIR}/bin/tmux"
}
