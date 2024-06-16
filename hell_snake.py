#!.venv/bin/python3
import constants
import sys
from src.settings import Settings
from src.controller import Controller
from src.model import Model

def main():
    # Initialize settings
    settings = Settings.getInstance()

    # Initialize and run the app
    model = Model()
    controller = Controller(model)

    # Initialize our presentation
    if settings.view_framework == constants.VIEW_PYQT5:
        from src.view.pyqt5.pyqt5 import PyQT5View
        view = PyQT5View(controller)
    else:
        # If the view framework is not supported or recognized, print an error and exit.
        print(f"Error: Unsupported view framework '{settings.view_framework}'.", file=sys.stderr)
        print("Please configure a supported view framework in the settings.", file=sys.stderr)
        sys.exit(1)

    controller.set_view(view)

if __name__ == "__main__":
    main()