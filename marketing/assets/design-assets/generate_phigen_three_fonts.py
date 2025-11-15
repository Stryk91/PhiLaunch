#!/usr/bin/env python3
"""
Generate three sharp SVG versions with different fonts:
1. Xirod
2. Xolonium Bold
3. Cyberdyne (needs extraction from zip)
"""

import os
import sys
from pathlib import Path

# Font paths
FONTS = {
    'xirod': r'E:\PythonProjects\PhiGEN\FONTS\Xirod.otf',
    'xolonium': r'E:\PythonProjects\PhiGEN\FONTS\Xolonium\Xolonium-Bold.otf',
    'cyberdyne': None  # Will check if extracted
}

def create_sharp_svg(font_family, font_file, output_name, width=900, height=160):
    """Create sharp chrome SVG with specified font"""

    svg_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"
     width="{width}" height="{height}" viewBox="0 0 {width} {height}">

  <defs>
    <!-- Pure Chrome Gradient -->
    <linearGradient id="chrome_grad_{output_name}" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="1"/>
      <stop offset="3%" stop-color="#c0c0c0" stop-opacity="1"/>
      <stop offset="8%" stop-color="#404040" stop-opacity="1"/>
      <stop offset="12%" stop-color="#909090" stop-opacity="1"/>
      <stop offset="25%" stop-color="#e8e8e8" stop-opacity="1"/>
      <stop offset="45%" stop-color="#a0a0a0" stop-opacity="1"/>
      <stop offset="55%" stop-color="#505050" stop-opacity="1"/>
      <stop offset="70%" stop-color="#b0b0b0" stop-opacity="1"/>
      <stop offset="85%" stop-color="#f0f0f0" stop-opacity="1"/>
      <stop offset="92%" stop-color="#606060" stop-opacity="1"/>
      <stop offset="100%" stop-color="#303030" stop-opacity="1"/>
    </linearGradient>

    <!-- Sharp Shadow Filter -->
    <filter id="sharp_shadow_{output_name}" x="-50%" y="-50%" width="200%" height="200%">
      <feOffset in="SourceAlpha" dx="10" dy="10" result="offsetShadow"/>
      <feFlood flood-color="#000000" flood-opacity="0.8"/>
      <feComposite in2="offsetShadow" operator="in" result="shadow"/>
      <feMerge>
        <feMergeNode in="shadow"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <!-- Top Highlight Mask -->
    <mask id="top_mask_{output_name}">
      <rect x="0" y="0" width="{width}" height="{height//4}" fill="white"/>
    </mask>

    <!-- Font Definition -->
    <style type="text/css">
      @font-face {{
        font-family: '{font_family}';
        src: url('file:///{font_file}') format('opentype');
      }}
    </style>
  </defs>

  <!-- 3D Depth Layers (shadows) -->
  <g id="depth_layers_{output_name}">'''

    # Add depth layers
    for depth in range(15, 0, -3):
        alpha = 0.15 - depth * 0.008
        svg_content += f'''
    <text x="{width//2 + depth}" y="{height//2 + 30 + depth}"
          font-family="{font_family}, Impact, Arial Black, sans-serif"
          font-size="95" font-weight="bold" text-anchor="middle"
          fill="rgba(0,0,0,{alpha})" stroke="none"
          shape-rendering="crispEdges">PhiGEN</text>'''

    svg_content += f'''
  </g>

  <!-- Main Text -->
  <g id="main_text_{output_name}">
    <text x="{width//2}" y="{height//2 + 30}"
          font-family="{font_family}, Impact, Arial Black, sans-serif"
          font-size="95" font-weight="bold" text-anchor="middle"
          fill="url(#chrome_grad_{output_name})"
          stroke="#101010" stroke-width="3"
          stroke-linejoin="miter" stroke-linecap="square"
          shape-rendering="crispEdges"
          filter="url(#sharp_shadow_{output_name})">PhiGEN</text>

    <!-- Top Highlight -->
    <text x="{width//2}" y="{height//2 + 25}"
          font-family="{font_family}, Impact, Arial Black, sans-serif"
          font-size="95" font-weight="bold" text-anchor="middle"
          fill="#ffffff" opacity="0.4" stroke="none"
          shape-rendering="crispEdges"
          mask="url(#top_mask_{output_name})">PhiGEN</text>
  </g>

  <!-- Angular Corner Brackets -->
  <g id="corner_brackets_{output_name}"
     stroke="#a0a0a0" stroke-width="3" fill="none"
     stroke-linejoin="miter" stroke-linecap="square">
    <polyline points="40,70 40,40 70,40"/>
    <polyline points="{width-70},40 {width-40},40 {width-40},70"/>
    <polyline points="40,{height-30} 40,{height} 70,{height}"/>
    <polyline points="{width-70},{height} {width-40},{height} {width-40},{height-30}"/>
  </g>

</svg>'''

    return svg_content

def main():
    print("="*70)
    print("PhiGEN Sharp SVG Generator - Three Font Versions")
    print("="*70)

    # Check cyberdyne
    cyberdyne_paths = [
        r'E:\PythonProjects\PhiGEN\FONTS\Cyberdyne-5Z48.otf',
        r'E:\PythonProjects\PhiGEN\FONTS\cyberdyne.ttf',
        r'E:\PythonProjects\PhiGEN\FONTS\cyberdyne\cyberdyne.ttf',
        r'E:\PythonProjects\PhiGEN\FONTS\Cyberdyne.ttf',
    ]

    for path in cyberdyne_paths:
        if os.path.exists(path):
            FONTS['cyberdyne'] = path
            break

    if FONTS['cyberdyne'] is None:
        print("\nWARNING: Cyberdyne font not found.")
        print("Please extract: E:\\PythonProjects\\PhiGEN\\FONTS\\cyberdyne-font.zip")
        print("Will use fallback font for cyberdyne version.\n")

    # Generate three versions
    versions = [
        ('Xirod', FONTS['xirod'], 'xirod'),
        ('Xolonium', FONTS['xolonium'], 'xolonium'),
        ('Cyberdyne', FONTS['cyberdyne'] or FONTS['xirod'], 'cyberdyne'),
    ]

    for font_name, font_path, output_name in versions:
        print(f"\nGenerating {font_name} version...")

        if not os.path.exists(font_path):
            print(f"  ERROR: Font not found: {font_path}")
            continue

        svg_content = create_sharp_svg(font_name, font_path, output_name)

        output_file = f'phigen_title_{output_name}.svg'
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(svg_content)

        print(f"  [OK] Created {output_file}")
        print(f"       Font: {font_name}")
        print(f"       Path: {font_path}")

    print("\n" + "="*70)
    print("Done! Created 3 versions with different fonts")
    print("All versions have:")
    print("  • Razor-sharp edges (crispEdges rendering)")
    print("  • Miter joins (sharp corners)")
    print("  • Pure chrome gradient")
    print("  • 3D depth layers")
    print("  • Angular corner brackets")
    print("="*70)

if __name__ == "__main__":
    main()
