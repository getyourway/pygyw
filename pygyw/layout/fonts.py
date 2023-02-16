class Font:
    """
    A font stored on an aRdent device used to style the display of a TextDrawing.

    Attributes:
        name (str): Display name of the font.
        index (int): Index of the font on the device.
        prefix (str): Prefix used on the device for the font.
        size (float): Size of a character in points.
        height (int): Height of a character in pixels.
        width (int): Width of a character in pixels.
        bold (bool): Whether the font is in bold or not.
    """
    
    def __init__(
        self, name: str, index: int, prefix: str, size: float, height: int, width: int, bold: bool = False
    ) -> None:
        """
        Initialize a new Font object.

        Args:
            name (str): Display name of the font.
            index (int): Index of the font on the device.
            prefix (str): Prefix used on the device for the font.
            size (float): Size of a character in points.
            height (int): Height of a character in pixels.
            width (int): Width of a character in pixels.
            bold (bool, optional): Whether the font is in bold or not. Defaults to False.
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

    def to_json(self) -> dict:
        """Return a JSON-serializable dictionary of the DrawingPosition object."""

        return {
            "title": self.index,
        }

class Fonts:
    """
    All fonts currently active on aRdent device.

    Attributes:
        SMALL (Font): The small font
        MEDIUM (Font): The medium font
        LARGE (Font): The large font
        HUGE (Font): The huge font
        values (List[Font]): A list containing all of the fonts in the class.
    """

    SMALL = Font(
        name="Small", index=0, prefix="a10", size=18, width=10, height=25)

    MEDIUM = Font(
        name="Medium", index=1, prefix="b14", size=24, width=14, height=33, bold=True)

    LARGE = Font(
        name="Large", index=2, prefix="a16", size=28, width=16, height=39)

    HUGE = Font(
        name="Huge", index=3, prefix="b28", size=48, width=28, height=67, bold=True)

    values = [SMALL, MEDIUM, LARGE, HUGE]
