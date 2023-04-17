class GYWCharacteristics:
    """
    A collection of Bluetooth Low Energy (BLE) characteristic UUIDs used to interact with GYW aRdent device.

    Attributes:
        DISPLAY_COMMAND (str): The UUID of the characteristic used to send commands to the display device.
        DISPLAY_DATA (str): The UUID of the characteristic used to send data (such as image name or text) to the display device.

    """

    DISPLAY_COMMAND = "00004c31-0000-1000-8000-00805f9b34fb"
    DISPLAY_DATA = "00004c32-0000-1000-8000-00805f9b34fb"


class ControlCodes:
    """
    A collection of control codes used by the GYW aRdent device to control the display.

    Attributes:
        START_DISPLAY (int): Turn on the screen.
        DISPLAY_IMAGE (int): Send an image to the display.
        DISPLAY_TEXT (int): Send text to the display.
        CLEAR (int): Clear the screen.
        SET_FONT (int): Set the font used to display text.

    """

    START_DISPLAY = 0x01
    DISPLAY_IMAGE = 0x02
    DISPLAY_TEXT = 0x03
    CLEAR = 0x05
    SET_FONT = 0x08


class BTCommand:
    """
    A command to be sent to an aRdent device.

    Attributes:
        characteristic: The UUID of the BLE characteristic to which the command will be sent.
        data: The data to be sent as part of the command.

    """

    def __init__(self, characteristic, data):
        """
        Initialize a new instance of the BTCommand class.

        Args:
            characteristic (str): The UUID of the BLE characteristic to which the command will be sent.
            data (bytes): The data to be sent as part of the command.

        """
        self.characteristic = characteristic
        self.data = data
