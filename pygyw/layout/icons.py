from typing import Any
from . import settings


class GYWIcon:
    """
    An icon available on aRdent smart glasses and that can be used with an `IconDrawing`.

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

    def to_json(self) -> dict[str, Any]:
        """Return a JSON-serializable dictionary of the object."""

        return {
            "icon": self.name,
        }


class GYWIcons:
    """
    All icons currently active on aRdent smart glasses.

    Attributes:
        BLANK: A blank icon that is usually used to remove an icon from the screen.
        .. image:: icons/blank.svg
            :width: 48px
            :height: 48px
            :alt: Blank icon
            :align: center

        BUILD: An icon representing construction tools.
        .. image:: icons/build.svg
            :width: 48px
            :height: 48px
            :alt: Build icon
            :align: center

        CAMERA: An icon representing a camera.
        .. image:: icons/camera.svg
            :width: 48px
            :height: 48px
            :alt: Camera icon
            :align: center

        CHAT: An icon representing a chat bubble
        .. image:: icons/chat.svg
            :width: 48px
            :height: 48px
            :alt: Chat icon
            :align: center

        CHECK: An icon representing a validated checkbox.
        .. image:: icons/check.svg
            :width: 48px
            :height: 48px
            :alt: Check icon
            :align: center

        DONE: An icon representing a check mark.
        .. image:: icons/done.svg
            :width: 48px
            :height: 48px
            :alt: Done icon
            :align: center

        DOWN: An icon representing a downward arrow.
        .. image:: icons/down.svg
            :width: 48px
            :height: 48px
            :alt: Downward arrow icon
            :align: center

        EDIT: An icon representing an edit operation.
        .. image:: icons/edit.svg
            :width: 48px
            :height: 48px
            :alt: Edit icon
            :align: center

        FILE: An icon representing a file.
        .. image:: icons/file.svg
            :width: 48px
            :height: 48px
            :alt: File icon
            :align: center

        GYW: An icon representing the Get Your Way logo.
        .. image:: icons/GYW.svg
            :width: 121px
            :height: 48px
            :alt: Get Your Way icon
            :align: center

        HELP: An icon representing the help question mark.
        .. image:: icons/help.svg
            :width: 48px
            :height: 48px
            :alt: Help icon
            :align: center

        INFO: An icon representing information.
        .. image:: icons/info.svg
            :width: 48px
            :height: 48px
            :alt: Info icon
            :align: center

        LEFT: An icon representing a left arrow.
        .. image:: icons/left.svg
            :width: 48px
            :height: 48px
            :alt: Left arrow icon
            :align: center

        LOCATION: An icon representing a location pin.
        .. image:: icons/location.svg
            :width: 48px
            :height: 48px
            :alt: Location icon
            :align: center

        NEXT: An icon representing a next or forward operation.
        .. image:: icons/next.svg
            :width: 48px
            :height: 48px
            :alt: Next icon
            :align: center

        NFC: An icon representing NFC
        .. image:: icons/nfc.svg
            :width: 48px
            :height: 48px
            :alt: NFC icon
            :align: center

        PREV: An icon representing a previous or backward operation.
        .. image:: icons/prev.svg
            :width: 48px
            :height: 48px
            :alt: Previous icon
            :align: center

        RENAME: An icon representing a rename operation.
        .. image:: icons/rename.svg
            :width: 48px
            :height: 48px
            :alt: Rename icon
            :align: center

        RIGHT: An icon representing a right arrow.
        .. image:: icons/right.svg
            :width: 48px
            :height: 48px
            :alt: Right arrow icon
            :align: center

        UNCHECK: An icon representing an unchecked checkbox.
        .. image:: icons/uncheck.svg
            :width: 48px
            :height: 48px
            :alt: Uncheck icon
            :align: center

        UP: An icon representing an upward arrow.
        .. image:: icons/up.svg
            :width: 48px
            :height: 48px
            :alt: Upward arrow icon
            :align: center

        WARNING: An icon representing warning
        .. image:: icons/warning.svg
            :width: 48px
            :height: 48px
            :alt: Warning icon
            :align: center

        WIFI: An icon representing Wi-Fi
        .. image:: icons/wifi.svg
            :width: 48px
            :height: 48px
            :alt: Wi-Fi icon
            :align: center

        KEY_0: An icon representing the key 0
        .. image:: icons/key_0.svg
            :width: 48px
            :height: 48px
            :alt: Key 0 icon
            :align: center

        KEY_1: An icon representing the key 1
        .. image:: icons/key_1.svg
            :width: 48px
            :height: 48px
            :alt: Key 1 icon
            :align: center

        KEY_2: An icon representing the key 2
        .. image:: icons/key_2.svg
            :width: 48px
            :height: 48px
            :alt: Key 2 icon
            :align: center

        KEY_3: An icon representing the key 3
        .. image:: icons/key_3.svg
            :width: 48px
            :height: 48px
            :alt: Key 3 icon
            :align: center

        KEY_4: An icon representing the key 4
        .. image:: icons/key_4.svg
            :width: 48px
            :height: 48px
            :alt: Key 4 icon
            :align: center

        KEY_5: An icon representing the key 5
        .. image:: icons/key_5.svg
            :width: 48px
            :height: 48px
            :alt: Key 5 icon
            :align: center

        KEY_6: An icon representing the key 6
        .. image:: icons/key_6.svg
            :width: 48px
            :height: 48px
            :alt: Key 6 icon
            :align: center

        KEY_7: An icon representing the key 7
        .. image:: icons/key_7.svg
            :width: 48px
            :height: 48px
            :alt: Key 7 icon
            :align: center

        KEY_8: An icon representing the key 8
        .. image:: icons/key_8.svg
            :width: 48px
            :height: 48px
            :alt: Key 8 icon
            :align: center

        KEY_9: An icon representing the key 9
        .. image:: icons/key_9.svg
            :width: 48px
            :height: 48px
            :alt: Key 9 icon
            :align: center

        KEY_A: An icon representing the key A
        .. image:: icons/key_A.svg
            :width: 48px
            :height: 48px
            :alt: Key A icon
            :align: center

        KEY_B: An icon representing the key B
        .. image:: icons/key_B.svg
            :width: 48px
            :height: 48px
            :alt: Key B icon
            :align: center

        KEY_C: An icon representing the key C
        .. image:: icons/key_C.svg
            :width: 48px
            :height: 48px
            :alt: Key C icon
            :align: center

        KEY_D: An icon representing the key D
        .. image:: icons/key_D.svg
            :width: 48px
            :height: 48px
            :alt: Key D icon
            :align: center

        KEY_STAR: An icon representing the key *
        .. image:: icons/key_star.svg
            :width: 48px
            :height: 48px
            :alt: Key * icon
            :align: center

        KEY_NUM: An icon representing the key #
        .. image:: icons/key_#.svg
            :width: 48px
            :height: 48px
            :alt: Key # icon
            :align: center

        values (list[`GYWIcon`]): A list of every available icons.

    """

    BLANK = GYWIcon("blank")
    BUILD = GYWIcon("build")
    CAMERA = GYWIcon("camera")
    CHAT = GYWIcon("chat")
    CHECK = GYWIcon("check")
    DONE = GYWIcon("done")
    DOWN = GYWIcon("down")
    EDIT = GYWIcon("edit")
    FILE = GYWIcon("file")
    GYW = GYWIcon("GYW")
    HELP = GYWIcon("help")
    INFO = GYWIcon("info")
    LEFT = GYWIcon("left")
    LOCATION = GYWIcon("location")
    NEXT = GYWIcon("next")
    NFC = GYWIcon("nfc")
    PREV = GYWIcon("prev")
    RENAME = GYWIcon("rename")
    RIGHT = GYWIcon("right")
    UNCHECK = GYWIcon("uncheck")
    UP = GYWIcon("up")
    WARNING = GYWIcon("warning")
    WIFI = GYWIcon("wifi")
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

    values = [
        BLANK,
        BUILD,
        CAMERA,
        CHAT,
        CHECK,
        DONE,
        DOWN,
        EDIT,
        FILE,
        GYW,
        HELP,
        INFO,
        LEFT,
        LOCATION,
        NEXT,
        NFC,
        PREV,
        RENAME,
        RIGHT,
        UNCHECK,
        UP,
        WARNING,
        WIFI,
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
    ]
