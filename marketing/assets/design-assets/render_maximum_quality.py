#!/usr/bin/env python3
"""
MAXIMUM QUALITY RENDER - File size is not a concern.
Renders at 16x super-sampling for absolute best quality.
"""

import subprocess
from pathlib import Path

INKSCAPE_EXE = r'E:\Inkscape\bin\inkscape.exe'

def export_maximum_quality(svg_path, final_width=900, final_height=160, supersample=16):
    """
    Export at maximum quality with high super-sampling.
    Default: 16x super-sampling (14400x2560)
    """

    render_width = final_width * supersample
    render_height = final_height * supersample

    temp_high = svg_path.parent / f"{svg_path.stem}_temp_{supersample}x.png"
    output_path = svg_path.parent / f"{svg_path.stem}_maximum_quality.png"

    print(f"[1/2] Exporting with Inkscape at {supersample}x ({render_width}x{render_height})...")
    print(f"      This will take longer but produce the best possible quality...")

    # Step 1: Inkscape export at high resolution
    cmd_inkscape = [
        INKSCAPE_EXE,
        str(svg_path),
        '--export-type=png',
        f'--export-filename={temp_high}',
        f'--export-width={render_width}',
        f'--export-height={render_height}',
        '--export-background=#000000',
        '--export-background-opacity=1.0'
    ]

    result = subprocess.run(cmd_inkscape, capture_output=True, text=True)

    if result.returncode != 0:
        raise RuntimeError(f"Inkscape export failed: {result.stderr}")

    temp_size_mb = temp_high.stat().st_size / (1024 * 1024)
    print(f"  >> {supersample}x render complete ({temp_size_mb:.2f} MB)")

    # Step 2: Downsample with Mitchell filter (best quality for downsampling)
    print(f"[2/2] Downsampling to {final_width}x{final_height} (Mitchell filter)...")

    cmd_magick = [
        'magick',
        str(temp_high),
        '-filter', 'Mitchell',  # Mitchell filter is excellent for downsampling
        '-resize', f'{final_width}x{final_height}',
        '-quality', '100',  # Maximum PNG quality
        str(output_path)
    ]

    result = subprocess.run(cmd_magick, capture_output=True, text=True)

    if result.returncode != 0:
        raise RuntimeError(f"ImageMagick failed: {result.stderr}")

    # Clean up temp file
    temp_high.unlink()
    print(f"  >> Temp file removed")

    size_kb = output_path.stat().st_size / 1024
    print(f"\n>> Complete: {output_path.name} ({size_kb:.1f} KB)")

    return output_path


def main():
    script_dir = Path(__file__).parent
    svg_path = script_dir / "phigen_title_xirod_framed_paths.svg"

    if not svg_path.exists():
        print(f"Error: {svg_path} not found")
        return

    print("=" * 70)
    print("MAXIMUM QUALITY RENDER - FILE SIZE NOT A CONCERN")
    print("=" * 70)
    print(f"Source: {svg_path.name}")
    print(f"Final dimensions: 900x160")
    print(f"Render dimensions: 14400x2560 (16x super-sampling)")
    print(f"Shadow blur: Ultra-high (40-50 stdDeviation)")
    print(f"Filter: Mitchell (best for quality)")
    print(f"PNG Quality: 100%")
    print("=" * 70)
    print()

    try:
        output = export_maximum_quality(svg_path, final_width=900, final_height=160, supersample=16)
        print("\n" + "=" * 70)
        print("SUCCESS - MAXIMUM QUALITY RENDER COMPLETE")
        print("=" * 70)
        print(f"Output: {output}")
        print("\nThis is the highest quality version possible:")
        print("  - 16x super-sampling")
        print("  - Ultra-smooth shadows (50+ blur)")
        print("  - Mitchell filter downsampling")
        print("  - 100% PNG quality")
        print("  - Xirod font embedded as paths")
        print("=" * 70)
    except Exception as e:
        print(f"\nFAILED: {e}")


if __name__ == '__main__':
    main()
