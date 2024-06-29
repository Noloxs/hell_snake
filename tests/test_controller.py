from src.controller import Controller
from src.executor.executer_arduino import ArduinoPassthroughExecuter
# from src.executor.executer_pyautogui import PyAutoGuiExecuter
# from src.executor.executer_pynput import PynputExecuter
from src.executor.executer_pico import PicoPassthroughExecuter
from src.executor.executer_pyautogui import PyAutoGuiExecuter
from src.executor.executer_pynput import PynputExecuter
from src.executor.executer_xdotool import XdotoolExecuter
from src.loadouts import LoadoutManager
from src.settings import SettingsManager
import constants

# Mocking and other utilities
from unittest.mock import MagicMock
from src.view.view_base import BaseView
import pytest

@pytest.fixture
def model_mock():
    settingsManager = MagicMock(spec=SettingsManager)
    settingsManager.triggerKey = "1"
    settingsManager.currentLoadoutId = "loadout1"
    loadoutsManager = MagicMock(spec=LoadoutManager)
    loadoutsManager.loadouts = {"loadout1": {}, "loadout2": {}, "loadout3": {}}

    model = MagicMock()
    model.settingsManager = settingsManager
    model.loadoutsManager = loadoutsManager

    return model
@pytest.fixture
def view_mock():
    view = MagicMock(spec=BaseView)
    view.update_executor_menu = MagicMock()
    view.update_loadout_menu = MagicMock()
    view.update_current_loadout = MagicMock()

    return view

def test_controller_should_initialize_correctly(model_mock):
    # Arrange
    # When
    Controller(model_mock)
    # Then expect no errors during initialization

@pytest.mark.parametrize("executor_constant, executor_class", [
    (constants.EXECUTOR_ARDUINO, ArduinoPassthroughExecuter),
    (constants.EXECUTOR_PYAUTOGUI, PyAutoGuiExecuter),
    (constants.EXECUTOR_PYNPUT, PynputExecuter),
    (constants.EXECUTOR_PICO, PicoPassthroughExecuter),
    (constants.EXECUTOR_XDOTOOL, XdotoolExecuter)
])
def test_controller_should_load_correct_executor(model_mock, view_mock, executor_constant, executor_class):
    # Arrange
    controller = Controller(model_mock)
    controller.view = view_mock
    # When setting the executor
    model_mock.settingsManager.selectedExecutor = executor_constant
    controller.set_executor()

    # Then the executor should be an instance of the specified executor class
    assert isinstance(controller.executer, executor_class)


def test_controller_should_raise_error_for_unsupported_executor(model_mock, view_mock):
    # Arrange
    controller = Controller(model_mock)
    controller.view = view_mock
    # When setting the executor to an unsupported executor
    model_mock.settingsManager.selectedExecutor = "unsupported_executor"
    # Then a ModuleNotFoundError should be raised
    with pytest.raises(ModuleNotFoundError):
        controller.set_executor()

def test_controller_should_cycle_loadout(model_mock, view_mock):
    # Arrange
    controller = Controller(model_mock)
    controller.view = view_mock

    # When cycling back
    controller.cycle_loadout(-1)

    # Then the selected loadout should be the last one in the list
    assert model_mock.settingsManager.currentLoadoutId == "loadout3"

    # When cycling the loadout again
    controller.cycle_loadout(1)

    # Then the selected loadout should be the first one in the list
    assert model_mock.settingsManager.currentLoadoutId == "loadout1"

    # When cycling the loadout a third time
    controller.cycle_loadout(1)

    # Then the selected loadout should be the next one in the list (cycling back to the middle)
    assert model_mock.settingsManager.currentLoadoutId == "loadout2"

