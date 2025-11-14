#!/usr/bin/env python3
"""
Create ultra-smooth 8x super-sampled PNG versions of all button SVGs.
Renders at 8x resolution then downsamples with Lanczos filter for perfect anti-aliasing.
"""

import os
import sys
import subprocess
from pathlib import Path

# Add MSYS2 Cairo DLLs to the search path
CAIRO_BIN = r'E:\Utilities\MINGSYS2\ucrt64\bin'
os.environ['PATH'] = CAIRO_BIN + os.pathsep + os.environ.get('PATH', '')

if hasattr(os, 'add_dll_directory'):
    os.add_dll_directory(CAIRO_BIN)

try:
    import cairosvg
except ImportError:
    print("Error: cairosvg not installed. Run: pip install cairosvg")
    sys.exit(1)


def render_8x(svg_path, output_path):
    """Render SVG at 8x resolution."""
    print(f"  [1/2] Rendering at 8x (7040x2560)...")

    temp_8x = svg_path.parent / f"{svg_path.stem}_temp_8x.png"

    cairosvg.svg2png(
        url=str(svg_path),
        write_to=str(temp_8x),
        output_width=7040,
        output_height=2560
    )

    return temp_8x


def downsample(temp_8x_path, final_path):
    """Downsample 8x PNG to final size with Lanczos filter."""
    print(f"  [2/2] Downsampling to 880x320 (Lanczos filter)...")

    cmd = [
        'magick',
        str(temp_8x_path),
        '-filter', 'Lanczos',
        '-resize', '880x320',
        str(final_path)
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        raise RuntimeError(f"ImageMagick failed: {result.stderr}")

    # Clean up temp file
    temp_8x_path.unlink()


def main():
    script_dir = Path(__file__).parent

    # Find all v2 button SVG files
    svg_files = sorted(script_dir.glob("*_v2.svg"))

    if not svg_files:
        print("No button SVG files found.")
        return

    print(f"Creating ultra-smooth 8x versions for {len(svg_files)} buttons...\n")

    successful = []
    failed = []

    for i, svg_path in enumerate(svg_files, 1):
        output_name = f"{svg_path.stem}_ultra_smooth.png"
        output_path = svg_path.parent / output_name

        print(f"[{i}/{len(svg_files)}] Processing: {svg_path.name}")

        try:
            # Step 1: Render at 8x
            temp_8x = render_8x(svg_path, output_path)

            # Step 2: Downsample with Lanczos
            downsample(temp_8x, output_path)

            # Get file size
            size_kb = output_path.stat().st_size / 1024

            successful.append((svg_path.name, output_name, size_kb))
            print(f"  [OK] Complete: {output_name} ({size_kb:.1f} KB)\n")

        except Exception as e:
            failed.append((svg_path.name, str(e)))
            print(f"  [FAIL] Failed: {e}\n")

    # Summary
    print("="*70)
    print(f"Successfully created: {len(successful)}/{len(svg_files)}")

    if successful:
        print(f"\nUltra-smooth buttons created:")
        for src, out, size in successful:
            print(f"  {out:35s} - {size:6.1f} KB")

        total_size = sum(size for _, _, size in successful)
        print(f"\nTotal size: {total_size:.1f} KB")

    if failed:
        print(f"\nFailed: {len(failed)}")
        for src, error in failed:
            print(f"  {src}: {error}")


if __name__ == '__main__':
    main()
