from PyQt5.QtWidgets import QApplication, QDialog, QTabWidget, QVBoxLayout, QLabel, QGridLayout, QPushButton, QWidget, QFrame
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt, QSize
from src import constants
from src.classes.settings import Settings
from src.view.pyqt5.util import show_capture_key_dialog, DropdownDialog

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
        self.tabs.addTab(self.createExecutorSettingsTab(), "Executor Settings")
        self.tabs.addTab(self.createMiscTab(), "Misc")
        
        # Create the layout and add the tab widget to it
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.tabs)
        
        # Set the layout for the dialog
        self.setLayout(main_layout)
    
    def create_key_bindings_tab(self):
        widget = QWidget()
        self.key_layout = QVBoxLayout()
        self.key_layout.setContentsMargins(5,5,5,5)
        
        widget.setLayout(self.key_layout)
        
        self.update_key_bindings()

        return widget
    
    def update_key_bindings(self):
        if getattr(self, 'key_grid_layout', None) is not None:
            while self.key_grid_layout.count():
                item = self.key_grid_layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()

        self.key_grid_layout = QGridLayout()
        self.key_layout.addLayout(self.key_grid_layout)

        self.add_settings_headline(self.key_grid_layout, "Statagem bindings")
        
        self.add_key_binding(self.key_grid_layout, "Open stratagem list", self.settings.triggerKey, False, lambda: self.show_capture_dialog(KeyBindingHandler(self, "triggerKey").on_next_key))
        self.add_key_binding(self.key_grid_layout, "Up", self.settings.stratagemKeys[0], True, lambda: self.show_capture_dialog(StratagemKeyBindingHandler(self, 0).on_next_key))
        self.add_key_binding(self.key_grid_layout, "Down", self.settings.stratagemKeys[2], True, lambda: self.show_capture_dialog(StratagemKeyBindingHandler(self, 2).on_next_key))
        self.add_key_binding(self.key_grid_layout, "Left", self.settings.stratagemKeys[1], True, lambda: self.show_capture_dialog(StratagemKeyBindingHandler(self, 1).on_next_key))
        self.add_key_binding(self.key_grid_layout, "Right", self.settings.stratagemKeys[3], True, lambda: self.show_capture_dialog(StratagemKeyBindingHandler(self, 3).on_next_key))

        self.add_settings_headline(self.key_grid_layout, "Global arm bindings")
        self.add_key_binding(self.key_grid_layout, "Global arm", self.settings.globalArmKey, False, lambda: self.show_capture_dialog(KeyBindingHandler(self, "globalArmKey").on_next_key))
        self.add_key_binding(self.key_grid_layout, "Toggle mode", self.settings.globalArmMode, True, self.open_global_arm_mode_dialog)
    
    def show_capture_dialog(self, on_key_captured):
        show_capture_key_dialog(self, self.controller, on_key_captured, "Press key to bind")
    
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

    def createExecutorSettingsTab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        # Add widgets for the Executor Settings tab here
        tab.setLayout(layout)
        return tab
    
    def createMiscTab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        # Add widgets for the Misc tab here
        tab.setLayout(layout)
        return tab

    def create_button(self, callback):
        button = QPushButton("")
        button.setFixedWidth(30)
        button.setIcon(QIcon(constants.ICON_BASE_PATH+"settings_swap.svg"))
        button.clicked.connect(callback)
        return button

class KeyBindingHandler:
    def __init__ (self, edit_config_dialog, settings_key):
        self.settings_key = settings_key
        self.edit_config_dialog = edit_config_dialog

    def on_next_key(self, key):
        setattr(self.edit_config_dialog.settings, self.settings_key, key)
        self.edit_config_dialog.update_key_bindings()

class StratagemKeyBindingHandler:
    def __init__ (self, edit_config_dialog, index):
        self.index = index
        self.edit_config_dialog = edit_config_dialog

    def on_next_key(self, key):
        # TODO Maybe check if the key is already used?
        self.edit_config_dialog.settings.stratagemKeys[self.index] = key
        self.edit_config_dialog.update_key_bindings()