from bleak import BleakScanner
import os
import platform

from .exceptions import BTException
from .device import BTDevice
from . import settings


class BTManager:
    """
    A class to manage Bluetooth Low Energy (BLE) devices and their connections.

    Attributes:
        devices: A list of `BTDevice` objects representing devices that have been discovered.
        is_scanning: A flag indicating whether a scan is currently in progress.

    """

    def __init__(self):
        """Initialize a new instance of the `BTManager` class."""

        self.devices: "list[BTDevice]" = []
        self.is_scanning: bool = False

    def __get_device_local_storage(self):
        system = platform.system()
        if os.name == "linux" or system == "Linux":
            return os.path.join(os.path.expanduser('~'), ".local", "pygyw", "devices")
        elif os.name == "windows" or system == "Windows":
            return os.path.join(os.getenv("LOCALAPPDATA"), "pygyw", "devices")
        elif os.name == "mac" or platform.system() == "Darwin":
            return os.path.join(os.path.expanduser("~"), "Library", "Application Support", "pygyw", "devices")
        else:
            raise BTException("OS not supported")

    async def scan_devices(self, filter: bool = True, store: bool = True, timeout: int = 3):
        """
        Scan for BLE devices and saves the information of newly discovered devices.

        :param filter: A flag indicating whether to filter discovered devices by their names. Defaults to True.
        :type filter: bool
        :param store: A flag indicating whether to store information about newly discovered devices on the local file system. Defaults to True.
        :type store: bool
        :param timeout: The duration of the discovery scan. Defaults to 3.
        :type timeout: int

        :raises `BTException`: If a scan is already in progress.

        """

        if self.is_scanning:
            raise BTException("A scan is already in progress")

        self.is_scanning = True
        print("Scanning for BLE devices...")

        device_local_storage = self.__get_device_local_storage()
        try:
            devices = await BleakScanner.discover(timeout=timeout)
            self.devices = []
            for device in devices:
                if not filter or device.name in settings.device_names:
                    print(f"BLE device {device.name} found! Address: {device.address}")
                    self.devices.append(BTDevice(device))

            if store:
                if not os.path.exists(device_local_storage):
                    os.makedirs(device_local_storage)

                with open(os.path.join(device_local_storage, "devices.txt"), "w") as f:
                    f.write("\n".join(device.address))

            if not self.devices:
                print("No BLE device found found...")
        finally:
            self.is_scanning = False

    async def pull_devices(self):
        """Load previously saved device information from the local file system."""

        print("Pulling devices...")
        self.devices = []

        device_local_storage = os.path.join(self.__get_device_local_storage(), "devices.txt")

        if not os.path.exists(device_local_storage):
            print("Device local storage not setup")
            return

        with open(device_local_storage, "r") as f:
            devices = f.read().split("\n")
            for device in devices:
                self.devices.append(BTDevice(device))
                print(f"{device} pulled")
