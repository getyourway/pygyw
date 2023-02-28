import asyncio
from bleak.backends.device import BLEDevice
from bleak import BleakClient
from bleak.exc import BleakError

from . import commands, exceptions
from ..layout import drawings


class BTDevice:
    """
    Representation of a Bluetooth Low Energy (BLE) device that can be used by the library.

    Attributes:
        device (BLEDevice): The underlying BLE device object that is used to communicate with the device.
        client (BleakClient): The Bleak client used to connect to and interact with the device. This attribute
            is set to None by default and will be initialized when a connection to the device is established.
        font (Font): The font currently used for drawing texts in the device
    """

    def __init__(self, device: BLEDevice):
        """
        Initialize a new instance of the BTDevice class.

        Args:
            device (BLEDevice): The underlying BLE device object that is used to communicate with the device.
        """
        self.device = device
        self.client: BleakClient = None

        # Optimisation for not executing the set font command when it is not changed
        self.font = None

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
        client = BleakClient(self.device, timeout=5.0, loop=loop)
        await client.connect()

        connected = client.is_connected
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

        await self.client.disconnect()
        
        disconnected = not self.client.is_connected
        if disconnected:
            self.client = None
            print(f"Disconnection from device {self.device.name} succeeded")
        else:
            print(f"Disconnection from device {self.device.name} failed")

        return disconnected

    async def __execute_commands(self, commands: 'list[commands.BTCommand]'):
        for command in commands:
            i = 0
            data_length = len(command.data)
            while i < data_length:
                await self.client.write_gatt_char(command.characteristic, command.data[i:i + 20], True)
                i += 20

    async def send_drawing(self, drawing: drawings.Drawing):
        """
        Send and display a drawing on the device.

        Args:
            drawing (drawings.Drawing): The drawing to show on the screen.
        """
        commands = drawing.to_commands()

        if isinstance(drawing, drawings.TextDrawing):
            if self.font == drawing.font:
                # Skip the instruction to set the font
                commands = commands[2:]
            else:
                # Keep the fonts instruction but change the saved font
                self.font = drawing.font

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

    async def send_drawings(self, drawings: "list[drawings.Drawing]"):
        """
        Send and display several drawings consecutively on the device.

        Args:
            drawings (list[drawings.Drawing]): The list of drawings to show.
        """

        for drawing in drawings:
            await self.send_drawing(drawing)

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
