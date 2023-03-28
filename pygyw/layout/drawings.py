from . import fonts
from . import icons
from . import settings

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


class TextDrawing(GYWDrawing):
    """
    Represents a text element displayed on the screen.

    Attributes:
        text: The text to display.
        left: The horizontal offset (from the left).
        top: The vertical offset (from the top).
        font: The font to use for the text (can be None).

    """

    def __init__(self, text: str, left: int = 0, top: int = 0, font: fonts.GYWFont = None):
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

        """

        super().__init__("text", left=left, top=top)
        self.text = text
        self.font = font

    def to_json(self) -> dict():
        data = super().to_json()
        data["text"] = self.text
        data["font"] = self.font.name
        return data

    def to_commands(self) -> "list[commands.BTCommand]":
        """
        Convert the `TextDrawing` into a list of commands understood by the aRdent Bluetooth device.

        :return: The list of `commands.BTCommand` that describes the Bluetooth instructions to perform.
        :rtype: `list[commands.BTCommand]`

        """

        operations = super().to_commands()

        # Set font
        if self.font:
            operations.extend([
                commands.BTCommand(
                    commands.GYWCharacteristics.DISPLAY_DATA,
                    bytes(self.font.prefix, 'utf-8'),
                ),
                commands.BTCommand(
                    commands.GYWCharacteristics.DISPLAY_COMMAND,
                    bytearray([commands.ControlCodes.SET_FONT]),
                ),
            ])

        # Send text data
        ctrl_data = bytearray([commands.ControlCodes.DISPLAY_TEXT]) + self.left.to_bytes(4, 'little') + self.top.to_bytes(4, 'little')
        operations.extend([
            commands.BTCommand(
                commands.GYWCharacteristics.DISPLAY_DATA,
                bytes(self.text, 'utf-8'),
            ),
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

    """

    def __init__(self, icon: icons.GYWIcon, left: int = 0, top: int = 0, ):
        """
        Initialize an `IconDrawing` object.

        :param icon: The icon to be displayed.
        :type icon: `icons.GYWIcon`
        :param left: The horizontal offset. Defaults to 0.
        :type left: int
        :param left: The vertical offset. Defaults to 0.
        :type top: int

        """

        super().__init__("icon", left=left, top=top)
        self.icon = icon

    def to_json(self) -> dict():
        data = super().to_json()
        data["icon"] = self.icon
        return data

    def to_commands(self) -> "list[commands.BTCommand]":
        """
        Convert the `IconDrawing` into a list of commands understood by the aRdent Bluetooth device.

        :return: The list of `commands.BTCommand` that describes the Bluetooth instructions to perform.
        :rtype: `list[commands.BTCommand]`

        """

        ctrl_data = bytearray([commands.ControlCodes.DISPLAY_IMAGE]) + self.left.to_bytes(4, 'little') + self.top.to_bytes(4, 'little')

        operations = super().to_commands()
        operations.extend([
            commands.BTCommand(
                commands.GYWCharacteristics.DISPLAY_DATA,
                bytes(f"{self.icon.name}.png", 'utf-8'),
            ),
            commands.BTCommand(
                commands.GYWCharacteristics.DISPLAY_COMMAND,
                ctrl_data,
            ),
        ])
