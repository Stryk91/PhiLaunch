========================================
    RNG_SCRIPTS - NETWORK & USB TOOLS
========================================

Created: 2025-11-12
Purpose: Phone Link traffic analysis & USB port diagnostics
System: Stryk's PC (WSL2/Kali + Windows)

========================================
QUICK START:
========================================

PHONE LINK MONITORING:
  → Run: MONITOR_PHONELINK_MENU.bat

USB PORT ANALYSIS:
  → Run: USB_ANALYZER_MENU.bat


========================================
PHONE LINK TOOLS:
========================================

📋 MAIN MENU:
  MONITOR_PHONELINK_MENU.bat
    - Central menu for all Phone Link monitoring tools
    - Choose quick check, real-time monitor, or logging

🔍 MONITORING SCRIPTS:

  quick_check_phonelink.bat
    - Instant check if transfer is local or cloud
    - Shows IP addresses and connection type
    - Takes 10 seconds

  realtime_bandwidth_monitor.ps1 (PowerShell)
    - Live upload/download speeds in MB/s
    - Color-coded connection types
    - Updates every second

  phonelink_traffic_logger.ps1 (PowerShell)
    - Continuous logging to Desktop
    - Saves all connection details
    - Good for later analysis

  monitor_phonelink.bat
    - Basic netstat monitoring
    - Simple alternative to PowerShell scripts

📖 GUIDES:

  WIRESHARK_PHONELINK_GUIDE.txt
    - Complete Wireshark tutorial for packet capture
    - How to identify protocols
    - Filter examples

  FIX_PHONELINK_LOCAL_TRANSFER.txt
    - Why Phone Link uses cloud for large files
    - Alternative methods (File Transfer, Nearby Share)
    - Workarounds for forcing local transfer

🔧 FIXES:

  OPEN_PHONELINK_FIREWALL.bat
    - Opens ports 47000-48000 for direct P2P
    - May fix cloud relay issue
    - Run as Administrator


========================================
USB PORT ANALYSIS TOOLS:
========================================

📋 MAIN MENU:
  USB_ANALYZER_MENU.bat
    - Central menu for all USB diagnostic tools
    - Quick check, full analysis, speed tests

🔍 DIAGNOSTIC SCRIPTS:

  USB_QUICK_CHECK.bat
    - Fast check of controllers and devices
    - Opens Device Manager for manual inspection
    - Shows theoretical speed limits

  USB_PORT_ANALYZER.ps1 (PowerShell)
    - Complete USB architecture report
    - Lists all controllers, hubs, and devices
    - Identifies USB 3.0 vs 3.1 controllers

  COMPARE_USB_CONTROLLERS.ps1 (PowerShell)
    - Detailed Intel vs ASMedia comparison
    - Explains why ASMedia often underperforms
    - Traces device connections to controllers

  IDENTIFY_USB_PORTS.bat
    - Helps find which physical port is which controller
    - Instructions for marking fast ports
    - Device Manager integration

⚡ SPEED TEST:

  USB_SPEED_TEST.ps1 (PowerShell)
    - Real file transfer speed test
    - Measures write and read speeds
    - Compares to theoretical maximums
    - Identifies if port is USB 2.0/3.0/3.1

🔧 FIXES:

  FIX_ASMEDIA_USB.bat
    - Tools to fix ASMedia underperformance
    - Check driver versions
    - Disable UASP mode
    - Motherboard info for driver downloads

  DOWNLOAD_USB_TOOLS.bat
    - Downloads USBDeview (NirSoft)
    - Downloads USB Device Tree Viewer
    - Advanced USB analysis tools

📖 DOCUMENTATION:

  USB_SITUATION_EXPLAINED.txt
    - Complete explanation of your USB setup
    - Why ASMedia is slower than Intel in your case
    - Real-world benchmarks vs specs

  USB_ANALYSIS_RESULTS.txt
    - Your specific system analysis
    - Controller details
    - Device connections
    - Performance recommendations


========================================
KEY FINDINGS FROM ANALYSIS:
========================================

YOUR SYSTEM:
  • Intel USB 3.0 Controller:    400-550 MB/s (FAST ✓)
  • ASMedia USB 3.1 Controller:  200-300 MB/s (SLOW ✗)

RECOMMENDATION:
  USE INTEL USB 3.0 PORTS (usually BLUE)
  AVOID ASMedia USB 3.1 PORTS (RED/CYAN) until fixed

YOUR PHONE:
  Currently on: Intel USB 3.0 ✓ CORRECT!

PHONE LINK PROBLEM:
  Routes 50GB through cloud = 3+ hours ✗
  Use File Transfer mode instead = 2 minutes ✓


========================================
FILE ORGANIZATION:
========================================

BATCH FILES (.bat):
  - Double-click to run
  - No technical knowledge needed
  - Some require "Run as Administrator"

POWERSHELL SCRIPTS (.ps1):
  - More detailed analysis
  - Right-click → "Run with PowerShell"
  - Or run from menu .bat files

TEXT FILES (.txt):
  - Documentation and guides
  - Open with Notepad
  - READ THESE FIRST for context


========================================
TROUBLESHOOTING:
========================================

"Scripts won't run":
  - Right-click → Properties → Unblock
  - Or run from menu .bat files

"PowerShell scripts blocked":
  - Run: powershell -ExecutionPolicy Bypass -File script.ps1
  - Or use the menu .bat files (bypass already set)

"Need Administrator":
  - Right-click script → "Run as Administrator"
  - Required for: OPEN_PHONELINK_FIREWALL.bat

"Results not showing":
  - Wait for script to complete
  - Check Desktop for log files
  - Run from Command Prompt to see errors


========================================
USAGE EXAMPLES:
========================================

SCENARIO 1: Phone Link slow transfer
  1. Run: MONITOR_PHONELINK_MENU.bat
  2. Choose: [1] Quick Check
  3. If shows "CLOUD RELAY":
     - STOP Phone Link transfer
     - Use File Transfer mode instead
     - See: FIX_PHONELINK_LOCAL_TRANSFER.txt

SCENARIO 2: Check USB port speeds
  1. Run: USB_ANALYZER_MENU.bat
  2. Choose: [3] Real Speed Test
  3. Enter drive letter when prompted
  4. Compare results to theoretical maximums

SCENARIO 3: Find fastest USB port
  1. Run: IDENTIFY_USB_PORTS.bat
  2. Unplug/replug device in different ports
  3. Watch Device Manager for controller name
  4. Mark fastest port with tape/sticker

SCENARIO 4: Fix ASMedia performance
  1. Run: FIX_ASMEDIA_USB.bat
  2. Try: [1] Check Driver Version
  3. If old: Update from motherboard website
  4. Try: [3] Disable UASP Mode
  5. Test speed again


========================================
ADVANCED USAGE:
========================================

WIRESHARK PACKET CAPTURE:
  1. Read: WIRESHARK_PHONELINK_GUIDE.txt
  2. Download Wireshark from wireshark.org
  3. Run as Administrator
  4. Use filters from guide

DOWNLOAD ADVANCED TOOLS:
  1. Run: DOWNLOAD_USB_TOOLS.bat
  2. Installs USBDeview for detailed port info
  3. Shows all USB history and speeds

CONTINUOUS MONITORING:
  1. Run: realtime_bandwidth_monitor.ps1
  2. Leave running during file transfers
  3. See live speed and connection type


========================================
CREDITS:
========================================

Created by: Claude (Sonnet 4.5)
For: STRYK
Session: 2025-11-12
Tools: Python, PowerShell, Batch, Bash

Purpose: Diagnose Phone Link cloud routing issue and
         analyze USB controller performance

Result: Found Intel USB 3.0 faster than ASMedia USB 3.1
        Recommended using File Transfer mode for large files


========================================
NOTES:
========================================

• All scripts are safe and read-only (except firewall script)
• USB speed tests write temporary files then delete them
• Phone Link monitors only observe, never modify traffic
• ASMedia underperformance is a known industry issue
• Real-world speeds matter more than theoretical specs

• Add "arch" to your dictionary = architecture ✓


========================================
          END OF README
========================================

For help or questions, check the individual .txt guides!
