import asyncio

from pygyw.bluetooth.manager import BTManager, BTDevice
from pygyw.bluetooth import exceptions
from pygyw.layout import drawings, displays, fonts


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
        await device.disconnect()

        # Connect to scanned device
        device = await _connect_scanned(loop)
        if device:
            f.write(f"{device} connected\n")
        else:
            f.write("Connection with a scanned device failed")

        try:
            # Start display
            await device.start_display()

            # Send white screen
            await device.send_drawing(
                drawings.WhiteScreen()
            )

            # Send text drawing
            await device.send_drawing(
                drawings.TextDrawing("Texte", position=drawings.DrawingPosition(100, 100))
            )

            # Send icon drawing
            await device.send_drawing(
                drawings.IconDrawing("done.png", position=drawings.DrawingPosition(100, 200))
            )

            # Send multiple texts through a paragraph
            await device.send_drawings(
                displays.Paragraph(
                    "Ceci est un paragraphe, un peu long certes, mais il permet de tester un ecran sur plusieurs lignes",
                    line_height=1.5,
                    font=fonts.Fonts.LARGE,
                ).get_drawings(),
            )

            # Send a text and some icons
            await device.send_drawings(
                displays.FullAppBar(
                    title="Mon titre",
                    left="up.png",
                    right="right.png",
                ).get_drawings(),
            )
        finally:
            await device.disconnect()

loop = asyncio.get_event_loop()
loop.run_until_complete(run(loop))
