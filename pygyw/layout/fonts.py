class Font:
    '''
    Font stored on aRdent device to style the display of a TextDrawing
    '''
    def __init__(
        self, name, index, prefix, size, height,
        width, bold=False,
    ):
        # Display name of the font
        self.name = name

        # Index in the device
        self.index = index

        # Prefix used on the device
        self.prefix = prefix

        # Size of a character in pt
        self.size = size

        # Height of a character in px
        self.height = height

        # Width of a character in px
        self.width = width

        # Whether the font is in bold or not
        self.bold = bold

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return self.__str__()

    def to_json(self) -> dict:
        return {
            "title": self.index,
        }


class Fonts:
    """
    All fonts currently active on aRdent device
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
