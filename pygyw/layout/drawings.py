from . import fonts
from . import settings

from ..bluetooth import commands

class DrawingPosition:
    """
    Represents the position of a drawing on the screen.

    Attributes:
        pos_x (int): The horizontal offset.
        pos_y (int): The vertical offset.

    """

    def __init__(self, pos_x: int, pos_y: int) -> None:
        """
        Initialize a DrawingPosition object.

        Args:
            pos_x (int): The horizontal offset.
            pos_y (int): The vertical offset.

        """

        self.pos_x = int(pos_x)
        self.pos_y = int(pos_y)

    def __str__(self) -> str:
        return f"pos_x: {self.pos_x} - pos_y: {self.pos_y}"

    def __repr__(self) -> str:
        return self.__str__()

    def to_json(self) -> dict:
        """Return a JSON-serializable dictionary of the DrawingPosition object."""

        return {
            "x_start": self.pos_x,
            "y_start": self.pos_y,
        }


class Drawing:
    """
    Represents an element displayed on the screen.

    Attributes:
        type (str): The type of the Drawing object.
        position (DrawingPosition): The position of the Drawing object.

    """

    # @TODO Replace type by drawing_type to avoid conflict with type() method
    def __init__(self, type: str, position: DrawingPosition) -> None:
        """
        Initialize a Drawing object.

        Args:
            type (str): The type of the Drawing object.
            position (DrawingPosition): The position of the Drawing object.

        """

        self.type = type
        self.position = position

    def __str__(self) -> str:
        return f"{self.type} - {self.position}"

    def __repr__(self) -> str:
        return self.__str__()

    def to_json(self) -> dict:
        data = self.position.to_json()
        data["type"] = self.type
        return data

    def to_commands(self) -> "list[commands.BTCommand]":
        """
        Convert the Drawing object into a list of commands understood by the aRdent Bluetooth device.

        Returns:
            list[commands.BTCommand]: A list of BTCommand objects.

        """

        return []


class WhiteScreen(Drawing):
    """Represents a white screen with nothing on it. Useful to reset what is displayed."""

    def __init__(self):
        """Initialize a WhiteScreen object."""

        super().__init__(type="white_screen", position=DrawingPosition(0, 0))

    def to_commands(self) -> "list[commands.BTCommand]":
        """
        Convert the WhiteScreen object into a list of commands understood by the aRdent Bluetooth device.

        Returns:
            list[commands.BTCommand]: A list of BTCommand objects.

        """

        return super().to_commands() + [
            commands.BTCommand(
                commands.GYWCharacteristics.DISPLAY_COMMAND,
                bytearray([commands.ControlCodes.CLEAR]),
            ),
        ]


class TextDrawing(Drawing):
    """
    Represents a text element displayed on the screen.

    Attributes:
        text (str): The text to display.
        position (DrawingPosition): The position of the text element.
        font (Font): The font to use for the text.

    """

    def __init__(self, text: str, position: DrawingPosition, font=fonts.Fonts.SMALL):
        """
        Initialize a TextDrawing object.

        Args:
            text (str): The text to display.
            position (DrawingPosition): The position of the text element.
            font (Font, optional): The font to use for the text. Defaults to SMALL.

        """

        super().__init__(type="text", position=position)
        self.text = text
        self.font = font

    def to_json(self) -> dict():
        data = super().to_json()
        data["data"] = self.text
        data["x_size"] = settings.screenWidth
        data.update(self.font.to_json())
        return data

    def to_commands(self, font=True) -> "list[commands.BTCommand]":
        """
        Convert the TextDrawing to a list of commands understood by the aRdent Bluetooth device.

        An option has been added to avoid resetting the font, i.e. to keep the previous one.

        Args:
            font (bool): Whether or not to include the font commands. Defaults to True.

        Returns:
            List[commands.BTCommand]: A list of commands to be sent to the aRdent Bluetooth device.

        """

        operations = super().to_commands()

        # Set font
        if font:
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
        ctrl_data = bytearray([commands.ControlCodes.DISPLAY_TEXT]) + self.position.pos_x.to_bytes(4, 'little') + self.position.pos_y.to_bytes(4, 'little')
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


class IconDrawing(Drawing):
    """
    Drawing made of an icon stored on aRdent and that can be displayed on the screen.

    Attributes:
        icon (str): The filename of the image to be displayed.
        position (DrawingPosition): The position of the image on the screen.

    """

    def __init__(self, icon: str, position: DrawingPosition):
        """
        Initialize an IconDrawing object.

        Args:
            icon (str): The name of the image to be displayed.
            position (DrawingPosition): The position of the image on the screen.

        """

        super().__init__(type="memory", position=position)
        self.icon = icon

    def to_json(self) -> dict():
        data = super().to_json()
        data["data"] = self.icon
        return data

    def to_commands(self) -> "list[commands.BTCommand]":
        """
        Convert the IconDrawing into a list of commands understood by the aRdent Bluetooth device.

        Returns:
            list[commands.BTCommand]: A list of BTCommand objects.

        """

        ctrl_data = bytearray([commands.ControlCodes.DISPLAY_IMAGE]) + self.position.pos_x.to_bytes(4, 'little') + self.position.pos_y.to_bytes(4, 'little')

        return super().to_commands() + [
            commands.BTCommand(
                commands.GYWCharacteristics.DISPLAY_DATA,
                bytes(self.icon, 'utf-8'),
            ),
            commands.BTCommand(
                commands.GYWCharacteristics.DISPLAY_COMMAND,
                ctrl_data,
            ),
        ]
