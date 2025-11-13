#!/bin/bash
# PhiLaunch Control Center - Launcher Script
# Checks requirements and launches the GUI

echo "╔════════════════════════════════════════════════════════════╗"
echo "║  PhiLaunch Control Center - Starting...                   ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Check X server
if [ -z "$DISPLAY" ]; then
    echo "✗ Error: No X server detected!"
    echo ""
    echo "WSL users need an X server:"
    echo "  - Windows 11: WSLg (built-in, run 'wsl --update')"
    echo "  - Windows 10: Install VcXsrv or Xming"
    echo ""
    exit 1
fi

echo "✓ X server detected: $DISPLAY"

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "✗ Error: Python 3 not found!"
    exit 1
fi

echo "✓ Python 3 found: $(python3 --version)"

# Check PyQt6
if ! python3 -c "import PyQt6" 2>/dev/null; then
    echo "⚠ PyQt6 not installed!"
    echo ""
    read -p "Install PyQt6 now? (y/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "Installing PyQt6..."
        pip3 install PyQt6
    else
        echo "✗ PyQt6 is required. Install with: pip3 install PyQt6"
        exit 1
    fi
fi

echo "✓ PyQt6 installed"
echo ""
echo "🚀 Launching PhiLaunch Control Center..."
echo ""

# Navigate to GUI directory
cd "$(dirname "$0")"

# Launch GUI
python3 philaunch_gui.py

# Exit code handling
EXIT_CODE=$?
if [ $EXIT_CODE -ne 0 ]; then
    echo ""
    echo "✗ GUI exited with error code: $EXIT_CODE"
    exit $EXIT_CODE
fi
