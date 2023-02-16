from . import settings
from . import fonts


##############################################
#   Helpers to compute the position of texts
##############################################
def center_text(text: str, font: fonts.Font) -> int:
    """
    Return the horizontal position of a text that should be horizontally centered.

    Args:
        text (str): The text to center.
        font (fonts.Font): The font used to display the text.

    Returns:
        int: The horizontal position of the centered text.
    """

    return int((settings.screenWidth - len(text) * font.width) / 2)


def left_align_text(text: str, font: fonts.Font) -> int:
    """
    Return the horizontal position of a text that should be aligned to the left.

    Args:
        text (str): The text to align.
        font (fonts.Font): The font used to display the text.

    Returns:
        int: The horizontal position of the left-aligned text.
    """

    return int(settings.contentHorizontalPadding)


def right_align_text(text: str, font: fonts.Font) -> int:
    """
    Return the horizontal position of a text that should be aligned to the right.

    Args:
        text (str): The text to align.
        font (fonts.Font): The font used to display the text.

    Returns:
        int: The horizontal position of the right-aligned text.
    """

    return int(settings.screenWidth - settings.contentHorizontalPadding - len(text) * font.width)


def top_text(lines: list, font: fonts.Font, line_height=2.0) -> int:
    """
    Return the vertical position of a text that should be aligned to the top.

    Args:
        lines (list): A list of lines of text.
        font (fonts.Font): The font used to display the text.
        line_height (float, optional): The height of each line of text, in multiples of font height. Defaults to 2.0.

    Returns:
        int: The vertical position of the top-aligned text.
    """

    return int(settings.appBarHeight + settings.contentVerticalPadding)


def vcenter_text(lines: list, font: fonts.Font, line_height=2.0) -> int:
    """
    Return the vertical position of a text that should be vertically centered.

    Args:
        lines (list): A list of lines of text.
        font (fonts.Font): The font used to display the text.
        line_height (float, optional): The height of each line of text, in multiples of font height. Defaults to 2.0.

    Returns:
        int: The vertical position of the vertically centered text.
    """

    lines_count = len(lines)
    return int(settings.appBarHeight + (settings.contentVerticalSpace - line_height * (lines_count - 1) * font.height) / 2)


def bottom_text(lines: list, font: fonts.Font, line_height=2.0) -> int:
    """
    Return the vertical position of a text that should be aligned to the bottom.

    Args:
        lines (list): A list of lines of text.
        font (fonts.Font): The font used to display the text.
        line_height (float, optional): The height of each line of text, in multiples of font height. Defaults to 2.0.

    Returns:
        int: The vertical position of the bottom-aligned text.
    """

    lines_count = len(lines)
    return int(settings.screenHeight - settings.contentVerticalPadding - line_height * (lines_count - 1) * font.height)


##############################################
#   Helpers to reformat text for a better rendering
##############################################
def left_justify(words: "list[str]", width: int):
    """
    Given an iterable of words and a desired line width, left-justifies the words and returns a string containing the justified text.

    Args:
        words (List[str]): A list of words to be left-justified.
        width (int): The desired width of the justified text.

    Returns:
        str: A string containing the left-justified text.

    Example:
        >> left_justify(["hello", "world"], 16)
         "hello world     "

    """

    text = ' '.join(words)
    spaces_to_add = width - len(text)
    text += ' ' * spaces_to_add
    return text


def justify(text: str, width: int):
    """
    Given a string of words and a desired line width, splits the words into lines of the given width, fully justifying all lines except for the last line, and left-justifying lines with only one word.

    Args:
        text (str): A string of words to be justified.
        width (int): The desired width of the justified lines.

    Returns:
        List[str]: A list of strings, where each string represents a justified line.

    Example:
        >> justify("This is an example of text justification.", 16)
        ['This    is    an', 'example  of text', 'justification.  ']

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
