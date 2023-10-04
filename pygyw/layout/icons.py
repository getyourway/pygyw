from . import settings


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

        KEY_0: An icon representing the key 0
        .. image:: icons/key_0.png
            :width: 48px
            :height: 48px
            :alt: Key 0 icon
            :align: center

        KEY_1: An icon representing the key 1
        .. image:: icons/key_1.png
            :width: 48px
            :height: 48px
            :alt: Key 1 icon
            :align: center

        KEY_2: An icon representing the key 2
        .. image:: icons/key_2.png
            :width: 48px
            :height: 48px
            :alt: Key 2 icon
            :align: center

        KEY_3: An icon representing the key 3
        .. image:: icons/key_3.png
            :width: 48px
            :height: 48px
            :alt: Key 3 icon
            :align: center

        KEY_4: An icon representing the key 4
        .. image:: icons/key_4.png
            :width: 48px
            :height: 48px
            :alt: Key 4 icon
            :align: center

        KEY_5: An icon representing the key 5
        .. image:: icons/key_5.png
            :width: 48px
            :height: 48px
            :alt: Key 5 icon
            :align: center

        KEY_6: An icon representing the key 6
        .. image:: icons/key_6.png
            :width: 48px
            :height: 48px
            :alt: Key 6 icon
            :align: center

        KEY_7: An icon representing the key 7
        .. image:: icons/key_7.png
            :width: 48px
            :height: 48px
            :alt: Key 7 icon
            :align: center

        KEY_8: An icon representing the key 8
        .. image:: icons/key_8.png
            :width: 48px
            :height: 48px
            :alt: Key 8 icon
            :align: center

        KEY_9: An icon representing the key 9
        .. image:: icons/key_9.png
            :width: 48px
            :height: 48px
            :alt: Key 9 icon
            :align: center

        KEY_A: An icon representing the key A
        .. image:: icons/key_A.png
            :width: 48px
            :height: 48px
            :alt: Key A icon
            :align: center

        KEY_B: An icon representing the key B
        .. image:: icons/key_B.png
            :width: 48px
            :height: 48px
            :alt: Key B icon
            :align: center

        KEY_C: An icon representing the key C
        .. image:: icons/key_C.png
            :width: 48px
            :height: 48px
            :alt: Key C icon
            :align: center

        KEY_D: An icon representing the key D
        .. image:: icons/key_D.png
            :width: 48px
            :height: 48px
            :alt: Key D icon
            :align: center

        KEY_STAR: An icon representing the key *
        .. image:: icons/key_star.png
            :width: 48px
            :height: 48px
            :alt: Key * icon
            :align: center

        KEY_NUM: An icon representing the key #
        .. image:: icons/key_#.png
            :width: 48px
            :height: 48px
            :alt: Key # icon
            :align: center

        CONSTRUCTION: An icon representing construction.
        .. image:: icons/construction.png
            :width: 48px
            :height: 48px
            :alt: Construction icon
            :align: center

        HELP: An icon representing the help question mark.
        .. image:: icons/help.png
            :width: 48px
            :height: 48px
            :alt: Help icon
            :align: center

        CAMERA: An icon representing a camera.
        .. image:: icons/camera.png
            :width: 48px
            :height: 48px
            :alt: Camera icon
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
    KEY_0 = GYWIcon("key_0")
    KEY_1 = GYWIcon("key_1")
    KEY_2 = GYWIcon("key_2")
    KEY_3 = GYWIcon("key_3")
    KEY_4 = GYWIcon("key_4")
    KEY_5 = GYWIcon("key_5")
    KEY_6 = GYWIcon("key_6")
    KEY_7 = GYWIcon("key_7")
    KEY_8 = GYWIcon("key_8")
    KEY_9 = GYWIcon("key_9")
    KEY_A = GYWIcon("key_A")
    KEY_B = GYWIcon("key_B")
    KEY_C = GYWIcon("key_C")
    KEY_D = GYWIcon("key_D")
    KEY_STAR = GYWIcon("key_star")
    KEY_NUM = GYWIcon("key_#")
    CONSTRUCTION = GYWIcon("construction")
    HELP = GYWIcon("help")
    CAMERA = GYWIcon("camera")

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
        KEY_0,
        KEY_1,
        KEY_2,
        KEY_3,
        KEY_4,
        KEY_5,
        KEY_6,
        KEY_7,
        KEY_8,
        KEY_9,
        KEY_A,
        KEY_B,
        KEY_C,
        KEY_D,
        KEY_STAR,
        KEY_NUM,
        CONSTRUCTION,
        HELP,
        CAMERA,
    ]
