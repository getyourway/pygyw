import asyncio

from pygyw.bluetooth.manager import BTManager, BTDevice
from pygyw.bluetooth import exceptions


async def _connect_previous(loop) -> BTDevice or None:
    manager: BTManager = BTManager()
    await manager.pull_devices()
    print("Trying to connect to a previously discovered device ...")
    for d in manager.devices:
        try:
            if await d.connect(loop):
                return d
        except Exception:
            pass


async def _connect_scanned(loop) -> BTDevice or None:
    manager: BTManager = BTManager()
    await manager.scan_devices()
    print("Trying to connect to a recently discovered device ...")
    for d in manager.devices:
        try:
            if await d.connect(loop):
                return d
        except Exception:
            pass


async def run(loop):
    manager = BTManager()

    with open("test_bluetooth.txt", "w") as f:
        # Scan with filter
        f.write("Results after scan with filter:\n")
        try:
            await manager.scan_devices(filter=True)
            f.writelines([f"{device}\n" for device in manager.devices])
        except exceptions.BTException as e:
            f.write(f"{e}\n")
        finally:
            f.write("\n")

        # Scan without filter
        f.write("Results after scan without filter:\n")
        try:
            await manager.scan_devices(filter=False, store=True)
            f.writelines([f"{device}\n" for device in manager.devices])
        except exceptions.BTException as e:
            f.write(f"{e}\n")
        finally:
            f.write("\n")

        # Scan with store and no filter
        f.write("Results of pull:\n")
        try:
            await manager.pull_devices()
            f.writelines([f"{device}\n" for device in manager.devices])
        except exceptions.BTException as e:
            f.write(f"{e}\n")
        finally:
            f.write("\n")

        # Connect to pulled device
        device = await _connect_previous(loop)
        if device:
            f.write(f"{device} connected\n")
        else:
            f.write("Connection with a pulled device failed")

        # Connect to scanned device
        device = await _connect_scanned(loop)
        if device:
            f.write(f"{device} connected\n")
        else:
            f.write("Connection with a scanned device failed")

        # Send one json data
        await device.send_jsons([
            {"type": "text", "data": "Data 1", "x_start": 100, "y_start": 100, "x_size": 800},
        ])

        # Send two jsons data
        await device.send_jsons([
            {"type": "text", "data": "Data 2", "x_start": 100, "y_start": 200, "x_size": 800},
            {"type": "text", "data": "Data 3", "x_start": 100, "y_start": 300, "x_size": 800},
        ])

        # Send white screen + text jsons data
        await device.send_jsons([
            {"type": "white_screen"},
            {"type": "text", "data": "Data 4", "x_start": 100, "y_start": 400, "x_size": 800},
        ])


loop = asyncio.get_event_loop()
loop.run_until_complete(run(loop))
