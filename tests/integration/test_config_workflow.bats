#!/usr/bin/env bats
# Integration tests for complete config workflow

load ../test_helper

setup() {
    setup_test_env
}

teardown() {
    teardown_test_env
}

@test "complete config workflow: create config and use in scripts" {
    # Setup
    mkdir -p "$TEST_TEMP_DIR/config"
    mkdir -p "$TEST_TEMP_DIR/automation"

    # Create config file
    cp "$TEST_CONFIG" "$TEST_TEMP_DIR/config/philaunch.conf"

    # Create a simple test script that uses config
    cat > "$TEST_TEMP_DIR/automation/test.sh" << 'EOF'
#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/../config/load-config.sh"
echo "User: $PHILAUNCH_USER"
echo "Host: $PHILAUNCH_HOST"
EOF
    chmod +x "$TEST_TEMP_DIR/automation/test.sh"

    # Copy config loader to test directory
    cp -r "$PHILAUNCH_ROOT/config" "$TEST_TEMP_DIR/"

    # Run the test script
    run bash "$TEST_TEMP_DIR/automation/test.sh"

    assert_success
    assert_output_contains "User: testuser"
    assert_output_contains "Host: 192.168.1.100"
}

@test "scripts work with environment variables from config" {
    mkdir -p "$TEST_TEMP_DIR/config"
    cp "$TEST_CONFIG" "$TEST_TEMP_DIR/config/philaunch.conf"
    cp -r "$PHILAUNCH_ROOT/config/load-config.sh" "$TEST_TEMP_DIR/config/"

    # Source config and check variables are exported
    export PHILAUNCH_HOME="$TEST_TEMP_DIR"
    run bash -c "source '$TEST_TEMP_DIR/config/load-config.sh' && env | grep PHILAUNCH_"

    assert_success
    assert_output_contains "PHILAUNCH_USER=testuser"
}
