from typing import Any, Dict


class GYWFont:
    """
    A font stored on an aRdent device used to style the display of a `drawings.TextDrawing`.

    Attributes:
        name: Display name of the font.
        filename: Filename of the font on the device.
    """

    def __init__(
            self,
            name: str,
            filename: str,
    ):
        """
        Initialize a new `GYWFont` object.

        :param name: Display name of the font.
        :type name: str
        :param filename: Filename of the font on the device.
        :type filename: str

        """

        self.name = name
        self.filename = filename

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

    ROBOTO_MONO_NORMAL = GYWFont(name="Roboto Mono Normal", filename="robmn")
    ROBOTO_MONO_BOLD = GYWFont(name="Roboto Mono Bold", filename="robmb")

    values = [ROBOTO_MONO_NORMAL, ROBOTO_MONO_BOLD]
