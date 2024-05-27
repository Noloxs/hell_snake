from src.view.view_base import BaseView
from PyQt5.QtWidgets import QApplication
from src.view.pyqt5.main import MainWindow

class PyQT5View(BaseView):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.gui = QApplication([])
        self.window = MainWindow(controller)

    def show_interface(self):
        self.window.show()
        self.gui.exec()
    
    def update_macros(self):
        self.window.update_macros()
    
    def update_current_loadout(self):
        self.window.update_current_loadout()
        self.window.update_macros()

    def update_armed(self):
        self.window.update_armed()
    
    def on_loadout_changed(self):
        self.window.update_loadout_menu_items()