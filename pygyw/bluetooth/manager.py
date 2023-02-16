from bleak import BleakScanner
import pickle
import os
import platform

from .exceptions import BTException
from .device import BTDevice
from . import settings


class BTManager:
    """
    Object that manages BLE devices to which it is possible to connect
    """
    def __init__(self):
        self.devices: "list[BTDevice]" = []
        self.is_scanning: bool = False

    def __get_device_local_storage():
        system = platform.system()
        if os.name == "linux" or system == "Linux":
            return os.path.join(os.path.expanduser('~'), ".local", "pygyw", "devices")
        elif os.name == "windows" or system == "Windows":
            return os.path.join(os.getenv("LOCALAPPDATA"), "pygyw", "devices")
        elif os.name == "mac" or platform.system() == "Darwin":
            return os.path.join(os.path.expanduser("~"), "Library", "Application Support", "pygyw", "devices")
        else:
            raise BTException("OS not supported")

    async def scan_devices(self, filter=True, store=True):
        if self.is_scanning:
            raise BTException("A scan is already in progress")

        self.is_scanning = True
        print(f"Scanning for BLE devices...")

        device_local_storage = self.__get_device_local_storage()
        try:
            devices = await BleakScanner.discover()
            self.devices = []
            for device in devices:
                if not filter or device.name in settings.device_names:
                    print(f"BLE device {device.name} found! Address: {device.address}")
                    bt_device = BTDevice(device)
                    self.devices.append(bt_device)

                    if store:
                        if not os.path.exists(device_local_storage):
                            os.makedirs(device_local_storage)

                        with open(os.path.join(device_local_storage, f"{device.address}.pkl"), "wb") as f:
                            pickle.dump(bt_device, file=f)

            if not self.devices:
                print(f"No BLE device found found...")
                raise BTException("No discoverable GYW device")
        finally:
            self.is_scanning = False

    async def pull_devices(self):
        print("Pulling devices...")
        self.devices = []

        device_local_storage = self.__get_device_local_storage()

        if os.path.exists(device_local_storage):
            filenames = os.listdir(device_local_storage)
        else:
            print("Device local storage not setup")
            return

        for filename in filenames:
            if filename.endswith(".pkl"):
                with open(f"{device_local_storage}/{filename}", "rb") as f:
                    device: BTDevice = pickle.load(f)
                    self.devices.append(device)
                    print(f"{device} pulled")
