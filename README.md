# PyGYW

PyGYW is a Python library that provides an easy-to-use interface to control the aRdent smart glasses via Bluetooth. This library allows you to send instructions to the glasses such as displaying text, icons, or images on the glasses' screen.

## Installation

To install PyGYW, clone the repository and use pip:

```console
> git clone https://www.github.com/getyourway/pygyw
> pip install -e pygyw
```

## Usage

To use the PyGYW library, you first need to find the aRdent glasses. There are two ways to do this:

1. You know the device MAC address:

```python
from pygyw.bluetooth import BTDevice

address = 'AA:BB:CC:DD:EE:FF'
device = BTDevice(address)
await device.connect()

```

2. If you don't know the device MAC address:
```python
from pygyw.bluetooth import BTManager

manager = BTManager()
await manager.scan_devices()

# manager.devices will contain a list of aRdent smart glasses available in the surrounding 

```

:note: You can also use `manager.pull_devices()` to retrieve the already scanned aRdent smart glasses

Once you have located the glasses, connect using the connect() method of the BTDevice object.

```python
await device.connect()
```

After the connection is established, you can display elements on the screen.

:note: :note: Before actually displaying information, you need to manually indicate to the glasses that the screen needs to be turned on with the `start_display` method.

## Display

To display elements on the aRdent glasses' screen, you need to create a `GYWDrawing` object and pass it to the `send_drawing(drawing)` method of the connected `BTDevice` object. There are three types of `GYWDrawing` objects:

### 1. WhiteScreen

A `WhiteScreen` object is a blank white screen that can be used to reset the display. You can create a `WhiteScreen` object like this:

```python
from pygyw.layout import drawings

ws = drawings.WhiteScreen()
```

### 2. TextDrawing

A `TextDrawing` object is used to display text on the screen. You can create a `TextDrawing` object like this:

```python
from pygyw.layout import drawings, fonts

text = "Hello, world!"
font = fonts.GYWFonts.LARGE
td = drawing.TextDrawing(text=text, left=100, top=100, font=font)
```

:note: If you do not specify any font, the last one used on the device will be used again.

You can specify the position of the `TextDrawing` on the screen by using the `left` and `top` parameters.

To change the font of the text, you can use the font parameter, which should be set to a `GYWFont` object. This object also describes the font properties such as the height of a character or the font size. A list of active fonts can be found in the `GYWFonts` object.

### 3. IconDrawing

A `IconDrawing` object is used to display text on the screen. You can create a `IconDrawing` object like this:

```python
from pygyw.layout import drawings, icons

icon = icons.GYWIcons.LEFT
id = drawing.IconDrawing(icon=icon, left=100, top=200)
```

Similarly to `TextDrawing`, the positions of the `IconDrawing` can be specified with the `left` and `top` properties.

To change the icon displayed, you can use the `icon` parameter, which should be set to a `GYWIcon` object. A list of active icons can be found in the `GYWIcons` object.

## Authors
 - Antoine Malherbe, Get Your Way
 - Nicolas Dessambre, Get Your Way
