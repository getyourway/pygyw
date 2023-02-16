import asyncio

from .manager import BTManager
from . import exceptions


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


loop = asyncio.new_event_loop()
loop.run_until_complete(run(loop))
