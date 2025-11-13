"""
PhiLaunch Color Palette - Soft Fade Matrix Theme
Eye-strain optimized colors for tactical automation interface
"""

COLORS = {
    # Base backgrounds (lifted blacks, not pure black)
    'bg_base': '#0D0D0D',        # Soft black base
    'bg_panel': '#151515',       # Panel backgrounds
    'bg_card': '#1A1A1A',        # Card/widget backgrounds
    'bg_input': '#0A0A0A',       # Darkest - input fields
    'bg_darker': '#080808',      # Even darker for depth

    # Primary greens (softer than neon, easier on eyes)
    'primary': '#00EE00',        # Main green (95% brightness)
    'primary_bright': '#00FF00', # Accents only
    'primary_dim': '#00AA00',    # Dimmed elements
    'primary_dark': '#007700',   # Darker accents

    # Status colors
    'success': '#00DD00',        # Success/active state
    'warning': '#FFAA00',        # Warning/attention needed
    'error': '#FF4444',          # Error/stopped
    'info': '#00DDFF',           # Info/SSH connections
    'inactive': '#555555',       # Inactive/disabled

    # Borders and overlays (rgba for transparency)
    'border_bright': 'rgba(0, 255, 0, 0.4)',    # Bright borders
    'border_dim': 'rgba(0, 255, 0, 0.2)',       # Subtle borders
    'border_selected': 'rgba(0, 255, 0, 0.6)',  # Selected items

    # Text colors
    'text_primary': '#CCCCCC',   # Main text
    'text_secondary': '#999999', # Secondary text
    'text_dim': '#666666',       # Dim/disabled text
    'text_green': '#00EE00',     # Highlighted text
}

# Interaction state colors
INTERACTION_STATES = {
    'normal': '#00AA00',
    'hover': '#00EE00',
    'selected': '#00FF00',
    'pressed': '#007700',

    # Background states with transparency
    'normal_bg': 'rgba(0, 170, 0, 0.08)',
    'hover_bg': 'rgba(0, 238, 0, 0.12)',
    'selected_bg': 'rgba(0, 238, 0, 0.20)',
    'pressed_bg': 'rgba(0, 119, 0, 0.25)',
}

# Component-specific colors
COMPONENT_COLORS = {
    # Task status indicators
    'task_running': '#00DD00',
    'task_stopped': '#FF4444',
    'task_paused': '#FFAA00',

    # Connection status
    'ssh_active': '#00DDFF',
    'ssh_inactive': '#555555',
    'wireguard_connected': '#00DD00',
    'wireguard_disconnected': '#FF4444',

    # System metrics
    'cpu_normal': '#00DD00',
    'cpu_high': '#FFAA00',
    'cpu_critical': '#FF4444',
    'ram_normal': '#00DD00',
    'ram_high': '#FFAA00',
    'ram_critical': '#FF4444',
}

# Color palette for quick reference
PALETTE_INFO = """
PhiLaunch Color System:
- Lifted blacks (#0D-#1A) prevent eye strain vs pure black
- Softer greens (#00EE00) prevent retinal burn vs neon #00FF00
- RGBA overlays create depth without harshness
- Tactical/cyberpunk aesthetic with professional polish
"""
