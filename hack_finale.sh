#!/bin/bash
# @SCRIPT_LAUNCHER_LOCAL - Script written by this computer
# The Ultimate Herring Finale

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

clear
sleep 0.5

# Big dramatic text
echo -e "${RED}"
cat << "EOF"
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║  ██╗   ██╗ ██████╗ ██╗   ██╗    ██╗  ██╗ █████╗ ██╗   ██╗║
║  ╚██╗ ██╔╝██╔═══██╗██║   ██║    ██║  ██║██╔══██╗██║   ██║║
║   ╚████╔╝ ██║   ██║██║   ██║    ███████║███████║██║   ██║║
║    ╚██╔╝  ██║   ██║██║   ██║    ██╔══██║██╔══██║╚██╗ ██╔╝║
║     ██║   ╚██████╔╝╚██████╔╝    ██║  ██║██║  ██║ ╚████╔╝ ║
║     ╚═╝    ╚═════╝  ╚═════╝     ╚═╝  ╚═╝╚═╝  ╚═╝  ╚═══╝  ║
║                                                           ║
║           ██████╗ ███████╗ ██████╗ ██████╗ ███╗   ███╗███████╗
║           ██╔══██╗██╔════╝██╔════╝██╔═══██╗████╗ ████║██╔════╝
║           ██████╔╝█████╗  ██║     ██║   ██║██╔████╔██║█████╗
║           ██╔══██╗██╔══╝  ██║     ██║   ██║██║╚██╔╝██║██╔══╝
║           ██████╔╝███████╗╚██████╗╚██████╔╝██║ ╚═╝ ██║███████╗
║           ╚═════╝ ╚══════╝ ╚═════╝ ╚═════╝ ╚═╝     ╚═╝╚══════╝
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

sleep 1.5

echo ""
echo -e "${YELLOW}              ████████╗██╗  ██╗███████╗${NC}"
echo -e "${YELLOW}              ╚══██╔══╝██║  ██║██╔════╝${NC}"
echo -e "${YELLOW}                 ██║   ███████║█████╗  ${NC}"
echo -e "${YELLOW}                 ██║   ██╔══██║██╔══╝  ${NC}"
echo -e "${YELLOW}                 ██║   ██║  ██║███████╗${NC}"
echo -e "${YELLOW}                 ╚═╝   ╚═╝  ╚═╝╚══════╝${NC}"
echo ""

sleep 1

echo -e "${GREEN}        ██╗  ██╗███████╗██████╗ ██████╗ ██╗███╗   ██╗ ██████╗ ${NC}"
echo -e "${GREEN}        ██║  ██║██╔════╝██╔══██╗██╔══██╗██║████╗  ██║██╔════╝ ${NC}"
echo -e "${GREEN}        ███████║█████╗  ██████╔╝██████╔╝██║██╔██╗ ██║██║  ███╗${NC}"
echo -e "${GREEN}        ██╔══██║██╔══╝  ██╔══██╗██╔══██╗██║██║╚██╗██║██║   ██║${NC}"
echo -e "${GREEN}        ██║  ██║███████╗██║  ██║██║  ██║██║██║ ╚████║╚██████╔╝${NC}"
echo -e "${GREEN}        ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝ ╚═════╝ ${NC}"

sleep 1.5

# ASCII Fish Animation - 3 frames
echo ""
echo ""

# Frame 1 - Normal
fish_frame1() {
    echo -e "${CYAN}                    >"'"'"'))))><
                   (  o  o  )
                    \  __  /
                     >=*=<
                    /      \
                   (  ^^^^  )${NC}"
}

# Frame 2 - Flail left
fish_frame2() {
    echo -e "${CYAN}                 >"'"'"'))))><
                (  O  o  )
                 \  __  /
                  >=*=<
                 /      \
                (  ^^^^  )${NC}"
}

# Frame 3 - Flail right
fish_frame3() {
    echo -e "${CYAN}                       >"'"'"'))))><
                      (  o  O  )
                       \  __  /
                        >=*=<
                       /      \
                      (  ^^^^  )${NC}"
}

# Animate the fish flailing
for i in {1..8}; do
    tput cup 22 0
    fish_frame1
    sleep 0.2

    tput cup 22 0
    fish_frame2
    sleep 0.2

    tput cup 22 0
    fish_frame3
    sleep 0.2
done

# Final frame - dead eyes
tput cup 22 0
echo -e "${CYAN}                    >"'"'"'))))><
                   (  X  X  )
                    \  __  /
                     >=*=<
                    /      \
                   (  ^^^^  )${NC}"

sleep 2

echo ""
echo ""
echo -e "${GREEN}╔═════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║                                                         ║${NC}"
echo -e "${GREEN}║          PhiVector Defense Grid: ${RED}VICTORIOUS${GREEN}             ║${NC}"
echo -e "${GREEN}║          Strike's Command Centre: ${YELLOW}IMPENETRABLE${GREEN}        ║${NC}"
echo -e "${GREEN}║                                                         ║${NC}"
echo -e "${GREEN}║          Fiverr Hacker Status: ${RED}FLOPPING${GREEN}                ║${NC}"
echo -e "${GREEN}║                                                         ║${NC}"
echo -e "${GREEN}╚═════════════════════════════════════════════════════════╝${NC}"

sleep 3
