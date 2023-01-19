import asyncio
from bleak.backends.device import BLEDevice
from bleak import BleakClient
import json

from . import exceptions
from . import settings
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

    async def __send_pseudo_json(self, data: str):
        if not self.client:
            raise exceptions.BTException("Device is not connected")

        data_bytes = data.encode('UTF-8')
        i = 0
        while i < len(data_bytes):
            try:
                await self.client.write_gatt_char(settings.display_characteristic, data_bytes[i:i + 20], False)
                i = i + 20
            except Exception as e:
                raise exceptions.BTException(f"Error while sending the data : {e}")

    async def __send_jsons(self, data: "list[dict]", sleep_time=0.1):
        if not self.client:
            raise exceptions.BTException("Device is not connected")

        print(f"Sending data: {data}")
        for d in data:
            await self.__send_pseudo_json(json.dumps(d) + "{END}")
            await asyncio.sleep(sleep_time)
        print("Data sent")

    def send_drawing(self, drawing: drawings.Drawing):
        return self.__send_jsons([drawing.to_json()])

    def send_drawings(self, drawings: "list[drawings.Drawing]", sleep_time: float = 0.1):
        return self.__send_jsons([
            drawing.to_json() for drawing in drawings
        ], sleep_time=sleep_time)
