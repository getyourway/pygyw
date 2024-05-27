import asyncio
from typing import Optional

from bleak import BleakClient
from bleak.backends.device import BLEDevice
from bleak.exc import BleakError, BleakDeviceNotFoundError

from . import commands, exceptions
from ..layout import drawings
from ..layout.color import Color


class BTDevice:
    """
    Representation of a Bluetooth Low Energy (BLE) device that can be used by the library.

    Attributes:
        device: The underlying BLE device object that is used to communicate with the device.
        client: The `BleakClient` used to connect to and interact with the device. This attribute
            is set to None by default and will be initialized when a connection to the device is established.
    """

    def __init__(self, device: "BLEDevice | str"):
        """
        Initialize a new instance of the `BTDevice` class.

        :param device: The underlying `bleak` object that is used to communicate with the device or the MAC address of the device.
        :type device: `BLEDevice` or str

        """

        self.device = device
        self.client: BleakClient = None

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
        try:
            await client.connect()
        except BleakDeviceNotFoundError:
            return False

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

    async def __execute_commands(self, commands: "list[commands.BTCommand]"):
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

    async def send_drawings(self, drawings: "list[drawings.GYWDrawing]"):
        """
        Send and display several drawings consecutively on the device.

        :param drawings: The list of drawings to show.
        :type drawings: `list[drawings.GYWDrawing]`

        """

        for drawing in drawings:
            await self.send_drawing(drawing)

    async def start_display(self):
        """
        Turn the screen on.

        ..note It has no effect if the screen is already on.

        """

        await self.__execute_commands([
            commands.BTCommand(
                commands.GYWCharacteristics.DISPLAY_COMMAND,
                bytearray([commands.ControlCodes.START_DISPLAY]),
            ),
        ])

    async def set_contrast(self, value: float):
        """
        Set the screen contrast.

        :param value: The contrast value (between 0 and 1).
        :type value: float

        """
        assert 0 <= value <= 1

        await self.__execute_commands([
            commands.BTCommand(
                commands.GYWCharacteristics.DISPLAY_COMMAND,
                bytearray([commands.ControlCodes.SET_CONTRAST, int(value * 255)]),
            ),
        ])

    async def set_brightness(self, value: float):
        """
        Set the screen brightness.

        :param value: The brightness value (between 0 and 1).
        :type value: float

        """
        assert 0 <= value <= 1

        await self.__execute_commands([
            commands.BTCommand(
                commands.GYWCharacteristics.DISPLAY_COMMAND,
                bytearray([commands.ControlCodes.SET_BRIGHTNESS, int(value * 255)]),
            ),
        ])

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

    async def enable_backlight(self, enable: bool):
        """
        Enable or disable the display backlight.

        :param enable: True to enable the backlight, False to disable it.
        :type enable: bool

        """

        await self.__execute_commands([
            commands.BTCommand(
                commands.GYWCharacteristics.DISPLAY_COMMAND,
                bytearray([commands.ControlCodes.ENABLE_BACKLIGHT, enable]),
            ),
        ])

    async def clear_screen(self, color: Optional[Color]):
        """
        Reset what is displayed.

        If a color is provided, the screen will be filled with this color, otherwise the screen will be filled
        with the last color used. If a color was never provided, if fills the screen with white.

        :param color: The color to use to clear the screen.
        :type color: Color or None

        """

        ctrl_bytes = bytearray([commands.ControlCodes.CLEAR])
        if color:
            ctrl_bytes += color.to_rgba8888_bytes()

        await self.__execute_commands([
            commands.BTCommand(
                commands.GYWCharacteristics.DISPLAY_COMMAND,
                ctrl_bytes,
            ),
        ])
