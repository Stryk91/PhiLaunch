#!/usr/bin/env python3
"""
Generate ULTRA 3D PhiGEN title with extreme depth
Rendered at 8x resolution then downscaled for maximum quality
Heavy gradients and depth like the buttons
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
import os

def create_ultra_chrome_3d_gradient(width, height):
    """Ultra-detailed chrome with extreme 3D depth - rendered at high res"""
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    for y in range(height):
        progress = y / height

        # EXTREME 3D chrome with multiple reflection bands
        if progress < 0.01:
            value = 255  # Blazing edge highlight
        elif progress < 0.03:
            value = int(255 - (progress - 0.01) * 3000)
        elif progress < 0.05:
            value = 195
        elif progress < 0.08:
            value = int(195 - (progress - 0.05) * 2500)
        elif progress < 0.10:
            value = 120
        elif progress < 0.15:
            value = int(120 + (progress - 0.10) * 1600)
        elif progress < 0.25:
            value = int(200 - (progress - 0.15) * 400)
        elif progress < 0.35:
            value = int(160 + (progress - 0.25) * 800)
        elif progress < 0.45:
            value = int(240 - (progress - 0.35) * 1000)
        elif progress < 0.50:
            value = int(140 - (progress - 0.45) * 800)
        elif progress < 0.55:
            value = int(100 + (progress - 0.50) * 1200)
        elif progress < 0.65:
            value = int(160 + (progress - 0.55) * 600)
        elif progress < 0.75:
            value = int(220 - (progress - 0.65) * 800)
        elif progress < 0.82:
            value = int(140 + (progress - 0.75) * 1100)
        elif progress < 0.88:
            value = int(217 + (progress - 0.82) * 500)
        elif progress < 0.92:
            value = int(247 - (progress - 0.88) * 3000)
        elif progress < 0.96:
            value = int(127 + (progress - 0.92) * 1500)
        else:
            value = int(187 - (progress - 0.96) * 2500)

        value = max(25, min(255, value))

        # Pure chrome - grayscale only
        draw.line([(0, y), (width, y)], fill=(value, value, value, 255))

    return img

def add_extreme_depth_outline(draw, x, y, text, font, max_depth=15):
    """Add extreme 3D depth with gradient shadow"""
    # Create deep 3D extrusion
    for depth in range(max_depth, 0, -1):
        # Calculate shadow darkness based on depth
        darkness = int(15 + (max_depth - depth) * 5)
        alpha = int(180 - depth * 8)

        # Offset for 3D effect (down and right)
        offset_x = depth
        offset_y = depth

        draw.text(
            (x + offset_x, y + offset_y),
            text,
            font=font,
            fill=(darkness, darkness, darkness, alpha)
        )

def add_ultra_mechanical_frame(draw, x, y, w, h, scale=1):
    """Ultra-detailed mechanical frame with 3D beveling"""
    frame_color = (170, 170, 170, 255)
    dark_bevel = (35, 35, 35, 255)
    mid_bevel = (100, 100, 100, 255)
    highlight = (245, 245, 245, 255)

    thickness = int(4 * scale)
    inset = int(12 * scale)
    corner_size = int(30 * scale)

    # Four corner frames with heavy 3D beveling
    corners_data = [
        # (start_x, start_y, direction)
        (x - 50 * scale, y - 35 * scale, "top-left"),
        (x + w + 50 * scale, y - 35 * scale, "top-right"),
        (x - 50 * scale, y + h + 35 * scale, "bottom-left"),
        (x + w + 50 * scale, y + h + 35 * scale, "bottom-right"),
    ]

    for cx, cy, corner_type in corners_data:
        if corner_type == "top-left":
            # Horizontal bar
            points_outer = [(cx, cy), (cx + corner_size, cy),
                           (cx + corner_size - inset, cy + inset), (cx + inset, cy + inset)]
            points_inner = [(cx, cy), (cx, cy + corner_size),
                           (cx + inset, cy + corner_size - inset), (cx + inset, cy + inset)]

        elif corner_type == "top-right":
            points_outer = [(cx, cy), (cx - corner_size, cy),
                           (cx - corner_size + inset, cy + inset), (cx - inset, cy + inset)]
            points_inner = [(cx, cy), (cx, cy + corner_size),
                           (cx - inset, cy + corner_size - inset), (cx - inset, cy + inset)]

        elif corner_type == "bottom-left":
            points_outer = [(cx, cy), (cx + corner_size, cy),
                           (cx + corner_size - inset, cy - inset), (cx + inset, cy - inset)]
            points_inner = [(cx, cy), (cx, cy - corner_size),
                           (cx + inset, cy - corner_size + inset), (cx + inset, cy - inset)]

        else:  # bottom-right
            points_outer = [(cx, cy), (cx - corner_size, cy),
                           (cx - corner_size + inset, cy - inset), (cx - inset, cy - inset)]
            points_inner = [(cx, cy), (cx, cy - corner_size),
                           (cx - inset, cy - corner_size + inset), (cx - inset, cy - inset)]

        # Draw 3D beveled segments
        for points in [points_outer, points_inner]:
            # Dark shadow base
            shadow_points = [(p[0] + 2 * scale, p[1] + 2 * scale) for p in points]
            draw.polygon(shadow_points, fill=dark_bevel)

            # Mid-tone bevel
            draw.polygon(points, fill=mid_bevel)

            # Highlight edges
            draw.line([points[0], points[1]], fill=highlight, width=int(3 * scale))
            draw.line([points[0], points[3]], fill=highlight, width=int(3 * scale))

            # Main frame outline
            draw.polygon(points, fill=None, outline=frame_color, width=thickness)

def create_ultra_3d_phigen(base_width=900, base_height=160, scale=8):
    """
    Create PhiGEN at 8x resolution with extreme 3D effects
    Then downscale for ultra-smooth result
    """
    width = base_width * scale
    height = base_height * scale

    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Load font at scaled size
    try:
        font_size = int(95 * scale)
        font_path = r"E:\PythonProjects\PhiGEN\FONTS\MECH\TREAL\terminator real nfi.ttf"

        if os.path.exists(font_path):
            font = ImageFont.truetype(font_path, font_size)
            print(f"Using font at {font_size}pt: {font_path}")
        else:
            font = ImageFont.load_default()
    except Exception as e:
        print(f"Font error: {e}")
        font = ImageFont.load_default()

    text = "PhiGEN"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    x = (width - text_width) // 2
    y = (height - text_height) // 2 - int(5 * scale)

    print(f"Rendering at {width}x{height} (text: {text_width}x{text_height})")

    # LAYER 1: Deep multi-level shadow for extreme depth
    shadow_layer = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow_layer)

    # Multiple shadow layers for depth
    for i in range(5):
        offset = int((15 + i * 3) * scale)
        alpha = int(60 - i * 10)
        shadow_draw.text((x + offset, y + offset), text, font=font, fill=(0, 0, 0, alpha))

    shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(int(8 * scale)))
    img = Image.alpha_composite(img, shadow_layer)

    # LAYER 2: Extreme 3D extrusion depth
    depth_layer = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    depth_draw = ImageDraw.Draw(depth_layer)
    add_extreme_depth_outline(depth_draw, x, y, text, font, max_depth=int(20 * scale))
    img = Image.alpha_composite(img, depth_layer)

    # LAYER 3: Dark angular outline
    outline_layer = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    outline_draw = ImageDraw.Draw(outline_layer)

    outline_thickness = int(5 * scale)
    for t in range(1, outline_thickness + 1):
        for ox, oy in [(-t, -t), (t, -t), (-t, t), (t, t), (-t, 0), (t, 0), (0, -t), (0, t)]:
            outline_draw.text((x + ox, y + oy), text, font=font, fill=(20, 20, 20, 200))

    img = Image.alpha_composite(img, outline_layer)

    # LAYER 4: Ultra-detailed chrome gradient
    chrome = create_ultra_chrome_3d_gradient(text_width + int(120 * scale), text_height + int(120 * scale))

    mask = Image.new('L', (width, height), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.text((x, y), text, font=font, fill=255)

    chrome_layer = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    chrome_layer.paste(chrome, (x - int(60 * scale), y - int(60 * scale)))
    chrome_layer.putalpha(mask)
    img = Image.alpha_composite(img, chrome_layer)

    # LAYER 5: Multiple specular highlights (extreme 3D feel)
    for highlight_offset, highlight_strength in [(0, 255), (2, 200), (4, 150)]:
        highlight_layer = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        highlight_draw = ImageDraw.Draw(highlight_layer)
        highlight_draw.text((x, y - int((6 + highlight_offset) * scale)), text, font=font,
                          fill=(255, 255, 255, highlight_strength))

        highlight_mask = Image.new('L', (width, height), 0)
        highlight_mask_draw = ImageDraw.Draw(highlight_mask)
        for i in range(height // (8 - highlight_offset)):
            alpha = int(255 * (1 - i / (height / (8 - highlight_offset))) ** 4)
            highlight_mask_draw.rectangle([0, i, width, i + 1], fill=alpha)

        highlight_layer.putalpha(ImageChops.multiply(highlight_layer.split()[3], highlight_mask))
        img = Image.alpha_composite(img, highlight_layer)

    # LAYER 6: Multiple dark edge shadows (depth)
    for edge_offset, edge_strength in [(0, 230), (2, 180), (4, 130)]:
        edge_layer = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        edge_draw = ImageDraw.Draw(edge_layer)
        edge_draw.text((x, y + int((6 + edge_offset) * scale)), text, font=font,
                      fill=(10, 10, 10, edge_strength))

        edge_mask = Image.new('L', (width, height), 0)
        edge_mask_draw = ImageDraw.Draw(edge_mask)
        for i in range(height // (6 - edge_offset)):
            y_pos = height - i - 1
            alpha = int(255 * (1 - i / (height / (6 - edge_offset))) ** 3)
            edge_mask_draw.rectangle([0, y_pos, width, y_pos + 1], fill=alpha)

        edge_layer.putalpha(ImageChops.multiply(edge_layer.split()[3], edge_mask))
        img = Image.alpha_composite(img, edge_layer)

    # LAYER 7: Ultra-detailed mechanical frame
    frame_layer = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    frame_draw = ImageDraw.Draw(frame_layer)
    add_ultra_mechanical_frame(frame_draw, x, y, text_width, text_height, scale)
    img = Image.alpha_composite(img, frame_layer)

    # LAYER 8: High-res brushed metal texture
    from random import randint, seed
    seed(42)

    noise_layer = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    noise_draw = ImageDraw.Draw(noise_layer)

    for _ in range(int(1500 * scale)):
        nx = randint(0, width)
        ny = randint(0, height)
        line_length = randint(int(5 * scale), int(15 * scale))
        brightness = randint(200, 255)
        noise_draw.line(
            [(nx, ny), (nx + line_length, ny)],
            fill=(brightness, brightness, brightness, 12),
            width=int(scale / 2)
        )

    noise_layer.putalpha(ImageChops.multiply(noise_layer.split()[3], mask))
    img = Image.alpha_composite(img, noise_layer)

    # DOWNSCALE with high-quality resampling for ultra-smooth result
    print(f"Downscaling to {base_width}x{base_height}...")
    img_final = img.resize((base_width, base_height), Image.Resampling.LANCZOS)

    return img_final

if __name__ == "__main__":
    print("="*70)
    print("ULTRA 3D PhiGEN Title Generator")
    print("Rendering at 8x resolution (7200x1280) for maximum detail...")
    print("="*70)

    img = create_ultra_3d_phigen(900, 160, scale=8)
    img.save("phigen_title_ultra_3d.png")
    print("\n[OK] Created phigen_title_ultra_3d.png (900x160 with 8x detail)")

    print("\nDone! Ultra-smooth 3D chrome with extreme depth and gradients!")
