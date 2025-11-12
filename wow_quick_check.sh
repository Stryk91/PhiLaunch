#!/bin/bash
# @SCRIPT_LAUNCHER_LOCAL - Script written by this computer
# Quick WoW connection analysis

WOW_SERVER="103.4.115.248"

echo "╔════════════════════════════════════════════════════════════╗"
echo "║  WoW Oceanic Connection Analysis - Quick Check            ║"
echo "║  From: Bullengarook VIC (4G LTE Telstra)                  ║"
echo "║  To: Sydney Datacenter                                     ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

echo "Running comprehensive trace (this takes ~30 seconds)..."
echo ""

mtr -r -c 30 $WOW_SERVER

echo ""
echo "═══════════════════════════════════════════════════════════"
echo "Key Metrics to Watch:"
echo "  • 4G Hop (10.4.151.136): Check jitter - should be <20ms"
echo "  • Final Hop: Latency should be <100ms for Sydney"
echo "  • Loss%: Should be 0.0% on all hops"
echo "═══════════════════════════════════════════════════════════"
