#!/usr/bin/python3

import asyncio

from pygyw.bluetooth import BTDevice, BTManager
from pygyw.layout import drawings, fonts, icons


async def main():
    manager = BTManager()

    await manager.scan_devices()
    device = manager.devices[0]

    # Alternatively, you can connect to a device using its MAC address:
    # device = BTDevice("AA:BB:CC:DD:EE:FF")

    await device.connect()
    await device.start_display()

    white_screen = drawings.BlankScreen(color="ffffffff")  # ARGB
    await device.send_drawing(white_screen)

    text = "Hello, world!"
    font = fonts.GYWFonts.LARGE
    text_drawing = drawings.TextDrawing(text=text, left=100, top=100, font=font, color="ff000000")
    await device.send_drawing(text_drawing)

    text = "Big green text!"
    text_drawing = drawings.TextDrawing(text=text, left=100, top=350, size=80, color="ff00ff00")
    await device.send_drawing(text_drawing)

    icon = icons.GYWIcons.HELP
    icon_drawing = drawings.IconDrawing(icon=icon, left=400, top=200, color="ffff0000")
    await device.send_drawing(icon_drawing)

    await device.disconnect()


if __name__ == '__main__':
    asyncio.run(main())
