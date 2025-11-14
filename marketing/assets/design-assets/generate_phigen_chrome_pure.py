#!/usr/bin/env python3
"""
Generate 100% PURE CHROME PhiGEN title
Angular beveled edges like the buttons - NO GREEN
Uses mechanical terminator fonts
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
import os

def create_pure_chrome_gradient(width, height):
    """Ultra-reflective pure chrome gradient - no color tint"""
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    for y in range(height):
        progress = y / height

        # Extreme chrome reflections
        if progress < 0.03:
            value = 255  # Blazing white highlight
        elif progress < 0.08:
            # Sharp drop
            value = int(255 - (progress - 0.03) * 2800)
        elif progress < 0.12:
            # Deep shadow
            value = 65
        elif progress < 0.25:
            # Rise to bright reflection
            value = int(65 + (progress - 0.12) * 1400)
        elif progress < 0.45:
            # Broad highlight band
            value = int(247 - (progress - 0.25) * 400)
        elif progress < 0.55:
            # Sharp valley
            value = int(167 - (progress - 0.45) * 800)
        elif progress < 0.70:
            # Mid-tone rise
            value = int(87 + (progress - 0.55) * 600)
        elif progress < 0.85:
            # Bright reflection
            value = int(177 + (progress - 0.70) * 400)
        elif progress < 0.92:
            # Sharp drop to edge shadow
            value = int(237 - (progress - 0.85) * 2200)
        else:
            # Dark bottom edge
            value = int(83 - (progress - 0.92) * 600)

        value = max(30, min(255, value))

        # PURE chrome - no color tint, just gray values
        draw.line([(0, y), (width, y)], fill=(value, value, value, 255))

    return img

def add_angular_bevel_outline(draw, x, y, text, font, thickness=3):
    """Add angular, straight beveled outline like the buttons"""
    # Draw angular outline in 8 directions for thickness
    offsets = []

    # Build thick angular outline
    for t in range(1, thickness + 1):
        offsets.extend([
            (-t, -t),   # Top-left
            (t, -t),    # Top-right
            (-t, t),    # Bottom-left
            (t, t),     # Bottom-right
            (-t, 0),    # Left
            (t, 0),     # Right
            (0, -t),    # Top
            (0, t),     # Bottom
        ])

    # Dark bevel edge (simulates depth)
    for ox, oy in offsets:
        draw.text((x + ox, y + oy), text, font=font, fill=(25, 25, 25, 200))

def add_mechanical_frame(draw, x, y, w, h):
    """Add angular mechanical frame like button edges"""
    frame_color = (160, 160, 160, 255)  # Chrome frame
    dark_edge = (50, 50, 50, 255)       # Dark beveled edge
    highlight = (230, 230, 230, 255)    # Bright beveled edge

    thickness = 3
    inset = 8

    # ANGULAR FRAME with beveled edges
    corners = [
        # Top-left corner
        [(x - 40, y - 25), (x + 20, y - 25), (x + 20, y - 25 + inset), (x - 40 + inset, y - 25 + inset)],
        [(x - 40, y - 25), (x - 40, y + 20), (x - 40 + inset, y + 20), (x - 40 + inset, y - 25 + inset)],

        # Top-right corner
        [(x + w + 40, y - 25), (x + w - 20, y - 25), (x + w - 20, y - 25 + inset), (x + w + 40 - inset, y - 25 + inset)],
        [(x + w + 40, y - 25), (x + w + 40, y + 20), (x + w + 40 - inset, y + 20), (x + w + 40 - inset, y - 25 + inset)],

        # Bottom-left corner
        [(x - 40, y + h + 25), (x + 20, y + h + 25), (x + 20, y + h + 25 - inset), (x - 40 + inset, y + h + 25 - inset)],
        [(x - 40, y + h + 25), (x - 40, y + h - 20), (x - 40 + inset, y + h - 20), (x - 40 + inset, y + h + 25 - inset)],

        # Bottom-right corner
        [(x + w + 40, y + h + 25), (x + w - 20, y + h + 25), (x + w - 20, y + h + 25 - inset), (x + w + 40 - inset, y + h + 25 - inset)],
        [(x + w + 40, y + h + 25), (x + w + 40, y + h - 20), (x + w + 40 - inset, y + h - 20), (x + w + 40 - inset, y + h + 25 - inset)],
    ]

    # Draw beveled frame segments
    for segment in corners:
        # Dark bottom/right edge
        draw.polygon(segment, fill=dark_edge, outline=dark_edge)
        # Highlight top/left edge
        draw.line([segment[0], segment[1]], fill=highlight, width=2)
        draw.line([segment[0], segment[3]], fill=highlight, width=2)
        # Main frame
        draw.polygon(segment, fill=None, outline=frame_color, width=thickness)

def create_pure_chrome_phigen(width=900, height=160):
    """
    Create 100% PURE CHROME PhiGEN with angular beveled edges
    NO GREEN - just pure polished metal
    """
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Load terminator/mechanical font
    try:
        font_size = 95
        font_options = [
            r"E:\PythonProjects\PhiGEN\FONTS\MECH\TREAL\terminator real nfi.ttf",
            r"E:\PythonProjects\PhiGEN\FONTS\MECH\GENI\TerminatorGenisys-Vodx.ttf",
            r"E:\PythonProjects\PhiGEN\FONTS\MECH\ARNOLD\Schwarzenegger-203K.ttf",
            "C:\\Windows\\Fonts\\impact.ttf",
        ]

        font = None
        for font_path in font_options:
            if os.path.exists(font_path):
                font = ImageFont.truetype(font_path, font_size)
                print(f"Using font: {font_path}")
                break

        if font is None:
            font = ImageFont.load_default()
    except Exception as e:
        print(f"Font error: {e}")
        font = ImageFont.load_default()

    text = "PhiGEN"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    x = (width - text_width) // 2
    y = (height - text_height) // 2 - 5

    # LAYER 1: Aggressive black shadow
    shadow_layer = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow_layer)
    shadow_draw.text((x + 10, y + 10), text, font=font, fill=(0, 0, 0, 200))
    shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(5))
    img = Image.alpha_composite(img, shadow_layer)

    # LAYER 2: Angular beveled dark outline
    outline_layer = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    outline_draw = ImageDraw.Draw(outline_layer)
    add_angular_bevel_outline(outline_draw, x, y, text, font, thickness=4)
    img = Image.alpha_composite(img, outline_layer)

    # LAYER 3: Pure chrome gradient fill
    chrome = create_pure_chrome_gradient(text_width + 60, text_height + 60)

    mask = Image.new('L', (width, height), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.text((x, y), text, font=font, fill=255)

    chrome_layer = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    chrome_layer.paste(chrome, (x - 30, y - 30))
    chrome_layer.putalpha(mask)
    img = Image.alpha_composite(img, chrome_layer)

    # LAYER 4: BLAZING white top highlight (sharp specular)
    highlight_layer = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    highlight_draw = ImageDraw.Draw(highlight_layer)
    highlight_draw.text((x, y - 4), text, font=font, fill=(255, 255, 255, 255))

    highlight_mask = Image.new('L', (width, height), 0)
    highlight_mask_draw = ImageDraw.Draw(highlight_mask)
    for i in range(height // 7):
        alpha = int(255 * (1 - i / (height / 7)) ** 3)
        highlight_mask_draw.rectangle([0, i, width, i + 1], fill=alpha)

    highlight_layer.putalpha(ImageChops.multiply(highlight_layer.split()[3], highlight_mask))
    img = Image.alpha_composite(img, highlight_layer)

    # LAYER 5: Sharp dark bottom edge (angular shadow)
    edge_layer = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    edge_draw = ImageDraw.Draw(edge_layer)
    edge_draw.text((x, y + 4), text, font=font, fill=(15, 15, 15, 220))

    edge_mask = Image.new('L', (width, height), 0)
    edge_mask_draw = ImageDraw.Draw(edge_mask)
    for i in range(height // 5):
        y_pos = height - i - 1
        alpha = int(255 * (1 - i / (height / 5)) ** 2.5)
        edge_mask_draw.rectangle([0, y_pos, width, y_pos + 1], fill=alpha)

    edge_layer.putalpha(ImageChops.multiply(edge_layer.split()[3], edge_mask))
    img = Image.alpha_composite(img, edge_layer)

    # LAYER 6: Angular mechanical frame (like button edges)
    frame_layer = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    frame_draw = ImageDraw.Draw(frame_layer)
    add_mechanical_frame(frame_draw, x, y, text_width, text_height)
    img = Image.alpha_composite(img, frame_layer)

    # LAYER 7: Subtle brushed metal texture
    from random import randint, seed
    seed(42)  # Consistent pattern

    noise_layer = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    noise_draw = ImageDraw.Draw(noise_layer)

    # Horizontal brush strokes
    for _ in range(300):
        nx = randint(0, width)
        ny = randint(0, height)
        line_length = randint(3, 10)
        brightness = randint(190, 255)
        noise_draw.line(
            [(nx, ny), (nx + line_length, ny)],
            fill=(brightness, brightness, brightness, 15)
        )

    noise_layer.putalpha(ImageChops.multiply(noise_layer.split()[3], mask))
    img = Image.alpha_composite(img, noise_layer)

    return img

if __name__ == "__main__":
    print("Generating 100% PURE CHROME PhiGEN title...")
    print("Angular beveled edges - NO GREEN - Pure polished metal")

    # Standard size
    img = create_pure_chrome_phigen(900, 160)
    img.save("phigen_title_pure_chrome.png")
    print("[OK] Created phigen_title_pure_chrome.png (900x160)")

    # Large version
    img_large = create_pure_chrome_phigen(1300, 220)
    img_large.save("phigen_title_pure_chrome_large.png")
    print("[OK] Created phigen_title_pure_chrome_large.png (1300x220)")

    print("\nDone! 100% pure chrome - no green - angular beveled like your buttons!")
