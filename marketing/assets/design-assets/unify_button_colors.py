#!/usr/bin/env python3
"""
Unify all button colors to match the GENERATE button's green scheme.
Keeps all unique patterns, brackets, and LED indicators.
"""

import re
from pathlib import Path

# Green color scheme from GENERATE button
GREEN_COLORS = {
    # Primary neon green
    'primary': '#39ff14',
    # Brighter green (for brackets, highlights)
    'bright': '#6fff4a',
    # Light green variants
    'light1': '#7dff6b',
    'light2': '#8fff6b',
    'light3': '#9dff9a',
    # Very light (almost white) greens
    'verylight1': '#dfffde',
    'verylight2': '#d0ffd0',
    'verylight3': '#baffb5',
    'verylight4': '#a0ff90',
    # Medium greens
    'med1': '#6cff78',
    'med2': '#58ff3f',
    'med3': '#5cff48',
    # Panel hints
    'panel1': '#cffff0',
    'panel2': '#c4ffea',
    'panel3': '#beffdf',
    'panel4': '#b6ffd1',
    'panel5': '#a0ff9a',
}

# Define color mappings for each button theme
BUTTON_COLORS = {
    'retrieve_v2.svg': {
        # Blue theme colors
        '#14a0ff': GREEN_COLORS['primary'],
        '#4db8ff': GREEN_COLORS['bright'],
        '#7fccff': GREEN_COLORS['light1'],
        '#b3e0ff': GREEN_COLORS['light2'],
        '#d9f2ff': GREEN_COLORS['verylight1'],
        '#c4eaff': GREEN_COLORS['verylight2'],
        '#afe1ff': GREEN_COLORS['verylight3'],
        '#9ad9ff': GREEN_COLORS['verylight4'],
        '#6ac4ff': GREEN_COLORS['med1'],
        '#33aaff': GREEN_COLORS['med2'],
        '#1fa3ff': GREEN_COLORS['med3'],
    },
    'copy_v2.svg': {
        # Orange theme colors
        '#ff9914': GREEN_COLORS['primary'],
        '#ffad4d': GREEN_COLORS['bright'],
        '#ffc17f': GREEN_COLORS['light1'],
        '#ffd5b3': GREEN_COLORS['light2'],
        '#ffead9': GREEN_COLORS['verylight1'],
        '#ffe3c4': GREEN_COLORS['verylight2'],
        '#ffdcaf': GREEN_COLORS['verylight3'],
        '#ffd59a': GREEN_COLORS['verylight4'],
        '#ffb86a': GREEN_COLORS['med1'],
        '#ffa333': GREEN_COLORS['med2'],
        '#ff9c1f': GREEN_COLORS['med3'],
    },
    'list_v2.svg': {
        # Purple theme colors
        '#c814ff': GREEN_COLORS['primary'],
        '#d44dff': GREEN_COLORS['bright'],
        '#e07fff': GREEN_COLORS['light1'],
        '#ecb3ff': GREEN_COLORS['light2'],
        '#f8d9ff': GREEN_COLORS['verylight1'],
        '#f3c4ff': GREEN_COLORS['verylight2'],
        '#eeafff': GREEN_COLORS['verylight3'],
        '#e99aff': GREEN_COLORS['verylight4'],
        '#dc6aff': GREEN_COLORS['med1'],
        '#d033ff': GREEN_COLORS['med2'],
        '#cb1fff': GREEN_COLORS['med3'],
    },
    'lock_v2.svg': {
        # Red theme colors
        '#ff1444': GREEN_COLORS['primary'],
        '#ff4d6a': GREEN_COLORS['bright'],
        '#ff7f90': GREEN_COLORS['light1'],
        '#ffb3c0': GREEN_COLORS['light2'],
        '#ffd9e2': GREEN_COLORS['verylight1'],
        '#ffc4d2': GREEN_COLORS['verylight2'],
        '#ffafc0': GREEN_COLORS['verylight3'],
        '#ff9aaf': GREEN_COLORS['verylight4'],
        '#ff6a82': GREEN_COLORS['med1'],
        '#ff3357': GREEN_COLORS['med2'],
        '#ff1f4a': GREEN_COLORS['med3'],
    },
    'unlock_v2.svg': {
        # Yellow theme colors
        '#ffdd14': GREEN_COLORS['primary'],
        '#ffe44d': GREEN_COLORS['bright'],
        '#ffea7f': GREEN_COLORS['light1'],
        '#fff1b3': GREEN_COLORS['light2'],
        '#fff8d9': GREEN_COLORS['verylight1'],
        '#fff5c4': GREEN_COLORS['verylight2'],
        '#fff2af': GREEN_COLORS['verylight3'],
        '#ffef9a': GREEN_COLORS['verylight4'],
        '#ffe86a': GREEN_COLORS['med1'],
        '#ffe033': GREEN_COLORS['med2'],
        '#ffde1f': GREEN_COLORS['med3'],
    },
    'set_master_v2.svg': {
        # Magenta theme colors
        '#ff14dd': GREEN_COLORS['primary'],
        '#ff4de4': GREEN_COLORS['bright'],
        '#ff7fea': GREEN_COLORS['light1'],
        '#ffb3f1': GREEN_COLORS['light2'],
        '#ffd9f8': GREEN_COLORS['verylight1'],
        '#ffc4f3': GREEN_COLORS['verylight2'],
        '#ffafee': GREEN_COLORS['verylight3'],
        '#ff9ae9': GREEN_COLORS['verylight4'],
        '#ff6ae2': GREEN_COLORS['med1'],
        '#ff33df': GREEN_COLORS['med2'],
        '#ff1fdc': GREEN_COLORS['med3'],
    },
    'set_vault_v2.svg': {
        # Cyan theme colors
        '#14ffc4': GREEN_COLORS['primary'],
        '#4dffd0': GREEN_COLORS['bright'],
        '#7fffdc': GREEN_COLORS['light1'],
        '#b3ffe8': GREEN_COLORS['light2'],
        '#d9fff4': GREEN_COLORS['verylight1'],
        '#c4fff0': GREEN_COLORS['verylight2'],
        '#afffeb': GREEN_COLORS['verylight3'],
        '#9affe7': GREEN_COLORS['verylight4'],
        '#6affd8': GREEN_COLORS['med1'],
        '#33ffc9': GREEN_COLORS['med2'],
        '#1fffc6': GREEN_COLORS['med3'],
    },
    'copy_path_v2.svg': {
        # Lime theme colors
        '#8cff14': GREEN_COLORS['primary'],
        '#a3ff4d': GREEN_COLORS['bright'],
        '#b5ff7f': GREEN_COLORS['light1'],
        '#c9ffb3': GREEN_COLORS['light2'],
        '#e0ffd9': GREEN_COLORS['verylight1'],
        '#d6ffc4': GREEN_COLORS['verylight2'],
        '#ccffaf': GREEN_COLORS['verylight3'],
        '#c2ff9a': GREEN_COLORS['verylight4'],
        '#acff6a': GREEN_COLORS['med1'],
        '#96ff33': GREEN_COLORS['med2'],
        '#8fff1f': GREEN_COLORS['med3'],
    },
}


def replace_colors(svg_content, color_map):
    """Replace all color occurrences in SVG content."""
    # Sort by length (longest first) to avoid partial replacements
    sorted_colors = sorted(color_map.items(), key=lambda x: len(x[0]), reverse=True)

    for old_color, new_color in sorted_colors:
        # Case-insensitive replacement for hex colors
        svg_content = re.sub(
            re.escape(old_color),
            new_color,
            svg_content,
            flags=re.IGNORECASE
        )

    return svg_content


def main():
    script_dir = Path(__file__).parent

    print("Unifying all button colors to green scheme...\n")

    successful = []
    failed = []

    for button_file, color_map in BUTTON_COLORS.items():
        svg_path = script_dir / button_file

        if not svg_path.exists():
            print(f"[SKIP] {button_file} - File not found")
            continue

        print(f"Processing: {button_file}")

        try:
            # Read SVG content
            svg_content = svg_path.read_text(encoding='utf-8')

            # Replace colors
            new_content = replace_colors(svg_content, color_map)

            # Write back
            svg_path.write_text(new_content, encoding='utf-8')

            print(f"  [OK] Updated {len(color_map)} color mappings\n")
            successful.append(button_file)

        except Exception as e:
            print(f"  [FAIL] Error: {e}\n")
            failed.append((button_file, str(e)))

    # Summary
    print("=" * 70)
    print(f"Successfully updated: {len(successful)}/{len(BUTTON_COLORS)}")

    if successful:
        print("\nButtons now using green scheme:")
        for btn in successful:
            print(f"  {btn}")

    if failed:
        print(f"\nFailed: {len(failed)}")
        for btn, error in failed:
            print(f"  {btn}: {error}")

    print("\nAll buttons now use unified green color scheme!")
    print("Ready to render: python create_ultra_smooth_buttons.py")


if __name__ == '__main__':
    main()
