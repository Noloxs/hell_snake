#!.venv/bin/python3
from views import Overview
from controller import Controller
from model import Model

if __name__ == "__main__":
    model = Model()
    controller = Controller(model)
    overview = Overview(controller)
    controller.set_view(overview)
    overview.mainloop()
