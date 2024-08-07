class GYWCharacteristics:
    """
    A collection of Bluetooth Low Energy (BLE) characteristic UUIDs used to interact with GYW aRdent device.

    Attributes:
        DISPLAY_COMMAND: The UUID of the characteristic used to send commands to the display device.
        DISPLAY_DATA: The UUID of the characteristic used to send data (such as image name or text) to the display device.

    """

    DISPLAY_COMMAND = "9f3443f3-5149-4d53-9b92-35def7b82e52"
    DISPLAY_DATA = "9f3443f3-5149-4d53-9b92-35def7b82e53"


class ControlCodes:
    """
    A collection of control codes used by the GYW aRdent device to control the display.

    Attributes:
        DRAW_IMAGE: Send an image to the display.
        DRAW_TEXT: Send text to the display.
        CLEAR: Clear the screen.
        DRAW_RECTANGLE: Draw a colored rectangle.
        DRAW_SPINNER: Draw a spinner.

    """

    DRAW_IMAGE = 0x02
    DRAW_TEXT = 0x03
    CLEAR = 0x05
    DRAW_RECTANGLE = 0x0C
    DRAW_SPINNER = 0x0D


class BTCommand:
    """
    A command to be sent to an aRdent device.

    Attributes:
        characteristic: The UUID of the BLE characteristic to which the command will be sent.
        data: The data to be sent as part of the command.

    """

    def __init__(self, characteristic, data):
        """
        Initialize a new instance of the `BTCommand` class.

        :param characteristic: The UUID of the BLE characteristic to which the command will be sent.
        :type characteristic: str
        :param data: The data to be sent as part of the command.
        :type data: bytearray or bytes

        """

        self.characteristic = characteristic
        self.data = data
