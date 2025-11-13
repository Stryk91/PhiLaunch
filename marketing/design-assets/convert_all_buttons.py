#!/usr/bin/env python3
"""
Convert all button SVG files to PNG using cairosvg.
"""

import os
import sys
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


def main():
    script_dir = Path(__file__).parent

    # Find all SVG files
    svg_files = sorted(script_dir.glob("*.svg"))

    if not svg_files:
        print("No SVG files found in directory.")
        return

    print(f"Found {len(svg_files)} SVG files. Converting to PNG...\n")

    converted = []
    failed = []

    for svg_path in svg_files:
        png_path = svg_path.with_suffix('.png')

        try:
            cairosvg.svg2png(
                url=str(svg_path),
                write_to=str(png_path),
                output_width=880,
                output_height=320
            )

            file_size = png_path.stat().st_size
            converted.append((svg_path.name, png_path.name, file_size))
            print(f"  [OK] {svg_path.name:20s} -> {png_path.name:20s} ({file_size/1024:.1f} KB)")

        except Exception as e:
            failed.append((svg_path.name, str(e)))
            print(f"  [FAIL] {svg_path.name}: {e}")

    # Summary
    print(f"\n{'='*70}")
    print(f"Converted: {len(converted)}/{len(svg_files)}")

    if failed:
        print(f"Failed: {len(failed)}")
        for name, error in failed:
            print(f"  - {name}: {error}")

    total_size = sum(size for _, _, size in converted)
    print(f"Total PNG size: {total_size/1024:.1f} KB")
    print(f"Average size: {total_size/len(converted)/1024:.1f} KB" if converted else "")


if __name__ == '__main__':
    main()