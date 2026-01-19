import constants
from src.utilities.resource_manager import ResourceManager
from src.controller import Controller
from src.view.view_base import BaseView
from PyQt5.QtWidgets import QApplication,QMessageBox
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtGui import QFontDatabase, QFont
from src.view.pyqt5.main import MainWindow
from src.view.view_base import SettingsItem
from src.view.pyqt5.util import KEY_ALWAYS_ON_TOP, KEY_ALWAYS_ON_TOP_DEFAULT
from src.view.pyqt5.theme import ThemeManager

class PyQT5View(BaseView):
    def __init__(self, controller : Controller):
        super().__init__()
        self.controller = controller
        self.gui = QApplication([])
        self.load_fonts()
        # Initialize theme manager with settings
        ThemeManager.initialize(self.gui, controller.get_settings_manager())
        self.window = MainWindow(controller)
        self.setup_ui_update_listener()
    
    def setup_ui_update_listener(self):
        self.ui_listener = UiUpdateListener()
        self.ui_listener.ui.connect(self.update_ui)
        self.gui.aboutToQuit.connect(self.on_exit)
    
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
        elif method_name == self.on_settings_changed.__name__:
            self.window.update_view_settings()

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
    
    def on_settings_changed(self):
        self.ui_listener.update(self.on_settings_changed.__name__, [])
    
    def confirm_save_loadouts(self) -> bool:
        # Show a confirmation dialog for saving settings
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText("Loadouts was changed. Do you want to save your loadouts?")
        msg.setWindowTitle("Save Loadouts")
        msg.setStandardButtons(QMessageBox.Save | QMessageBox.Discard)
        result = msg.exec_()
        return result == QMessageBox.Save

    def get_settings_items(self):
        settings = []
        settings.append(SettingsItem("PYQT5 Settings", None, None, constants.SETTINGS_VALUE_TYPE_HEADER))
        settings.append(SettingsItem("Always on top", KEY_ALWAYS_ON_TOP_DEFAULT, KEY_ALWAYS_ON_TOP, constants.SETTINGS_VALUE_TYPE_BOOL))
        
        return settings

    def on_exit(self):
        # This method will be called when the application is about to quit
        # You can add your cleanup code here
        self.controller.on_exit()
    
    def load_fonts(self):
        font_id = QFontDatabase.addApplicationFont(ResourceManager.get_font_path('ChakraPetch-Medium.ttf'))
        if font_id == -1:
            print("Failed to load font: ChakraPetch-Medium")
        else:    
            chakra_petch_medium = QFontDatabase.applicationFontFamilies(0)[0]
            font = QFont(chakra_petch_medium, 12)
            self.gui.setFont(font)
        
        font_id = QFontDatabase.addApplicationFont(ResourceManager.get_font_path('ChakraPetch-Bold.ttf'))
        if font_id == -1:
            print("Failed to load font: ChakraPetch-Bold")

class UiUpdateListener(QObject):
    ui = pyqtSignal(str, list)

    def __init__(self):
        super().__init__()

    def update(self, method_name, list):
        self.ui.emit(method_name, list)
