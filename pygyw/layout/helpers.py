import textwrap

from . import settings
from . import fonts


##############################################
#   Helpers to compute the position of texts
##############################################
def center_text(text: str, font: fonts.Font) -> int:
    """
    Returns the horizontal position of a text that should be horizontally centered
    """
    return int((settings.screenWidth - len(text) * font.width) / 2)

def left_align_text(text: str, font: fonts.Font) -> int:
    """
    Returns the horizontal position of a text that should be aligned to the left
    """
    return int(settings.contentHorizontalPadding)

def right_align_text(text: str, font: fonts.Font) -> int:
    """
    Returns the horizontal position of a text that should be aligned to the right
    """
    return int(settings.screenWidth - settings.contentHorizontalPadding - len(text) * font.width)

def top_text(lines: list, font: fonts.Font, line_height=2.0) -> int:
    """
    Returns the vertical position of a text that should be aligned to the top
    """
    return int(settings.appBarHeight + settings.contentVerticalPadding)

def vcenter_text(lines: list, font: fonts.Font, line_height=2.0):
    """
    Returns the vertical position of a text that should be vertically centered
    """
    lines_count = len(lines)
    return int(settings.appBarHeight + (settings.contentVerticalSpace - line_height * (lines_count - 1) * font.height) / 2)

def bottom_text(lines: list, font: fonts.Font, line_height=2.0):
    """
    Returns the vertical position of a text that should be aligned to the bottom
    """
    lines_count = len(lines)
    return int(settings.screenHeight - settings.contentVerticalPadding - line_height * (lines_count - 1) * font.height)


##############################################
#   Helpers to reformat text for a better rendering
##############################################
def left_justify(words: "list[str]", width: int):
    """
    Given an iterable of words, return a string consisting of the words
    left-justified in a line of the given width.

    >>> left_justify(["hello", "world"], 16)
    'hello world     '

    """
    return ' '.join(words).ljust(width)

def justify(text: str, width: int):
    """
    Divide words (an iterable of strings) into lines of the given
    width, and generate them. The lines are fully justified, except
    for the last line, and lines with a single word, which are
    left-justified.

    >>> words = "This is an example of text justification.".split()
    >>> list(justify(words, 16))
    ['This    is    an', 'example  of text', 'justification.  ']
    """
    width = len(max(textwrap.fill(text, width).split("\n"), key=len))
    words = text.split()
    line = []             # List of words in current line.
    col = 0               # Starting column of next word added to line.
    lines = []
    for word in words:
        if line and col + len(word) > width:
            if len(line) == 1:
                lines.append(left_justify(line, width))
            else:
                # After n + 1 spaces are placed between each pair of
                # words, there are r spaces left over; these result in
                # wider spaces at the left.
                n, r = divmod(width - col + 1, len(line) - 1)
                narrow = ' ' * (n + 1)
                if r == 0:
                    lines.append(narrow.join(line))
                else:
                    wide = ' ' * (n + 2)
                    lines.append((wide.join(line[:r] + [narrow.join(line[r:])])))
            line, col = [], 0
        line.append(word)
        col += len(word) + 1
    if line:
        lines.append(left_justify(line, width))
    return lines
