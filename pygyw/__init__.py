"""
PyGYW.

PyGYW is a Python library that provides an easy-to-use interface to control the aRdent smart glasses via Bluetooth.
This library allows you to send instructions to the glasses such as displaying text, icons, or images on the glasses' screen.

"""
from importlib.metadata import version
import logging
import os
import sys

from . import bluetooth
from . import exceptions
from . import layout

__version__ = version("pygyw")

_logger = logging.getLogger(__name__)
_logger.addHandler(logging.NullHandler())
if bool(os.getenv("PYGYW_LOGGING", False)):
    FORMAT = "%(asctime)-15s %(name)-8s %(threadName)s %(levelname)s: %(message)s"
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(logging.Formatter(fmt=FORMAT))
    _logger.addHandler(handler)
    _logger.setLevel(logging.DEBUG)
