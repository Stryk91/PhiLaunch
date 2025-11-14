#!/usr/bin/env python3
"""
Correctly convert ONLY text elements to paths, preserving all other layers.
Uses Inkscape actions to select text by type, then convert.
"""

import subprocess
from pathlib import Path
import shutil

INKSCAPE_EXE = r'E:\Inkscape\bin\inkscape.exe'

def convert_text_only_to_paths(svg_input, svg_output):
    """
    Use Inkscape actions to convert only text elements to paths.
    This preserves all other elements (rects, circles, patterns, etc.)
    """

    print(f"Converting ONLY text elements to paths...")
    print(f"  Input:  {svg_input.name}")
    print(f"  Output: {svg_output.name}")
    print()

    # First, make a working copy
    temp_svg = svg_input.parent / f"{svg_input.stem}_temp.svg"
    shutil.copy(svg_input, temp_svg)

    print(f"Using Inkscape actions to:")
    print(f"  1. Select all text elements")
    print(f"  2. Convert ONLY text to paths")
    print(f"  3. Save with all other elements intact")
    print()

    # Inkscape actions:
    # - select-by-element:text - selects all <text> elements
    # - object-to-path - converts selected to paths
    # - export-plain-svg - saves as plain SVG
    cmd = [
        INKSCAPE_EXE,
        str(temp_svg),
        '--actions=select-by-element:text;object-to-path;export-plain-svg;export-do',
        f'--export-filename={svg_output}'
    ]

    print(f"Running Inkscape with action chain...")
    result = subprocess.run(cmd, capture_output=True, text=True)

    # Clean up temp file
    if temp_svg.exists():
        temp_svg.unlink()

    if result.returncode != 0:
        print(f"Inkscape stderr: {result.stderr}")
        raise RuntimeError(f"Inkscape failed with return code {result.returncode}")

    if not svg_output.exists():
        raise RuntimeError("Output file was not created")

    input_size = svg_input.stat().st_size / 1024
    output_size = svg_output.stat().st_size / 1024

    print(f"\nSUCCESS!")
    print(f"  Input size:  {input_size:.1f} KB")
    print(f"  Output size: {output_size:.1f} KB")
    print(f"\nONLY text converted to paths - all other elements preserved!")
    print(f"Output: {svg_output}")

    return svg_output


def main():
    script_dir = Path(__file__).parent
    svg_input = script_dir / "phigen_title_xirod_framed.svg"
    svg_output = script_dir / "phigen_title_complete_paths.svg"

    if not svg_input.exists():
        print(f"Error: {svg_input} not found")
        return

    print("=" * 70)
    print("CORRECT TEXT-TO-PATH CONVERSION")
    print("=" * 70)
    print("This converts ONLY text elements to paths.")
    print("All other elements (circuit board, frame, bolts) stay intact.")
    print("=" * 70)
    print()

    try:
        convert_text_only_to_paths(svg_input, svg_output)

        print("\n" + "=" * 70)
        print("VERIFICATION:")
        print("=" * 70)
        print(f"1. Open {svg_output.name} in Firefox")
        print(f"2. Check that ALL elements are visible:")
        print(f"   - Circuit board background with green traces")
        print(f"   - Chrome corner bolts")
        print(f"   - Frame border")
        print(f"   - 'Mil-Spec' text on circuit traces")
        print(f"   - 'v1.0a' version text")
        print(f"   - 'PhiGEN' title (now as paths)")
        print(f"")
        print(f"If all elements visible → SUCCESS")
        print(f"If only text visible → Problem with Inkscape actions")
        print("=" * 70)

    except Exception as e:
        print(f"\nFAILED: {e}")


if __name__ == '__main__':
    main()
