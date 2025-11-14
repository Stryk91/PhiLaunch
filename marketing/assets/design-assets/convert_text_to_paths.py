#!/usr/bin/env python3
"""
Convert all text in SVG to paths using Inkscape CLI.
This embeds the font as vector shapes, making it render correctly everywhere.
"""

import subprocess
from pathlib import Path

# Inkscape installation path
INKSCAPE_EXE = r'E:\Inkscape\bin\inkscape.exe'

def convert_text_to_paths(svg_input, svg_output):
    """
    Use Inkscape to convert all text elements to paths.
    This makes the font embedded as vector shapes.
    """

    print(f"Converting text to paths...")
    print(f"  Input:  {svg_input.name}")
    print(f"  Output: {svg_output.name}")
    print()

    # Inkscape command to convert text to paths
    # --export-text-to-path converts all text to path objects
    cmd = [
        INKSCAPE_EXE,
        str(svg_input),
        '--export-text-to-path',
        '--export-plain-svg',
        f'--export-filename={svg_output}'
    ]

    print(f"Running Inkscape...")
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        raise RuntimeError(f"Inkscape failed: {result.stderr}")

    if not svg_output.exists():
        raise RuntimeError("Output file was not created")

    input_size = svg_input.stat().st_size / 1024
    output_size = svg_output.stat().st_size / 1024

    print(f"\nSUCCESS!")
    print(f"  Input size:  {input_size:.1f} KB")
    print(f"  Output size: {output_size:.1f} KB")
    print(f"\nText converted to paths - SVG now works without Xirod font!")
    print(f"Output: {svg_output}")

    return svg_output


def main():
    script_dir = Path(__file__).parent
    svg_input = script_dir / "phigen_title_xirod_framed.svg"
    svg_output = script_dir / "phigen_title_xirod_framed_paths.svg"

    if not svg_input.exists():
        print(f"Error: {svg_input} not found")
        return

    print("=" * 70)
    print("INKSCAPE TEXT-TO-PATH CONVERTER")
    print("=" * 70)
    print("This converts all text (including Xirod font) to vector paths.")
    print("Result: SVG will render correctly everywhere, no font needed.")
    print("=" * 70)
    print()

    try:
        convert_text_to_paths(svg_input, svg_output)

        print("\n" + "=" * 70)
        print("NEXT STEPS:")
        print("=" * 70)
        print("1. Test the new SVG in Firefox/Browser")
        print("2. Should now show correct font (paths embedded)")
        print("3. Export to PNG using the Inkscape 8x script:")
        print()
        print("   python render_title_inkscape_8x.py")
        print()
        print("   (Update script to use phigen_title_xirod_framed_paths.svg)")
        print("=" * 70)

    except Exception as e:
        print(f"\nFAILED: {e}")


if __name__ == '__main__':
    main()
