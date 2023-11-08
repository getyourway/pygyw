from typing import Optional, Any

from typing_extensions import deprecated

from . import fonts
from . import icons
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

    def to_json(self) -> dict:
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


@deprecated("`WhiteScreen` has been replaced by `BlankScreen` who has a variable background color")
class WhiteScreen(GYWDrawing):
    """Represents a white screen with nothing on it. Useful to reset what is displayed."""

    def __init__(self):
        """Initialize a `WhiteScreen` object."""

        super().__init__("white_screen")

    def to_commands(self) -> "list[commands.BTCommand]":
        """
        Convert the `WhiteScreen` into a list of commands understood by the aRdent Bluetooth device.

        :return: The list of `commands.BTCommand` that describes the Bluetooth instructions to perform.
        :rtype: `list[commands.BTCommand]`

        """

        return super().to_commands() + [
            commands.BTCommand(
                commands.GYWCharacteristics.DISPLAY_COMMAND,
                bytearray([commands.ControlCodes.CLEAR]),
            ),
        ]


class BlankScreen(GYWDrawing):
    """
    Reset what is displayed.

    If an ARGB color is provided, the screen will be filled with this color, otherwise the screen will be filled with
    the last color used.If a color was never provided, if fills the screen with white.
    """

    def __init__(self, color: Optional[str] = None):
        """Initialize a `BlankScreen` object."""

        super().__init__("blank_screen")
        self.color = color  # ARGB

    def to_commands(self) -> "list[commands.BTCommand]":
        """
        Convert the `BlankScreen` into a list of commands understood by the aRdent Bluetooth device.

        :return: The list of `commands.BTCommand` that describes the Bluetooth instructions to perform.
        :rtype: `list[commands.BTCommand]`

        """

        ctrl_bytes = bytearray([commands.ControlCodes.CLEAR])
        if self.color:
            ctrl_bytes += bytes(self.color, 'ascii')

        return super().to_commands() + [
            commands.BTCommand(
                commands.GYWCharacteristics.DISPLAY_COMMAND,
                ctrl_bytes,
            ),
        ]


class TextDrawing(GYWDrawing):
    """
    Represents a text element displayed on the screen.

    Attributes:
        text: The text to display.
        left: The horizontal offset (from the left).
        top: The vertical offset (from the top).
        font: The font to use for the text (can be None).
        size: The font size.
        color: The text color.
    """

    def __init__(self,
                 text: str,
                 left: int = 0,
                 top: int = 0,
                 font: fonts.GYWFont = None,
                 size: int = None,
                 color: str = None):
        """
        Initialize a `TextDrawing` object.

        :param text: The text to be displayed.
        :type text: str
        :param left: The horizontal offset. Defaults to 0.
        :type left: int
        :param left: The vertical offset. Defaults to 0.
        :type top: int
        :param font: The font used for the text. Defaults to None.
        :type font: `fonts.GYWFont`
        :param size: The font size.
        :type size: int
        :param color: The text color in ORGB format.
        :type color: str
        """

        super().__init__("text", left=left, top=top)
        self.text = text
        self.font = font
        self.size = size
        self.color = color

    def to_json(self) -> dict():
        data = super().to_json()
        data["text"] = self.text
        data["font"] = self.font.name
        data["size"] = self.size
        data["color"] = self.color
        return data

    def to_commands(self) -> "list[commands.BTCommand]":
        """
        Convert the `TextDrawing` into a list of commands understood by the aRdent Bluetooth device.

        :return: The list of `commands.BTCommand` that describes the Bluetooth instructions to perform.
        :rtype: `list[commands.BTCommand]`

        """

        operations = super().to_commands()

        # Generate control instruction
        ctrl_data = bytearray([commands.ControlCodes.DISPLAY_TEXT])
        ctrl_data += self.left.to_bytes(4, 'little')
        ctrl_data += self.top.to_bytes(4, 'little')
        ctrl_data += bytes(self.font.prefix if self.font is not None else "NUL", 'utf-8')
        ctrl_data += (self.size if self.size is not None else 0).to_bytes(1, 'little')

        short_color = "NULL"
        if self.color:
            short_color = f"{self.color[0]}{self.color[2]}{self.color[4]}{self.color[6]}"

        ctrl_data += bytes(short_color, 'utf-8')

        operations.extend([
            # Text data
            commands.BTCommand(
                commands.GYWCharacteristics.DISPLAY_DATA,
                bytes(self.text, 'utf-8'),
            ),
            # Control
            commands.BTCommand(
                commands.GYWCharacteristics.DISPLAY_COMMAND,
                ctrl_data,
            ),
        ])

        return operations


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

    def to_json(self) -> dict[str, Any]:
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

        left = self.left.to_bytes(4, 'little')
        top = self.top.to_bytes(4, 'little')
        ctrl_data = bytearray([commands.ControlCodes.DISPLAY_IMAGE]) + left + top

        if self.color:
            ctrl_data += bytes(self.color, 'utf-8')

        def clamp(n, smallest, largest):
            return max(smallest, min(n, largest))

        self.scale = clamp(self.scale, 0.01, 13.8)
        if self.scale >= 1.0:
            # min: 1.0 -> 0.0 -> 0
            # max: 13.8 -> 12.8 -> 128
            scale = round((self.scale - 1.0) * 10.0)
        else:
            # min: 0.01 -> -1
            # max: 0.99 -> -99
            scale = round(-self.scale * 100.0)

        assert -99 <= scale <= 128

        ctrl_data += scale.to_bytes(1, 'little', signed=True)

        operations = super().to_commands()
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
