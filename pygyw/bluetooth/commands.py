class GYWCharacteristics:
    """
    A collection of Bluetooth Low Energy (BLE) characteristic UUIDs used to interact with GYW aRdent device.

    Attributes:
        DISPLAY_COMMAND: The UUID of the characteristic used to send commands to the display device.
        DISPLAY_DATA: The UUID of the characteristic used to send data (such as image name or text) to the display device.

    """

    DISPLAY_COMMAND = "00004C31-0000-1000-8000-00805F9B34FB"
    DISPLAY_DATA = "00004C32-0000-1000-8000-00805F9B34FB"
    FIRMWARE_VERSION = "00004CA2-0000-1000-8000-00805F9B34FB"


class ControlCodes:
    """
    A collection of control codes used by the GYW aRdent device to control the display.

    Attributes:
        START_DISPLAY: Turn on the screen.
        DISPLAY_IMAGE: Send an image to the display.
        DISPLAY_TEXT: Send text to the display.
        CLEAR: Clear the screen.
        SET_FONT: Set the font used to display text.
        AUTO_ROTATE_SCREEN: Enables or disables the screen autorotation.

    """

    START_DISPLAY = 0x01
    DISPLAY_IMAGE = 0x02
    DISPLAY_TEXT = 0x03
    CLEAR = 0x05
    SET_FONT = 0x08
    AUTO_ROTATE_SCREEN = 0x0A


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
