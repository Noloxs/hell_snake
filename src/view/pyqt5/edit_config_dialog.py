from PyQt5.QtWidgets import QDialog, QTabWidget, QVBoxLayout, QLabel, QGridLayout, QPushButton, QWidget, QFrame
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt
from src import constants
from src.classes.settings import Settings
from src.view.pyqt5.util import show_capture_key_dialog, DropdownDialog, NumberInputDialog

class EditConfigDialog(QDialog):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.settings = Settings.getInstance()

        # Set up the dialog
        self.setWindowTitle("Edit settings")
        self.setGeometry(100, 100, 400, 300)
        
        # Create a QTabWidget
        self.tabs = QTabWidget()
        
        # Add tabs
        self.tabs.addTab(self.create_key_bindings_tab(), "Key Bindings")
        self.tabs.addTab(self.create_executor_settings_tab(), "Executor Settings")
        
        # Create the layout and add the tab widget to it
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.tabs)
        
        # Set the layout for the dialog
        self.setLayout(main_layout)
    
    def create_key_bindings_tab(self):
        key_tab = QWidget()
        self.key_layout = QVBoxLayout()
        self.key_layout.setAlignment(Qt.AlignTop)
        self.key_layout.setContentsMargins(5,5,5,5)
        
        key_tab.setLayout(self.key_layout)
        
        self.update_key_settings()

        return key_tab
    
    def update_key_settings(self):
        if getattr(self, 'key_grid_layout', None) is not None:
            while self.key_grid_layout.count():
                item = self.key_grid_layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()

        self.key_grid_layout = QGridLayout()
        self.key_layout.addLayout(self.key_grid_layout)

        self.add_settings_headline(self.key_grid_layout, "Statagem bindings")
        
        self.add_key_binding(self.key_grid_layout, "Open stratagem list", self.settings.triggerKey, False, lambda: self.show_capture_dialog(SettingsBindingHandler(self, "triggerKey", self.update_key_settings).on_next_value))
        self.add_key_binding(self.key_grid_layout, "Up", self.settings.stratagemKeys[0], True, lambda: self.show_capture_dialog(StratagemKeyBindingHandler(self, 0).on_next_key))
        self.add_key_binding(self.key_grid_layout, "Down", self.settings.stratagemKeys[2], True, lambda: self.show_capture_dialog(StratagemKeyBindingHandler(self, 2).on_next_key))
        self.add_key_binding(self.key_grid_layout, "Left", self.settings.stratagemKeys[1], True, lambda: self.show_capture_dialog(StratagemKeyBindingHandler(self, 1).on_next_key))
        self.add_key_binding(self.key_grid_layout, "Right", self.settings.stratagemKeys[3], True, lambda: self.show_capture_dialog(StratagemKeyBindingHandler(self, 3).on_next_key))

        self.add_settings_headline(self.key_grid_layout, "Global arm bindings")
        self.add_key_binding(self.key_grid_layout, "Global arm", self.settings.globalArmKey, False, lambda: self.show_capture_dialog(SettingsBindingHandler(self, "globalArmKey", self.update_key_settings).on_next_value))
        self.add_key_binding(self.key_grid_layout, "Toggle mode", self.settings.globalArmMode, True, self.open_global_arm_mode_dialog)
    
    def open_global_arm_mode_dialog(self):
        items = {
            constants.ARM_MODE_PUSH: 'Push',
            constants.ARM_MODE_TOGGLE: 'Toggle'
        }

        dialog = DropdownDialog(items, self.change_arm_mode)
        dialog.exec_()

    def change_arm_mode(self, mode):
        self.settings.globalArmMode = mode
        self.update_key_bindings()

    def create_executor_settings_tab(self):
        executor_tab = QWidget()
        self.executor_layout = QVBoxLayout()
        self.executor_layout.setAlignment(Qt.AlignTop)
        self.executor_layout.setContentsMargins(5,5,5,5)

        executor_tab.setLayout(self.executor_layout)

        self.update_executor_settings()

        return executor_tab
    
    def update_executor_settings(self):
        if getattr(self, 'executor_grid_layout', None) is not None:
            while self.executor_grid_layout.count():
                item = self.executor_grid_layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()

        self.executor_grid_layout = QGridLayout()
        self.executor_layout.addLayout(self.executor_grid_layout)

        self.add_settings_headline(self.executor_grid_layout, "Executor settings")
        
        self.add_key_binding(self.executor_grid_layout, "Selected executor", self.settings.selectedExecutor, False, self.open_executor_selector_dialog)

        if self.settings.selectedExecutor == constants.EXECUTOR_PYNPUT:
            self.add_settings_headline(self.executor_grid_layout, "pynput settings")
        elif self.settings.selectedExecutor == constants.EXECUTOR_ARDUINO:
            self.add_settings_headline(self.executor_grid_layout, "Arduino passthrough settings")
        elif self.settings.selectedExecutor == constants.EXECUTOR_PYAUTOGUI:
            self.add_settings_headline(self.executor_grid_layout, "pyautogui settings")
        elif self.settings.selectedExecutor == constants.EXECUTOR_XDOTOOL:
            self.add_settings_headline(self.executor_grid_layout, "XDPTool settings")
        
        settings_items = self.controller.executer.get_settings_items()
        for i, item in enumerate(settings_items):
            if item.value_type == constants.SETTINGS_VALUE_TYPE_INT:
                value = getattr(self.settings, item.key, 0)
                self.add_key_binding(self.executor_grid_layout, item.title, str(value), i > 0, lambda checked, default_value=value, key=item.key: self.show_number_input_dialog(default_value, SettingsBindingHandler(self, key, self.update_executor_settings).on_next_value))
            elif item.value_type == constants.SETTINGS_VALUE_TYPE_HEADER:
                self.add_settings_headline(self.executor_grid_layout, item.title)

    def open_executor_selector_dialog(self):
        items = {
            constants.EXECUTOR_PYNPUT: 'pynput',
            constants.EXECUTOR_PYAUTOGUI: 'pyautogui',
            constants.EXECUTOR_ARDUINO: 'Arduino passthrough',
            constants.EXECUTOR_XDOTOOL: 'XDOTool'
        }

        dialog = DropdownDialog(items, self.change_selected_executor)
        dialog.exec_()

    def change_selected_executor(self, executor):
        self.settings.selectedExecutor = executor
        self.controller.set_executor()
        self.update_executor_settings()

    def show_number_input_dialog(self, current_value, on_number_entered):
        dialog = NumberInputDialog(current_value, on_number_entered)
        dialog.exec_()

    def show_capture_dialog(self, on_key_captured):
        show_capture_key_dialog(self, self.controller, on_key_captured, "Press key to bind")

    def add_key_binding(self, grid_layout, desc, key, add_separator, callback):
        if grid_layout.count() == 0:
            row = 0
        else:
            row = grid_layout.rowCount()
        
        if add_separator:
            self.add_separator_line(grid_layout, row)
            row = row+1
        grid_layout.addWidget(QLabel(desc), row, 0)

        key_label = QLabel(key)
        key_label.setAlignment(Qt.AlignCenter)
        grid_layout.addWidget(key_label, row, 1)

        grid_layout.addWidget(self.create_button(callback), row, 2)

    def add_settings_headline(self, grid_layout, headline):
        headline = QLabel(headline)
        headline.setFixedHeight(35)
        headline.setContentsMargins(20,0,0,0)
        headline.setStyleSheet("background-color: "+constants.COLOR_SETTINGS_HEADLINE_BACKGROUND)
        font = QFont("Arial", 14)
        font.setBold(True)
        headline.setFont(font)

        if grid_layout.count() == 0:
            row = 0
        else:
            row = grid_layout.rowCount()

        grid_layout.addWidget(headline, row, 0, 1, 3)
    
    def add_separator_line(self, layout, row):
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        layout.addWidget(line, row, 0, 1, 3)

    def create_button(self, callback):
        button = QPushButton("")
        button.setFixedWidth(30)
        button.setIcon(QIcon(constants.ICON_BASE_PATH+"settings_swap.svg"))
        button.clicked.connect(callback)
        return button

class SettingsBindingHandler:
    def __init__ (self, edit_config_dialog, settings_key, callback):
        self.settings_key = settings_key
        self.edit_config_dialog = edit_config_dialog
        self.callback = callback

    def on_next_value(self, value):
        setattr(self.edit_config_dialog.settings, self.settings_key, value)
        self.callback()

class StratagemKeyBindingHandler:
    def __init__ (self, edit_config_dialog, index):
        self.index = index
        self.edit_config_dialog = edit_config_dialog

    def on_next_key(self, key):
        # TODO Maybe check if the key is already used?
        self.edit_config_dialog.settings.stratagemKeys[self.index] = key
        self.edit_config_dialog.update_key_bindings()