#!/usr/bin/env bats
# Unit tests for config loading system

load ../test_helper

setup() {
    setup_test_env
}

teardown() {
    teardown_test_env
}

@test "config loader exists and is executable" {
    [ -f "$PHILAUNCH_ROOT/config/load-config.sh" ]
    [ -x "$PHILAUNCH_ROOT/config/load-config.sh" ]
}

@test "config example file exists" {
    [ -f "$PHILAUNCH_ROOT/config/philaunch.conf.example" ]
}

@test "config loader fails when config file missing" {
    # Try to load config when no config file exists
    export PHILAUNCH_HOME="$TEST_TEMP_DIR"
    run bash -c "source '$PHILAUNCH_ROOT/config/load-config.sh' 2>&1"

    assert_failure
    assert_output_contains "config file not found"
}

@test "config loader succeeds with valid config" {
    # Create config directory and file
    mkdir -p "$TEST_TEMP_DIR/config"
    cp "$TEST_CONFIG" "$TEST_TEMP_DIR/config/philaunch.conf"

    # Load config
    export PHILAUNCH_HOME="$TEST_TEMP_DIR"
    run bash -c "source '$PHILAUNCH_ROOT/config/load-config.sh' && echo \$PHILAUNCH_USER"

    assert_success
    assert_output_contains "testuser"
}

@test "config loader exports required variables" {
    mkdir -p "$TEST_TEMP_DIR/config"
    cp "$TEST_CONFIG" "$TEST_TEMP_DIR/config/philaunch.conf"

    export PHILAUNCH_HOME="$TEST_TEMP_DIR"
    source "$PHILAUNCH_ROOT/config/load-config.sh" 2>/dev/null || true

    # Check required variables are set
    [ -n "$PHILAUNCH_USER" ]
    [ -n "$PHILAUNCH_HOST" ]
    [ -n "$PHILAUNCH_SSH_PORT" ]
    [ -n "$PHILAUNCH_HOME" ]
}

@test "config loader validates required variables" {
    # Create config with missing required variable
    mkdir -p "$TEST_TEMP_DIR/config"
    cat > "$TEST_TEMP_DIR/config/philaunch.conf" << EOF
PHILAUNCH_HOST="192.168.1.100"
PHILAUNCH_SSH_PORT="2222"
EOF

    export PHILAUNCH_HOME="$TEST_TEMP_DIR"
    run bash -c "source '$PHILAUNCH_ROOT/config/load-config.sh' 2>&1"

    assert_failure
    assert_output_contains "PHILAUNCH_USER"
}
