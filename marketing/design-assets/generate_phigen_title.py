#!/usr/bin/env python3
"""
Generate custom PhiGEN title with metallic chrome edges and circuit board aesthetic
Matches the button design style
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os

def create_metallic_gradient(width, height):
    """Create metallic chrome gradient"""
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    for y in range(height):
        # Metallic chrome gradient
        progress = y / height
        if progress < 0.1:
            gray = int(100 + progress * 500)
        elif progress < 0.3:
            gray = int(150 - (progress - 0.1) * 200)
        elif progress < 0.5:
            gray = int(130 + (progress - 0.3) * 300)
        elif progress < 0.7:
            gray = int(190 - (progress - 0.5) * 400)
        else:
            gray = int(110 + (progress - 0.7) * 200)

        gray = max(80, min(220, gray))
        draw.line([(0, y), (width, y)], fill=(gray, gray, gray + 10, 255))

    return img

def add_circuit_details(draw, x, y, w, h):
    """Add circuit board details to letters"""
    circuit_color = (57, 255, 20, 180)  # Green with alpha

    # Small circuit nodes
    nodes = [
        (x + w * 0.2, y + h * 0.3),
        (x + w * 0.8, y + h * 0.3),
        (x + w * 0.5, y + h * 0.7),
    ]

    for nx, ny in nodes:
        # Draw small circuit node
        draw.ellipse([nx-2, ny-2, nx+2, ny+2], fill=circuit_color)
        # Draw connecting lines
        draw.line([(nx-8, ny), (nx-2, ny)], fill=circuit_color, width=1)
        draw.line([(nx+2, ny), (nx+8, ny)], fill=circuit_color, width=1)

def create_phigen_title(width=800, height=120):
    """
    Create PhiGEN title with metallic chrome styling and circuit details
    """
    # Create base image
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Try to load a bold font, fallback to default
    try:
        # Try multiple font options
        font_size = 80
        font_options = [
            "C:\\Windows\\Fonts\\impact.ttf",
            "C:\\Windows\\Fonts\\ariblk.ttf",
            "C:\\Windows\\Fonts\\arialbd.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        ]

        font = None
        for font_path in font_options:
            if os.path.exists(font_path):
                font = ImageFont.truetype(font_path, font_size)
                break

        if font is None:
            font = ImageFont.load_default()
    except:
        font = ImageFont.load_default()

    # Text to render
    text = "PhiGEN"

    # Get text bounding box
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    # Center text
    x = (width - text_width) // 2
    y = (height - text_height) // 2 - 10

    # Create layers for depth effect

    # Layer 1: Deep shadow (far back)
    shadow_layer = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow_layer)
    shadow_draw.text((x + 6, y + 6), text, font=font, fill=(0, 0, 0, 100))
    shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(3))
    img = Image.alpha_composite(img, shadow_layer)

    # Layer 2: Green glow
    glow_layer = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow_layer)
    glow_draw.text((x, y), text, font=font, fill=(57, 255, 20, 150))
    glow_layer = glow_layer.filter(ImageFilter.GaussianBlur(8))
    img = Image.alpha_composite(img, glow_layer)

    # Layer 3: Metallic chrome base
    metallic = create_metallic_gradient(text_width + 20, text_height + 20)

    # Create text mask
    mask = Image.new('L', (width, height), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.text((x, y), text, font=font, fill=255)

    # Apply metallic gradient to text
    chrome_layer = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    chrome_layer.paste(metallic, (x - 10, y - 10))
    chrome_layer.putalpha(mask)
    img = Image.alpha_composite(img, chrome_layer)

    # Layer 4: Bright highlight on top edge
    highlight_layer = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    highlight_draw = ImageDraw.Draw(highlight_layer)
    highlight_draw.text((x, y - 2), text, font=font, fill=(255, 255, 255, 80))

    # Mask to only show top portion
    highlight_mask = Image.new('L', (width, height), 0)
    highlight_mask_draw = ImageDraw.Draw(highlight_mask)
    for i in range(height // 3):
        alpha = int(255 * (1 - i / (height / 3)))
        highlight_mask_draw.rectangle([0, i, width, i + 1], fill=alpha)

    highlight_layer.putalpha(ImageChops.multiply(highlight_layer.split()[3], highlight_mask))
    img = Image.alpha_composite(img, highlight_layer)

    # Layer 5: Dark edge on bottom
    edge_layer = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    edge_draw = ImageDraw.Draw(edge_layer)
    edge_draw.text((x, y + 2), text, font=font, fill=(20, 20, 20, 100))

    edge_mask = Image.new('L', (width, height), 0)
    edge_mask_draw = ImageDraw.Draw(edge_mask)
    for i in range(height // 3):
        y_pos = height - i - 1
        alpha = int(255 * (1 - i / (height / 3)))
        edge_mask_draw.rectangle([0, y_pos, width, y_pos + 1], fill=alpha)

    edge_layer.putalpha(ImageChops.multiply(edge_layer.split()[3], edge_mask))
    img = Image.alpha_composite(img, edge_layer)

    # Layer 6: Green accent outline
    outline_layer = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    outline_draw = ImageDraw.Draw(outline_layer)

    # Draw outline in multiple directions for thickness
    for offset_x, offset_y in [(-1, -1), (1, -1), (-1, 1), (1, 1), (-2, 0), (2, 0), (0, -2), (0, 2)]:
        outline_draw.text((x + offset_x, y + offset_y), text, font=font, fill=(57, 255, 20, 60))

    img = Image.alpha_composite(img, outline_layer)

    # Layer 7: Add circuit details overlay
    circuit_layer = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    circuit_draw = ImageDraw.Draw(circuit_layer)

    # Add subtle circuit lines
    circuit_color = (57, 255, 20, 100)

    # Horizontal circuit traces
    for i in range(3):
        y_line = y + (i * text_height // 3)
        circuit_draw.line([(x - 20, y_line), (x, y_line)], fill=circuit_color, width=1)
        circuit_draw.line([(x + text_width, y_line), (x + text_width + 20, y_line)], fill=circuit_color, width=1)

    # Corner brackets
    bracket_size = 15
    for corner in [(x - 25, y - 15), (x + text_width + 10, y - 15),
                   (x - 25, y + text_height), (x + text_width + 10, y + text_height)]:
        cx, cy = corner
        # L-bracket
        circuit_draw.line([(cx, cy), (cx + bracket_size, cy)], fill=circuit_color, width=2)
        circuit_draw.line([(cx, cy), (cx, cy + bracket_size)], fill=circuit_color, width=2)
        # Corner dot
        circuit_draw.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=(57, 255, 20, 200))

    img = Image.alpha_composite(img, circuit_layer)

    return img

# Import ImageChops for layer operations
from PIL import ImageChops

if __name__ == "__main__":
    print("Generating PhiGEN title with metallic chrome styling...")

    # Create standard size
    img = create_phigen_title(800, 120)
    img.save("phigen_title_metallic.png")
    print("[OK] Created phigen_title_metallic.png (800x120)")

    # Create larger version for high-DPI displays
    img_large = create_phigen_title(1200, 180)
    img_large.save("phigen_title_metallic_large.png")
    print("[OK] Created phigen_title_metallic_large.png (1200x180)")

    # Create compact version
    img_compact = create_phigen_title(600, 90)
    img_compact.save("phigen_title_metallic_compact.png")
    print("[OK] Created phigen_title_metallic_compact.png (600x90)")

    print("\nDone! Preview the files to see the metallic chrome + circuit board style!")
