class GYWCharacteristics:
  DISPLAY_COMMAND = "00004c31-0000-1000-8000-00805f9b34fb"
  DISPLAY_DATA = "00004c32-0000-1000-8000-00805f9b34fb"


class ControlCodes:
  START_DISPLAY = 0x01
  DISPLAY_IMAGE = 0x02
  DISPLAY_TEXT = 0x03
  CLEAR = 0x05
  SET_FONT = 0x08


class BTCommand:
    def __init__(self, characteristic, data):
        self.characteristic = characteristic
        self.data = data

start_screen = BTCommand(
    GYWCharacteristics.DISPLAY_COMMAND,
    bytearray([ControlCodes.START_DISPLAY]),
)
