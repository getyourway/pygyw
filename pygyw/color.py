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
    def hex(cls, color: int):
        """Transforms a hexadecimal ARGB color into a Color object."""
        return Color(
            (color >> 16) & 0xFF,
            (color >> 8) & 0xFF,
            color & 0xFF,
            (color >> 24) & 0xFF,
        )

    def __str__(self):
        return f"{self.red:02x}{self.green:02x}{self.blue:02x}{self.alpha:02x}"


class Colors:
    BLACK = Color(0, 0, 0, 255)
    WHITE = Color(255, 255, 255, 255)
    RED = Color(255, 0, 0, 255)
    GREEN = Color(0, 255, 0, 255)
    BLUE = Color(0, 0, 255, 255)
