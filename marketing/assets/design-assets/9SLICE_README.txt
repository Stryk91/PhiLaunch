PHIGEN 9-SLICE BORDER SCALING GUIDE
====================================

Created: 2025-11-04
Purpose: Enable dynamic resizing of UI elements while preserving corner details

WHAT IS 9-SLICE SCALING?
-------------------------
9-slice scaling divides an image into 9 regions:

    +--------+----------------+--------+
    | Corner |      Edge      | Corner |  <- Top (fixed corners, stretch edge)
    +--------+----------------+--------+
    |        |                |        |
    | Edge   |     Center     | Edge   |  <- Middle (stretch edges, fill center)
    |        |                |        |
    +--------+----------------+--------+
    | Corner |      Edge      | Corner |  <- Bottom (fixed corners, stretch edge)
    +--------+----------------+--------+

- Corners: Stay FIXED at original size (preserve decorative details)
- Edges: STRETCH or TILE to fit new dimensions
- Center: FILLS the remaining space (usually transparent or solid color)

WHY USE 9-SLICE?
----------------
Without 9-slice:
✗ Entire image stretches/squashes - corners get distorted
✗ Circuit traces, brackets, LEDs become warped
✗ Chrome effects look wrong at different sizes

With 9-slice:
✓ Corners stay crisp and detailed at any size
✓ Edges stretch smoothly (chrome borders, straight lines)
✓ Decorative elements (brackets, LEDs, circuits) stay perfect
✓ Works with Qt's QLineEdit, QTextEdit, any widget that supports border-image

FILES CREATED:
--------------
1. list_panel_9slice.svg                - Optimized list panel border for slicing
2. list_panel_9slice_ultra_smooth.png   - 600x400 (12.7 KB)
3. text_input_9slice.svg                - Optimized text input border for slicing
4. text_input_9slice_ultra_smooth.png   - 500x50 (4.2 KB)
5. example_9slice_ui.py                 - Complete working demo
6. render_9slice.py                     - Rendering script

9-SLICE DESIGN PRINCIPLES:
--------------------------
When creating 9-slice graphics:

1. Corner regions (40x40px for list, 20x20px for inputs):
   - Contains ALL decorative elements (brackets, LEDs, circuit traces)
   - Must be self-contained and look good at fixed size
   - Never put important details outside corner regions

2. Edge regions (between corners):
   - Simple, repeatable patterns only
   - Chrome borders, straight lines, subtle accents
   - Should look good when tiled or stretched
   - No complex decorations

3. Center region:
   - Usually transparent or solid color
   - Widget content appears here
   - No decorative elements

USAGE IN QT/PYQT6:
------------------

Basic syntax:
    border-image: url(path/to/image.png) TOP RIGHT BOTTOM LEFT stretch;

The four numbers define slice distances from each edge in pixels.

Example 1: List Panel (QTextEdit)
    QTextEdit {
        border-image: url(list_panel_9slice_ultra_smooth.png) 40 40 40 40 stretch;
        padding: 45px;  /* Space for the border graphic */
        background-color: rgba(5, 10, 6, 0.95);
        color: #39ff14;
    }

Explanation:
    - 40 40 40 40 = slice 40px from top, right, bottom, left
    - Corners are 40x40px and stay fixed
    - Edges stretch between corners
    - padding: 45px gives room for the border inside the widget
    - background-color shows through the center

Example 2: Text Input (QLineEdit)
    QLineEdit {
        border-image: url(text_input_9slice_ultra_smooth.png) 20 20 20 20 stretch;
        padding: 10px 40px;  /* Vertical 10px, horizontal 40px */
        background-color: rgba(10, 15, 10, 0.95);
        color: #39ff14;
    }

Explanation:
    - 20 20 20 20 = slice 20px from all sides
    - Corners are 20x20px (contains brackets and LEDs)
    - Horizontal padding 40px accommodates corner brackets
    - Vertical padding 10px for text spacing

Example 3: Alternative - 'repeat' instead of 'stretch'
    QTextEdit {
        border-image: url(list_panel_9slice_ultra_smooth.png) 40 40 40 40 repeat;
    }

    - 'stretch': Edges stretch to fit (smooth, continuous look)
    - 'repeat': Edges tile/repeat (good for patterns)
    - 'round': Like repeat but scales to fit evenly

HOW TO CALCULATE SLICE VALUES:
-------------------------------
1. Open the PNG in an image editor
2. Find where decorative elements end (brackets, circuits, LEDs)
3. Measure from edge to this point
4. Use these measurements for slice values

For our assets:
    - list_panel_9slice_ultra_smooth.png: Use 40 40 40 40
      (Corners contain brackets at ~40px from edges)

    - text_input_9slice_ultra_smooth.png: Use 20 20 20 20
      (Corners contain brackets at ~20px from edges)

PADDING vs SLICE VALUES:
------------------------
slice values: Tell Qt where to cut the image
padding: Creates space inside the widget for the border

Rule of thumb: padding ≈ slice + 5px extra

Example:
    border-image: url(panel.png) 40 40 40 40 stretch;
    padding: 45px;  /* 40px for border + 5px breathing room */

COMMON ISSUES & SOLUTIONS:
--------------------------

Issue 1: Corners look cut off
    → Increase padding values
    → Check that slice values match actual corner size in PNG

Issue 2: Edges look weird/distorted
    → Try 'repeat' instead of 'stretch'
    → Ensure edge regions are simple/uniform in the original graphic

Issue 3: Content overlaps border
    → Increase padding
    → Reduce font size or content margins

Issue 4: Border looks blurry
    → Use ultra_smooth PNG versions (already 8x anti-aliased)
    → Don't resize widget to very small sizes

Issue 5: Text cursor not visible
    → Increase padding
    → Set explicit text color: color: #39ff14;
    → Check background opacity isn't too high

TESTING YOUR 9-SLICE:
---------------------
1. Run: python example_9slice_ui.py
2. Resize the window - watch the borders scale
3. Corners should stay crisp and detailed
4. Edges should stretch smoothly
5. No distortion of brackets, LEDs, or circuit traces

COMPARISON:
-----------

Method 1: Solid PNG background (no scaling)
    ✗ Fixed size only
    ✗ Doesn't resize with widget
    ✓ Simple to implement

Method 2: CSS borders only (no PNG)
    ✓ Perfect scaling
    ✗ Can't achieve complex chrome effects
    ✗ No decorative elements (brackets, LEDs)

Method 3: 9-Slice PNG (RECOMMENDED)
    ✓ Perfect scaling with decorative elements preserved
    ✓ Complex graphics (chrome, brackets, LEDs)
    ✓ Works with any widget size
    ✓ Professional, polished look

ADVANCED: ASYMMETRIC SLICING
-----------------------------
You can use different values for each side:

    border-image: url(panel.png) 50 30 40 30 stretch;
                                  ^  ^  ^  ^
                              top  |  |  left
                                right  |
                                    bottom

Useful when:
- Top has more decorations than bottom
- Left/right corners are different sizes
- Design is intentionally asymmetric

PERFORMANCE NOTES:
------------------
✓ 9-slice is GPU-accelerated in Qt
✓ No performance penalty vs regular images
✓ Files are small (list: 12.7KB, input: 4.2KB)
✓ Rendered once at startup, cached by Qt
✓ Resizing is real-time smooth

INTEGRATION CHECKLIST:
----------------------
[ ] PNG files in correct directory (TEMPSVG/)
[ ] Correct slice values calculated (measure in image editor)
[ ] Padding values set (slice + 5px extra)
[ ] Background color matches theme (rgba with transparency)
[ ] Text color set (#39ff14)
[ ] Test resizing - corners stay crisp?
[ ] Text cursor visible and blinking?
[ ] Selection color set (rgba(57, 255, 20, 0.3))?

RESOURCES:
----------
- Qt Documentation: https://doc.qt.io/qt-6/stylesheet-reference.html#border-image
- Example app: example_9slice_ui.py
- Test by running and resizing the window

SUMMARY:
--------
9-slice scaling is the BEST method for our tactical UI because:
✓ Preserves all decorative details (brackets, LEDs, circuits)
✓ Chrome effects stay perfect at any size
✓ Dynamic resizing without distortion
✓ Professional appearance
✓ Easy to implement with border-image CSS

Use border-image: url(...) SLICE_VALUES stretch; and enjoy perfect scaling!
