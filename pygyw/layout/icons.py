import settings


class GYWIcon:
    """
    An icon available on aRdent smart glasses and that can be used wuth an `IconDrawing`.

    Attributes:
        name (str): Display name of the font.
        size (int): Size (in pixels) of the icon.

    """

    def __init__(self, name: str, size: int = settings.iconSize):
        """
        Initialize a new `GYWIcon` object.

        Args:
            name (str): Display name of the font.
            size (int): Size (in pixels) of the icon. Defaults to `settings.iconSize`

        """

        self.name = name
        self.size = size

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return self.__str__()

    def to_json(self) -> dict:
        """Return a JSON-serializable dictionary of the object."""

        return {
            "icon": self.name,
        }


class GYWIcons:
    """
    All icons currently active on aRdent smart glasses.

    Attributes:
        BLANK: A blank icon that is usually used to remove an icon from the screen.
        .. image:: icons/blank.png
            :width: 48px
            :height: 48px
            :alt: Blank icon
            :align: center

        CHECK: An icon representing a validated checkbox.
        .. image:: icons/check.png
            :width: 48px
            :height: 48px
            :alt: Check icon
            :align: center

        DONE: An icon representing a check mark.
        .. image:: icons/done.png
            :width: 48px
            :height: 48px
            :alt: Done icon
            :align: center

        DOWN: An icon representing a downward arrow.
        .. image:: icons/down.png
            :width: 48px
            :height: 48px
            :alt: Downward arrow icon
            :align: center

        EDIT: An icon representing an edit operation.
        .. image:: icons/edit.png
            :width: 48px
            :height: 48px
            :alt: Edit icon
            :align: center

        FILE: An icon representing a file.
        .. image:: icons/file.png
            :width: 48px
            :height: 48px
            :alt: File icon
            :align: center

        INFO: An icon representing information.
        .. image:: icons/info.png
            :width: 48px
            :height: 48px
            :alt: Info icon
            :align: center

        LEFT: An icon representing a left arrow.
        .. image:: icons/left.png
            :width: 48px
            :height: 48px
            :alt: Left arrow icon
            :align: center

        LOCATION: An icon representing a location pin.
        .. image:: icons/location.png
            :width: 48px
            :height: 48px
            :alt: Location icon
            :align: center

        NEXT: An icon representing a next or forward operation.
        .. image:: icons/next.png
            :width: 48px
            :height: 48px
            :alt: Next icon
            :align: center

        PREV: An icon representing a previous or backward operation.
        .. image:: icons/prev.png
            :width: 48px
            :height: 48px
            :alt: Previous icon
            :align: center

        RENAME: An icon representing a rename operation.
        .. image:: icons/rename.png
            :width: 48px
            :height: 48px
            :alt: Rename icon
            :align: center

        RIGHT: An icon representing a right arrow.
        .. image:: icons/right.png
            :width: 48px
            :height: 48px
            :alt: Right arrow icon
            :align: center

        UNCHECK: An icon representing an unchecked checkbox.
        .. image:: icons/uncheck.png
            :width: 48px
            :height: 48px
            :alt: Uncheck icon
            :align: center

        UP: An icon representing an upward arrow.
        .. image:: icons/up.png
            :width: 48px
            :height: 48px
            :alt: Upward arrow icon
            :align: center

        values (list[`GYWIcon`]): A list of every available icons.
    """

    BLANK = GYWIcon("blank")
    CHECK = GYWIcon("check")
    DONE = GYWIcon("done")
    DOWN = GYWIcon("down")
    EDIT = GYWIcon("edit")
    FILE = GYWIcon("file")
    INFO = GYWIcon("info")
    LEFT = GYWIcon("left")
    LOCATION = GYWIcon("location")
    NEXT = GYWIcon("next")
    PREV = GYWIcon("prev")
    RENAME = GYWIcon("rename")
    RIGHT = GYWIcon("right")
    UNCHECK = GYWIcon("uncheck")
    UP = GYWIcon("up")

    values = [
        BLANK,
        CHECK,
        DONE,
        DOWN,
        EDIT,
        FILE,
        INFO,
        LEFT,
        LOCATION,
        NEXT,
        PREV,
        RENAME,
        RIGHT,
        UNCHECK,
        UP,
    ]
