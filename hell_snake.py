#!.venv/bin/python3
import constants
import sys
from src.controller import Controller
from src.loadouts import LoadoutManager
from src.model import Model
from src.settings import SettingsManager

def main():
    # Settings manager handles app configuration (e.g. hotkeys)
    settingsManager = SettingsManager()
    # Loadout manager handles persistance of loadouts.
    loadoutsManager = LoadoutManager()
    # Model handles combining loadouts with stratagem macros
    model = Model(loadoutsManager, settingsManager)
    # Controller handles logic and communication between the model and view
    controller = Controller(model)

    # Key listener handles hotkey detection
    # Select listener based on settings (evdev for Wayland, pynput for X11)
    if settingsManager.key_listener == constants.LISTENER_EVDEV:
        from src.listener_evdev import EvdevKeyListener
        keylistener = EvdevKeyListener(controller)
    else:
        from src.listener_pynput import PynputKeyListener
        keylistener = PynputKeyListener(controller)

    # Add keylisterner to controller to allow callbacks
    controller.set_keylistener(keylistener)

    # Initialize our presentation
    if settingsManager.view_framework == constants.VIEW_PYQT5:
        from src.view.pyqt5.pyqt5 import PyQT5View
        view = PyQT5View(controller)
    else:
        # If the view framework is not supported or recognized, print an error and exit.
        print(f"Error: Unsupported view framework '{settingsManager.view_framework}'.", file=sys.stderr)
        print("Please configure a supported view framework in the settings.", file=sys.stderr)
        sys.exit(1)

    # Set the view in the controller so it can communicate with the view.
    controller.set_view(view)

if __name__ == "__main__":
    main()