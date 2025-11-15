import os
import sys

# Add Cairo DLLs to the DLL search path
cairo_bin = r'E:\Utilities\MINGSYS2\ucrt64\bin'
os.environ['PATH'] = cairo_bin + os.pathsep + os.environ.get('PATH', '')

# Also add to DLL search paths for Windows
if hasattr(os, 'add_dll_directory'):
    os.add_dll_directory(cairo_bin)

print("Testing cairosvg with MSYS2 Cairo libraries...")
print(f"Cairo bin path: {cairo_bin}")

try:
    import cairosvg

    # Test conversion
    svg_path = r'E:\PythonProjects\PhiGEN\TEMPSVG\BTNS.svg'
    png_path = r'E:\PythonProjects\PhiGEN\TEMPSVG\BTNS_cairo.png'

    print(f"\nConverting {svg_path}...")
    cairosvg.svg2png(
        url=svg_path,
        write_to=png_path,
        output_width=880,
        output_height=320
    )

    print(f"✓ Success! PNG saved to: {png_path}")
    print(f"  Method: cairosvg with MSYS2 Cairo")

    # Check file size
    size = os.path.getsize(png_path)
    print(f"  File size: {size:,} bytes")

except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()