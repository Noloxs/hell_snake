#!.venv/bin/python3
from controller import Controller
from model import Model

if __name__ == "__main__":
    model = Model()
    controller = Controller(model)

    if model.settings.view_framework == "tkinter":
        from view_tkinter import TkinterView
        view = TkinterView(controller)
    elif model.settings.view_framework == "pyqt5":
        from view_pyqt5 import PyQT5View
        view = PyQT5View(controller)
    
    controller.set_view(view)
    view.show_interface()
