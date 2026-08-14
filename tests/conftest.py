import sys
from unittest.mock import MagicMock
import pytest

# Pre-patch CircuitPython specific modules before any tests are run
sys.modules['usb_cdc'] = MagicMock()
sys.modules['usb_hid'] = MagicMock()
sys.modules['adafruit_hid'] = MagicMock()
sys.modules['adafruit_hid.keyboard'] = MagicMock()
sys.modules['adafruit_hid.keycode'] = MagicMock()
sys.modules['time'] = MagicMock()
sys.modules['time'].sleep = MagicMock()
sys.modules['gc'] = MagicMock()
sys.modules['gc'].collect = MagicMock()

@pytest.fixture(autouse=True)
def reset_mocks():
    sys.modules['time'].sleep.reset_mock()
    sys.modules['gc'].collect.reset_mock()
