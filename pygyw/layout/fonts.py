from typing import Any, Dict


class GYWFont:
    """
    A font stored on an aRdent device used to style the display of a `drawings.TextDrawing`.

    Attributes:
        name: Display name of the font.
        filename: Filename of the font on the device. (5 characters-long and no type extension).
        bold: Whether the font is bold.
        italic: Whether the font is italic.
    """

    def __init__(
            self,
            name: str,
            filename: str,
            bold: bool = False,
            italic: bool = False,
    ):
        """
        Initialize a new `GYWFont` object.

        :param name: Display name of the font.
        :type name: str
        :param filename: Filename of the font on the device. (5 characters-long and no type extension).
        :type filename: str
        :param bold: Whether the font is bold. Defaults to False.
        :type bold: bool
        :param italic: Whether the font is italic. Defaults to False.
        :type italic: bool

        """

        assert len(filename) == 5, "The filename must be 5 characters long."

        self.name = name
        self.filename = filename
        self.bold = bold
        self.italic = italic

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return self.__str__()

    def to_json(self) -> Dict[str, Any]:
        """Return a JSON-serializable dictionary of the object."""

        return {
            "title": self.filename,
        }


class GYWFonts:
    """Active fonts on aRdent smart glasses."""

    ROBOTO_MONO = GYWFont(name="Roboto Mono", filename="robmn")
    ROBOTO_MONO_BOLD = GYWFont(name="Roboto Mono Bold", filename="robmb", bold=True)
    ROBOTO_MONO_ITALIC = GYWFont(name="Roboto Mono Italic", filename="robmi", bold=True)
    ROBOTO_MONO_BOLD_ITALIC = GYWFont(name="Roboto Mono Bold Italic", filename="robmB", bold=True)

    values = [ROBOTO_MONO, ROBOTO_MONO_BOLD, ROBOTO_MONO_ITALIC, ROBOTO_MONO_BOLD_ITALIC]
