class Color:
    red: int
    green: int
    blue: int
    alpha: int

    def __init__(self, r: int, g: int, b: int, a: int = 255):
        assert 0 <= r <= 255
        assert 0 <= g <= 255
        assert 0 <= b <= 255
        assert 0 <= a <= 255

        self.red = r
        self.green = g
        self.blue = b
        self.alpha = a

    @classmethod
    def from_rgba(cls, r: int, g: int, b: int, a: int = 255):
        """Creates a new Color object with the given RGBA values."""
        return cls(r, g, b, a)

    @classmethod
    def from_hex(cls, color: str):
        """Creates a new Color object from a hexadecimal string."""

        # https://www.w3.org/TR/css-color-4/#hex-notation
        assert len(color) in [3, 4, 6, 8], "Color must be in the format RGB, RGBA, RRGGBB, or RRGGBBAA."

        # RGB
        if len(color) == 3:
            return cls(int(color[0], 16) * 17,
                       int(color[1], 16) * 17,
                       int(color[2], 16) * 17)

        # RGBA
        elif len(color) == 4:
            return cls(int(color[0], 16) * 17,
                       int(color[1], 16) * 17,
                       int(color[2], 16) * 17,
                       int(color[3], 16) * 17)

        # RRGGBB
        elif len(color) == 6:
            return cls(int(color[:2], 16),
                       int(color[2:4], 16),
                       int(color[4:6], 16))

        # RRGGBBAA
        elif len(color) == 8:
            return cls(int(color[:2], 16),
                       int(color[2:4], 16),
                       int(color[4:6], 16),
                       int(color[6:8], 16))

    def to_rgba8888_bytes(self):
        red = self.red.to_bytes(1, "little")
        green = self.green.to_bytes(1, "little")
        blue = self.blue.to_bytes(1, "little")
        alpha = self.alpha.to_bytes(1, "little")
        return red + green + blue + alpha

    def __str__(self):
        return f"{self.red:02x}{self.green:02x}{self.blue:02x}{self.alpha:02x}"


class Colors:
    BLACK = Color(0, 0, 0, 255)
    WHITE = Color(255, 255, 255, 255)
    RED = Color(255, 0, 0, 255)
    GREEN = Color(0, 255, 0, 255)
    BLUE = Color(0, 0, 255, 255)
