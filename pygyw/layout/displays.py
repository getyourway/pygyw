import math
from .drawings import Drawing, DrawingPosition, TextDrawing, IconDrawing
from . import fonts
from . import helpers
from . import settings


class TextVerticalAlign:
    """A collection of vertical alignement for the displays."""

    TOP = "top"
    CENTER = "center"
    BOTTOM = "bottom"
    NONE = "none"


class TextAlign:
    """A collection of horizontal alignement for the displays."""

    LEFT = "left"
    CENTER = "center"
    RIGHT = "right"
    NONE = "none"


class DrawingTemplate:
    """
    Abstract view of a template that defines everything show on a screen.
    
    Attributes:
        name (str): Name of the template

    """

    def __init__(self, name):
        """
        Initialize a DrawingTemplate object.
        
        Args:
            name (str): Name of the template

        """

        self.name = name

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return self.name

    def get_drawings(self) -> "list[Drawing]":
        """
        Generate a list of drawings that describes the content of the screen.
        
        Returns:
            list[Drawing]: A list of drawings

        """
        pass


##############################################
#   Templates with text only
##############################################
class Title(DrawingTemplate):
    """
    Display a title in the appbar area.

    Attributes:
        text (str): Text to put as a title
        font (Font, optional): Font used to write the text. Defaults to MEDIUM

    Example:
    --------------------------------
    |   Lorem Ipsum, lorem Ipsum   |
    --------------------------------
    |                              |
    |                              |
    |                              |
    |                              |
    |                              |
    --------------------------------

    """

    def __init__(self, text, font: fonts.Font = fonts.Fonts.MEDIUM):
        """
        Initialize the Title object.

        Args:
            text (str): Text to put as a title
            font (Font, optional): Font used to write the text. Defaults to MEDIUM

        """

        super().__init__(name="Title")
        self.text = text
        self.font = font

    def get_drawings(self) -> "list[Drawing]":
        """
        Generate a list of drawings that describes the display.

        Returns:
            list[Drawing]: A list of drawings

        """

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
    """
    A class for displaying several lines of text.

    Attributes:
        text (str): The text to display.
        font (Font): The font to use for the text.
        line_height (float): The vertical spacing between lines of text.
        x_offset (int): The horizontal offset for the text.
        y_offset (int): The vertical offset for the text.

    Example:
    --------------------------------
    |                              |
    --------------------------------
    |                              |
    |  Lorem Ipsum, lorem Ipsum    |
    |  Lorem Ipsum, lorem Ipsum    |
    |  Lorem Ipsum, lorem Ipsum    |
    |                              |
    --------------------------------

    """

    def __init__(
        self, text: str, font: fonts.Font = fonts.Fonts.SMALL,
        line_height: float = 2.0, x_offset: int = 0, y_offset: int = 0
    ):
        """
        Initialize a Paragraph display.

        Args:
            text (str): The text to display
            font (Font, optional): The font used for the text. Defaults to SMALL.
            line_height (float, optional): _The vertical spacing between lines of text. Defaults to 2.0.
            x_offset (int, optional): The horizontal offset for the text. Defaults to 0.
            y_offset (int, optional): The vertical offset for the text. Defaults to 0.

        """

        super().__init__(name="Paragraph")
        self.text = text
        self.font = font
        self.line_height = line_height
        self.x_offset = x_offset
        self.y_offset = y_offset

    def get_drawings(self) -> "list[Drawing]":
        """
        Generate a list of drawings that describes the display.

        Returns:
            list[Drawing]: A list of drawings

        """

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
    """
    A class for displaying a line of text.

    Attributes:
        text (str): The text to display.
        font (Font): The font to use for the text.
        x_offset (int): The horizontal offset for the text.
        y_offset (int): The vertical offset for the text.
        align (TextAlign): The horizontal alignment of the text.
        vertical_align (TextVerticalAlign): The vertical alignment of the text.

    Example:
    --------------------------------
    |                              |
    --------------------------------
    |                              |
    |   Lorem Ipsum, lorem Ipsum   |
    |                              |
    |                              |
    |                              |
    --------------------------------

    """

    def __init__(
        self, text: str, font: fonts.Font = fonts.Fonts.SMALL,
        x_offset: int = 0, y_offset: int = 0, align=TextAlign.CENTER,
        vertical_align=TextVerticalAlign.CENTER,
    ):
        """
        Initialize a TextLine object.

        Args:
            text (str): The text to display.
            font (Font, optional): The font to use for the text. Defaults to SMALL.
            x_offset (int, optional): The horizontal offset for the text. Defaults to 0.
            y_offset (int, optional): The vertical offset for the text. Defaults to 0.
            align (TextAlign, optional): The horizontal alignment of the text. Defaults to CENTER.
            vertical_align (TextVerticalAlign, optional): The vertical alignment of the text. Defaults to CENTER.

        """

        super().__init__(name="One line text")
        self.text = text
        self.font = font
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.align = align
        self.vertical_align = vertical_align

    def get_drawings(self) -> "list[Drawing]":
        """
        Generate a list of drawings that describes the display.

        Returns:
            list[Drawing]: A list of drawings

        """

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
    """
    Display a list of text items.

    Attributes:
        items (list[str]): A list of texts
        font (Font): The font used to display the text.
        line_height (float): The height of each line of text.
        x_offset (int): The horizontal offset for the texts.
        y_offset (int): The vertical offset for the texts.
        align (TextAlign): The horizontal alignment for the texts.
        vertical_align (TextVerticalAlign): The vertical alignment for the text within the texts.

    Example:
    --------------------------------
    |                              |
    --------------------------------
    |                              |
    |  • Ipsum                     |
    |  • Ipsum                     |
    |  • Ipsum                     |
    |                              |
    --------------------------------

    """

    def __init__(
        self, items: "list[str]", font: fonts.Font = fonts.Fonts.SMALL,
        line_height=2.0, x_offset=0, y_offset=0, align=TextAlign.LEFT,
        vertical_align=TextVerticalAlign.TOP,
    ):
        """
        Initialize a TextList object.

        Args:
            items (list[str]): A list of texts
            font (Font, optional): The font used to display the text.
            line_height (float, optional): The height of each line of text. Defaults to 2.0.
            x_offset (int, optional): The horizontal offset for the texts. Defaults to 0.
            y_offset (int, optional): The vertical offset for the texts. Defaults to 0.
            align (TextAlign, optional): The horizontal alignment for the texts. Defaults to LEFT.
            vertical_align (TextVerticalAlign, optional): The vertical alignment for the text within the texts. Defaults to TOP.

        """

        super().__init__(name="Text list")
        self.items = items
        self.font = font
        self.line_height = line_height
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.align = align
        self.vertical_align = vertical_align

    def get_drawings(self) -> "list[Drawing]":
        """
        Generate a list of drawings that describes the display.

        Returns:
            list[Drawing]: A list of drawings

        """
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
    """
    A class for displaying a grid of texts.

    Attributes:
        lines (List[List[str]]): A list of strings where each inner list represents a row in the grid.
        font (Font): The font used to display the text.
        line_height (float): The height of each line of text.
        x_offset (int): The horizontal offset for the grid.
        y_offset (int): The vertical offset for the grid.
        vertical_align (TextVerticalAlign): The vertical alignment for the text within the grid.

    Note:
        Lines must not have the same length.

    Example:
    --------------------------------
    |                              |
    --------------------------------
    |                              |
    |  • Ipsum   • Ipsum           |
    |                              |
    |  • Ipsum   • Ipsum           |
    |                              |
    --------------------------------

    """

    def __init__(
        self, lines, font: fonts.Font = fonts.Fonts.SMALL,
        line_height: int = 2.0, x_offset: int = 0, y_offset : int = 0,
        vertical_align=TextVerticalAlign.TOP,
    ):
        """
        Initialize the TextGrid object.

        Args:
            lines (List[List[str]]): A list of strings where each inner list represents a row in the grid.
            font (Font, optional): The font used to display the text. Defaults to SMALL.
            line_height (float, optional): The height of each line of text. Defaults to 2.0.
            x_offset (int, optional): The horizontal offset for the grid. Defaults to 0.
            y_offset (int, optional): The vertical offset for the grid. Defaults to 0.
            vertical_align (TextVerticalAlign, optional): The vertical alignment for the text within the grid. Defaults to TOP.

        """

        super().__init__(name="Text Grid")
        self.lines = lines
        self.font = font
        self.line_height = line_height
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.vertical_align = vertical_align

    def get_drawings(self) -> "list[Drawing]":
        """
        Generate a list of drawings that describes the display.

        Returns:
            list[Drawing]: A list of drawings

        """
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
    """
    Display three texts on the same line.

    Attributes:
        texts (tuple): A list containing two strings to be displayed.
        font (Font): The font to use for the text.
        x_offset (int): The horizontal offset from the left edge of the screen.
        y_offset (int): The vertical offset from the top edge of the screen.
        vertical_align (TextVerticalAlign): The vertical alignment of the text.

    Raises:
        AssertionError: If the `texts` parameter does not contain exactly two strings.

    Example:
    --------------------------------
    |                              |
    --------------------------------
    |                              |
    | Left      Center       Right |
    |                              |
    |                              |
    |                              |
    --------------------------------

    """

    def __init__(
        self, texts: "list[str]", font: fonts.Font = fonts.Fonts.SMALL,
        x_offset : int = 0, y_offset : int = 0, vertical_align = TextVerticalAlign.TOP
    ):
        """
        Initialize a LineOfTwo object.

        Attributes:
            texts (tuple): A list containing the strings to be displayed.
            font (Font, optional): The font to use for the text. Defaults to SMALL.
            x_offset (int, optional): The horizontal offset from the left edge of the screen. Defaults to 0.
            y_offset (int, optional): The vertical offset from the top edge of the screen. Defaults to 0.
            vertical_align (TextVerticalAlign, optional): The vertical alignment of the text. Defaults to TOP.

        Raises:
            AssertionError: If the `texts` parameter does not contain exactly three strings.

        """

        super().__init__(name="Line of three")

        assert len(texts) == 3
        self.texts = texts
        self.font = font
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.vertical_align = vertical_align

    def get_drawings(self) -> "list[Drawing]":
        """
        Generate a list of drawings that describes the display.

        Returns:
            list[Drawing]: A list of drawings

        """

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
    """
    Display two texts on the same line.

    Attributes:
        texts (tuple): A list containing two strings to be displayed.
        font (Font): The font to use for the text.
        x_offset (int): The horizontal offset from the left edge of the screen.
        y_offset (int): The vertical offset from the top edge of the screen.
        vertical_align (TextVerticalAlign): The vertical alignment of the text.

    Raises:
        AssertionError: If the `texts` parameter does not contain exactly two strings.

    Example:
    --------------------------------
    |                              |
    --------------------------------
    |                              |
    | Left                   Right |
    |                              |
    |                              |
    |                              |
    --------------------------------

    """

    def __init__(
        self, texts, font: fonts.Font = fonts.Fonts.SMALL,
        x_offset: int = 0, y_offset: int = 0,
        vertical_align=TextVerticalAlign.TOP,
    ):
        """
        Initialize a LineOfTwo object.

        Args:
            texts (tuple): A tuple containing two strings to be displayed.
            font (Font, optional): The font to use for the text. Defaults to SMALL.
            x_offset (int, optional): The horizontal offset from the left edge of the screen. Defaults to 0.
            y_offset (int, optional): The vertical offset from the top edge of the screen. Defaults to 0.
            vertical_align (TextVerticalAlign, optional): The vertical alignment of the text. Defaults to TOP.

        Raises:
            AssertionError: If the `texts` parameter does not contain exactly two strings.

        """

        super().__init__(name="Line of two")

        assert len(texts) == 2
        self.texts = texts
        self.font = font
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.vertical_align = vertical_align

    def get_drawings(self) -> "list[Drawing]":
        """
        Generate a list of drawings that describes the display.

        Returns:
            list[Drawing]: A list of drawings

        """

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
    """
    Display an icon on the left side of the appbar.

    Attributes:
        icon (str): The filename of the icon to display.
        x_offset (int): The horizontal offset from the left edge of the screen.
        y_offset (int): The vertical offset from the top edge of the screen.

    Example:
        --------------------------------
        | XX                           |
        --------------------------------
        |                              |
        |                              |
        |                              |
        |                              |
        |                              |
        --------------------------------

    """

    def __init__(self, icon: str, x_offset=0, y_offset=0):
        """
        Initialize an IconAppBarLeft object.

        Args:
            icon (str): The filename of the icon to display.
            x_offset (int, optional): The horizontal offset. Defaults to 0.
            y_offset (int, optional): The vertical offset. Defaults to 0.

        """

        super().__init__(name="Appbar icon left")
        self.icon = icon
        self.x_offset = x_offset
        self.y_offset = y_offset

    def get_drawings(self) -> "list[Drawing]":
        """
        Generate a list of drawings that describes the icon on the screen.
        
        Returns:
            list[Drawing]: A list of drawings

        """

        return [
            IconDrawing(
                icon=self.icon,
                position=DrawingPosition(
                    pos_x=settings.appBarHorizontalPadding,
                    pos_y=settings.appBarTopPadding + (settings.appBarHeight - settings.iconImageSize) / 2
                )
            )
        ]


class IconCenter(DrawingTemplate):
    """
    Display an icon at the center of the screen.

    Attributes:
        icon (str): The filename of the icon to display.
        x_offset (int): The horizontal offset from the left edge of the screen.
        y_offset (int): The vertical offset from the top edge of the screen.

    Example:
        --------------------------------
        |                              |
        |                              |
        |                              |
        |              XX              |
        |                              |
        |                              |
        |                              |
        --------------------------------

    """

    def __init__(self, icon: str, x_offset=0, y_offset=0):
        """
        Initialize the IconAppBarRight object.

        Args:
            icon (str): The filename of the icon to display.
            x_offset (int, optional): The horizontal offset. Defaults to 0.
            y_offset (int, optional): The vertical offset. Defaults to 0.

        """

        super().__init__(name="icon center")
        self.icon = icon
        self.x_offset = x_offset
        self.y_offset = y_offset

    def get_drawings(self) -> "list[Drawing]":
        """
        Generate a list of drawings that describes the icon on the screen.
        
        Returns:
            list[Drawing]: A list of drawings

        """

        return [
            IconDrawing(
                icon=self.icon,
                position=DrawingPosition(
                    pos_x=self.x_offset + (settings.screenWidth - settings.iconImageSize) / 2,
                    pos_y=self.y_offset + (settings.screenHeight - settings.iconImageSize) / 2,
                )
            )
        ]


class IconAppBarRight(DrawingTemplate):
    """
    Display an icon on the right side of the appbar.

    Attributes:
        icon (str): The filename of the icon to display.
        x_offset (int): The horizontal offset from the right edge of the screen.
        y_offset (int): The vertical offset from the top edge of the screen.

    Example:
        --------------------------------
        |                           XX |
        --------------------------------
        |                              |
        |                              |
        |                              |
        |                              |
        |                              |
        --------------------------------

    """

    def __init__(self, icon: str, x_offset=0, y_offset=0):
        """
        Initialize the IconAppBarRight object.

        Args:
            icon (str): The filename of the icon to display.
            x_offset (int, optional): The horizontal offset. Defaults to 0.
            y_offset (int, optional): The vertical offset. Defaults to 0.

        """

        super().__init__(name="Appbar icon right")
        self.icon = icon
        self.x_offset = x_offset
        self.y_offset = y_offset

    def get_drawings(self) -> "list[Drawing]":
        """
        Generate a list of drawings that describes the icon on the screen.
        
        Returns:
            list[Drawing]: A list of drawings

        """

        return [
            IconDrawing(
                icon=self.icon,
                position=DrawingPosition(
                    pos_x=settings.screenWidth - settings.iconImageSize - settings.appBarHorizontalPadding - self.x_offset,
                    pos_y=self.y_offset + settings.appBarTopPadding + (settings.appBarHeight - settings.iconImageSize) / 2
                )
            )
        ]


##############################################
#   Templates with icons and text
##############################################
class FullAppBar(DrawingTemplate):
    """
    Display a screen that contains an appbar with a title and two icons.

    Every element on this template is optional

    Args:
        title (str): The text to display as the appbar title.
        left (str): The filename of the icon to display on the left side of the appbar.
        right (str): The filename of the icon to display on the right side of the appbar.
        title_font (Font): The font to use for the appbar title.

    Example:
        --------------------------------
        | LEFT       TITLE       RIGHT |
        --------------------------------
        |                              |
        |                              |
        |                              |
        |                              |
        |                              |
        --------------------------------

    """

    def __init__(
        self, title: str = None, left: str = None, right: str = None,
        title_font: fonts.Font = fonts.Fonts.MEDIUM,
    ):
        """
        Initialize a FullAppBar object.

        Args:
            title (str, optional): The text to display as the appbar title. Defaults to None.
            left (str, optional): The filename of the icon to display on the left side of the appbar. Defaults to None.
            right (str, optional): The filename of the icon to display on the right side of the appbar. Defaults to None.
            title_font (Font, optional): The font to use for the appbar title. Defaults to MEDIUM.

        """

        super().__init__(name="Full appbar")
        self.title = title
        self.left = left
        self.right = right
        self.title_font = title_font

    def get_drawings(self) -> "list[Drawing]":
        """
        Generate a list of drawings that describes the display.
        
        Returns:
            list[Drawing]: A list of drawings

        """

        out = []
        if self.left:
            out.extend(IconAppBarLeft(icon=self.left).get_drawings())

        if self.right:
            out.extend(IconAppBarRight(icon=self.right).get_drawings())

        if self.title:
            out.extend(Title(text=self.title, font=self.title_font).get_drawings())

        return out
