import asyncio
from bleak.backends.device import BLEDevice
from bleak import BleakClient

from . import commands
from ..layout import drawings


class BTDevice:
    """
    Representation of a Bluetooth Low Energy (BLE) device that can be used by the library.

    Attributes:
        device (BLEDevice): The underlying BLE device object that is used to communicate with the device.
        client (BleakClient): The Bleak client used to connect to and interact with the device. This attribute
            is set to None by default and will be initialized when a connection to the device is established.
    """

    def __init__(self, device: BLEDevice):
        """
        Initialize a new instance of the BTDevice class.

        Args:
            device (BLEDevice): The underlying BLE device object that is used to communicate with the device.
        """
        self.device = device
        self.client: BleakClient = None


    def __str__(self) -> str:
        return self.device.name

    def __repr__(self) -> str:
        return self.__str__()

    async def connect(self, loop: asyncio.AbstractEventLoop = None) -> bool:
        """
        Establish a connection with the device.

        Args:
            loop (asyncio.AbstractEventLoop, optional): The event loop used in the global app. Defaults to None.

        Returns:
            bool: The result of the connection (True if success, False otherwise).
        """

        print(f"Connecting to {self.device.name} with address: {self.device.address}")
        client = BleakClient(
            self.device, timeout=10.0, loop=loop,
            disconnected_callback=self.disconnect)
        connected = await client.connect()
        if connected:
            self.client = client
            print(f"Connection to device {self.device.name} succeeded")
        else:
            print(f"Connection to device {self.device.name} failed")

        return connected

    async def disconnect(self) -> bool:
        """
        Stop the connection with the device.

        Returns:
            bool: The result of the connection (True if success, False otherwise).
        """

        print(f"Disconnecting from {self.device.name} with address: {self.device.address}")
        if not self.client:
            # No connection
            print("Already disconnected")
            return True

        disconnected = await self.client.disconnect()
        if disconnected:
            self.client = None
            print(f"Disconnection from device {self.device.name} succeeded")
        else:
            print(f"Disconnection from device {self.device.name} failed")

        return disconnected

    async def __execute_commands(self, commands: 'list[commands.BTCommand]', sleep_time: float = 0.15):
        for command in commands:
            i = 0
            data_length = len(command.data)
            while i < data_length:
                await self.client.write_gatt_char(command.characteristic, command.data[i:i + 20])
                i += 20
            await asyncio.sleep(sleep_time)

    async def send_drawing(self, drawing: drawings.Drawing):
        """
        Send and display a drawing on the device.

        Args:
            drawing (drawings.Drawing): The drawing to show on the screen.
        """
        await self.__execute_commands(drawing.to_commands())

    async def send_drawings(self, drawings: "list[drawings.Drawing]", sleep_time: float = 0.1):
        """
        Send and display several drawings consecutively on the device.

        Args:
            drawings (list[drawings.Drawing]): The list of drawings to show.
            sleep_time (float, optional): The time to wait between two drawings. Defaults to 0.1.
        """

        for drawing in drawings:
            await self.send_drawing(drawing)
            await asyncio.sleep(sleep_time)

    async def start_display(self, sleep_time: float = 0.5):
        """
        Turn the screen on. If the screen is already on, it has no effect.

        Args:
            sleep_time (float, optional): Time to wait after having switched on the screen. Defaults to 0.5.
        """

        await self.__execute_commands([
            commands.BTCommand(
                commands.GYWCharacteristics.DISPLAY_COMMAND,
                bytearray([commands.ControlCodes.START_DISPLAY]),
            ),
        ])
        await asyncio.sleep(sleep_time)
