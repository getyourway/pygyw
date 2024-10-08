import asyncio
import logging
import platform
from typing import Optional

from bleak import BleakClient
from bleak.backends.device import BLEDevice
from bleak.exc import BleakError, BleakDeviceNotFoundError

from . import commands, exceptions
from ..layout import drawings
from ..layout.color import Color

logger = logging.getLogger(__name__)


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

    async def start_notify(self, char_uuid_for_notifications, handler):
        if self.client is not None and self.client.is_connected:
            logger.debug(f"Listening for notifications on UUID: {char_uuid_for_notifications}...")
            await self.client.start_notify(char_uuid_for_notifications, handler)
        else:
            logger.warning("Client not connected or not available.")

    async def stop_notify(self, char_uuid):
        if self.client is not None and self.client.is_connected:
            await self.client.stop_notify(char_uuid)
        else:
            logger.warning("Client not connected or not available.")

    async def connect(self, loop: asyncio.AbstractEventLoop = None) -> bool:
        """
        Establish a connection with the device.

        :param loop: The event loop used in the global app. Defaults to None.
        :type loop: asyncio.AbstractEventLoop

        :return: The result of the connection (True if success, False otherwise).
        :rtype: bool

        """

        logger.debug(f"Connecting to {self.device}")
        client = BleakClient(self.device, timeout=5.0, loop=loop)
        try:
            await client.connect()
        except BleakDeviceNotFoundError:
            return False

        connected = client.is_connected
        if connected:
            self.client = client

            # BlueZ doesn't have a proper way to get the MTU, so we have this hack.
            # https://github.com/hbldh/bleak/blob/322346d/examples/mtu_size.py
            if client._backend.__class__.__name__ == "BleakClientBlueZDBus":
                await client._backend._acquire_mtu()

            logger.info(f"Connection to device {self.device} succeeded")
        else:
            logger.warning(f"Connection to device {self.device} failed")

        return connected

    async def disconnect(self) -> bool:
        """
        Stop the connection with the device.

        :return: The result of the disconnection (True if success, False otherwise).
        :rtype: bool

        """

        logger.debug(f"Disconnecting from {self.device} with address: {self.device}")
        if not self.client:
            # No connection
            logger.warning("Already disconnected")
            return True

        await self.client.disconnect()

        disconnected = not self.client.is_connected
        if disconnected:
            self.client = None
            logger.info(f"Disconnection from device {self.device} succeeded")
        else:
            logger.warning(f"Disconnection from device {self.device} failed")

        return disconnected

    async def __execute_commands(self, commands: "list[commands.BTCommand]"):
        system = platform.system()
        for command in commands:
            i = 0
            data_length = len(command.data)
            while i < data_length:
                await self.client.write_gatt_char(command.characteristic, command.data[i:i + 20], False)
                if system == "Darwin":  # Darwin is the name for MacOS
                    await asyncio.sleep(0.004)
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
            logger.error(f"Bluetooth Error while sending data: {e}")
            await self.disconnect()
            raise exceptions.BTException(f"BT Error: {e}")
        except OSError as e:
            logger.error(f"OS Error while sending data: {e}")
            await self.disconnect()
            raise exceptions.BTException(f"OS Error: {e}")

    async def send_drawings(self, drawings: "list[drawings.GYWDrawing]"):
        """
        Send and display several drawings consecutively on the device.

        :param drawings: The list of drawings to show.
        :type drawings: `list[drawings.GYWDrawing]`

        """

        for drawing in drawings:
            await self.send_drawing(drawing)

    async def clear_screen(self, color: Optional[Color] = None):
        """
        Reset what is displayed.

        If a color is provided, the screen will be filled with this color, otherwise the screen will be filled
        with the last color used. If a color was never provided, if fills the screen with white.

        :param color: The color to use to clear the screen. Defaults to None.
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
