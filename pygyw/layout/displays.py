import enum
import math

from .drawings import Drawing, DrawingPosition, TextDrawing, IconDrawing
from . import fonts
from . import helpers
from . import settings


class TextVerticalAlign(enum.Enum):
    TOP = "top"
    CENTER = "center"
    BOTTOM = "bottom"
    NONE = "none"


class TextAlign(enum.Enum):
    LEFT = "left"
    CENTER = "center"
    RIGHT = "right"
    NONE = "none"


class DrawingTemplate:
    """
    Abstract view of a template that defines everything show on a screen
    """
    def __init__(self, name):
        self.name = name

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return self.name

    def get_drawings(self) -> "list[Drawing]":
        """
        Returns a list of drawings that describe the content of the screen
        """
        pass


##############################################
#   Templates with text only
##############################################
class Title(DrawingTemplate):
    '''
    Display an appbar title
    ________________________________
    |   Lorem Ipsum, lorem Ipsum   |
    ________________________________
    |                              |
    |                              |
    |                              |
    |                              |
    |                              |
    ▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔
    '''
    def __init__(self, text, font: fonts.Font = fonts.Fonts.TITLE):
        super().__init__(name="Title")
        self.text = text
        self.font = font

    def get_drawings(self) -> "list[Drawing]":
        return [
            TextDrawing(
                text=self.text,
                font=self.font,
                position=DrawingPosition(
                    pos_x=helpers.center_text(self.text, self.font),
                    pos_y=settings.appBarHeight - self.font.height / 2),
            )
        ]


class Paragraph(DrawingTemplate):
    '''
    Display several lines of text
    ________________________________
    |                              |
    ________________________________
    |                              |
    |  Lorem Ipsum, lorem Ipsum    |
    |  Lorem Ipsum, lorem Ipsum    |
    |  Lorem Ipsum, lorem Ipsum    |
    |                              |
    ▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔
    '''
    def __init__(self, text: str, font: fonts.Font = fonts.Fonts.BASIC,
                 line_height=2.0, x_offset=0, y_offset=0):
        super().__init__(name="Paragraph")
        self.text = text
        self.font = font
        self.line_height = line_height
        self.x_offset = x_offset
        self.y_offset = y_offset

    def get_drawings(self) -> "list[Drawing]":
        text_max_length = math.ceil(settings.contentHorizontalSpace / self.font.width)
        informations = helpers.justify(self.text, text_max_length)

        out = []
        for index, information in enumerate(informations):
            out.append(TextDrawing(
                text=information,
                font=self.font,
                position=DrawingPosition(
                    pos_x=settings.contentHorizontalPadding + self.x_offset,
                    pos_y=settings.appBarHeight + settings.appBarContentPadding + index * self.font.height * self.line_height + self.y_offset,
                )
            ))

        return out


class TextLine(DrawingTemplate):
    '''
    Display a line of text
    ________________________________
    |                              |
    ________________________________
    |                              |
    |   Lorem Ipsum, lorem Ipsum   |
    |                              |
    |                              |
    |                              |
    ▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔
    '''
    def __init__(self, text: str, font: fonts.Font = fonts.Fonts.BASIC,
                 x_offset=0, y_offset=0, align=TextAlign.CENTER,
                 vertical_align=TextVerticalAlign.CENTER):
        super().__init__(name="One line text")
        self.text = text
        self.font = font
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.align = align
        self.vertical_align = vertical_align

    def get_drawings(self) -> "list[Drawing]":
        # Vertical align management
        if self.vertical_align == TextVerticalAlign.TOP:
            pos_y = self.y_offset + helpers.top_text([self.text], font=self.font)
        elif self.vertical_align == TextVerticalAlign.CENTER:
            pos_y = self.y_offset + helpers.vcenter_text([self.text], font=self.font)
        else:
            pos_y = helpers.bottom_text([self.text], font=self.font)

        # Horizontal align management
        if self.align == TextAlign.LEFT:
            pos_x = helpers.left_align_text(self.text, self.font) + self.x_offset
        elif self.align == TextAlign.CENTER:
            pos_x = helpers.center_text(self.text, self.font) + self.x_offset
        else:
            pos_x = helpers.right_align_text(self.text, self.font)

        return [
            TextDrawing(
                text=self.text,
                font=self.font,
                position=DrawingPosition(pos_x=pos_x, pos_y=pos_y)
            )
        ]


class TextList(DrawingTemplate):
    '''
    Display a list of texts
    ________________________________
    |                              |
    ________________________________
    |                              |
    |  • Ipsum                     |
    |  • Ipsum                     |
    |  • Ipsum                     |
    |                              |
    ▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔
    '''
    def __init__(self, items: "list[str]", font: fonts.Font = fonts.Fonts.BASIC,
                 line_height=2.0, x_offset=0, y_offset=0, align=TextAlign.LEFT,
                 vertical_align=TextVerticalAlign.TOP):
        super().__init__(name="Text list")
        self.items = items
        self.font = font
        self.line_height = line_height
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.align = align
        self.vertical_align = vertical_align

    def get_drawings(self) -> "list[Drawing]":
        if self.vertical_align == TextVerticalAlign.TOP:
            pos_y = self.y_offset + helpers.top_text(
                self.items, font=self.font, line_height=self.line_height)
        elif self.vertical_align == TextVerticalAlign.CENTER:
            pos_y = self.y_offset + helpers.vcenter_text(
                self.items, font=self.font, line_height=self.line_height)
        else:
            pos_y = helpers.bottom_text(
                self.items, font=self.font, line_height=self.line_height)

        out = []
        for index, item in enumerate(self.items):
            if self.align == TextAlign.LEFT:
                pos_x = self.x_offset + helpers.left_align_text(item, self.font)
            elif self.align == TextAlign.CENTER:
                pos_x = self.x_offset + helpers.center_text(item, self.font)
            else:
                pos_x = helpers.right_align_text(item, self.font)

            out.append(TextDrawing(
                text=item,
                font=self.font,
                position=DrawingPosition(
                    pos_x=pos_x,
                    pos_y=pos_y + index * self.font.height * self.line_height
                )
            ))
        return out


class TextGrid(DrawingTemplate):
    '''
    Display a grid of texts
    :note: Lines must not have the same length
    ________________________________
    |                              |
    ________________________________
    |                              |
    |  • Ipsum   • Ipsum           |
    |                              |
    |  • Ipsum   • Ipsum           |
    |                              |
    ▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔
    '''
    def __init__(self, lines, font: fonts.Font = fonts.Fonts.BASIC,
                 line_height=2.0, x_offset=0, y_offset=0,
                 vertical_align=TextVerticalAlign.TOP):
        super().__init__(name="Text Grid")
        self.lines = lines
        self.font = font
        self.line_height = line_height
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.vertical_align = vertical_align

    def get_drawings(self) -> "list[Drawing]":
        out = []

        if self.vertical_align == TextVerticalAlign.TOP:
            pos_y = self.y_offset + helpers.top_text(
                self.lines, font=self.font, line_height=self.line_height)
        elif self.vertical_align == TextVerticalAlign.CENTER:
            pos_y = self.y_offset + helpers.vcenter_text(
                self.lines, font=self.font, line_height=self.line_height)
        else:
            pos_y = helpers.bottom_text(
                self.lines, font=self.font, line_height=self.line_height)

        for line in self.lines:
            pos_x = self.x_offset + settings.contentHorizontalPadding

            if line:
                x_gap = int((settings.contentHorizontalSpace - self.x_offset) / len(line))
            else:
                # Handle empty lines
                x_gap = 0

            for text in line:
                out.append(TextDrawing(
                    text=text,
                    font=self.font,
                    position=DrawingPosition(pos_x=pos_x, pos_y=pos_y),
                ))
                pos_x += x_gap

            pos_y += self.line_height * self.font.height

        return out


class LineOfThree(DrawingTemplate):
    '''
        Display three texts on the same line
        ________________________________
        |                              |
        ________________________________
        |                              |
        | Left      Center       Right |
        |                              |
        |                              |
        |                              |
        ▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔
        '''
    def __init__(self, texts: "list[str]", font: fonts.Font = fonts.Fonts.BASIC,
                 x_offset=0, y_offset=0, vertical_align=TextVerticalAlign.TOP):
        super().__init__(name="Line of three")

        assert len(texts) == 3
        self.texts = texts
        self.font = font
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.vertical_align = vertical_align

    def get_drawings(self) -> "list[Drawing]":
        return TextLine(
            text=self.texts[0], font=self.font, align=TextAlign.LEFT,
            x_offset=self.x_offset, y_offset=self.x_offset,
            vertical_align=self.vertical_align,
        ).get_drawings() + TextLine(
            text=self.texts[1], font=self.font, align=TextAlign.CENTER,
            x_offset=self.x_offset, y_offset=self.x_offset,
            vertical_align=self.vertical_align,
        ).get_drawings() + TextLine(
            text=self.texts[2], font=self.font, align=TextAlign.RIGHT,
            x_offset=self.x_offset, y_offset=self.x_offset,
            vertical_align=self.vertical_align,
        ).get_drawings()


class LineOfTwo(DrawingTemplate):
    '''
    Display two texts on the same line
    ________________________________
    |                              |
    ________________________________
    |                              |
    | Left                   Right |
    |                              |
    |                              |
    |                              |
    ▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔
    '''
    def __init__(self, texts, font: fonts.Font = fonts.Fonts.BASIC,
                 x_offset: int = 0, y_offset: int = 0,
                 vertical_align=TextVerticalAlign.TOP):
        super().__init__(name="Line of two")

        assert len(texts) == 2
        self.texts = texts
        self.font = font
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.vertical_align = vertical_align

    def get_drawings(self) -> "list[Drawing]":
        return TextLine(
            text=self.texts[0], font=self.font, align=TextAlign.LEFT,
            x_offset=self.x_offset, y_offset=self.y_offset,
            vertical_align=self.vertical_align,
        ).get_drawings() + TextLine(
            text=self.texts[1], font=self.font, align=TextAlign.RIGHT,
            x_offset=self.x_offset, y_offset=self.y_offset,
            vertical_align=self.vertical_align,
        ).get_drawings()


##############################################
#   Templates with icons only
##############################################
class IconAppBarLeft(DrawingTemplate):
    '''
    Display an icon on the left side of the appbar
    ________________________________
    | XX                           |
    ________________________________
    |                              |
    |                              |
    |                              |
    |                              |
    |                              |
    ▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔
    '''
    def __init__(self, icon: str, x_offset=0, y_offset=0):
        super().__init__(name="Appbar icon left")
        self.icon = icon
        self.x_offset = x_offset
        self.y_offset = y_offset

    def get_drawings(self) -> "list[Drawing]":
        return [
            IconDrawing(
                icon=self.icon,
                x_size=settings.iconImageSize,
                y_size=settings.iconImageSize,
                position=DrawingPosition(
                    pos_x=settings.appBarHorizontalPadding,
                    pos_y=settings.appBarTopPadding + (settings.appBarHeight - settings.iconImageSize) / 2
                )
            )
        ]


class IconCenter(DrawingTemplate):
    '''
    Display an icon at the center of the screen
    ________________________________
    |                              |
    |                              |
    |                              |
    |              XX              |
    |                              |
    |                              |
    |                              |
    ▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔
    '''
    def __init__(self, icon: str, x_offset=0, y_offset=0):
        super().__init__(name="icon center")
        self.icon = icon
        self.x_offset = x_offset
        self.y_offset = y_offset

    def get_drawings(self) -> "list[Drawing]":
        return [
            IconDrawing(
                icon=self.icon,
                x_size=settings.iconImageSize,
                y_size=settings.iconImageSize,
                position=DrawingPosition(
                    pos_x=self.x_offset + (settings.screenWidth - settings.iconImageSize) / 2,
                    pos_y=self.y_offset + (settings.screenHeight - settings.iconImageSize) / 2,
                )
            )
        ]


class IconAppBarRight(DrawingTemplate):
    '''
    Display an icon on the right side of the appbar
    ________________________________
    |                           XX |
    ________________________________
    |                              |
    |                              |
    |                              |
    |                              |
    |                              |
    ▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔
    '''
    def __init__(self, icon: str, x_offset=0, y_offset=0):
        super().__init__(name="Appbar icon right")
        self.icon = icon
        self.x_offset = x_offset
        self.y_offset = y_offset

    def get_drawings(self) -> "list[Drawing]":
        return [
            IconDrawing(
                icon=self.icon,
                x_size=settings.iconImageSize,
                y_size=settings.iconImageSize,
                position=DrawingPosition(
                    pos_x=settings.screenWidth - settings.iconImageSize - settings.appBarHorizontalPadding,
                    pos_y=settings.appBarTopPadding + (settings.appBarHeight - settings.iconImageSize) / 2
                )
            )
        ]


class GYWLogo(DrawingTemplate):
    '''
    Display Get Your Way logo on full screen
    '''
    def __init__(self):
        super().__init__(name="GYW Logo")

    def get_drawings(self) -> "list[Drawing]":
        return [
            IconDrawing(
                icon="gyw",
                position=DrawingPosition(0, 0),
                x_size=800,
                y_size=450,
            )
        ]


##############################################
#   Templates with icons and text
##############################################
class FullAppBar(DrawingTemplate):
    '''
    Display a screen that contains an appbar with a title and two icons
    ________________________________
    | LEFT       TITLE       RIGHT |
    ________________________________
    |                              |
    |                              |
    |                              |
    |                              |
    |                              |
    ▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔
    '''
    def __init__(self, title: str = None, left: str = None, right: str = None,
                 title_font: fonts.Font = fonts.Fonts.TITLE):
        super().__init__(name="Full appbar")
        self.title = title
        self.left = left
        self.right = right
        self.title_font = title_font

    def get_drawings(self) -> "list[Drawing]":
        out = []
        if self.left:
            out.extend(IconAppBarLeft(icon=self.left).get_drawings())

        if self.right:
            out.extend(IconAppBarRight(icon=self.right).get_drawings())

        if self.title:
            out.extend(Title(text=self.title, font=self.title_font).get_drawings())

        return out
