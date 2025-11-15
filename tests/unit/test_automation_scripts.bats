#!/usr/bin/env bats
# Unit tests for automation scripts

load ../test_helper

setup() {
    setup_test_env
    mock_ssh
    mock_tmux
}

teardown() {
    teardown_test_env
}

@test "home-control.sh exists and is executable" {
    [ -f "$PHILAUNCH_ROOT/automation/home-control.sh" ]
    [ -x "$PHILAUNCH_ROOT/automation/home-control.sh" ]
}

@test "home-control.sh has valid syntax" {
    run bash -n "$PHILAUNCH_ROOT/automation/home-control.sh"
    assert_success
}

@test "home-control.sh shows help when no argument" {
    # Create test config
    mkdir -p "$TEST_TEMP_DIR/config"
    cp "$TEST_CONFIG" "$TEST_TEMP_DIR/config/philaunch.conf"

    cd "$PHILAUNCH_ROOT/automation"
    run bash -c "PHILAUNCH_HOME='$TEST_TEMP_DIR' ./home-control.sh 2>&1"

    assert_success
    assert_output_contains "HOME AUTOMATION CONTROL"
}

@test "launch-script.sh exists and is executable" {
    [ -f "$PHILAUNCH_ROOT/automation/launch-script.sh" ]
    [ -x "$PHILAUNCH_ROOT/automation/launch-script.sh" ]
}

@test "launch-script.sh has valid syntax" {
    run bash -n "$PHILAUNCH_ROOT/automation/launch-script.sh"
    assert_success
}

@test "launch-script.sh lists scripts when no argument" {
    mkdir -p "$TEST_TEMP_DIR/config"
    cp "$TEST_CONFIG" "$TEST_TEMP_DIR/config/philaunch.conf"

    cd "$PHILAUNCH_ROOT/automation"
    run bash -c "PHILAUNCH_HOME='$TEST_TEMP_DIR' ./launch-script.sh 2>&1"

    # Should show available scripts message
    assert_output_contains "Available scripts"
}
