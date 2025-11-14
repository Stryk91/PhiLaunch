import os
import sys

svg_path = r'E:\PythonProjects\PhiGEN\TEMPSVG\BTNS.svg'
png_path = r'E:\PythonProjects\PhiGEN\TEMPSVG\BTNS.png'

# Try multiple methods
methods_tried = []

# Method 1: Try cairosvg
try:
    import cairosvg
    cairosvg.svg2png(url=svg_path, write_to=png_path, output_width=880, output_height=320)
    print(f"Success! PNG saved to: {png_path}")
    print("Method: cairosvg")
    sys.exit(0)
except ImportError:
    methods_tried.append("cairosvg (not installed)")
except Exception as e:
    methods_tried.append(f"cairosvg (error: {e})")

# Method 2: Try svglib + reportlab
try:
    from svglib.svglib import svg2rlg
    from reportlab.graphics import renderPM
    drawing = svg2rlg(svg_path)
    renderPM.drawToFile(drawing, png_path, fmt="PNG", dpi=300)
    print(f"Success! PNG saved to: {png_path}")
    print("Method: svglib + reportlab")
    sys.exit(0)
except ImportError:
    methods_tried.append("svglib/reportlab (not installed)")
except Exception as e:
    methods_tried.append(f"svglib/reportlab (error: {e})")

# Method 3: Try wand (ImageMagick)
try:
    from wand.image import Image
    with Image(filename=svg_path, resolution=300) as img:
        img.format = 'png'
        img.save(filename=png_path)
    print(f"Success! PNG saved to: {png_path}")
    print("Method: wand (ImageMagick)")
    sys.exit(0)
except ImportError:
    methods_tried.append("wand (not installed)")
except Exception as e:
    methods_tried.append(f"wand (error: {e})")

# Method 4: Try Pillow with svg support
try:
    from PIL import Image
    import io
    # Read SVG and convert
    img = Image.open(svg_path)
    img.save(png_path, 'PNG')
    print(f"Success! PNG saved to: {png_path}")
    print("Method: Pillow")
    sys.exit(0)
except ImportError:
    methods_tried.append("Pillow (not installed)")
except Exception as e:
    methods_tried.append(f"Pillow (error: {e})")

# If all methods failed
print("Failed to convert SVG to PNG. Tried:")
for method in methods_tried:
    print(f"  - {method}")
print("\nTo fix, install one of these:")
print("  pip install cairosvg")
print("  pip install svglib reportlab")
print("  pip install wand (requires ImageMagick)")
sys.exit(1)