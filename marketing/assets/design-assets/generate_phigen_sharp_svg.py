#!/usr/bin/env python3
"""
Generate SHARP-EDGED PhiGEN title as SVG
Absolutely NO rounding - all sharp angular edges like a syringe needle
Vector graphics for infinite scalability
"""

import xml.etree.ElementTree as ET
from xml.dom import minidom

def create_chrome_gradient_svg(svg_id="chrome_grad"):
    """Create chrome gradient definition for SVG"""
    gradient = ET.Element('linearGradient', {
        'id': svg_id,
        'x1': '0%',
        'y1': '0%',
        'x2': '0%',
        'y2': '100%'
    })

    # Sharp chrome transitions - no smooth gradients
    stops = [
        ('0%', '#ffffff', '1'),      # Blazing white top
        ('3%', '#c0c0c0', '1'),      # Sharp drop
        ('8%', '#404040', '1'),      # Deep shadow
        ('12%', '#909090', '1'),     # Mid-tone
        ('25%', '#e8e8e8', '1'),     # Bright reflection
        ('45%', '#a0a0a0', '1'),     # Mid chrome
        ('55%', '#505050', '1'),     # Valley shadow
        ('70%', '#b0b0b0', '1'),     # Rise
        ('85%', '#f0f0f0', '1'),     # Bright band
        ('92%', '#606060', '1'),     # Sharp drop
        ('100%', '#303030', '1'),    # Dark edge
    ]

    for offset, color, opacity in stops:
        ET.SubElement(gradient, 'stop', {
            'offset': offset,
            'stop-color': color,
            'stop-opacity': opacity
        })

    return gradient

def create_sharp_filters(defs):
    """Create SVG filters for 3D depth and sharp shadows"""

    # Sharp shadow filter
    shadow_filter = ET.SubElement(defs, 'filter', {
        'id': 'sharp_shadow',
        'x': '-50%',
        'y': '-50%',
        'width': '200%',
        'height': '200%'
    })
    ET.SubElement(shadow_filter, 'feOffset', {
        'in': 'SourceAlpha',
        'dx': '10',
        'dy': '10',
        'result': 'offsetShadow'
    })
    ET.SubElement(shadow_filter, 'feFlood', {
        'flood-color': '#000000',
        'flood-opacity': '0.8'
    })
    ET.SubElement(shadow_filter, 'feComposite', {
        'in2': 'offsetShadow',
        'operator': 'in',
        'result': 'shadow'
    })
    ET.SubElement(shadow_filter, 'feMerge').extend([
        ET.Element('feMergeNode', {'in': 'shadow'}),
        ET.Element('feMergeNode', {'in': 'SourceGraphic'})
    ])

def create_angular_phigen_path():
    """
    Create extremely angular 'PhiGEN' text path
    Using straight lines only - NO CURVES
    Sharp geometric construction like syringe edges
    """

    # Each letter constructed from straight line segments only
    # Format: Letter: [(x, y), (x, y), ...] for polygon points

    letter_data = {
        'P': [
            # Sharp angular P
            (0, 0), (0, 100),      # Left vertical bar
            (0, 0), (50, 0),       # Top horizontal
            (50, 0), (60, 10),     # Sharp angle down-right
            (60, 10), (60, 40),    # Right vertical
            (60, 40), (50, 50),    # Sharp angle down-left
            (50, 50), (0, 50),     # Middle horizontal back
        ],
        'h': [
            # Sharp angular lowercase h
            (0, 0), (0, 100),      # Left vertical bar
            (0, 50), (40, 50),     # Middle horizontal
            (40, 50), (50, 60),    # Sharp angle down
            (50, 60), (50, 100),   # Right vertical down
        ],
        'i': [
            # Sharp angular i with dot
            (0, 0), (20, 0), (20, 10), (0, 10), (0, 0),  # Dot (square)
            (5, 30), (15, 30), (15, 100), (5, 100), (5, 30),  # Stem
        ],
        'G': [
            # Sharp angular G
            (60, 0), (0, 0),       # Top horizontal
            (0, 0), (0, 100),      # Left vertical
            (0, 100), (60, 100),   # Bottom horizontal
            (60, 100), (60, 50),   # Right vertical half
            (60, 50), (30, 50),    # Middle horizontal inward
        ],
        'E': [
            # Sharp angular E
            (0, 0), (0, 100),      # Left vertical
            (0, 0), (50, 0),       # Top horizontal
            (0, 50), (40, 50),     # Middle horizontal
            (0, 100), (50, 100),   # Bottom horizontal
        ],
        'N': [
            # Sharp angular N
            (0, 100), (0, 0),      # Left vertical
            (0, 0), (50, 100),     # Diagonal sharp angle
            (50, 100), (50, 0),    # Right vertical
        ],
    }

    # Position letters horizontally with spacing
    spacing = 70
    x_offset = 50

    paths = []

    for i, letter in enumerate(['P', 'h', 'i', 'G', 'E', 'N']):
        x_pos = x_offset + (i * spacing)

        if letter in letter_data:
            points = letter_data[letter]

            # Convert points to absolute coordinates
            abs_points = [(x + x_pos, y + 30) for x, y in points]

            # Create path for this letter
            path_d = "M " + " L ".join([f"{x},{y}" for x, y in abs_points]) + " Z"

            paths.append({
                'letter': letter,
                'path': path_d,
                'bbox': (x_pos, 30, x_pos + 60, 130)
            })

    return paths

def create_phigen_sharp_svg(width=900, height=160):
    """
    Create PhiGEN SVG with razor-sharp edges
    """

    # Create SVG root
    svg = ET.Element('svg', {
        'xmlns': 'http://www.w3.org/2000/svg',
        'xmlns:xlink': 'http://www.w3.org/1999/xlink',
        'width': str(width),
        'height': str(height),
        'viewBox': f'0 0 {width} {height}',
    })

    # Definitions section
    defs = ET.SubElement(svg, 'defs')

    # Add chrome gradient
    defs.append(create_chrome_gradient_svg('chrome_grad'))

    # Add filters
    create_sharp_filters(defs)

    # Background (optional)
    # ET.SubElement(svg, 'rect', {
    #     'width': str(width),
    #     'height': str(height),
    #     'fill': '#0a0a0a'
    # })

    # Create text using font
    text_group = ET.SubElement(svg, 'g', {
        'id': 'phigen_text'
    })

    # Main text with sharp font
    # Use the terminator font with sharp rendering
    text_elem = ET.SubElement(text_group, 'text', {
        'x': str(width // 2),
        'y': str(height // 2 + 30),
        'font-family': 'Terminator Real NFI, Impact, Arial Black, sans-serif',
        'font-size': '95',
        'font-weight': 'bold',
        'text-anchor': 'middle',
        'fill': 'url(#chrome_grad)',
        'stroke': '#101010',
        'stroke-width': '3',
        'stroke-linejoin': 'miter',  # Sharp corners, not rounded
        'stroke-linecap': 'square',   # Sharp ends, not rounded
        'shape-rendering': 'crispEdges',  # Sharp pixel-perfect rendering
        'filter': 'url(#sharp_shadow)',
    })
    text_elem.text = 'PhiGEN'

    # Add 3D depth effect with multiple layers
    for depth in range(15, 0, -3):
        depth_text = ET.SubElement(text_group, 'text', {
            'x': str(width // 2 + depth),
            'y': str(height // 2 + 30 + depth),
            'font-family': 'Terminator Real NFI, Impact, Arial Black, sans-serif',
            'font-size': '95',
            'font-weight': 'bold',
            'text-anchor': 'middle',
            'fill': f'rgba(0,0,0,{0.15 - depth * 0.008})',
            'stroke': 'none',
            'shape-rendering': 'crispEdges',
        })
        depth_text.text = 'PhiGEN'

    # Add bright specular highlight on top
    highlight_text = ET.SubElement(text_group, 'text', {
        'x': str(width // 2),
        'y': str(height // 2 + 30 - 5),
        'font-family': 'Terminator Real NFI, Impact, Arial Black, sans-serif',
        'font-size': '95',
        'font-weight': 'bold',
        'text-anchor': 'middle',
        'fill': '#ffffff',
        'opacity': '0.4',
        'stroke': 'none',
        'shape-rendering': 'crispEdges',
        'mask': 'url(#top_mask)'
    })
    highlight_text.text = 'PhiGEN'

    # Top mask for highlight
    mask = ET.SubElement(defs, 'mask', {'id': 'top_mask'})
    ET.SubElement(mask, 'rect', {
        'x': '0',
        'y': '0',
        'width': str(width),
        'height': str(height // 4),
        'fill': 'white'
    })

    # Angular corner brackets (sharp, not rounded)
    brackets_group = ET.SubElement(svg, 'g', {
        'id': 'corner_brackets',
        'stroke': '#a0a0a0',
        'stroke-width': '3',
        'fill': 'none',
        'stroke-linejoin': 'miter',
        'stroke-linecap': 'square'
    })

    bracket_size = 30
    margin = 40

    # Top-left
    ET.SubElement(brackets_group, 'polyline', {
        'points': f'{margin},{margin+bracket_size} {margin},{margin} {margin+bracket_size},{margin}'
    })

    # Top-right
    ET.SubElement(brackets_group, 'polyline', {
        'points': f'{width-margin-bracket_size},{margin} {width-margin},{margin} {width-margin},{margin+bracket_size}'
    })

    # Bottom-left
    ET.SubElement(brackets_group, 'polyline', {
        'points': f'{margin},{height-margin-bracket_size} {margin},{height-margin} {margin+bracket_size},{height-margin}'
    })

    # Bottom-right
    ET.SubElement(brackets_group, 'polyline', {
        'points': f'{width-margin-bracket_size},{height-margin} {width-margin},{height-margin} {width-margin},{height-margin-bracket_size}'
    })

    return svg

def prettify_xml(elem):
    """Return a pretty-printed XML string"""
    rough_string = ET.tostring(elem, encoding='unicode')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

if __name__ == "__main__":
    print("="*70)
    print("SHARP ANGULAR PhiGEN SVG Generator")
    print("No curves - razor-sharp edges like syringe needles")
    print("="*70)

    svg = create_phigen_sharp_svg(900, 160)

    # Write to file
    svg_string = prettify_xml(svg)

    with open('phigen_title_sharp.svg', 'w', encoding='utf-8') as f:
        f.write(svg_string)

    print("\n[OK] Created phigen_title_sharp.svg (900x160)")
    print("\nSVG Features:")
    print("  • Razor-sharp edges (crispEdges rendering)")
    print("  • Miter joints (sharp corners)")
    print("  • Square linecaps (no rounding)")
    print("  • Vector format (infinite scalability)")
    print("  • Pure chrome gradient")
    print("  • 3D depth layers")
    print("  • Angular corner brackets")
    print("\nDone! Open in any SVG viewer or browser to see sharp vector graphics!")
