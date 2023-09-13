import asyncio
from bleak.backends.device import BLEDevice
from bleak import BleakClient
from bleak.exc import BleakError

from . import commands, exceptions
from ..layout import drawings, fonts


class BTDevice:
    """
    Representation of a Bluetooth Low Energy (BLE) device that can be used by the library.

    Attributes:
        device: The underlying BLE device object that is used to communicate with the device.
        client: The `BleakClient` used to connect to and interact with the device. This attribute
            is set to None by default and will be initialized when a connection to the device is established.
        font: The font currently used for drawing texts in the device
    """

    def __init__(self, device: BLEDevice):
        """
        Initialize a new instance of the `BTDevice` class.

        :param device: The underlying `bleak` object that is used to communicate with the device or the MAC address of the device.
        :type device: `BLEDevice` or str

        """

        self.device = device
        self.client: BleakClient = None

        # Optimisation for not executing the set font command when it is not changed
        self.font = None
        # Whether the font optimisation should be used or not
        self.font_optimized = True

    def __str__(self) -> str:
        return self.device

    def __repr__(self) -> str:
        return self.__str__()

    async def connect(self, loop: asyncio.AbstractEventLoop = None) -> bool:
        """
        Establish a connection with the device.

        :param loop: The event loop used in the global app. Defaults to None.
        :type loop: asyncio.AbstractEventLoop

        :return: The result of the connection (True if success, False otherwise).
        :rtype: bool

        """

        print(f"Connecting to {self.device}")
        client = BleakClient(self.device, timeout=5.0, loop=loop)
        await client.connect()

        connected = client.is_connected
        if connected:
            self.client = client
            print(f"Connection to device {self.device} succeeded")
        else:
            print(f"Connection to device {self.device} failed")

        return connected

    async def disconnect(self) -> bool:
        """
        Stop the connection with the device.

        :return: The result of the disconnection (True if success, False otherwise).
        :rtype: bool

        """

        print(f"Disconnecting from {self.device} with address: {self.device}")
        if not self.client:
            # No connection
            print("Already disconnected")
            return True

        await self.client.disconnect()

        disconnected = not self.client.is_connected
        if disconnected:
            self.client = None
            print(f"Disconnection from device {self.device} succeeded")
        else:
            print(f"Disconnection from device {self.device} failed")

        return disconnected

    async def __execute_commands(self, commands: 'list[commands.BTCommand]'):
        for command in commands:
            i = 0
            data_length = len(command.data)
            while i < data_length:
                await self.client.write_gatt_char(command.characteristic, command.data[i:i + 20], True)
                i += 20

    async def send_drawing(self, drawing: drawings.GYWDrawing):
        """
        Send and display a drawing on the device.

        :param drawing:The drawing to show on the screen.
        :type drawing: `drawings.GYWDrawing`

        """

        commands = drawing.to_commands()

        try:
            await self.__execute_commands(commands)
        except BleakError as e:
            print("Bluetooth Error while sending data: %s" % e)
            await self.disconnect()
            raise exceptions.BTException("BT Error: %s" % str(e))
        except OSError as e:
            print("OS Error while sending data: %s" % e)
            await self.disconnect()
            raise exceptions.BTException("OS Error: %s" % str(e))

        # Save font
        if isinstance(drawing, drawings.TextDrawing) and drawing.font is not None:
            self.font = drawing.font

    async def send_drawings(self, drawings: "list[drawings.GYWDrawing]"):
        """
        Send and display several drawings consecutively on the device.

        :param drawings: The list of drawings to show.
        :type drawings: `list[drawings.GYWDrawing]`

        """

        for drawing in drawings:
            await self.send_drawing(drawing)

    async def start_display(self, sleep_time: float = 0.5):
        """
        Turn the screen on.

        ..note It has no effect if the screen is already on.

        :param sleep_time: Time to wait after having switched on the screen. Defaults to 0.5.
        :type sleep_time: float

        """

        await self.__execute_commands([
            commands.BTCommand(
                commands.GYWCharacteristics.DISPLAY_COMMAND,
                bytearray([commands.ControlCodes.START_DISPLAY]),
            ),
        ])
        await asyncio.sleep(sleep_time)

    async def set_font(self, font: fonts.GYWFont, sleep_time: float = 0.1):
        """
        Set the default font.

        :param font: The font to use as default
        :type font: `font.GYWFont`
        :param sleep_time: Time to wait after having set up the font. Defaults to 0.1.
        :type sleep_time: float

        """

        await self.__execute_commands([
            commands.BTCommand(
                commands.GYWCharacteristics.DISPLAY_DATA,
                bytes(font.prefix, 'utf-8'),
            ),
            commands.BTCommand(
                commands.GYWCharacteristics.DISPLAY_COMMAND,
                bytearray([commands.ControlCodes.SET_FONT]),
            ),
        ])

        await asyncio.sleep(sleep_time)

        # Save font
        self.font = font

    async def auto_rotate_screen(self, enable: bool):
        """
        Enable or disable the screen autorotation.

        :param enable: True to enable screen auto-rotate, False to disable it.
        :type enable: bool

        """

        await self.__execute_commands([
            commands.BTCommand(
                commands.GYWCharacteristics.DISPLAY_COMMAND,
                bytearray([commands.ControlCodes.AUTO_ROTATE_SCREEN, int(enable)]),
            ),
        ])
