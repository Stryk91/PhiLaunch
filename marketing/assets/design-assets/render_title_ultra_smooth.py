#!/usr/bin/env python3
"""
Create ultra-smooth 8x super-sampled PNG version of phigen_title_xirod_framed.svg
Renders at 8x resolution (7200x1280) then downsamples with Lanczos filter for perfect anti-aliasing.
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


def render_8x(svg_path, output_width, output_height):
    """Render SVG at 8x resolution."""
    temp_8x = svg_path.parent / f"{svg_path.stem}_temp_8x.png"

    print(f"  [1/2] Rendering at 8x ({output_width}x{output_height})...")

    cairosvg.svg2png(
        url=str(svg_path),
        write_to=str(temp_8x),
        output_width=output_width,
        output_height=output_height
    )

    size_kb = temp_8x.stat().st_size / 1024
    print(f"        8x temp file: {size_kb:.1f} KB")

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
    print(f"        Temp file removed")


def main():
    script_dir = Path(__file__).parent
    svg_path = script_dir / "phigen_title_xirod_framed.svg"

    if not svg_path.exists():
        print(f"Error: {svg_path} not found")
        sys.exit(1)

    # Original dimensions: 900x160
    # 8x dimensions: 7200x1280
    FINAL_WIDTH = 900
    FINAL_HEIGHT = 160
    RENDER_WIDTH = FINAL_WIDTH * 8
    RENDER_HEIGHT = FINAL_HEIGHT * 8

    output_path = script_dir / "phigen_title_xirod_framed_ultra_smooth.png"

    print(f"Creating ultra-smooth title PNG...")
    print(f"Source: {svg_path.name}")
    print(f"Final size: {FINAL_WIDTH}x{FINAL_HEIGHT}")
    print(f"Render size: {RENDER_WIDTH}x{RENDER_HEIGHT} (8x)\n")

    try:
        # Step 1: Render at 8x
        temp_8x = render_8x(svg_path, RENDER_WIDTH, RENDER_HEIGHT)

        # Step 2: Downsample with Lanczos
        downsample(temp_8x, output_path, FINAL_WIDTH, FINAL_HEIGHT)

        # Get final file size
        size_kb = output_path.stat().st_size / 1024

        print(f"\n✅ SUCCESS!")
        print(f"   Output: {output_path.name}")
        print(f"   Size: {size_kb:.1f} KB")
        print(f"   Dimensions: {FINAL_WIDTH}x{FINAL_HEIGHT}")
        print(f"   Quality: 8x super-sampled with Lanczos downsampling")

    except Exception as e:
        print(f"\n❌ FAILED: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()