#!/usr/bin/env python3
"""
Render the paths-converted SVG (text embedded as vectors) with 8x super-sampling.
"""

import subprocess
from pathlib import Path

# Inkscape installation path
INKSCAPE_EXE = r'E:\Inkscape\bin\inkscape.exe'

def export_svg_8x_inkscape(svg_path, final_width=900, final_height=160):
    """
    1. Export at 8x with Inkscape (correct rendering)
    2. Downsample with ImageMagick (smooth quality)
    """

    render_width = final_width * 8
    render_height = final_height * 8

    temp_8x = svg_path.parent / f"{svg_path.stem}_temp_8x.png"
    output_path = svg_path.parent / f"{svg_path.stem}_final.png"

    print(f"[1/2] Exporting with Inkscape at 8x ({render_width}x{render_height})...")

    # Step 1: Inkscape export at 8x
    cmd_inkscape = [
        INKSCAPE_EXE,
        str(svg_path),
        '--export-type=png',
        f'--export-filename={temp_8x}',
        f'--export-width={render_width}',
        f'--export-height={render_height}',
        '--export-background=#000000',
        '--export-background-opacity=1.0'
    ]

    result = subprocess.run(cmd_inkscape, capture_output=True, text=True)

    if result.returncode != 0:
        raise RuntimeError(f"Inkscape export failed: {result.stderr}")

    temp_size_kb = temp_8x.stat().st_size / 1024
    print(f"  >> 8x render complete ({temp_size_kb:.1f} KB)")

    # Step 2: Downsample with Lanczos
    print(f"[2/2] Downsampling to {final_width}x{final_height} (Lanczos)...")

    cmd_magick = [
        'magick',
        str(temp_8x),
        '-filter', 'Lanczos',
        '-resize', f'{final_width}x{final_height}',
        str(output_path)
    ]

    result = subprocess.run(cmd_magick, capture_output=True, text=True)

    if result.returncode != 0:
        raise RuntimeError(f"ImageMagick failed: {result.stderr}")

    # Clean up temp file
    temp_8x.unlink()
    print(f"  >> Temp file removed")

    size_kb = output_path.stat().st_size / 1024
    print(f"\n>> Complete: {output_path.name} ({size_kb:.1f} KB)")

    return output_path


def main():
    script_dir = Path(__file__).parent
    svg_path = script_dir / "phigen_title_xirod_framed_paths.svg"

    if not svg_path.exists():
        print(f"Error: {svg_path} not found")
        print("Run convert_text_to_paths.py first!")
        return

    print("=" * 70)
    print("RENDERING PATHS-BASED SVG (FONT EMBEDDED AS VECTORS)")
    print("=" * 70)
    print(f"Source: {svg_path.name}")
    print(f"Final dimensions: 900x160")
    print(f"Render dimensions: 7200x1280 (8x)")
    print("Font: Xirod embedded as vector paths (no font needed!)")
    print("=" * 70)
    print()

    try:
        output = export_svg_8x_inkscape(svg_path, final_width=900, final_height=160)
        print("\n" + "=" * 70)
        print("SUCCESS - Xirod font now embedded as paths!")
        print("=" * 70)
        print(f"Output: {output}")
        print("\nThis PNG should show correct Xirod font rendering.")
        print("SVG no longer needs Xirod.otf to be installed.")
        print("=" * 70)
    except Exception as e:
        print(f"\nFAILED: {e}")


if __name__ == '__main__':
    main()
