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

    Ex.
     In : left_justify(["hello", "world"], 16)
     Out : 'hello world     '
    """
    text = ' '.join(words)
    spaces_to_add = width - len(text)
    text += ' ' * spaces_to_add
    return text


def justify(text: str, width: int):
    """
    Given a string made of words, split them into lines of a given
    fixed width. The lines are fully justified, except for the last
    line, and lines with a single word, which are left-justified.

    Ex.
     In : words = "This is an example of text justification.".split()
          list(justify(words, 16))
     Out : ['This    is    an', 'example  of text', 'justification.  ']
    """
    lines = []
    line = []
    line_length = 0
    for word in text.split():
        if line_length + len(word) + len(line) <= width:
            line.append(word)
            line_length += len(word)
        else:
            if len(line) == 1:
                lines.append(line[0] + ' ' * (width - len(line[0])))
            else:
                spaces_to_insert = width - line_length
                spaces_per_gap = spaces_to_insert // (len(line) - 1)
                extra_spaces = spaces_to_insert % (len(line) - 1)
                for i in range(len(line) - 1):
                    if extra_spaces:
                        line[i] += ' '
                        extra_spaces -= 1
                    line[i] += ' ' * spaces_per_gap
                lines.append(''.join(line))
            line = [word]
            line_length = len(word)

    if line:
        if len(line) == 1:
            lines.append(line[0] + ' ' * (width - len(line[0])))
        else:
            lines.append(' '.join(line))

    return lines
