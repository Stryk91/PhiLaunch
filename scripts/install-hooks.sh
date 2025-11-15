#!/bin/bash
# Install git hooks for PhiLaunch

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "Installing git hooks..."

# Configure git to use .githooks directory
cd "$REPO_ROOT"
git config core.hooksPath .githooks

echo "✓ Git hooks installed"
echo ""
echo "Hooks are now active:"
echo "  - pre-commit: Checks for secrets, syntax, and shellcheck"
echo ""
echo "To disable hooks temporarily, use: git commit --no-verify"
