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
        assert len(color) == 6 or len(color) == 8, "Color must be in the format RRGGBB or RRGGBBAA."

        if len(color) == 6:
            # RRGGBB
            return cls(int(color[:2], 16),
                       int(color[2:4], 16),
                       int(color[4:6], 16))

        if len(color) == 8:
            # RRGGBBAA
            return cls(int(color[:2], 16),
                       int(color[2:4], 16),
                       int(color[4:6], 16),
                       int(color[6:8], 16))

    def __str__(self):
        return f"{self.red:02x}{self.green:02x}{self.blue:02x}{self.alpha:02x}"


class Colors:
    BLACK = Color(0, 0, 0, 255)
    WHITE = Color(255, 255, 255, 255)
    RED = Color(255, 0, 0, 255)
    GREEN = Color(0, 255, 0, 255)
    BLUE = Color(0, 0, 255, 255)
