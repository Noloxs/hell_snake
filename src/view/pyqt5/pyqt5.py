from src.view.view_base import BaseView
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt, pyqtSignal, QObject
from src.view.pyqt5.main import MainWindow

class PyQT5View(BaseView):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.gui = QApplication([])
        self.window = MainWindow(controller)
        self.setup_ui_update_listener()
    
    def setup_ui_update_listener(self):
        self.ui_listener = UiUpdateListener()
        self.ui_listener.ui.connect(self.update_ui)
    
    def update_ui(self, method_name, arguments):
        if method_name == self.show_interface.__name__:
            self.window.show()
            self.gui.exec()
        elif method_name == self.update_current_loadout.__name__:
            self.window.update_current_loadout()
            self.window.update_macros()
        elif method_name == self.update_macros.__name__:
            self.window.update_macros()
        elif method_name == self.update_armed.__name__:
            self.window.update_armed()
        elif method_name == self.on_loadout_changed.__name__:
            self.window.update_loadout_menu_items()
        elif method_name == self.update_executor_menu.__name__:
            self.window.update_executor_menu()
        elif method_name == self.update_title_description.__name__:
            self.window.update_title_description(arguments[0])

    def show_interface(self):
        self.ui_listener.update(self.show_interface.__name__, [])
    
    def update_macros(self):
        self.ui_listener.update(self.update_macros.__name__, [])
    
    def update_current_loadout(self):
        self.ui_listener.update(self.update_current_loadout.__name__, [])

    def update_armed(self):
        self.ui_listener.update(self.update_armed.__name__, [])

    def update_title_description(self, description):
        self.ui_listener.update(self.update_title_description.__name__, [description])

    def on_loadout_changed(self):
        self.ui_listener.update(self.on_loadout_changed.__name__, [])

    def update_executor_menu(self):
        self.ui_listener.update(self.update_executor_menu.__name__, [])

class UiUpdateListener(QObject):
    ui = pyqtSignal(str, list)

    def __init__(self):
        super().__init__()

    def update(self, method_name, list):
        self.ui.emit(method_name, list)