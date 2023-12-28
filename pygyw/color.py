from dataclasses import dataclass
from typing import Self

from pygyw.layout.helpers import clamp


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

    def invert_lightness(self) -> Self:
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
        try:
            saturation = 0.0 if lightness == 1.0 else clamp(delta / (1.0 - abs(2.0 * lightness - 1.0)), 0.0, 1.0)
        except ZeroDivisionError:
            saturation = 1.0

        return HSLColor(alpha, hue, saturation, lightness)

    def to_color(self) -> Color:
        chroma = (1.0 - abs(2.0 * self.lightness - 1.0)) * self.saturation
        secondary = chroma * (1.0 - abs((self.hue / 60.0) % 2.0 - 1.0))
        match = self.lightness - chroma / 2.0

        return _color_from_hue(self.alpha, self.hue, chroma, secondary, match)


def _get_hue(red: float, green: float, blue: float, max_channel: float, delta: float):
    """Return the hue of a color. Translated from `colors.dart` from Flutter."""

    if delta == 0.0:
        # Set hue to 0.0 when red == green == blue.
        return 0.0

    if max_channel == 0.0:
        hue = 0.0
    elif max_channel == red:
        hue = 60.0 * (((green - blue) / delta) % 6)
    elif max_channel == green:
        hue = 60.0 * (((blue - red) / delta) + 2)
    elif max_channel == blue:
        hue = 60.0 * (((red - green) / delta) + 4)

    return hue


def _color_from_hue(alpha: float, hue: float, chroma: float, secondary: float, match: float) -> Color:
    """Convert hue into color. Translated from `colors.dart` from Flutter"""

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
