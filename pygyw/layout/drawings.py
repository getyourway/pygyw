from . import fonts
from . import settings

class DrawingPosition:
    '''
    Position of a drawing on the screen
    '''

    def __init__(self, pos_x, pos_y):
        # Horizontal offset
        self.pos_x = int(pos_x)
        # Vertical offset
        self.pos_y = int(pos_y)

    def __str__(self) -> str:
        return f"pos_x: {self.pos_x} - pos_y: {self.pos_y}"

    def __repr__(self) -> str:
        return self.__str__()

    def to_json(self) -> dict:
        return {
            "x_start": self.pos_x,
            "y_start": self.pos_y,
        }


class Drawing:
    '''
    Element displayed on the screen
    '''
    def __init__(self, type: str, position: DrawingPosition):
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


class WhiteScreen(Drawing):
    '''
    White screen with nothing on it. Useful to reset what is displayed.
    '''
    def __init__(self):
        # The position is not important but needed by the library
        super().__init__(type="white_screen", position=DrawingPosition(0, 0))


class TextDrawing(Drawing):
    '''
    Text displayed on the screen
    '''
    def __init__(self, text: str, position: DrawingPosition, font=fonts.Fonts.BASIC):
        super().__init__(type="text", position=position)
        self.text = text
        self.font = font

    def to_json(self) -> dict():
        data = super().to_json()
        data["data"] = self.text
        data["x_size"] = settings.screenWidth
        data.update(self.font.to_json())
        return data


class IconDrawing(Drawing):
    '''
    Image stored on aRdent and that can be displayed on the screen
    '''
    def __init__(self, icon: str, position: DrawingPosition,
                 x_size: int = 80, y_size: int = 80):
        super().__init__(type="memory", position=position)
        self.icon = icon
        self.x_size = x_size
        self.y_size = y_size

    def to_json(self) -> dict():
        data = super().to_json()
        data["data"] = self.icon
        data["x_size"] = self.x_size
        data["y_size"] = self.y_size
        return data
