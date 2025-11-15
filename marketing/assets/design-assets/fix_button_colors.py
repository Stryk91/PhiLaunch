#!/usr/bin/env python3
"""
More comprehensive color replacement - finds ALL non-grayscale colors and replaces with green.
"""

import re
from pathlib import Path

# Green color scheme
GREEN_PRIMARY = '#39ff14'
GREEN_BRIGHT = '#6fff4a'

def is_grayscale(hex_color):
    """Check if a color is grayscale (R=G=B)."""
    hex_color = hex_color.lstrip('#')
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    return r == g == b

def get_brightness(hex_color):
    """Get brightness value (0-255) of a hex color."""
    hex_color = hex_color.lstrip('#')
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    # Use standard luminance formula
    return 0.299 * r + 0.587 * g + 0.114 * b

def hex_to_rgb(hex_color):
    """Convert hex color to RGB tuple."""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(r, g, b):
    """Convert RGB to hex color."""
    return f'#{r:02x}{g:02x}{b:02x}'

def map_to_green(hex_color):
    """Map a colored hex value to appropriate green shade."""
    if is_grayscale(hex_color):
        return hex_color  # Don't touch grayscale colors

    brightness = get_brightness(hex_color)

    # Map brightness to green shades
    if brightness < 50:
        # Very dark colors - keep dark but add slight green tint
        return rgb_to_hex(5, 10, 6)
    elif brightness < 100:
        # Dark colors
        return rgb_to_hex(8, 13, 8)
    elif brightness < 150:
        # Medium-dark colors - use primary green
        return GREEN_PRIMARY
    elif brightness < 200:
        # Medium-bright colors - use bright green
        return GREEN_BRIGHT
    elif brightness < 230:
        # Bright colors - lighter green
        return '#8fff6b'
    else:
        # Very bright colors - almost white with green tint
        return '#dfffde'

def replace_all_colors(svg_content):
    """Find and replace all hex colors in SVG."""
    # Find all hex colors
    def replace_color(match):
        color = match.group(0)
        return map_to_green(color)

    # Replace all #RRGGBB patterns
    svg_content = re.sub(
        r'#[0-9a-fA-F]{6}',
        replace_color,
        svg_content
    )

    return svg_content

def main():
    script_dir = Path(__file__).parent

    # Process all v2 buttons except generate (it's already correct)
    svg_files = [f for f in script_dir.glob("*_v2.svg") if f.name != 'generate_v2.svg']

    print(f"Fixing colors for {len(svg_files)} buttons...\n")

    for svg_path in sorted(svg_files):
        print(f"Processing: {svg_path.name}")

        try:
            # Read content
            content = svg_path.read_text(encoding='utf-8')

            # Replace colors
            new_content = replace_all_colors(content)

            # Write back
            svg_path.write_text(new_content, encoding='utf-8')

            print(f"  [OK] Colors unified to green\n")

        except Exception as e:
            print(f"  [FAIL] Error: {e}\n")

    print("=" * 70)
    print("All buttons now use unified green color scheme!")
    print("Ready to render: python create_ultra_smooth_buttons.py")

if __name__ == '__main__':
    main()
