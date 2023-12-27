from __future__ import annotations

import math
from dataclasses import dataclass

from . import settings
from . import fonts


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


def dark_mode_color(color: Color):
    hsl_color = HSLColor.from_color(color)
    hsl_color.lightness = 1.0 - hsl_color.lightness
    return hsl_color.to_color()


@dataclass
class Color:
    red: int
    green: int
    blue: int
    alpha: int

    @staticmethod
    def from_argb_hex(hex_color: str):
        return Color(
            red=int(hex_color[2:4], 16),
            green=int(hex_color[4:6], 16),
            blue=int(hex_color[6:8], 16),
            alpha=int(hex_color[0:2], 16),
        )

    def to_argb_hex(self) -> str:
        return "%02x%02x%02x%02x" % (self.alpha, self.red, self.green, self.blue)

    def to_rgba8888_bytes(self) -> bytes:
        alpha = self.alpha.to_bytes(1, "little")
        red = self.red.to_bytes(1, "little")
        green = self.green.to_bytes(1, "little")
        blue = self.blue.to_bytes(1, "little")
        return red + green + blue + alpha

    def invert_lightness(self) -> Color:
        hsl_color = HSLColor.from_color(self)
        hsl_color.lightness = 1.0 - hsl_color.lightness
        return hsl_color.to_color()


@dataclass
class HSLColor:
    alpha: float
    hue: float
    saturation: float
    lightness: float

    @staticmethod
    def from_color(color: Color):
        red = color.red / 0xFF
        green = color.green / 0xFF
        blue = color.blue / 0xFF

        max_channel = max(red, green, blue)
        min_channel = min(red, green, blue)
        delta = max_channel - min_channel

        alpha = color.alpha / 0xFF
        hue = _get_hue(red, green, blue, max_channel, delta)
        lightness = (max_channel + min_channel) / 2.0
        saturation = 0.0 if lightness == 1.0 else clamp(delta / (1.0 - abs(2.0 * lightness - 1.0)), 0.0, 1.0)

        return HSLColor(alpha, hue, saturation, lightness)

    def to_color(self) -> Color:
        chroma = (1.0 - abs(2.0 * self.lightness - 1.0)) * self.saturation
        secondary = chroma * (1.0 - abs((self.hue / 60.0) % 2.0 - 1.0))
        match = self.lightness - chroma / 2.0

        return _color_from_hue(self.alpha, self.hue, chroma, secondary, match)


def _get_hue(red: float, green: float, blue: float, max_channel: float, delta: float):
    """Translated from `colors.dart` from Flutter"""

    if max_channel == 0.0:
        hue = 0.0
    elif max_channel == red:
        hue = 60.0 * (((green - blue) / delta) % 6)
    elif max_channel == green:
        hue = 60.0 * (((blue - red) / delta) + 2)
    elif max_channel == blue:
        hue = 60.0 * (((red - green) / delta) + 4)

    assert hue

    # Set hue to 0.0 when red == green == blue.
    hue = 0.0 if math.isnan(hue) else hue
    return hue


def _color_from_hue(alpha: float, hue: float, chroma: float, secondary: float, match: float) -> Color:
    """Translated from `colors.dart` from Flutter"""

    if hue < 60.0:
        red = chroma
        green = secondary
        blue = 0.0
    elif hue < 120.0:
        red = secondary
        green = chroma
        blue = 0.0
    elif hue < 180.0:
        red = 0.0
        green = chroma
        blue = secondary
    elif hue < 240.0:
        red = 0.0
        green = secondary
        blue = chroma
    elif hue < 300.0:
        red = secondary
        green = 0.0
        blue = chroma
    else:
        red = chroma
        green = 0.0
        blue = secondary

    return Color(
        red=round((red + match) * 0xFF),
        green=round((green + match) * 0xFF),
        blue=round((blue + match) * 0xFF),
        alpha=round(alpha * 0xFF),
    )
