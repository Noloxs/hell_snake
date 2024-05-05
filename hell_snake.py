#!.venv/bin/python3
from src.controller import Controller
from src.model import Model

if __name__ == "__main__":
    model = Model()
    controller = Controller(model)

    if model.settings.view_framework == "pyqt5":
        from src.view_pyqt5 import PyQT5View
        view = PyQT5View(controller)
    
    controller.set_view(view)