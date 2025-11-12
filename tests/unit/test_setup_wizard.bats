#!/usr/bin/env bats
# Unit tests for setup wizard

load ../test_helper

setup() {
    setup_test_env
}

teardown() {
    teardown_test_env
}

@test "setup wizard exists and is executable" {
    [ -f "$PHILAUNCH_ROOT/setup.sh" ]
    [ -x "$PHILAUNCH_ROOT/setup.sh" ]
}

@test "setup wizard has valid bash syntax" {
    run bash -n "$PHILAUNCH_ROOT/setup.sh"
    assert_success
}

@test "setup wizard creates config directory" {
    # This is a placeholder - actual interactive testing would need expect/autoexpect
    [ -d "$PHILAUNCH_ROOT/config" ]
}

@test "setup wizard has proper shebang" {
    head -1 "$PHILAUNCH_ROOT/setup.sh" | grep -q "#!/bin/bash"
}
