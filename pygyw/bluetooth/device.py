import asyncio
from bleak.backends.device import BLEDevice
from bleak import BleakClient

from . import commands
from ..layout import drawings


class BTDevice:
    """
    Representation of a BLE device that can be used by the library
    """
    def __init__(self, device: BLEDevice):
        self.device = device
        self.client: BleakClient = None

    def __str__(self) -> str:
        return self.device.name

    def __repr__(self) -> str:
        return self.__str__()

    async def connect(self, loop: asyncio.AbstractEventLoop = None) -> bool:
        """
        Try to connect to the device
        Returns True in case of success, else otherwise
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

    async def disconnect(self, *args, **kwargs) -> bool:
        """
        Try to disconnect to the device
        Returns True in case of success, else otherwise
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
            await self.client.write_gatt_char(command.characterisctic, command.data)
            await asyncio.sleep(sleep_time)

    async def send_drawing(self, drawing: drawings.Drawing):
        return await self.__execute_commands(drawing.to_commands())

    async def send_drawings(self, drawings: "list[drawings.Drawing]", sleep_time: float = 0.1):
        for drawing in drawings:
            await self.send_drawing(drawing)
            await asyncio.sleep(sleep_time)

    async def start_display(self, sleep_time: float = 1):
        await self.__execute_commands([commands.start_screen])
        await asyncio.sleep(sleep_time)
