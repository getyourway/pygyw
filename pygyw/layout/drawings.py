from __future__ import annotations

import textwrap
from enum import IntEnum
from math import ceil
from typing import Optional, Any

from . import fonts
from . import icons
from .helpers import rgba8888_bytes_from_color_string, byte_from_scale_float, clamp
from .settings import screen_width
from ..bluetooth import commands


class GYWDrawing:
    """
    Represents an element displayed on the screen.

    Attributes:
        type: The type of the object.
        left: The horizontal offset (from left).
        top: The vertical offset (from top).

    """

    def __init__(self, drawing_type: str, left: int = 0, top: int = 0):
        """
        Initialize a `GYWDrawing` object.

        :param drawing_type: The type of the Drawing object.
        :type drawing_type: str
        :param left: The horizontal offset. Defaults to 0.
        :type left: int
        :param left: The vertical offset. Defaults to 0.
        :type top: int

        """

        self.drawing_type = drawing_type
        self.left = left
        self.top = top

    def __str__(self) -> str:
        return f"{self.drawing_type} - ({self.left}, {self.top})"

    def __repr__(self) -> str:
        return self.__str__()

    def to_json(self) -> "dict[str, Any]":
        return {
            "type": self.drawing_type,
            "left": self.left,
            "top": self.top,
        }

    def to_commands(self) -> "list[commands.BTCommand]":
        """
        Convert the `GYWDrawing` into a list of commands understood by the aRdent Bluetooth device.

        :return: The list of `commands.BTCommand` that describes the Bluetooth instructions to perform.
        :rtype: `list[commands.BTCommand]`

        """

        return []


class TextDrawing(GYWDrawing):
    """
    Represents a text element displayed on the screen.

    Attributes:
        text: The text to display.
        left: The horizontal offset (from the left).
        top: The vertical offset (from the top).
        font: The font to use for the text.
        size: The font size.
        color: The text color.
        max_width: The maximum width (in pixels) of the text. It will be wrapped on multiple lines if it is too long.
        max_lines: The maximum number of lines the text can be wrapped on. All extra lines will be ignored. The value 0 is special and disables the limit.
    """

    def __init__(self,
                 text: str,
                 font: fonts.GYWFont = fonts.GYWFonts.ROBOTO_MONO,
                 size: int = 24,
                 left: int = 0,
                 top: int = 0,
                 color: str = None,
                 max_width: int = None,
                 max_lines: int = 1):
        """
        Initialize a `TextDrawing` object.

        :param text: The text to be displayed.
        :type text: str
        :param left: The horizontal offset. Defaults to 0.
        :type left: int
        :param left: The vertical offset. Defaults to 0.
        :type top: int
        :param font: The font used for the text.
        :type font: `fonts.GYWFont`
        :param size: The font size.
        :type size: int
        :param color: The text color in ORGB format.
        :type color: str
        :param max_width: The maximum width of the text.
        :type max_width: int
        :param max_lines: The maximum number of lines the text can be wrapped on.
        :type max_lines: int
        """

        super().__init__("text", left=left, top=top)
        self.text = text
        self.font = font
        self.size = size
        self.color = color
        self.max_width = max_width
        self.max_lines = max_lines

    def to_json(self) -> "dict[str, Any]":
        data = super().to_json()
        data["text"] = self.text
        data["font"] = self.font.name
        data["size"] = self.size
        data["color"] = self.color
        data["max_width"] = self.max_width
        data["max_lines"] = self.max_lines
        return data

    @property
    def wrapped_text(self) -> str:
        """
        Returns the text wrapped on multiple lines constrained by `max_width` and `max_lines`.

        :return: The wrapped text.
        :rtype: str

        """
        return "\n".join(self._wrap_text())

    def to_commands(self) -> "list[commands.BTCommand]":
        """
        Convert the `TextDrawing` into a list of commands understood by the aRdent Bluetooth device.

        :return: The list of `commands.BTCommand` that describes the Bluetooth instructions to perform.
        :rtype: `list[commands.BTCommand]`

        """
        operations = super().to_commands()

        if not self.text:
            return operations

        char_height = ceil(self.size * 1.33)

        commands = []
        current_top = self.top
        for line in self._wrap_text():
            commands.extend(self._line_to_commands(line, current_top))
            current_top += char_height

        return commands

    def _wrap_text(self) -> "list[str]":
        # An invalid value will be considered as unconstrained.
        max_width = None if self.max_width is not None and self.max_width < 1 else self.max_width
        max_lines = max(0, self.max_lines)

        available_width = screen_width - self.left
        if max_width is None or max_width >= available_width:
            # Never let the text overflow the screen on width.
            text_width = available_width
        else:
            text_width = max_width

        char_width = ceil(self.size * 0.6)
        max_chars_per_line = text_width // char_width

        lines = textwrap.wrap(self.text, width=max_chars_per_line)
        if max_lines > 0:
            lines = lines[:max_lines]

        return lines

    def _line_to_commands(self, line: str, top: int) -> "list[commands.BTCommand]":
        """
        Convert a line of text into a list of commands understood by the aRdent Bluetooth device.

        :return: The list of `commands.BTCommand` that describes the Bluetooth instructions to perform.
        :rtype: `list[commands.BTCommand]`

        """
        # Generate control instruction
        ctrl_data = bytearray([commands.ControlCodes.DISPLAY_TEXT])
        ctrl_data += self.left.to_bytes(2, 'little', signed=True)
        ctrl_data += top.to_bytes(2, 'little', signed=True)
        ctrl_data += bytes(self.font.filename.ljust(5, '\0'), 'utf-8')
        ctrl_data += self.size.to_bytes(1, 'little')

        short_color = "NULL"
        if self.color:
            short_color = f"{self.color[0]}{self.color[2]}{self.color[4]}{self.color[6]}"

        ctrl_data += bytes(short_color, 'utf-8')

        return [
            # Text data
            commands.BTCommand(
                commands.GYWCharacteristics.DISPLAY_DATA,
                bytes(line, 'utf-8'),
            ),
            # Control
            commands.BTCommand(
                commands.GYWCharacteristics.DISPLAY_COMMAND,
                ctrl_data,
            ),
        ]


class IconDrawing(GYWDrawing):
    """
    Drawing made of an icon stored on aRdent and that can be displayed on the screen.

    Attributes:
        icon: The filename of the image to be displayed.
        left: The horizontal offset (from the left).
        top: The vertical offset (from the top).
        color: The color of the icon (can be None).
        scale: The icon scale.

    """

    def __init__(self, icon: icons.GYWIcon, left: int = 0, top: int = 0, color: str = None, scale: float = 1.0):
        """
        Initialize an `IconDrawing` object.

        :param icon: The icon to be displayed.
        :type icon: `icons.GYWIcon`
        :param left: The horizontal offset. Defaults to 0.
        :type left: int
        :param top: The vertical offset. Defaults to 0.
        :type top: int
        :param color: The color of the icon in ORGB format. Defaults to None.
        :type color: str
        :param scale: The icon scale. Defaults to 1.0.
        :type scale: float

        """

        super().__init__("icon", left=left, top=top)
        self.icon = icon
        self.color = color
        assert scale > 0
        self.scale = scale

    def to_json(self) -> "dict[str, Any]":
        data = super().to_json()
        data["icon"] = self.icon
        data["color"] = self.color
        data["scale"] = self.scale
        return data

    def to_commands(self) -> "list[commands.BTCommand]":
        """
        Convert the `IconDrawing` into a list of commands understood by the aRdent Bluetooth device.

        :return: The list of `commands.BTCommand` that describes the Bluetooth instructions to perform.
        :rtype: `list[commands.BTCommand]`

        """

        operations = super().to_commands()

        if not self.icon:
            return operations

        left = self.left.to_bytes(2, 'little', signed=True)
        top = self.top.to_bytes(2, 'little', signed=True)
        ctrl_data = bytearray([commands.ControlCodes.DISPLAY_IMAGE]) + left + top
        ctrl_data += bytes(self.color or "NULLNULL", 'utf-8')
        ctrl_data += byte_from_scale_float(self.scale)

        operations.extend([
            commands.BTCommand(
                commands.GYWCharacteristics.DISPLAY_DATA,
                bytes(f"{self.icon.name}.bin", 'utf-8'),
            ),
            commands.BTCommand(
                commands.GYWCharacteristics.DISPLAY_COMMAND,
                ctrl_data,
            ),
        ])

        return operations


class RectangleDrawing(GYWDrawing):
    """
    A colored rectangle.

    Attributes:
        left: The horizontal offset.
        top: The vertical offset.
        width: The rectangle width.
        height: The rectangle height.
        color: The fill color. Defaults to None in which case the current background color is used.
    """

    def __init__(self,
                 left: int,
                 top: int,
                 width: int,
                 height: int,
                 color: str = None):
        super().__init__("rectangle", left, top)
        self.width = width
        self.height = height
        self.color = color

    def to_json(self) -> "dict[str, Any]":
        data = super().to_json()
        data["width"] = self.width
        data["height"] = self.height
        data["color"] = self.color
        return data

    def to_commands(self) -> "list[commands.BTCommand]":
        """Convert this `RectangleDrawing` into a list of commands."""

        operations = super().to_commands()

        left = self.left.to_bytes(2, 'little', signed=True)
        top = self.top.to_bytes(2, 'little', signed=True)
        width = self.width.to_bytes(2, 'little')
        height = self.height.to_bytes(2, 'little')
        color = rgba8888_bytes_from_color_string(self.color)

        ctrl_data = bytearray([commands.ControlCodes.DRAW_RECTANGLE]) + left + top + width + height + color

        operations.append(
            commands.BTCommand(
                commands.GYWCharacteristics.DISPLAY_COMMAND,
                ctrl_data,
            ),
        )

        return operations


class AnimationTimingFunction(IntEnum):
    """The animation timing function to use for the spinner."""

    LINEAR = 0
    EASE_IN = 1
    EASE_OUT = 2


class SpinnerDrawing(GYWDrawing):
    """
    Animated spinner and that can be displayed on the screen.

    Attributes:
        left: The horizontal offset (from the left).
        top: The vertical offset (from the top).
        color: The color of the spinner.
        scale: The spinner scale.
        animation_timing_function: The animation timing function to use.
        spins_per_second: The number of spins per second.

    """

    def __init__(self,
                 left: int = 0,
                 top: int = 0,
                 color: str | None = None,
                 scale: float = 1.0,
                 animation_timing_function: AnimationTimingFunction = AnimationTimingFunction.LINEAR,
                 spins_per_second: float = 1.0):
        super().__init__("spinner", left=left, top=top)
        self.color = color
        assert scale > 0
        self.scale = scale
        self.animation_timing_function = animation_timing_function
        self.spins_per_second = spins_per_second
        assert spins_per_second >= 0

    def to_json(self) -> "dict[str, Any]":
        data = super().to_json()
        data["color"] = self.color
        data["scale"] = self.scale
        data["animation_timing_function"] = self.animation_timing_function
        data["spins_per_second"] = self.spins_per_second
        return data

    def to_commands(self) -> "list[commands.BTCommand]":
        """
        Convert the `SpinnerDrawing` into a list of commands understood by the aRdent Bluetooth device.

        :return: The list of `commands.BTCommand` that describes the Bluetooth instructions to perform.
        :rtype: `list[commands.BTCommand]`

        """

        operations = super().to_commands()

        left = self.left.to_bytes(2, 'little', signed=True)
        top = self.top.to_bytes(2, 'little', signed=True)
        ctrl_data = bytearray([commands.ControlCodes.DISPLAY_SPINNER]) + left + top
        ctrl_data += rgba8888_bytes_from_color_string(self.color)
        ctrl_data += byte_from_scale_float(self.scale)
        ctrl_data += self.animation_timing_function.value.to_bytes(1, 'little')

        spins_per_second = int(clamp(self.spins_per_second, 0.0, 25.5) * 10)
        ctrl_data += spins_per_second.to_bytes(1, 'little')

        operations.extend([
            commands.BTCommand(
                commands.GYWCharacteristics.DISPLAY_DATA,
                bytes(f"spinner_1.svg", 'utf-8'),
            ),
            commands.BTCommand(
                commands.GYWCharacteristics.DISPLAY_COMMAND,
                ctrl_data,
            ),
        ])

        return operations
