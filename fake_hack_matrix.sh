#!/bin/bash
# @SCRIPT_LAUNCHER_LOCAL - Script written by this computer
# PhiVector Fake Hack - MATRIX EDITION
# For entertainment purposes only

# Matrix rain function (runs in background)
matrix_rain() {
    local cols=$(tput cols)
    local lines=$(tput lines)
    local rain_width=20  # Width of the rain column on right side
    local rain_start=$((cols - rain_width))

    declare -A drops

    # Initialize random drops
    for ((i=0; i<rain_width; i++)); do
        drops[$i]=$((RANDOM % lines))
    done

    while true; do
        for ((i=0; i<rain_width; i++)); do
            local x=$((rain_start + i))
            local y=${drops[$i]}

            # Random characters (mix of Matrix-style chars)
            local chars=('ﾊ' 'ﾐ' 'ﾋ' 'ｰ' 'ｳ' 'ｼ' 'ﾅ' 'ﾓ' 'ﾆ' 'ｻ' 'ﾜ' 'ﾂ' 'ｵ' 'ﾘ' 'ｱ' 'ﾎ' 'ﾃ' 'ﾏ' 'ｹ' 'ﾒ' '0' '1' 'Z' '$' '@' '#')
            local char=${chars[$RANDOM % ${#chars[@]}]}

            # Position cursor and draw
            if [ $y -ge 0 ] && [ $y -lt $lines ]; then
                tput cup $y $x 2>/dev/null
                echo -ne "\033[1;32m${char}\033[0m"

                # Fade previous characters
                if [ $((y - 1)) -ge 0 ]; then
                    tput cup $((y - 1)) $x 2>/dev/null
                    echo -ne "\033[0;32m${char}\033[0m"
                fi
                if [ $((y - 2)) -ge 0 ]; then
                    tput cup $((y - 2)) $x 2>/dev/null
                    echo -ne "\033[2;32m${char}\033[0m"
                fi
            fi

            # Update position
            drops[$i]=$((y + 1))

            # Reset if off screen
            if [ ${drops[$i]} -ge $lines ]; then
                drops[$i]=$((RANDOM % (lines / 2)))
            fi
        done
        sleep 0.05
    done
}

# Start matrix rain in background
matrix_rain &
MATRIX_PID=$!

# Trap to kill background process on exit
trap "kill $MATRIX_PID 2>/dev/null; tput cnorm; tput sgr0; clear" EXIT

# Hide cursor for cleaner look
tput civis

# Main script starts here
clear
sleep 0.5

# Cool ASCII banner
tput cup 1 0
echo -e "\033[1;32m"
cat << "EOF"
╔═══════════════════════════════════════════════════════════╗
║  ██████╗ ██╗  ██╗██╗██╗   ██╗███████╗ ██████╗████████╗   ║
║  ██╔══██╗██║  ██║██║██║   ██║██╔════╝██╔════╝╚══██╔══╝   ║
║  ██████╔╝███████║██║██║   ██║█████╗  ██║        ██║      ║
║  ██╔═══╝ ██╔══██║██║╚██╗ ██╔╝██╔══╝  ██║        ██║      ║
║  ██║     ██║  ██║██║ ╚████╔╝ ███████╗╚██████╗   ██║      ║
║  ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═══╝  ╚══════╝ ╚═════╝   ╚═╝      ║
║                SIGINT MODULE v3.7.2                       ║
╚═══════════════════════════════════════════════════════════╝
EOF
echo -e "\033[0m"

sleep 1

# Position for main output (left side)
row=11

tput cup $row 0; echo -e "\033[1;32m[*] PhiVector SIGINT Module - Deep Packet Analysis\033[0m"
((row++))
sleep 0.4
tput cup $row 0; echo -e "\033[1;32m[*] Initializing Discord WebSocket tap...\033[0m"
((row++))
sleep 0.5
tput cup $row 0; echo -e "\033[1;33m[+] Capturing TLS handshake\033[0m"
((row++))
sleep 0.4
tput cup $row 0; echo -e "\033[1;36m[DEBUG] Gateway: wss://gateway.discord.gg/?v=10\033[0m"
((row++))
sleep 0.6
tput cup $row 0; echo -e "\033[1;32m[*] Intercepting session tokens...\033[0m"
((row++))
sleep 0.5

for i in {1..6}; do
    tput cup $row 0
    echo -e "\033[0;90m    ├─ Token: $(head /dev/urandom | tr -dc 'A-Za-z0-9' | head -c 24)\033[0m"
    ((row++))
    sleep 0.2
done

sleep 0.5
tput cup $row 0; echo -e "\033[1;33m[+] AES-256 key extraction...\033[0m"
((row++))
sleep 0.8
tput cup $row 0; echo -e "\033[1;36m[CRYPTO] Differential power analysis\033[0m"
((row++))
sleep 0.6

for i in {1..4}; do
    tput cup $row 0
    echo -e "\033[0;90m    └─ Round $i: $(head /dev/urandom | tr -dc 'a-f0-9' | head -c 16)\033[0m"
    ((row++))
    sleep 0.25
done

sleep 0.5
tput cup $row 0; echo -e "\033[1;31m[!] Encryption: ChaCha20-Poly1305\033[0m"
((row++))
sleep 0.5
tput cup $row 0; echo -e "\033[1;33m[+] Deploying quantum bruteforce...\033[0m"
((row++))
sleep 0.9
tput cup $row 0; echo -e "\033[1;32m[*] Session DECRYPTED\033[0m"
((row++))
sleep 0.6
tput cup $row 0; echo -e "\033[1;32m[*] Extracting 873 message payloads...\033[0m"
((row++))
sleep 0.7

for i in {1..8}; do
    tput cup $row 0
    echo -e "\033[0;90m    ├─ Msg $(head /dev/urandom | tr -dc '0-9' | head -c 18)\033[0m"
    ((row++))
    sleep 0.12
done

sleep 0.6
((row++))
tput cup $row 0; echo -e "\033[1;33m[+] Found 1,247 georeferenced data points\033[0m"
((row++))
sleep 0.5
tput cup $row 0; echo -e "\033[1;32m[*] Geolocation triangulation (Stage 1/3)\033[0m"
((row++))
sleep 0.7
tput cup $row 0; echo -e "\033[1;36m[TRACE] Position: -33.8688°S, 151.2093°E\033[0m"
((row++))
sleep 0.4
tput cup $row 0; echo -e "\033[0;90m        ±500km (Sydney metro)\033[0m"
((row++))
sleep 0.5
tput cup $row 0; echo -e "\033[1;36m[TRACE] ISP: Telstra BigPond | AS1221\033[0m"
((row++))
sleep 0.6

((row++))
tput cup $row 0; echo -e "\033[1;32m[*] Stage 2/3: NTP packets analysis\033[0m"
((row++))
sleep 0.7
tput cup $row 0; echo -e "\033[1;36m[TRACE] Refined: -37.8136°S, 144.9631°E\033[0m"
((row++))
sleep 0.4
tput cup $row 0; echo -e "\033[0;90m        ±50km (Melbourne region)\033[0m"
((row++))
sleep 0.5
tput cup $row 0; echo -e "\033[1;33m[+] Kernel injection probe...\033[0m"
((row++))
sleep 0.8
tput cup $row 0; echo -e "\033[1;36m[KERNEL] Linux 6.6.87.2-WSL2 | x86_64\033[0m"
((row++))
sleep 0.5
tput cup $row 0; echo -e "\033[1;33m[+] CVE-2024-FAKE exploit\033[0m"
((row++))
sleep 0.7

for i in {1..5}; do
    tput cup $row 0
    echo -e "\033[0;36m    [$(shuf -e 'kworker' 'systemd' 'docker' | head -1):$(shuf -i 1000-9999 -n 1)] @ 0x$(head /dev/urandom | tr -dc 'a-f0-9' | head -c 8)\033[0m"
    ((row++))
    sleep 0.2
done

sleep 0.6
((row++))
tput cup $row 0; echo -e "\033[1;32m[*] Stage 3/3: Cell tower analysis\033[0m"
((row++))
sleep 0.8
tput cup $row 0; echo -e "\033[1;36m[TRACE] -36.$(shuf -i 7500-7800 -n 1)°S, 144.$(shuf -i 2800-3300 -n 1)°E\033[0m"
((row++))
sleep 0.4
tput cup $row 0; echo -e "\033[0;90m        ±5km (Bendigo area)\033[0m"
((row++))
sleep 0.5
tput cup $row 0; echo -e "\033[1;36m[TRACE] WiFi AP fingerprints...\033[0m"
((row++))
sleep 0.7
tput cup $row 0; echo -e "\033[1;31m[!] TARGET LOCK ACQUIRED\033[0m"
((row++))
sleep 0.5

tput cup $row 0; echo -e "\033[1;33m    Bouncing between:\033[0m"
((row++))
sleep 0.3
tput cup $row 0; echo -e "\033[1;33m      → Lockwood:    -36.7834°S, 144.3312°E\033[0m"
((row++))
sleep 0.25
tput cup $row 0; echo -e "\033[1;33m      → Bridgewater: -36.5917°S, 144.1523°E\033[0m"
((row++))
sleep 0.25
tput cup $row 0; echo -e "\033[1;33m      → Bendigo:     -36.7570°S, 144.2794°E\033[0m"
((row++))
sleep 0.25
tput cup $row 0; echo -e "\033[1;33m      → Huntly:      -36.6105°S, 144.3087°E\033[0m"
((row++))
sleep 0.6

((row++))
tput cup $row 0; echo -e "\033[1;32m[*] Reverse-engineering mainframe...\033[0m"
((row++))
sleep 0.6

for i in {1..7}; do
    tput cup $row 0
    echo -e "\033[0;36m    [Port $(shuf -i 1024-65535 -n 1)] $(shuf -e OPEN FILTERED | head -1)\033[0m"
    ((row++))
    sleep 0.2
done

sleep 0.5
tput cup $row 0; echo -e "\033[1;31m[CRITICAL] PhiVector Quantum Encryption™\033[0m"
((row++))
sleep 0.6
tput cup $row 0; echo -e "\033[1;33m[+] Attempting Fibonacci bypass...\033[0m"
((row++))
sleep 0.9
tput cup $row 0; echo -e "\033[1;31m[ERROR] Access denied\033[0m"
((row++))
sleep 0.6

((row++))
tput cup $row 0; echo -e "\033[1;31m[!!!] INTRUSION DETECTED\033[0m"
((row++))
sleep 0.7
tput cup $row 0; echo -e "\033[1;32m[*] Reverse-trace active...\033[0m"
((row++))
sleep 0.8
tput cup $row 0; echo -e "\033[1;31m[!] Fiverr IP: $(shuf -i 1-255 -n 1).$(shuf -i 1-255 -n 1).$(shuf -i 1-255 -n 1).$(shuf -i 1-255 -n 1)\033[0m"
((row++))
sleep 0.4
tput cup $row 0; echo -e "\033[1;31m[!] Location: Bangalore, India\033[0m"
((row++))
sleep 0.5
tput cup $row 0; echo -e "\033[1;33m[+] Counter-payload via ICMP...\033[0m"
((row++))
sleep 0.8
tput cup $row 0; echo -e "\033[1;32m[*] Browser history: LEAKED\033[0m"
((row++))
sleep 0.6

((row+=2))
tput cup $row 0
echo -e "\033[1;32m╔═════════════════════════════════════════════════════╗\033[0m"
((row++))
tput cup $row 0
echo -e "\033[1;32m║  Strike's Command Centre remains impenetrable.     ║\033[0m"
((row++))
tput cup $row 0
echo -e "\033[1;32m║                                                     ║\033[0m"
((row++))
tput cup $row 0
echo -e "\033[1;32m║  Fiverr hacker status:                              ║\033[0m"
((row++))
tput cup $row 0
echo -e "\033[1;32m║    • IP logged and forwarded to ISP                 ║\033[0m"
((row++))
tput cup $row 0
echo -e "\033[1;32m║    • Browser history leaked to client               ║\033[0m"
((row++))
tput cup $row 0
echo -e "\033[1;32m║    • Mom has been called                            ║\033[0m"
((row++))
tput cup $row 0
echo -e "\033[1;32m║                                                     ║\033[0m"
((row++))
tput cup $row 0
echo -e "\033[1;32m║  PhiVector Defense Grid: ACTIVE                     ║\033[0m"
((row++))
tput cup $row 0
echo -e "\033[1;32m╚═════════════════════════════════════════════════════╝\033[0m"

# Keep matrix rain going for a bit
sleep 2

# Show cursor and cleanup matrix
tput cnorm
tput sgr0
kill $MATRIX_PID 2>/dev/null
clear

# Launch the epic finale
bash ~/hack_finale.sh
