from __future__ import annotations

from . import settings
from . import fonts
from ..color import Color


##############################################
# Helpers to horizontally align texts
##############################################
def center_text(text: str, font: fonts.GYWFont) -> int:
    """
    Return the horizontal position of a text that should be horizontally centered.

    :param text: The text to align.
    :type text: str
    :param font: The font used to display the text.
    :type font: `fonts.GYWFont`

    :return: The horizontal position of the text.
    :rtype: int

    """

    return int((settings.screen_width - len(text) * font.width) / 2)


def left_align_text(text: str, font: fonts.GYWFont) -> int:
    """
    Return the horizontal position of a text that should be aligned to the left.

    :param text: The text to align.
    :type text: str
    :param font: The font used to display the text.
    :type font: `fonts.GYWFont`

    :return: The horizontal position of the text.
    :rtype: int

    """

    return settings.horizontal_padding


def right_align_text(text: str, font: fonts.GYWFont) -> int:
    """
    Return the horizontal position of a text that should be aligned to the right.

    :param text: The text to align.
    :type text: str
    :param font: The font used to display the text.
    :type font: `fonts.GYWFont`

    :return: The horizontal position of the text.
    :rtype: int

    """

    return int(settings.screen_width - settings.horizontal_padding - len(text) * font.width)


##############################################
# Helpers to vertically align texts
##############################################
def top_text(lines: list, font: fonts.GYWFont, line_height: float = 2.0) -> int:
    """
    Return the vertical position of a text that should be aligned to the top.

    :param lines: A list of lines of text.
    :type lines: list
    :param font: The font used to display the text.
    :type font: `fonts.GYWFont`
    :param line_height: The height of each line of text, in multiples of font height. Defaults to 2.0.
    :type line_height: float

    :return: The vertical position of the text.
    :rtype: int

    """

    return settings.vertical_padding


def vcenter_text(lines: list, font: fonts.GYWFont, line_height=2.0) -> int:
    """
    Return the vertical position of a text that should vertically be centered.

    :param lines: A list of lines of text.
    :type lines: list
    :param font: The font used to display the text.
    :type font: `fonts.GYWFont`
    :param line_height: The height of each line of text, in multiples of font height. Defaults to 2.0.
    :type line_height: float

    :return: The vertical position of the text.
    :rtype: int

    """

    lines_count = len(lines)
    return int((settings.screen_height - lines_count * font.height - (line_height - 1) * (lines_count - 1)) / 2)


def bottom_text(lines: list, font: fonts.GYWFont, line_height=2.0) -> int:
    """
    Return the vertical position of a text that should be aligned at the bottom.

    :param lines: A list of lines of text.
    :type lines: list
    :param font: The font used to display the text.
    :type font: `fonts.GYWFont`
    :param line_height: The height of each line of text, in multiples of font height. Defaults to 2.0.
    :type line_height: float

    :return: The vertical position of the text.
    :rtype: int

    """

    lines_count = len(lines)
    return int(settings.screen_height - settings.vertical_padding - lines_count * font.height - (
                line_height - 1) * font.height * (lines_count - 1))


##############################################
# Helpers to justify text
##############################################
def left_justify(words: "list[str]", width: int) -> str:
    """
    Given an iterable of words and a desired line width, left-justifies the words and returns a string containing the justified text.

    :param words: A list of words to be left-justified.
    :type words: list[str]
    :param width: The desired width of the justified text.
    :type width: int

    :return: A string containing the left-justified text.
    :rtype: str

    :example:
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

    :param text: A string to be justified.
    :type words: str
    :param width: The desired width of the justified lines.
    :type width: int

    :return: A list of strings, where each string represents a justified line.
    :rtype: list[str]

    :example:
        >> justify("This is an example of text justification.", 16)
        ['This    is    an', 'example  of text', 'justification.  ']  "

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


def rgba8888_bytes_from_color(color: Color | None) -> bytes:
    """Transform a Color object into an RGBA8888 byte array of length 4."""

    if color is None:
        return bytearray([0, 0, 0, 0])

    red = color.red.to_bytes(1, "little")
    green = color.green.to_bytes(1, "little")
    blue = color.blue.to_bytes(1, "little")
    alpha = color.alpha.to_bytes(1, "little")
    return red + green + blue + alpha


def clamp(n, smallest, largest):
    """Clamp a value between two bounds."""
    return max(smallest, min(n, largest))


def byte_from_scale_float(scale: float) -> bytes:
    """Encode the scale into a single byte."""
    scale = clamp(scale, 0.01, 13.7)

    if scale >= 1.0:
        # min: 1.0 -> 0.0 -> 0
        # max: 13.7 -> 12.7 -> 127
        byte = round((scale - 1.0) * 10.0)
    else:
        # min: 0.01 -> -1
        # max: 0.99 -> -99
        byte = round(-scale * 100.0)

    assert -99 <= byte <= 127
    return byte.to_bytes(1, 'little', signed=True)
