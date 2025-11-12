#!/bin/bash
# @SCRIPT_LAUNCHER_LOCAL - Script written by this computer
# Right pane effects - Network monitoring & GIF display

clear

# Colors
GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Check if we can display the GIF in terminal
if command -v chafa &> /dev/null; then
    # Display the GIF using chafa
    chafa --clear --duration 3 --loop -s 60x30 "/mnt/e/PythonProjects/PhiGEN/assets/animations/central_victoria_tactical_scan.gif" &
    GIF_PID=$!
    sleep 4
    kill $GIF_PID 2>/dev/null
elif command -v timg &> /dev/null; then
    # Alternative: timg
    timg -g 60x30 --loops 3 "/mnt/e/PythonProjects/PhiGEN/assets/animations/central_victoria_tactical_scan.gif" &
    sleep 4
else
    # Fallback: Show static ASCII art satellite view
    echo -e "${GREEN}"
    cat << "EOF"
    ╔═══════════════════════════╗
    ║   SATELLITE TRACKING      ║
    ║                           ║
    ║      .-""-._.-""-._       ║
    ║     /    -  /    - \      ║
    ║    |  -    |  -     |     ║
    ║     \     -\  -   _/      ║
    ║      `._    `.__.-'       ║
    ║         `-._____.-'       ║
    ║                           ║
    ║   CENTRAL VICTORIA        ║
    ║   LAT: -37.8136° S        ║
    ║   LON: 144.9631° E        ║
    ╚═══════════════════════════╝
EOF
    echo -e "${NC}"
    sleep 3
fi

clear

# Network monitoring effects
echo -e "${GREEN}╔════════════════════════════════╗${NC}"
echo -e "${GREEN}║   NETWORK INTERCEPT ACTIVE     ║${NC}"
echo -e "${GREEN}╚════════════════════════════════╝${NC}"
echo ""

# Simulate network traffic
while true; do
    # Random IP addresses
    SRC_IP="$((RANDOM%255)).$((RANDOM%255)).$((RANDOM%255)).$((RANDOM%255))"
    DST_IP="192.168.$((RANDOM%255)).$((RANDOM%255))"
    PORT=$((1024 + RANDOM%64511))
    BYTES=$((RANDOM%9999))

    # Protocol
    PROTO=$(shuf -n1 -e "TCP" "UDP" "HTTPS" "SSH" "DNS")

    # Status
    if [ $((RANDOM%10)) -gt 7 ]; then
        STATUS="${RED}[SUSPICIOUS]${NC}"
    else
        STATUS="${GREEN}[OK]${NC}"
    fi

    echo -e "${CYAN}$(date +%H:%M:%S.%N | cut -b1-12)${NC} $STATUS"
    echo -e "  ${YELLOW}$SRC_IP:$PORT${NC} → ${YELLOW}$DST_IP${NC}"
    echo -e "  ${PROTO} | ${BYTES}B"
    echo ""

    # Occasional special messages
    if [ $((RANDOM%20)) -eq 0 ]; then
        echo -e "${RED}[!] ENCRYPTED PAYLOAD DETECTED${NC}"
        echo -e "${YELLOW}    Attempting decryption...${NC}"
        echo ""
    fi

    if [ $((RANDOM%25)) -eq 0 ]; then
        echo -e "${GREEN}[+] GEOLOCATION DATA EXTRACTED${NC}"
        echo -e "${CYAN}    Coordinates: -36.7$((RANDOM%9))° S${NC}"
        echo ""
    fi

    sleep 0.15
done
