#!.venv/bin/python3
from controller import Controller
from model import Model

if __name__ == "__main__":
    model = Model()
    controller = Controller(model)

    if model.settings.view_model == "tkinter":
        from view_tkinter import TkinterView
        view = TkinterView(model, controller)
    
    controller.set_view(view)
    view.show_interface()
