class Font:
    '''
    Font stored on aRdent device to style the display of a TextDrawing
    '''
    def __init__(self, name, index, height, width, bold=False, textLinePadding=10):
        # Display name of the font
        self.name = name

        # Index in the device
        self.index = index

        # Height of a single character
        self.height = height

        # Width of a single character
        self.width = width

        # Whether the font is in bold or not
        self.bold = bold

        # TODO: Usage
        self.textLinePadding = textLinePadding

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
    BASIC = Font(
        name="Basic font", index=0, width=14, height=22)

    TITLE = Font(
        name="Title font", index=1, width=20, height=31, bold=True)

    BIG_BASIC = Font(
        name="Big basic font", index=2, width=29, height=47)

    BIG_TITLE = Font(
        name="Big title font", index=3, width=42, height=71, bold=True)

    values = [BASIC, TITLE, BIG_BASIC, BIG_TITLE]
