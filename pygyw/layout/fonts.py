from typing import Any


class GYWFont:
    """
    A font stored on an aRdent device used to style the display of a `drawings.TextDrawing`.

    Attributes:
        name: Display name of the font.
        index: Index of the font on the device.
        prefix: Prefix used on the device for the font.
        size: Size of a character in points.
        height: Height of a character in pixels.
        width: Width of a character in pixels.
        bold: Whether the font is in bold or not.
    """

    def __init__(
        self, name: str, index: int, prefix: str, size: float,
        height: int, width: int, bold: bool = False,
    ):
        """
        Initialize a new `GYWFont` object.

        :param name: Display name of the font.
        :type name: str
        :param index: Index of the font on the device.
        :type index: int
        :param prefix: Prefix used on the device for the font.
        :type prefix: str
        :param size: Size (in points) of a character.
        :type size: float
        :param height: Height (in pixels) of a character.
        :type height: int
        :param width: Width (in pixels) of a character.
        :type width: int
        :param bold: Whether the font is in bold or not. Defaults to False.
        :type bold: bool

        """

        self.name = name
        self.index = index
        self.prefix = prefix
        self.size = size
        self.height = height
        self.width = width
        self.bold = bold

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return self.__str__()

    def to_json(self) -> dict[str, Any]:
        """Return a JSON-serializable dictionary of the object."""

        return {
            "title": self.index,
        }


class GYWFonts:
    """
    Active fonts on aRdent smart glasses.

    Attributes:
        SMALL: A small font
        MEDIUM: A medium font
        LARGE: A large font
        HUGE: A huge font
        values: List containing every fonts available on aRdent smart glasses.
    """

    SMALL = GYWFont(
        name="Small", index=0, prefix="a10", size=18, width=10, height=25)

    MEDIUM = GYWFont(
        name="Medium", index=1, prefix="b14", size=24, width=14, height=33, bold=True)

    LARGE = GYWFont(
        name="Large", index=2, prefix="a16", size=28, width=16, height=39)

    HUGE = GYWFont(
        name="Huge", index=3, prefix="b28", size=48, width=28, height=67, bold=True)

    values = [SMALL, MEDIUM, LARGE, HUGE]
