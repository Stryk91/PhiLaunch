#!/usr/bin/env python3
"""
Generate a subtle circuit board background pattern for PhiGEN
Even more subtle than the button circuit lines
"""

from PIL import Image, ImageDraw
import random

def create_circuit_background(width=1920, height=1080, opacity=15):
    """
    Create a subtle circuit board background pattern

    Args:
        width: Image width in pixels
        height: Image height in pixels
        opacity: Green line opacity (0-255, lower = more subtle)
    """
    # Create dark background
    img = Image.new('RGBA', (width, height), (10, 10, 10, 255))
    draw = ImageDraw.Draw(img)

    # Very subtle green with low opacity
    line_color = (57, 255, 20, opacity)  # #39ff14 with alpha
    node_color = (57, 255, 20, opacity + 10)  # Slightly brighter nodes
    dot_color = (57, 255, 20, opacity - 5)  # Even subtler dots

    # Grid spacing
    grid_size = 80

    # Draw horizontal and vertical circuit traces
    for y in range(0, height, grid_size):
        # Horizontal lines with random breaks
        x_start = 0
        while x_start < width:
            segment_length = random.randint(100, 300)
            draw.line([(x_start, y), (min(x_start + segment_length, width), y)],
                     fill=line_color, width=1)
            x_start += segment_length + random.randint(50, 150)

    for x in range(0, width, grid_size):
        # Vertical lines with random breaks
        y_start = 0
        while y_start < height:
            segment_length = random.randint(100, 300)
            draw.line([(x, y_start), (x, min(y_start + segment_length, height))],
                     fill=line_color, width=1)
            y_start += segment_length + random.randint(50, 150)

    # Draw circuit nodes at grid intersections
    for y in range(0, height, grid_size):
        for x in range(0, width, grid_size):
            if random.random() > 0.7:  # Only 30% of intersections get nodes
                # Draw small square node
                node_size = 3
                draw.rectangle([x-node_size, y-node_size, x+node_size, y+node_size],
                             fill=node_color)

    # Add random circuit pads (small circles)
    for _ in range(int((width * height) / 10000)):  # Density based on area
        x = random.randint(0, width)
        y = random.randint(0, height)
        radius = random.randint(2, 4)
        draw.ellipse([x-radius, y-radius, x+radius, y+radius], fill=dot_color)

    # Add occasional corner brackets (like in the button)
    bracket_size = 15
    for y in range(grid_size, height, grid_size * 3):
        for x in range(grid_size, width, grid_size * 3):
            if random.random() > 0.85:  # Very sparse
                # Top-left bracket
                draw.line([(x, y), (x + bracket_size, y)], fill=node_color, width=1)
                draw.line([(x, y), (x, y + bracket_size)], fill=node_color, width=1)
                # Add corner dot
                draw.ellipse([x-2, y-2, x+2, y+2], fill=node_color)

    return img

if __name__ == "__main__":
    print("Generating ultra-subtle circuit board background...")

    # Create multiple versions with different opacity levels
    for opacity in [10, 15, 20]:
        img = create_circuit_background(1920, 1080, opacity=opacity)
        filename = f"circuit_background_opacity_{opacity}.png"
        img.save(filename)
        print(f"[OK] Created {filename} (opacity: {opacity}/255)")

    # Create a seamless tileable version (smaller for better tiling)
    print("\nGenerating tileable version...")
    img_tile = create_circuit_background(512, 512, opacity=12)
    img_tile.save("circuit_background_tileable.png")
    print("[OK] Created circuit_background_tileable.png (512x512, seamless)")

    print("\nDone! Use circuit_background_opacity_15.png for default subtle look")
    print("Or circuit_background_tileable.png for smaller repeating pattern")
