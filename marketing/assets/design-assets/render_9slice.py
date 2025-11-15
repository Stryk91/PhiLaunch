#!/usr/bin/env python3
"""
Render 9-slice optimized borders to ultra-smooth PNGs.
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


# 9-slice elements: (svg_file, final_width, final_height)
NINESLICE_ELEMENTS = [
    ('list_panel_9slice.svg', 600, 400),
    ('text_input_9slice.svg', 500, 50),
]


def render_8x(svg_path, output_width, output_height):
    """Render SVG at 8x resolution."""
    print(f"  [1/2] Rendering at 8x ({output_width*8}x{output_height*8})...")

    temp_8x = svg_path.parent / f"{svg_path.stem}_temp_8x.png"

    cairosvg.svg2png(
        url=str(svg_path),
        write_to=str(temp_8x),
        output_width=output_width * 8,
        output_height=output_height * 8
    )

    return temp_8x


def downsample(temp_8x_path, final_path, final_width, final_height):
    """Downsample 8x PNG to final size with Lanczos filter."""
    print(f"  [2/2] Downsampling to {final_width}x{final_height} (Lanczos filter)...")

    cmd = [
        'magick',
        str(temp_8x_path),
        '-filter', 'Lanczos',
        '-resize', f'{final_width}x{final_height}',
        str(final_path)
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        raise RuntimeError(f"ImageMagick failed: {result.stderr}")

    # Clean up temp file
    temp_8x_path.unlink()


def main():
    script_dir = Path(__file__).parent

    print(f"Rendering {len(NINESLICE_ELEMENTS)} 9-slice borders with 8x super-sampling...\n")

    successful = []
    failed = []

    for i, (svg_file, width, height) in enumerate(NINESLICE_ELEMENTS, 1):
        svg_path = script_dir / svg_file
        output_name = f"{svg_path.stem}_ultra_smooth.png"
        output_path = svg_path.parent / output_name

        print(f"[{i}/{len(NINESLICE_ELEMENTS)}] Processing: {svg_file}")

        try:
            # Step 1: Render at 8x
            temp_8x = render_8x(svg_path, width, height)

            # Step 2: Downsample with Lanczos
            downsample(temp_8x, output_path, width, height)

            # Get file size
            size_kb = output_path.stat().st_size / 1024

            successful.append((svg_file, output_name, size_kb))
            print(f"  [OK] Complete: {output_name} ({size_kb:.1f} KB)\n")

        except Exception as e:
            failed.append((svg_file, str(e)))
            print(f"  [FAIL] Failed: {e}\n")

    # Summary
    print("=" * 70)
    print(f"Successfully created: {len(successful)}/{len(NINESLICE_ELEMENTS)}")

    if successful:
        print(f"\n9-slice borders created:")
        for src, out, size in successful:
            print(f"  {out:45s} - {size:6.1f} KB")

        total_size = sum(size for _, _, size in successful)
        print(f"\nTotal size: {total_size:.1f} KB")

    if failed:
        print(f"\nFailed: {len(failed)}")
        for src, error in failed:
            print(f"  {src}: {error}")

    print("\n9-slice borders ready for border-image CSS!")


if __name__ == '__main__':
    main()
