"""
Test script used to check that every display can be converted to drawings.

The results are written in **test_displays.json**.
By following versions on this file, it is easy to see what has changed in a
display in terms of drawings content
"""

from io import TextIOWrapper
import json

from pygyw.layout import displays, fonts


def _unit_test(template: displays.DrawingTemplate, f: TextIOWrapper,
               index: int = 0, name: str = None,):
    if name is None:
        name = template.name

    f.write(f"// Test {index} - {name} - {template.name}\n")
    drawings = template.get_drawings()

    for drawing in drawings:
        f.write(json.dumps(drawing.to_json()))
        f.write("\n")

    f.write("\n")

    return index + 1


index = 0
with open("test_displays.json", "w") as f:
    f.write("// GYW Layout automated tests - Displays\n")

    # Title
    drawing = displays.Title("This is a title")
    index = _unit_test(drawing, f, index=index)

    # Title with different font
    drawing = displays.Title("This is a big title", font=fonts.Fonts.HUGE)
    index = _unit_test(drawing, f, index=index, name="Big title")

    # Paragraph short
    drawing = displays.Paragraph("This is a short paragraph", font=fonts.Fonts.SMALL)
    index = _unit_test(drawing, f, index=index, name="Short paragraph")

    # Paragraph long
    drawing = displays.Paragraph("This is a very very very very very very long paragraph", font=fonts.Fonts.SMALL)
    index = _unit_test(drawing, f, index=index, name="Long paragraph")

    # Paragraph long with big typo
    drawing = displays.Paragraph("This is a very very very very very very long paragraph", font=fonts.Fonts.LARGE)
    index = _unit_test(drawing, f, index=index, name="Long paragraph with bigger typo")

    # Paragraph short with offset
    drawing = displays.Paragraph("This is a short paragraph", font=fonts.Fonts.SMALL, x_offset=40, y_offset=60)
    index = _unit_test(drawing, f, index=index, name="Paragraph with offsets")

    # TextLine
    drawing = displays.TextLine("This is a line")
    index = _unit_test(drawing, f, index=index, name="Text line SMALL")

    # TextLine with big typo
    drawing = displays.TextLine("This is a line", font=fonts.Fonts.LARGE)
    index = _unit_test(drawing, f, index=index, name="Text line big typo")

    # TextLine with left align
    drawing = displays.TextLine("This line is aligned to the left", align=displays.TextAlign.LEFT)
    index = _unit_test(drawing, f, index=index, name="Text line to the left")

    # TextLine with right align
    drawing = displays.TextLine("This line is aligned to the right", align=displays.TextAlign.RIGHT)
    index = _unit_test(drawing, f, index=index, name="Text line to the right")

    # TextLine with top align
    drawing = displays.TextLine("This line is aligned to the top", vertical_align=displays.TextVerticalAlign.TOP)
    index = _unit_test(drawing, f, index=index, name="Text line to the top")

    # TextLine with bottom align
    drawing = displays.TextLine("This line is aligned to the bottom", vertical_align=displays.TextVerticalAlign.BOTTOM)
    index = _unit_test(drawing, f, index=index, name="Text line to the bottom")

    # TextLine with offset
    drawing = displays.TextLine("This line is aligned to the bottom", font=fonts.Fonts.SMALL, x_offset=40, y_offset=60)
    index = _unit_test(drawing, f, index=index, name="Text line with offsets")

    # TextList 1 line
    drawing = displays.TextList(["line 1"])
    index = _unit_test(drawing, f, index=index, name="Text list with 1 line")

    # TextList 3 lines
    drawing = displays.TextList(["line 1", "line 2", "line 3"])
    index = _unit_test(drawing, f, index=index, name="Text list with 3 lines")

    # TextList 6 lines
    drawing = displays.TextList(["line 1", "line 2", "line 3", "line 4", "line 5", "line 6"])
    index = _unit_test(drawing, f, index=index, name="Text list with 6 lines")

    # TextList with big typo
    drawing = displays.TextList(["line 1", "line 2", "line 3"], font=fonts.Fonts.LARGE)
    index = _unit_test(drawing, f, index=index, name="Text list big typo")

    # TextList with left align
    drawing = displays.TextList(["line 1", "line 2", "line 3"], align=displays.TextAlign.LEFT)
    index = _unit_test(drawing, f, index=index, name="Text list to the left")

    # TextList with right align
    drawing = displays.TextList(["line 1", "line 2", "line 3"], align=displays.TextAlign.RIGHT)
    index = _unit_test(drawing, f, index=index, name="Text list to the right")

    # TextList with top align
    drawing = displays.TextList(["line 1", "line 2", "line 3"], vertical_align=displays.TextVerticalAlign.TOP)
    index = _unit_test(drawing, f, index=index, name="Text list to the top")

    # TextList with bottom align
    drawing = displays.TextList(["line 1", "line 2", "line 3"], vertical_align=displays.TextVerticalAlign.BOTTOM)
    index = _unit_test(drawing, f, index=index, name="Text list to the bottom")

    # TextList with offset
    drawing = displays.TextList(["line 1", "line 2", "line 3"], font=fonts.Fonts.SMALL, x_offset=40, y_offset=60)
    index = _unit_test(drawing, f, index=index, name="Text list with offsets")

    # TextGrid 1 x 1
    drawing = displays.TextGrid([["1.1"]])
    index = _unit_test(drawing, f, index=index, name="Text grid 1 x 1")

    # TextGrid 2 x 2
    drawing = displays.TextGrid([["1.1", "1.2"], ["2.1", "2.2"]])
    index = _unit_test(drawing, f, index=index, name="Text grid 2 x 2")

    # TextGrid 3 x 3
    drawing = displays.TextGrid([["1.1", "1.2", "1.3"], ["2.1", "2.2", "2.3"], ["3.1", "3.2", "3.3"]])
    index = _unit_test(drawing, f, index=index, name="Text grid 3 x 3")

    # TextGrid 4 x 3
    drawing = displays.TextGrid([["1.1", "1.2", "1.3"], ["2.1", "2.2", "2.3"], ["3.1", "3.2", "3.3"], ["4.1", "4.2", "4.3"]])
    index = _unit_test(drawing, f, index=index, name="Text grid 4 x 3")

    # TextGrid several length of line
    drawing = displays.TextGrid([["1.1", "1.2", "1.3"], ["2.1"], ["3.1", "3.2"]])
    index = _unit_test(drawing, f, index=index, name="Text grid several length of lines")

    # TextGrid empty line
    drawing = displays.TextGrid([["1.1", "1.2", "1.3"], [], ["3.1", "3.2"]])
    index = _unit_test(drawing, f, index=index, name="Text grid empty line")

    # TextGrid with big typo
    drawing = displays.TextGrid([["1.1", "1.2"], ["2.1", "2.2"]], font=fonts.Fonts.LARGE)
    index = _unit_test(drawing, f, index=index, name="Text grid big typo")

    # TextGrid with top align
    drawing = displays.TextGrid([["1.1", "1.2"], ["2.1", "2.2"]], vertical_align=displays.TextVerticalAlign.TOP)
    index = _unit_test(drawing, f, index=index, name="Text grid to the top")

    # TextGrid with bottom align
    drawing = displays.TextGrid([["1.1", "1.2"], ["2.1", "2.2"]], vertical_align=displays.TextVerticalAlign.BOTTOM)
    index = _unit_test(drawing, f, index=index, name="Text grid to the bottom")

    # TextGrid with offset
    drawing = displays.TextGrid([["1.1", "1.2"], ["2.1", "2.2"]], font=fonts.Fonts.SMALL, x_offset=40, y_offset=60)
    index = _unit_test(drawing, f, index=index, name="Text grid with offsets")

    # Line of 3
    drawing = displays.LineOfThree(["Text 1", "Text 2", "Text 3"])
    index = _unit_test(drawing, f, index=index, name="3 texts SMALL")

    # Line of 3 with big typo
    drawing = displays.LineOfThree(["Text 1", "Text 2", "Text 3"], font=fonts.Fonts.LARGE)
    index = _unit_test(drawing, f, index=index, name="3 texts big typo")

    # Line of 3 with center align
    drawing = displays.LineOfThree(["Text 1", "Text 2", "Text 3"], vertical_align=displays.TextVerticalAlign.CENTER)
    index = _unit_test(drawing, f, index=index, name="3 texts to the top")

    # Line of 3 with bottom align
    drawing = displays.LineOfThree(["Text 1", "Text 2", "Text 3"], vertical_align=displays.TextVerticalAlign.BOTTOM)
    index = _unit_test(drawing, f, index=index, name="3 texts to the bottom")

    # Line of 3 with offset
    drawing = displays.LineOfThree(["Text 1", "Text 2", "Text 3"], font=fonts.Fonts.SMALL, x_offset=40, y_offset=60)
    index = _unit_test(drawing, f, index=index, name="3 texts with offsets")

    # Line of 2
    drawing = displays.LineOfTwo(["Text 1", "Text 2"])
    index = _unit_test(drawing, f, index=index, name="2 texts SMALL")

    # Line of 2 with big typo
    drawing = displays.LineOfTwo(["Text 1", "Text 2"], font=fonts.Fonts.LARGE)
    index = _unit_test(drawing, f, index=index, name="2 texts big typo")

    # Line of 2 with center align
    drawing = displays.LineOfTwo(["Text 1", "Text 2"], vertical_align=displays.TextVerticalAlign.CENTER)
    index = _unit_test(drawing, f, index=index, name="2 texts to the top")

    # Line of 2 with bottom align
    drawing = displays.LineOfTwo(["Text 1", "Text 2"], vertical_align=displays.TextVerticalAlign.BOTTOM)
    index = _unit_test(drawing, f, index=index, name="2 texts to the bottom")

    # Line of 2 with offset
    drawing = displays.LineOfTwo(["Text 1", "Text 2"], font=fonts.Fonts.SMALL, x_offset=40, y_offset=60)
    index = _unit_test(drawing, f, index=index, name="2 texts with offsets")

    # Icon left
    drawing = displays.IconAppBarLeft(icon="IconAwesomeArrowLeft")
    index = _unit_test(drawing, f, index=index, name="icon left")

    # Icon left with offsets
    drawing = displays.IconAppBarLeft(icon="IconAwesomeArrowLeft", x_offset=20, y_offset=15)
    index = _unit_test(drawing, f, index=index, name="icon left with offsets")

    # Icon right
    drawing = displays.IconAppBarRight(icon="IconAwesomeArrowRight")
    index = _unit_test(drawing, f, index=index, name="icon right")

    # Icon right with offsets
    drawing = displays.IconAppBarRight(icon="IconAwesomeArrowRight", x_offset=20, y_offset=15)
    index = _unit_test(drawing, f, index=index, name="icon right with offsets")

    # Full appbar
    drawing = displays.FullAppBar(title="Title", left="IconAwesomeArrowLeft", right="IconAwesomeArrowRight")
    index = _unit_test(drawing, f, index=index, name="Full app bar")

    # Full appbar with big typo
    drawing = displays.FullAppBar(title="Large title", left="IconAwesomeArrowLeft", right="IconAwesomeArrowRight", title_font=fonts.Fonts.HUGE)
    index = _unit_test(drawing, f, index=index, name="Full app bar")
