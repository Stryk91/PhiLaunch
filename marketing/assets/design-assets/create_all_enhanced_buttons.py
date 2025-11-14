#!/usr/bin/env python3
"""
Create enhanced v2 versions of all buttons with unique graphical themes.
Each button gets its own visual identity while maintaining cohesive design language.
"""

from pathlib import Path

# Button themes and configurations
BUTTON_THEMES = {
    'retrieve': {
        'label': 'RETRIEVE',
        'color_primary': '#14a0ff',  # Blue - data retrieval
        'color_secondary': '#4cc0ff',
        'color_accent': '#2ad4ff',
        'theme': 'data_retrieval',
        'led_style': 'circular_pulse',
        'bracket_style': 'arrow_inward',
        'pattern': 'upload_arrows'
    },
    'copy': {
        'label': 'COPY',
        'color_primary': '#ff9914',  # Orange - duplication
        'color_secondary': '#ffb84c',
        'color_accent': '#ffa82a',
        'theme': 'duplication',
        'led_style': 'twin_dots',
        'bracket_style': 'double_line',
        'pattern': 'mirror_blocks'
    },
    'list': {
        'label': 'LIST',
        'color_primary': '#c814ff',  # Purple - enumeration
        'color_secondary': '#da4cff',
        'color_accent': '#d02aff',
        'theme': 'enumeration',
        'led_style': 'sequential_dots',
        'bracket_style': 'list_markers',
        'pattern': 'horizontal_lines'
    },
    'lock': {
        'label': 'LOCK',
        'color_primary': '#ff1444',  # Red - security engaged
        'color_secondary': '#ff4c6c',
        'color_accent': '#ff2a52',
        'theme': 'security_engaged',
        'led_style': 'solid_bars',
        'bracket_style': 'closed_lock',
        'pattern': 'shield_grid'
    },
    'unlock': {
        'label': 'UNLOCK',
        'color_primary': '#ffdd14',  # Yellow - security released
        'color_secondary': '#ffe84c',
        'color_accent': '#ffe22a',
        'theme': 'security_released',
        'led_style': 'pulsing_rings',
        'bracket_style': 'open_lock',
        'pattern': 'unlock_keyhole'
    },
    'set_master': {
        'label': 'SET MASTER',
        'color_primary': '#ff14dd',  # Magenta - master control
        'color_secondary': '#ff4ce8',
        'color_accent': '#ff2ae2',
        'theme': 'master_control',
        'led_style': 'crown_pattern',
        'bracket_style': 'command_chevron',
        'pattern': 'authority_diamond'
    },
    'set_vault': {
        'label': 'SET VAULT',
        'color_primary': '#14ffc4',  # Cyan - vault configuration
        'color_secondary': '#4cffd8',
        'color_accent': '#2affce',
        'theme': 'vault_config',
        'led_style': 'vault_segments',
        'bracket_style': 'vault_door',
        'pattern': 'safe_tumblers'
    },
    'copy_path': {
        'label': 'COPY PATH',
        'color_primary': '#8cff14',  # Lime - path/directory
        'color_secondary': '#a8ff4c',
        'color_accent': '#9cff2a',
        'theme': 'path_navigation',
        'led_style': 'path_dots',
        'bracket_style': 'folder_edges',
        'pattern': 'breadcrumb_trail'
    }
}


def create_button_svg(button_key, config):
    """Generate enhanced button SVG with unique theme."""

    label = config['label']
    color1 = config['color_primary']
    color2 = config['color_secondary']
    color3 = config['color_accent']

    # Convert hex to RGB for gradient generation
    def hex_to_rgb(hex_color):
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    r, g, b = hex_to_rgb(color1)

    svg_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="220" height="80" viewBox="0 0 880 320" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="title desc">
  <title id="title">Metallic Angular Button - {label} - Enhanced Style</title>
  <desc id="desc">A sleek metallic button with {config['theme']} themed circuit patterns and accents.</desc>

  <defs>
    <!-- Chrome frame gradient - Polished Steel -->
    <linearGradient id="chromeGreen" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%"  stop-color="#050505"/>
      <stop offset="5%"  stop-color="#0d0d0d"/>
      <stop offset="10%" stop-color="#1f1f1f"/>
      <stop offset="15%" stop-color="#3a3a3a"/>
      <stop offset="20%" stop-color="#5a5a5a"/>
      <stop offset="25%" stop-color="#8a8a8a"/>
      <stop offset="30%" stop-color="#c0c0c0"/>
      <stop offset="35%" stop-color="#e8e8e8"/>
      <stop offset="40%" stop-color="#ffffff"/>
      <stop offset="42%" stop-color="#ffffff"/>
      <stop offset="45%" stop-color="#f8f8f8"/>
      <stop offset="48%" stop-color="#e0e0e0"/>
      <stop offset="51%" stop-color="#ffffff"/>
      <stop offset="54%" stop-color="#fafafa"/>
      <stop offset="57%" stop-color="#e5e5e5"/>
      <stop offset="62%" stop-color="#b8b8b8"/>
      <stop offset="67%" stop-color="#888888"/>
      <stop offset="72%" stop-color="#5a5a5a"/>
      <stop offset="77%" stop-color="#353535"/>
      <stop offset="82%" stop-color="#1f1f1f"/>
      <stop offset="87%" stop-color="#121212"/>
      <stop offset="92%" stop-color="#0d0d0d"/>
      <stop offset="97%" stop-color="#0a0a0a"/>
      <stop offset="100%" stop-color="#080808"/>
    </linearGradient>

    <!-- Chrome stroke shimmer -->
    <linearGradient id="chromeStroke" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#c8c8c8"/>
      <stop offset="15%" stop-color="#e8e8e8"/>
      <stop offset="25%" stop-color="#ffffff"/>
      <stop offset="35%" stop-color="#f5f5f5"/>
      <stop offset="48%" stop-color="#ffffff"/>
      <stop offset="50%" stop-color="#ffffff"/>
      <stop offset="52%" stop-color="#ffffff"/>
      <stop offset="65%" stop-color="#f0f0f0"/>
      <stop offset="75%" stop-color="#ffffff"/>
      <stop offset="85%" stop-color="#e0e0e0"/>
      <stop offset="100%" stop-color="#b8b8b8"/>
    </linearGradient>

    <!-- Inner panel with color hint -->
    <linearGradient id="innerPanel" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%"   stop-color="#{int(r*0.02):02x}{int(g*0.02):02x}{int(b*0.02):02x}"/>
      <stop offset="22%"  stop-color="#{int(r*0.04):02x}{int(g*0.04):02x}{int(b*0.04):02x}"/>
      <stop offset="45%"  stop-color="#{int(r*0.05):02x}{int(g*0.05):02x}{int(b*0.05):02x}"/>
      <stop offset="60%"  stop-color="#{int(r*0.03):02x}{int(g*0.03):02x}{int(b*0.03):02x}"/>
      <stop offset="100%" stop-color="#020302"/>
    </linearGradient>

    <!-- Top gloss with color tint -->
    <linearGradient id="panelSheen" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%"   stop-color="{color2}" stop-opacity="0.18"/>
      <stop offset="15%"  stop-color="{color3}" stop-opacity="0.12"/>
      <stop offset="38%"  stop-color="{color1}" stop-opacity="0.05"/>
      <stop offset="75%"  stop-color="{color1}" stop-opacity="0.01"/>
      <stop offset="100%" stop-color="{color1}" stop-opacity="0"/>
    </linearGradient>

    <!-- Colored rim light -->
    <linearGradient id="greenRim" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%"   stop-color="{color1}" stop-opacity="0.6"/>
      <stop offset="4%"   stop-color="{color1}" stop-opacity="0.5"/>
      <stop offset="18%"  stop-color="{color1}" stop-opacity="0.0"/>
      <stop offset="45%"  stop-color="{color2}" stop-opacity="0.5"/>
      <stop offset="50%"  stop-color="{color3}" stop-opacity="0.9"/>
      <stop offset="55%"  stop-color="{color2}" stop-opacity="0.5"/>
      <stop offset="82%"  stop-color="{color1}" stop-opacity="0.0"/>
      <stop offset="96%"  stop-color="{color1}" stop-opacity="0.5"/>
      <stop offset="100%" stop-color="{color1}" stop-opacity="0.6"/>
    </linearGradient>

    <!-- Colored text gradient -->
    <linearGradient id="textNeon" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%"   stop-color="#ffffff"/>
      <stop offset="20%"  stop-color="{color2}"/>
      <stop offset="50%"  stop-color="{color3}"/>
      <stop offset="80%"  stop-color="{color1}"/>
      <stop offset="100%" stop-color="{color1}"/>
    </linearGradient>

    <!-- Filters -->
    <filter id="btnShadow" x="-30%" y="-50%" width="160%" height="220%">
      <feDropShadow dx="0" dy="24" stdDeviation="24" flood-color="#000" flood-opacity="0.6"/>
    </filter>

    <filter id="innerGlow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur in="SourceAlpha" stdDeviation="4.4" result="blur"/>
      <feComposite in="blur" in2="SourceAlpha" operator="arithmetic" k2="-1" k3="1" result="innerShadow"/>
      <feFlood flood-color="{color1}" flood-opacity="0.35" result="flood"/>
      <feComposite in="flood" in2="innerShadow" operator="in" result="coloredInner"/>
      <feMerge>
        <feMergeNode in="coloredInner"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="textGlow" x="-60%" y="-60%" width="220%" height="220%">
      <feDropShadow dx="0" dy="-2" stdDeviation="1" flood-color="#ffffff" flood-opacity="0.15"/>
      <feDropShadow dx="0" dy="3" stdDeviation="2" flood-color="#000000" flood-opacity="0.4"/>
      <feDropShadow dx="0" dy="4" stdDeviation="3.6" flood-color="{color1}" flood-opacity="0.55"/>
      <feDropShadow dx="0" dy="0" stdDeviation="2" flood-color="{color2}" flood-opacity="0.45"/>
    </filter>

    <filter id="subtleUnderglow" x="-80%" y="-80%" width="260%" height="260%">
      <feDropShadow dx="0" dy="0" stdDeviation="16" flood-color="{color1}" flood-opacity="0.08"/>
      <feDropShadow dx="0" dy="0" stdDeviation="8" flood-color="{color2}" flood-opacity="0.12"/>
      <feDropShadow dx="0" dy="0" stdDeviation="4" flood-color="{color3}" flood-opacity="0.15"/>
    </filter>

    <filter id="outerAura" x="-60%" y="-60%" width="220%" height="220%">
      <feDropShadow dx="0" dy="0" stdDeviation="9.6" flood-color="{color1}" flood-opacity="0.12"/>
    </filter>

    <filter id="ledGlow" x="-100%" y="-100%" width="300%" height="300%">
      <feDropShadow dx="0" dy="0" stdDeviation="4" flood-color="{color2}" flood-opacity="0.8"/>
      <feDropShadow dx="0" dy="0" stdDeviation="2" flood-color="#ffffff" flood-opacity="0.6"/>
    </filter>

    <filter id="circuitGlow" x="-100%" y="-100%" width="300%" height="300%">
      <feDropShadow dx="0" dy="0" stdDeviation="3" flood-color="{color1}" flood-opacity="0.6"/>
      <feDropShadow dx="0" dy="0" stdDeviation="1.5" flood-color="{color2}" flood-opacity="0.8"/>
    </filter>

    <filter id="innerShadow" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur in="SourceAlpha" stdDeviation="8" result="blur"/>
      <feOffset in="blur" dx="0" dy="6" result="offsetBlur"/>
      <feFlood flood-color="#000000" flood-opacity="0.6" result="offsetColor"/>
      <feComposite in="offsetColor" in2="offsetBlur" operator="in" result="offsetBlur"/>
      <feComposite in="SourceGraphic" in2="offsetBlur" operator="over"/>
    </filter>

    <!-- Beveled corners -->
    <linearGradient id="bevelTopLeft" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#8e8e8e" stop-opacity="0.25"/>
      <stop offset="100%" stop-color="#1a1a1a" stop-opacity="0.05"/>
    </linearGradient>

    <linearGradient id="bevelTopRight" x1="1" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#8e8e8e" stop-opacity="0.25"/>
      <stop offset="100%" stop-color="#1a1a1a" stop-opacity="0.05"/>
    </linearGradient>

    <linearGradient id="bevelBottomLeft" x1="0" y1="1" x2="1" y2="0">
      <stop offset="0%" stop-color="#000000" stop-opacity="0.35"/>
      <stop offset="100%" stop-color="#2a2a2a" stop-opacity="0.1"/>
    </linearGradient>

    <linearGradient id="bevelBottomRight" x1="1" y1="1" x2="0" y2="0">
      <stop offset="0%" stop-color="#000000" stop-opacity="0.35"/>
      <stop offset="100%" stop-color="#2a2a2a" stop-opacity="0.1"/>
    </linearGradient>
  </defs>

  <!-- Button group -->
  <g transform="translate(80,48)" filter="url(#subtleUnderglow)">
    <g filter="url(#outerAura)">
      <!-- Outer angular frame -->
      <path d="M40 0 L680 0 L720 40 L720 184 L680 224 L40 224 L0 184 L0 40 Z"
            fill="url(#chromeGreen)"
            stroke="url(#chromeStroke)"
            stroke-width="8.8"
            filter="url(#btnShadow)"
            shape-rendering="geometricPrecision"/>

      <!-- Sharp specular highlights -->
      <path d="M50 4 L670 4 L710 44 L680 20 L40 20 L10 44 Z" fill="#ffffff" opacity="0.4"/>
      <path d="M60 10 L660 10 L690 32 L660 24 L60 24 L30 32 Z" fill="#ffffff" opacity="0.2"/>
      <path d="M50 220 L670 220 L710 180 L680 204 L40 204 L10 180 Z" fill="#ffffff" opacity="0.15"/>
      <path d="M4 50 L4 174 L12 180 L12 44 Z" fill="#ffffff" opacity="0.25"/>
      <path d="M716 50 L716 174 L708 180 L708 44 Z" fill="#ffffff" opacity="0.25"/>

      <!-- Inner panel -->
      <path d="M56 16 L664 16 L704 56 L704 168 L664 208 L56 208 L16 168 L16 56 Z"
            fill="url(#innerPanel)"
            stroke="{color1}" stroke-opacity="0.26" stroke-width="3.6"
            filter="url(#innerGlow)"/>

      <path d="M56 16 L664 16 L704 56 L704 168 L664 208 L56 208 L16 168 L16 56 Z"
            fill="none" filter="url(#innerShadow)"/>

      <!-- Top gloss -->
      <path d="M56 16 L664 16 L704 56 L704 112 L16 112 L16 56 Z" fill="url(#panelSheen)"/>

      <!-- Beveled corners -->
      <polygon points="40,0 80,0 56,16" fill="url(#bevelTopLeft)"/>
      <polygon points="640,0 680,0 664,16" fill="url(#bevelTopRight)"/>
      <polygon points="40,224 56,208 80,224" fill="url(#bevelBottomLeft)"/>
      <polygon points="640,224 664,208 680,224" fill="url(#bevelBottomRight)"/>

      <!-- Top rim accent -->
      <path d="M48 6 L672 6 L712 46" fill="none" stroke="url(#greenRim)" stroke-width="4.8" stroke-linecap="round" opacity="0.7"/>
      <path d="M8 178 L48 218 L672 218" fill="none" stroke="url(#greenRim)" stroke-width="4.8" stroke-linecap="round" opacity="0.5"/>

      <!-- Micro notches -->
      <g stroke="{color2}" stroke-opacity="0.45" stroke-width="3.6">
        <line x1="136" y1="3.2" x2="184" y2="3.2"/>
        <line x1="536" y1="220.8" x2="584" y2="220.8"/>
      </g>

      {generate_unique_circuits(button_key, config)}

      {generate_unique_brackets(button_key, config)}

      {generate_unique_leds(button_key, config)}

      <!-- Label -->
      <text x="360" y="140" text-anchor="middle"
            fill="url(#textNeon)"
            filter="url(#textGlow)"
            font-family="Xolonium, Orbitron, 'Bank Gothic', Eurostile, system-ui, sans-serif"
            font-size="64" letter-spacing="6.4" font-weight="800">
        {label}
      </text>
    </g>
  </g>
</svg>
'''

    return svg_content


def generate_unique_circuits(button_key, config):
    """Generate unique circuit patterns based on button theme."""
    color1 = config['color_primary']
    pattern = config['pattern']

    if pattern == 'upload_arrows':
        # RETRIEVE - upward data arrows
        return f'''
      <g stroke="{color1}" stroke-width="0.8" fill="none" filter="url(#circuitGlow)">
        <path d="M 120 120 L 120 80 L 115 85 M 120 80 L 125 85" opacity="0.45"/>
        <path d="M 150 130 L 150 90 L 145 95 M 150 90 L 155 95" opacity="0.4"/>
        <path d="M 180 125 L 180 85 L 175 90 M 180 85 L 185 90" opacity="0.4"/>
        <path d="M 540 140 L 540 100 L 535 105 M 540 100 L 545 105" opacity="0.45"/>
        <path d="M 570 135 L 570 95 L 565 100 M 570 95 L 575 100" opacity="0.4"/>
        <path d="M 600 145 L 600 105 L 595 110 M 600 105 L 605 110" opacity="0.4"/>
        <circle cx="120" cy="120" r="2" fill="{color1}" opacity="0.6"/>
        <circle cx="150" cy="130" r="2" fill="{color1}" opacity="0.6"/>
        <circle cx="180" cy="125" r="2" fill="{color1}" opacity="0.6"/>
        <circle cx="540" cy="140" r="2" fill="{color1}" opacity="0.6"/>
        <circle cx="570" cy="135" r="2" fill="{color1}" opacity="0.6"/>
        <circle cx="600" cy="145" r="2" fill="{color1}" opacity="0.6"/>
      </g>'''

    elif pattern == 'mirror_blocks':
        # COPY - mirrored symmetric blocks
        return f'''
      <g stroke="{color1}" stroke-width="0.8" fill="none" filter="url(#circuitGlow)">
        <rect x="100" y="70" width="40" height="30" rx="2" opacity="0.45"/>
        <rect x="160" y="70" width="40" height="30" rx="2" opacity="0.45"/>
        <rect x="100" y="124" width="40" height="30" rx="2" opacity="0.4"/>
        <rect x="160" y="124" width="40" height="30" rx="2" opacity="0.4"/>
        <rect x="520" y="70" width="40" height="30" rx="2" opacity="0.45"/>
        <rect x="580" y="70" width="40" height="30" rx="2" opacity="0.45"/>
        <rect x="520" y="124" width="40" height="30" rx="2" opacity="0.4"/>
        <rect x="580" y="124" width="40" height="30" rx="2" opacity="0.4"/>
        <line x1="140" y1="85" x2="160" y2="85" opacity="0.35"/>
        <line x1="140" y1="139" x2="160" y2="139" opacity="0.35"/>
        <line x1="560" y1="85" x2="580" y2="85" opacity="0.35"/>
        <line x1="560" y1="139" x2="580" y2="139" opacity="0.35"/>
      </g>'''

    elif pattern == 'horizontal_lines':
        # LIST - ordered horizontal lines
        return f'''
      <g stroke="{color1}" stroke-width="0.8" fill="none" filter="url(#circuitGlow)">
        <line x1="100" y1="70" x2="200" y2="70" opacity="0.45"/>
        <line x1="100" y1="85" x2="180" y2="85" opacity="0.4"/>
        <line x1="100" y1="100" x2="190" y2="100" opacity="0.4"/>
        <line x1="100" y1="115" x2="170" y2="115" opacity="0.35"/>
        <line x1="100" y1="130" x2="185" y2="130" opacity="0.35"/>
        <line x1="100" y1="145" x2="175" y2="145" opacity="0.35"/>
        <line x1="520" y1="79" x2="620" y2="79" opacity="0.45"/>
        <line x1="540" y1="94" x2="620" y2="94" opacity="0.4"/>
        <line x1="530" y1="109" x2="620" y2="109" opacity="0.4"/>
        <line x1="550" y1="124" x2="620" y2="124" opacity="0.35"/>
        <line x1="535" y1="139" x2="620" y2="139" opacity="0.35"/>
        <line x1="545" y1="154" x2="620" y2="154" opacity="0.35"/>
        <circle cx="90" cy="70" r="2" fill="{color1}" opacity="0.6"/>
        <circle cx="90" cy="85" r="2" fill="{color1}" opacity="0.6"/>
        <circle cx="90" cy="100" r="2" fill="{color1}" opacity="0.6"/>
        <circle cx="630" cy="79" r="2" fill="{color1}" opacity="0.6"/>
        <circle cx="630" cy="94" r="2" fill="{color1}" opacity="0.6"/>
        <circle cx="630" cy="109" r="2" fill="{color1}" opacity="0.6"/>
      </g>'''

    elif pattern == 'shield_grid':
        # LOCK - protective grid pattern
        return f'''
      <g stroke="{color1}" stroke-width="0.8" fill="none" filter="url(#circuitGlow)">
        <path d="M 150 60 L 150 90 L 120 110 L 150 130 L 150 160" opacity="0.45"/>
        <path d="M 130 80 L 150 90 L 170 80" opacity="0.4"/>
        <path d="M 130 130 L 150 120 L 170 130" opacity="0.4"/>
        <path d="M 570 60 L 570 90 L 600 110 L 570 130 L 570 160" opacity="0.45"/>
        <path d="M 550 80 L 570 90 L 590 80" opacity="0.4"/>
        <path d="M 550 130 L 570 120 L 590 130" opacity="0.4"/>
        <circle cx="150" cy="110" r="15" opacity="0.35"/>
        <circle cx="570" cy="110" r="15" opacity="0.35"/>
      </g>'''

    elif pattern == 'unlock_keyhole':
        # UNLOCK - open keyhole pattern
        return f'''
      <g stroke="{color1}" stroke-width="0.8" fill="none" filter="url(#circuitGlow)">
        <circle cx="140" cy="90" r="20" opacity="0.45"/>
        <rect x="135" y="90" width="10" height="35" rx="2" opacity="0.4"/>
        <path d="M 100 70 L 100 50 Q 100 40 110 40 L 130 40" opacity="0.35"/>
        <circle cx="580" cy="130" r="20" opacity="0.45"/>
        <rect x="575" y="130" width="10" height="35" rx="2" opacity="0.4"/>
        <path d="M 620 150 L 620 170 Q 620 180 610 180 L 590 180" opacity="0.35"/>
      </g>'''

    elif pattern == 'authority_diamond':
        # SET MASTER - authority diamond patterns
        return f'''
      <g stroke="{color1}" stroke-width="0.8" fill="none" filter="url(#circuitGlow)">
        <path d="M 140 80 L 160 100 L 140 120 L 120 100 Z" opacity="0.45"/>
        <path d="M 140 85 L 155 100 L 140 115 L 125 100 Z" opacity="0.35"/>
        <path d="M 170 50 L 175 60 L 170 70 L 165 60 Z" opacity="0.4"/>
        <path d="M 110 50 L 115 60 L 110 70 L 105 60 Z" opacity="0.4"/>
        <path d="M 580 140 L 560 120 L 580 100 L 600 120 Z" opacity="0.45"/>
        <path d="M 580 135 L 565 120 L 580 105 L 595 120 Z" opacity="0.35"/>
        <path d="M 550 170 L 545 160 L 550 150 L 555 160 Z" opacity="0.4"/>
        <path d="M 610 170 L 605 160 L 610 150 L 615 160 Z" opacity="0.4"/>
        <line x1="140" y1="80" x2="140" y2="50" opacity="0.35"/>
        <line x1="580" y1="100" x2="580" y2="170" opacity="0.35"/>
      </g>'''

    elif pattern == 'safe_tumblers':
        # SET VAULT - vault tumbler mechanism
        return f'''
      <g stroke="{color1}" stroke-width="0.8" fill="none" filter="url(#circuitGlow)">
        <circle cx="120" cy="80" r="12" opacity="0.45"/>
        <circle cx="150" cy="80" r="12" opacity="0.45"/>
        <circle cx="180" cy="80" r="12" opacity="0.45"/>
        <line x1="132" y1="80" x2="138" y2="80" opacity="0.4"/>
        <line x1="162" y1="80" x2="168" y2="80" opacity="0.4"/>
        <circle cx="600" cy="140" r="12" opacity="0.45"/>
        <circle cx="570" cy="140" r="12" opacity="0.45"/>
        <circle cx="540" cy="140" r="12" opacity="0.45"/>
        <line x1="588" y1="140" x2="582" y2="140" opacity="0.4"/>
        <line x1="558" y1="140" x2="552" y2="140" opacity="0.4"/>
        <rect x="115" y="100" width="70" height="40" rx="4" opacity="0.35"/>
        <rect x="535" y="80" width="70" height="40" rx="4" opacity="0.35"/>
      </g>'''

    elif pattern == 'breadcrumb_trail':
        # COPY PATH - path breadcrumb trail
        return f'''
      <g stroke="{color1}" stroke-width="0.8" fill="none" filter="url(#circuitGlow)">
        <path d="M 100 90 L 130 90 L 140 100 L 130 110 L 100 110 Z" opacity="0.45"/>
        <path d="M 145 90 L 175 90 L 185 100 L 175 110 L 145 110 Z" opacity="0.4"/>
        <path d="M 535 130 L 565 130 L 575 120 L 565 110 L 535 110 Z" opacity="0.45"/>
        <path d="M 580 130 L 610 130 L 620 120 L 610 110 L 580 110 Z" opacity="0.4"/>
        <line x1="130" y1="100" x2="145" y2="100" opacity="0.35"/>
        <line x1="575" y1="120" x2="580" y2="120" opacity="0.35"/>
        <path d="M 190 100 L 200 100 L 195 105 L 200 110 L 190 110" opacity="0.35"/>
        <path d="M 530 120 L 520 120 L 525 115 L 520 110 L 530 110" opacity="0.35"/>
      </g>'''

    return ''


def generate_unique_brackets(button_key, config):
    """Generate unique bracket styles based on button theme."""
    color = config['color_accent']
    style = config['bracket_style']

    if style == 'arrow_inward':
        # RETRIEVE - arrows pointing inward
        return f'''
      <g stroke="{color}" stroke-width="5" fill="none" opacity="1.0" filter="url(#circuitGlow)">
        <path d="M 72 52 L 62 52 L 52 62 L 52 72"/>
        <path d="M 648 52 L 658 52 L 668 62 L 668 72"/>
        <path d="M 72 172 L 62 172 L 52 162 L 52 152"/>
        <path d="M 648 172 L 658 172 L 668 162 L 668 152"/>
      </g>'''

    elif style == 'double_line':
        # COPY - double parallel lines
        return f'''
      <g stroke="{color}" stroke-width="4" fill="none" opacity="1.0" filter="url(#circuitGlow)">
        <path d="M 52 52 L 52 72 M 52 52 L 72 52"/>
        <path d="M 58 58 L 58 78 M 58 58 L 78 58"/>
        <path d="M 668 52 L 668 72 M 668 52 L 648 52"/>
        <path d="M 662 58 L 662 78 M 662 58 L 642 58"/>
        <path d="M 52 172 L 52 152 M 52 172 L 72 172"/>
        <path d="M 58 166 L 58 146 M 58 166 L 78 166"/>
        <path d="M 668 172 L 668 152 M 668 172 L 648 172"/>
        <path d="M 662 166 L 662 146 M 662 166 L 642 166"/>
      </g>'''

    elif style == 'list_markers':
        # LIST - bullet/number style markers
        return f'''
      <g stroke="{color}" stroke-width="5" fill="none" opacity="1.0" filter="url(#circuitGlow)">
        <line x1="52" y1="52" x2="52" y2="72"/>
        <line x1="48" y1="62" x2="72" y2="62"/>
        <line x1="668" y1="52" x2="668" y2="72"/>
        <line x1="648" y1="62" x2="692" y2="62"/>
        <line x1="52" y1="172" x2="52" y2="152"/>
        <line x1="48" y1="162" x2="72" y2="162"/>
        <line x1="668" y1="172" x2="668" y2="152"/>
        <line x1="648" y1="162" x2="692" y2="162"/>
      </g>'''

    elif style == 'closed_lock':
        # LOCK - closed bracket style
        return f'''
      <g stroke="{color}" stroke-width="5" fill="none" opacity="1.0" filter="url(#circuitGlow)">
        <path d="M 52 52 L 52 72"/>
        <path d="M 48 52 L 72 52"/>
        <path d="M 48 72 L 72 72"/>
        <path d="M 668 52 L 668 72"/>
        <path d="M 648 52 L 692 52"/>
        <path d="M 648 72 L 692 72"/>
        <path d="M 52 172 L 52 152"/>
        <path d="M 48 152 L 72 152"/>
        <path d="M 48 172 L 72 172"/>
        <path d="M 668 172 L 668 152"/>
        <path d="M 648 152 L 692 152"/>
        <path d="M 648 172 L 692 172"/>
      </g>'''

    elif style == 'open_lock':
        # UNLOCK - open/separated brackets
        return f'''
      <g stroke="{color}" stroke-width="5" fill="none" opacity="1.0" filter="url(#circuitGlow)">
        <path d="M 52 62 L 52 72 L 72 72"/>
        <path d="M 668 62 L 668 72 L 648 72"/>
        <path d="M 52 162 L 52 152 L 72 152"/>
        <path d="M 668 162 L 668 152 L 648 152"/>
        <line x1="58" y1="52" x2="72" y2="52"/>
        <line x1="662" y1="52" x2="648" y2="52"/>
        <line x1="58" y1="172" x2="72" y2="172"/>
        <line x1="662" y1="172" x2="648" y2="172"/>
      </g>'''

    elif style == 'command_chevron':
        # SET MASTER - command chevron style
        return f'''
      <g stroke="{color}" stroke-width="5" fill="none" opacity="1.0" filter="url(#circuitGlow)">
        <path d="M 62 52 L 52 62 L 62 72"/>
        <path d="M 658 52 L 668 62 L 658 72"/>
        <path d="M 62 152 L 52 162 L 62 172"/>
        <path d="M 658 152 L 668 162 L 658 172"/>
        <path d="M 72 52 L 62 62 L 72 72"/>
        <path d="M 648 52 L 658 62 L 648 72"/>
        <path d="M 72 152 L 62 162 L 72 172"/>
        <path d="M 648 152 L 658 162 L 648 172"/>
      </g>'''

    elif style == 'vault_door':
        # SET VAULT - vault door hinges
        return f'''
      <g stroke="{color}" stroke-width="5" fill="none" opacity="1.0" filter="url(#circuitGlow)">
        <circle cx="52" cy="52" r="8"/>
        <path d="M 60 52 L 72 52"/>
        <circle cx="668" cy="52" r="8"/>
        <path d="M 660 52 L 648 52"/>
        <circle cx="52" cy="172" r="8"/>
        <path d="M 60 172 L 72 172"/>
        <circle cx="668" cy="172" r="8"/>
        <path d="M 660 172 L 648 172"/>
        <line x1="52" y1="60" x2="52" y2="72"/>
        <line x1="668" y1="60" x2="668" y2="72"/>
        <line x1="52" y1="152" x2="52" y2="164"/>
        <line x1="668" y1="152" x2="668" y2="164"/>
      </g>'''

    elif style == 'folder_edges':
        # COPY PATH - folder tab style
        return f'''
      <g stroke="{color}" stroke-width="5" fill="none" opacity="1.0" filter="url(#circuitGlow)">
        <path d="M 52 72 L 52 62 L 62 52 L 72 52"/>
        <path d="M 668 72 L 668 62 L 658 52 L 648 52"/>
        <path d="M 52 152 L 52 162 L 62 172 L 72 172"/>
        <path d="M 668 152 L 668 162 L 658 172 L 648 172"/>
      </g>'''

    return f'''
      <g stroke="{color}" stroke-width="5" fill="none" opacity="1.0" filter="url(#circuitGlow)">
        <path d="M 52 52 L 52 72 M 52 52 L 72 52"/>
        <path d="M 668 52 L 668 72 M 668 52 L 648 52"/>
        <path d="M 52 172 L 52 152 M 52 172 L 72 172"/>
        <path d="M 668 172 L 668 152 M 668 172 L 648 172"/>
      </g>'''


def generate_unique_leds(button_key, config):
    """Generate unique LED indicator styles based on button theme."""
    color1 = config['color_primary']
    color2 = config['color_secondary']
    style = config['led_style']

    if style == 'circular_pulse':
        # RETRIEVE - circular pulsing indicators
        return f'''
      <g filter="url(#ledGlow)">
        <circle cx="50" cy="70" r="5" fill="{color1}"/>
        <circle cx="50" cy="70" r="8" fill="none" stroke="{color2}" stroke-width="1" opacity="0.5"/>
        <circle cx="70" cy="70" r="5" fill="{color1}" opacity="0.7"/>
        <circle cx="90" cy="70" r="5" fill="{color1}" opacity="0.4"/>
        <circle cx="630" cy="154" r="5" fill="{color1}" opacity="0.4"/>
        <circle cx="650" cy="154" r="5" fill="{color1}" opacity="0.7"/>
        <circle cx="670" cy="154" r="5" fill="{color1}"/>
        <circle cx="670" cy="154" r="8" fill="none" stroke="{color2}" stroke-width="1" opacity="0.5"/>
      </g>'''

    elif style == 'twin_dots':
        # COPY - paired twin dots
        return f'''
      <g filter="url(#ledGlow)">
        <circle cx="48" cy="68" r="4" fill="{color1}"/>
        <circle cx="58" cy="68" r="4" fill="{color1}"/>
        <circle cx="68" cy="72" r="4" fill="{color1}" opacity="0.7"/>
        <circle cx="78" cy="72" r="4" fill="{color1}" opacity="0.7"/>
        <circle cx="642" cy="152" r="4" fill="{color1}" opacity="0.7"/>
        <circle cx="652" cy="152" r="4" fill="{color1}" opacity="0.7"/>
        <circle cx="662" cy="156" r="4" fill="{color1}"/>
        <circle cx="672" cy="156" r="4" fill="{color1}"/>
      </g>'''

    elif style == 'sequential_dots':
        # LIST - sequential numbered dots
        return f'''
      <g filter="url(#ledGlow)">
        <circle cx="50" cy="60" r="4" fill="{color1}"/>
        <circle cx="50" cy="75" r="4" fill="{color1}" opacity="0.8"/>
        <circle cx="50" cy="90" r="4" fill="{color1}" opacity="0.6"/>
        <circle cx="50" cy="105" r="4" fill="{color1}" opacity="0.4"/>
        <circle cx="670" cy="119" r="4" fill="{color1}" opacity="0.4"/>
        <circle cx="670" cy="134" r="4" fill="{color1}" opacity="0.6"/>
        <circle cx="670" cy="149" r="4" fill="{color1}" opacity="0.8"/>
        <circle cx="670" cy="164" r="4" fill="{color1}"/>
      </g>'''

    elif style == 'solid_bars':
        # LOCK - solid security bars
        return f'''
      <g filter="url(#ledGlow)">
        <rect x="48" y="68" width="8" height="6" rx="1" fill="{color1}"/>
        <rect x="48" y="78" width="8" height="6" rx="1" fill="{color1}"/>
        <rect x="48" y="88" width="8" height="6" rx="1" fill="{color1}"/>
        <rect x="664" y="146" width="8" height="6" rx="1" fill="{color1}"/>
        <rect x="664" y="156" width="8" height="6" rx="1" fill="{color1}"/>
        <rect x="664" y="166" width="8" height="6" rx="1" fill="{color1}"/>
      </g>'''

    elif style == 'pulsing_rings':
        # UNLOCK - expanding ring indicators
        return f'''
      <g filter="url(#ledGlow)">
        <circle cx="52" cy="70" r="6" fill="{color1}"/>
        <circle cx="52" cy="70" r="9" fill="none" stroke="{color2}" stroke-width="1" opacity="0.4"/>
        <circle cx="52" cy="70" r="12" fill="none" stroke="{color2}" stroke-width="1" opacity="0.2"/>
        <circle cx="668" cy="154" r="6" fill="{color1}"/>
        <circle cx="668" cy="154" r="9" fill="none" stroke="{color2}" stroke-width="1" opacity="0.4"/>
        <circle cx="668" cy="154" r="12" fill="none" stroke="{color2}" stroke-width="1" opacity="0.2"/>
      </g>'''

    elif style == 'crown_pattern':
        # SET MASTER - crown/authority pattern
        return f'''
      <g filter="url(#ledGlow)">
        <path d="M 45 75 L 50 65 L 55 75 L 60 65 L 65 75" fill="none" stroke="{color1}" stroke-width="2"/>
        <circle cx="50" cy="65" r="3" fill="{color1}"/>
        <circle cx="60" cy="65" r="3" fill="{color1}"/>
        <path d="M 655 149 L 660 159 L 665 149 L 670 159 L 675 149" fill="none" stroke="{color1}" stroke-width="2"/>
        <circle cx="660" cy="159" r="3" fill="{color1}"/>
        <circle cx="670" cy="159" r="3" fill="{color1}"/>
      </g>'''

    elif style == 'vault_segments':
        # SET VAULT - vault dial segments
        return f'''
      <g filter="url(#ledGlow)">
        <circle cx="52" cy="70" r="10" fill="none" stroke="{color1}" stroke-width="2" opacity="0.6"/>
        <path d="M 52 60 L 52 65" stroke="{color1}" stroke-width="2"/>
        <path d="M 52 75 L 52 80" stroke="{color1}" stroke-width="2"/>
        <path d="M 42 70 L 47 70" stroke="{color1}" stroke-width="2"/>
        <path d="M 57 70 L 62 70" stroke="{color1}" stroke-width="2"/>
        <circle cx="668" cy="154" r="10" fill="none" stroke="{color1}" stroke-width="2" opacity="0.6"/>
        <path d="M 668 144 L 668 149" stroke="{color1}" stroke-width="2"/>
        <path d="M 668 159 L 668 164" stroke="{color1}" stroke-width="2"/>
        <path d="M 658 154 L 663 154" stroke="{color1}" stroke-width="2"/>
        <path d="M 673 154 L 678 154" stroke="{color1}" stroke-width="2"/>
      </g>'''

    elif style == 'path_dots':
        # COPY PATH - path navigation dots
        return f'''
      <g filter="url(#ledGlow)">
        <circle cx="48" cy="70" r="3" fill="{color1}"/>
        <circle cx="58" cy="70" r="2" fill="{color1}" opacity="0.8"/>
        <circle cx="66" cy="70" r="2" fill="{color1}" opacity="0.6"/>
        <circle cx="74" cy="70" r="2" fill="{color1}" opacity="0.4"/>
        <circle cx="646" cy="154" r="2" fill="{color1}" opacity="0.4"/>
        <circle cx="654" cy="154" r="2" fill="{color1}" opacity="0.6"/>
        <circle cx="662" cy="154" r="2" fill="{color1}" opacity="0.8"/>
        <circle cx="672" cy="154" r="3" fill="{color1}"/>
      </g>'''

    return f'''
      <g filter="url(#ledGlow)">
        <circle cx="50" cy="70" r="5" fill="{color1}"/>
        <circle cx="70" cy="70" r="5" fill="{color1}" opacity="0.7"/>
        <circle cx="90" cy="70" r="5" fill="{color1}" opacity="0.4"/>
        <circle cx="630" cy="154" r="5" fill="{color1}" opacity="0.4"/>
        <circle cx="650" cy="154" r="5" fill="{color1}" opacity="0.7"/>
        <circle cx="670" cy="154" r="5" fill="{color1}"/>
      </g>'''


def main():
    output_dir = Path(__file__).parent

    print("="*70)
    print("Creating Enhanced v2 Buttons with Unique Themes")
    print("="*70)
    print()

    created = []

    for button_key, config in BUTTON_THEMES.items():
        filename = f"{button_key}_v2.svg"
        filepath = output_dir / filename

        print(f"Creating: {filename:20s} - {config['label']:12s} ({config['theme']})")

        svg_content = create_button_svg(button_key, config)
        filepath.write_text(svg_content, encoding='utf-8')

        created.append(filename)

    print()
    print("="*70)
    print(f"Successfully created {len(created)} enhanced buttons!")
    print("="*70)
    print()
    print("Files created:")
    for filename in created:
        print(f"  {filename}")

    print()
    print("Next step: Render to ultra-smooth PNGs with:")
    print("  python create_ultra_smooth_buttons.py")


if __name__ == '__main__':
    main()
