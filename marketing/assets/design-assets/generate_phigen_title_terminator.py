#!/usr/bin/env python3
"""
Generate aggressive metallic PhiGEN title - T-800 terminator style
Polished chrome skeleton aesthetic - intimidating and industrial
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
import os

def create_terminator_chrome_gradient(width, height):
    """Create ultra-polished chrome gradient like T-800 endoskeleton"""
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    for y in range(height):
        progress = y / height

        # Aggressive chrome with sharp transitions
        if progress < 0.05:
            # Bright highlight at top
            value = 240
        elif progress < 0.15:
            # Sharp drop to shadow
            value = int(240 - (progress - 0.05) * 1500)
        elif progress < 0.25:
            # Mid chrome
            value = int(100 + (progress - 0.15) * 800)
        elif progress < 0.4:
            # Bright reflection band
            value = int(180 + (progress - 0.25) * 400)
        elif progress < 0.6:
            # Deep shadow valley
            value = int(240 - (progress - 0.4) * 900)
        elif progress < 0.75:
            # Rise to mid-tone
            value = int(60 + (progress - 0.6) * 600)
        elif progress < 0.85:
            # Sharp highlight
            value = int(150 + (progress - 0.75) * 800)
        else:
            # Dark bottom edge
            value = int(230 - (progress - 0.85) * 1200)

        value = max(40, min(255, value))

        # Add slight blue tint to chrome for cold metal feel
        r = value
        g = value
        b = min(255, value + 15)  # Slight blue tint

        draw.line([(0, y), (width, y)], fill=(r, g, b, 255))

    return img

def add_mechanical_details(draw, x, y, w, h, color):
    """Add mechanical/robotic details like terminator endoskeleton"""
    # Small tech details
    detail_color = color

    # Rivets/bolts
    for i in range(5):
        rx = x + (i * w // 5) + w // 10
        ry = y - 8
        draw.ellipse([rx-3, ry-3, rx+3, ry+3], fill=detail_color, outline=(180, 180, 200, 255))

    # Bottom rivets
    for i in range(5):
        rx = x + (i * w // 5) + w // 10
        ry = y + h + 8
        draw.ellipse([rx-3, ry-3, rx+3, ry+3], fill=detail_color, outline=(180, 180, 200, 255))

def create_terminator_phigen(width=800, height=140):
    """
    Create intimidating T-800 style PhiGEN title
    """
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Load bold aggressive font
    try:
        font_size = 90
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

    text = "PhiGEN"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    x = (width - text_width) // 2
    y = (height - text_height) // 2 - 5

    # LAYER 1: Deep aggressive shadow
    shadow_layer = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow_layer)
    shadow_draw.text((x + 8, y + 8), text, font=font, fill=(0, 0, 0, 180))
    shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(4))
    img = Image.alpha_composite(img, shadow_layer)

    # LAYER 2: Minimal green glow (much subtler, more intimidating)
    glow_layer = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow_layer)
    glow_draw.text((x, y), text, font=font, fill=(57, 255, 20, 80))
    glow_layer = glow_layer.filter(ImageFilter.GaussianBlur(6))
    img = Image.alpha_composite(img, glow_layer)

    # LAYER 3: Ultra-polished chrome base
    chrome = create_terminator_chrome_gradient(text_width + 40, text_height + 40)

    # Create text mask
    mask = Image.new('L', (width, height), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.text((x, y), text, font=font, fill=255)

    # Apply chrome to text
    chrome_layer = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    chrome_layer.paste(chrome, (x - 20, y - 20))
    chrome_layer.putalpha(mask)
    img = Image.alpha_composite(img, chrome_layer)

    # LAYER 4: AGGRESSIVE top highlight (sharp specular reflection)
    highlight_layer = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    highlight_draw = ImageDraw.Draw(highlight_layer)
    highlight_draw.text((x, y - 3), text, font=font, fill=(255, 255, 255, 220))

    # Sharp highlight mask - only top 15%
    highlight_mask = Image.new('L', (width, height), 0)
    highlight_mask_draw = ImageDraw.Draw(highlight_mask)
    for i in range(height // 6):
        alpha = int(255 * (1 - i / (height / 6)) ** 2)  # Sharper falloff
        highlight_mask_draw.rectangle([0, i, width, i + 1], fill=alpha)

    highlight_layer.putalpha(ImageChops.multiply(highlight_layer.split()[3], highlight_mask))
    img = Image.alpha_composite(img, highlight_layer)

    # LAYER 5: Sharp dark bottom edge (mechanical edge)
    edge_layer = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    edge_draw = ImageDraw.Draw(edge_layer)
    edge_draw.text((x, y + 3), text, font=font, fill=(10, 10, 15, 180))

    edge_mask = Image.new('L', (width, height), 0)
    edge_mask_draw = ImageDraw.Draw(edge_mask)
    for i in range(height // 5):
        y_pos = height - i - 1
        alpha = int(255 * (1 - i / (height / 5)) ** 2)
        edge_mask_draw.rectangle([0, y_pos, width, y_pos + 1], fill=alpha)

    edge_layer.putalpha(ImageChops.multiply(edge_layer.split()[3], edge_mask))
    img = Image.alpha_composite(img, edge_layer)

    # LAYER 6: Thin sharp metallic outline
    outline_layer = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    outline_draw = ImageDraw.Draw(outline_layer)

    # Sharp metallic outline
    for offset_x, offset_y in [(-2, -2), (2, -2), (-2, 2), (2, 2)]:
        outline_draw.text((x + offset_x, y + offset_y), text, font=font, fill=(40, 40, 50, 150))

    # Green accent only on corners
    for offset_x, offset_y in [(-1, -1), (1, 1)]:
        outline_draw.text((x + offset_x, y + offset_y), text, font=font, fill=(57, 255, 20, 40))

    img = Image.alpha_composite(img, outline_layer)

    # LAYER 7: Mechanical/industrial details
    mech_layer = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    mech_draw = ImageDraw.Draw(mech_layer)

    # Aggressive corner brackets (industrial clamps)
    bracket_color = (57, 255, 20, 200)
    metal_color = (180, 180, 200, 255)
    bracket_size = 20
    thickness = 3

    corners = [
        (x - 35, y - 20),
        (x + text_width + 15, y - 20),
        (x - 35, y + text_height + 5),
        (x + text_width + 15, y + text_height + 5)
    ]

    for cx, cy in corners:
        # Heavy L-bracket
        mech_draw.line([(cx, cy), (cx + bracket_size, cy)], fill=metal_color, width=thickness)
        mech_draw.line([(cx, cy), (cx, cy + bracket_size)], fill=metal_color, width=thickness)

        # Green tech accent inside bracket
        mech_draw.line([(cx + 3, cy + 3), (cx + bracket_size - 3, cy + 3)], fill=bracket_color, width=1)
        mech_draw.line([(cx + 3, cy + 3), (cx + 3, cy + bracket_size - 3)], fill=bracket_color, width=1)

        # Corner bolt
        mech_draw.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=metal_color, outline=bracket_color)

    # Industrial horizontal bars (like terminator ribcage)
    for i in range(2):
        bar_y = y + text_height // 2 + (i - 0.5) * (text_height // 3)
        # Left bar
        mech_draw.line([(x - 40, bar_y), (x - 5, bar_y)], fill=metal_color, width=2)
        mech_draw.line([(x - 40, bar_y + 1), (x - 5, bar_y + 1)], fill=bracket_color, width=1)
        # Right bar
        mech_draw.line([(x + text_width + 5, bar_y), (x + text_width + 40, bar_y)], fill=metal_color, width=2)
        mech_draw.line([(x + text_width + 5, bar_y + 1), (x + text_width + 40, bar_y + 1)], fill=bracket_color, width=1)

    # Rivet details
    add_mechanical_details(mech_draw, x, y, text_width, text_height, metal_color)

    img = Image.alpha_composite(img, mech_layer)

    # LAYER 8: Final sharpening - brushed metal texture
    # Add subtle noise for brushed metal effect
    from random import randint
    noise_layer = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    noise_draw = ImageDraw.Draw(noise_layer)

    for _ in range(500):
        nx = randint(0, width)
        ny = randint(0, height)
        brightness = randint(200, 255)
        noise_draw.point((nx, ny), fill=(brightness, brightness, brightness, 20))

    # Apply noise only to text area
    noise_layer.putalpha(ImageChops.multiply(noise_layer.split()[3], mask))
    img = Image.alpha_composite(img, noise_layer)

    return img

if __name__ == "__main__":
    print("Generating T-800 TERMINATOR style PhiGEN title...")
    print("Ultra-polished chrome endoskeleton aesthetic...")

    # Standard size
    img = create_terminator_phigen(800, 140)
    img.save("phigen_title_terminator.png")
    print("[OK] Created phigen_title_terminator.png (800x140)")

    # Large version
    img_large = create_terminator_phigen(1200, 200)
    img_large.save("phigen_title_terminator_large.png")
    print("[OK] Created phigen_title_terminator_large.png (1200x200)")

    print("\nDone! This should look like polished T-800 endoskeleton metal - intimidating and industrial!")
