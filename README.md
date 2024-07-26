# PyGYW

PyGYW is a Python library that provides an easy-to-use interface to control the aRdent smart glasses via Bluetooth. This library allows you to send instructions to the glasses such as displaying text, icons, or images on the glasses' screen.

## Installation

To install PyGYW, append this line to your `requirements.txt`:

`pygyw @ git+https://github.com/getyourway/pygyw.git`

Then run the following:

```shell
pip install --upgrade pip
pip install -r requirements.txt
```

If you are a developer, and you want to contribute to PyGYW, clone the develop branch through SSH and install it in editable mode:

```shell
git clone -b develop git@github.com:getyourway/pygyw.git
pip install --upgrade pip
pip install -e ./pygyw
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

> :warning: This method does not work with Apple devices because the MAC address of peripherals is not available.

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

## Display

To display elements on the aRdent glasses' screen, you need to create a `GYWDrawing` object and pass it to the `send_drawing(drawing)` method of the connected `BTDevice` object. There are three types of `GYWDrawing` objects:

### 1. TextDrawing

A `TextDrawing` object is used to display text on the screen. You can create a `TextDrawing` object like this:

```python
from pygyw.layout import drawings, fonts, color

drawing = drawings.TextDrawing(
    text="Hello, world!", left=100, top=100,
    font=fonts.GYWFonts.ROBOTO_MONO_BOLD, size=32,
    color=color.Color.from_hex("000000ff"))
```

:note: If you do not specify any font, the last one used on the device will be used again.

You can specify the position of the `TextDrawing` on the screen by using the `left` and `top` parameters.

To change the font of the text, you can use the font parameter, which should be set to a `GYWFont` object. This object also describes the font properties such as the height of a character or the font size. A list of active fonts can be found in the `GYWFonts` object.

### 2. IconDrawing

A `IconDrawing` object is used to display text on the screen. You can create a `IconDrawing` object like this:

```python
from pygyw.layout import drawings, icons, color

drawing = drawings.IconDrawing(
    icon=icons.GYWIcons.LEFT, left=100, top=200,
    color=color.Colors.BLUE, scale=2.5)
```

Similarly to `TextDrawing`, the positions of the `IconDrawing` can be specified with the `left` and `top` properties.

To change the icon displayed, you can use the `icon` parameter, which should be set to a `GYWIcon` object. A list of active icons can be found in the `GYWIcons` object.

To change the size of the icon, you can use the `scale` parameter. It's an optional parameter with a default value of 1.0. If the icon is 48x48, a scale factor of 2.0 will make it 96x96. The scale factor has a range between 0.01 and 13.7. Any scale factor outside of this range will be clamped to the nearest value within the range.

### 3. RectangleDrawing

A `RectangleDrawing` object is used to draw rectangles on the screen. You can create a `RectangleDrawing` object like this:

```python
from pygyw.layout import drawings, color

drawing = drawings.RectangleDrawing(
    left=100, top=200, width=50, height=70,
    color=color.Color.from_hex("00ff"))
```

The position of the rectangle can be specified with the `left` and `top` properties.

The size of the rectangle can be specified with the `width` and `height` properties.

The color is optional and if not specified, the rectangle will be filled with the current background color, useful for erasing parts of the screen.

### 4. SpinnerDrawing

A `SpinnerDrawing` object is used to display an animated spinner on the screen. You can create a `SpinnerDrawing` object like this:

```python
from pygyw.layout import drawings, color

drawing = drawings.SpinnerDrawing(
    left=400, top=200, color=color.Color.from_hex("f00"),
    scale=3, spins_per_second=1,
    animation_timing_function=drawings.AnimationTimingFunction.EASE_OUT)
```

### Colors

As shown in the various drawings, a custom `Color` object is provided by the library to define colors. A list of basic colors (RED, BLUE, ...) is available in the `Colors` object. Otherwise, the `Color.from_hex()` constructor allows to parse RBG and RGBA colors with 3, 4, 6 or 8 characters.

### Display a drawing on the screen

To display a single drawing use `device.send_drawing(drawing)`.

If you want to send multiple drawings at once, use `device.send_drawings(drawings)` where `drawings` is a list of `GYWDrawing` objects.

## Authors
 - Antoine Malherbe, Get Your Way
 - Nicolas Dessambre, Get Your Way
 - Alex Rosca, Get Your Way
