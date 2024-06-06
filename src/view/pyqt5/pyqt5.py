from src.view.view_base import BaseView
from PyQt5.QtWidgets import QApplication
from src.view.pyqt5.main import MainWindow
from src import constants
from src.view.view_base import SettingsItem
from src.view.pyqt5.util import KEY_ALWAYS_ON_TOP, KEY_ALWAYS_ON_TOP_DEFAULT

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
    
    def update_title_description(self, description):
        self.window.update_title_description(description)

    def on_loadout_changed(self):
        self.window.update_loadout_menu_items()
    
    def update_executor_menu(self):
        self.window.update_executor_menu()

    def on_settings_changed(self):
        self.window.update_view_settings()
    
    def get_settings_items(self):
        settings = []
        settings.append(SettingsItem("PYQT5 Settings", None, None, constants.SETTINGS_VALUE_TYPE_HEADER))
        settings.append(SettingsItem("Always on top", KEY_ALWAYS_ON_TOP_DEFAULT, KEY_ALWAYS_ON_TOP, constants.SETTINGS_VALUE_TYPE_BOOL))
        
        return settings
