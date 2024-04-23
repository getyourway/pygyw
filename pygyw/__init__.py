"""
PyGYW.

PyGYW is a Python library that provides an easy-to-use interface to control the aRdent smart glasses via Bluetooth.
This library allows you to send instructions to the glasses such as displaying text, icons, or images on the glasses' screen.

"""

from . import bluetooth
from . import exceptions
from . import layout
from . import color

from importlib.metadata import version

__version__ = version("pygyw")
