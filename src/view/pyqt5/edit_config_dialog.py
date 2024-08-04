import constants
from PyQt5.QtWidgets import QDialog, QTabWidget, QVBoxLayout, QLabel, QGridLayout, QPushButton, QWidget, QFrame
from PyQt5.QtGui import QFont, QIcon, QFontDatabase
from PyQt5.QtCore import Qt
from src.view.pyqt5.util import show_capture_key_dialog, DropdownDialog, NumberInputDialog

class EditConfigDialog(QDialog):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.settings = controller.get_settings_manager()

        # Set up the dialog
        self.setWindowTitle("Edit settings")
        self.setGeometry(100, 100, 425, 300)
        
        # Create a QTabWidget
        self.tabs = QTabWidget()
        
        # Add tabs
        self.tabs.addTab(self.create_key_bindings_tab(), "Key Bindings")
        self.tabs.addTab(self.create_executor_settings_tab(), "Executor Settings")
        self.tabs.addTab(self.create_view_settings_tab(), "View settings")
        
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

        self.add_settings_headline(self.key_grid_layout, "Stratagem bindings")
        
        self.add_key_binding(self.key_grid_layout, "Open stratagem list", self.settings.triggerKey, False, lambda: self.show_capture_dialog(SettingsBindingHandler(self.settings, "triggerKey", self.update_key_settings).on_next_value))
        self.add_key_binding(self.key_grid_layout, "Up", self.settings.stratagemKeys[0], True, lambda: self.show_capture_dialog(StratagemKeyBindingHandler(self, 0).on_next_key))
        self.add_key_binding(self.key_grid_layout, "Down", self.settings.stratagemKeys[2], True, lambda: self.show_capture_dialog(StratagemKeyBindingHandler(self, 2).on_next_key))
        self.add_key_binding(self.key_grid_layout, "Left", self.settings.stratagemKeys[1], True, lambda: self.show_capture_dialog(StratagemKeyBindingHandler(self, 1).on_next_key))
        self.add_key_binding(self.key_grid_layout, "Right", self.settings.stratagemKeys[3], True, lambda: self.show_capture_dialog(StratagemKeyBindingHandler(self, 3).on_next_key))

        self.add_settings_headline(self.key_grid_layout, "Global arm bindings")
        self.add_key_binding(self.key_grid_layout, "Global arm", self.settings.globalArmKey, False, lambda: self.show_capture_dialog(SettingsBindingHandler(self.settings, "globalArmKey", self.update_key_settings).on_next_value))
        self.add_key_binding(self.key_grid_layout, "Toggle mode", self.settings.globalArmMode, True, self.open_global_arm_mode_dialog)

        self.add_settings_headline(self.key_grid_layout, "Loadout browsing")
        self.add_key_binding(self.key_grid_layout, "Next loadout", self.settings.nextLoadoutKey, False, lambda: self.show_capture_dialog(SettingsBindingHandler(self.settings, "nextLoadoutKey", self.update_key_settings).on_next_value))
        self.add_key_binding(self.key_grid_layout, "Previous loadout", self.settings.prevLoadoutKey, True, lambda: self.show_capture_dialog(SettingsBindingHandler(self.settings, "prevLoadoutKey", self.update_key_settings).on_next_value))

    def open_global_arm_mode_dialog(self):
        items = {
            constants.ARM_MODE_PUSH: 'Push',
            constants.ARM_MODE_TOGGLE: 'Toggle'
        }

        dialog = DropdownDialog(items, self.change_arm_mode)
        dialog.exec_()

    def change_arm_mode(self, mode):
        self.settings.globalArmMode = mode
        self.update_key_settings()

    def create_executor_settings_tab(self):
        executor_tab = QWidget()
        self.executor_layout = QVBoxLayout()
        self.executor_layout.setAlignment(Qt.AlignTop)
        self.executor_layout.setContentsMargins(5,5,5,5)

        executor_tab.setLayout(self.executor_layout)

        self.update_executor_settings()

        return executor_tab
    
    def create_view_settings_tab(self):
        view_tab = QWidget()
        self.view_layout = QVBoxLayout()
        self.view_layout.setAlignment(Qt.AlignTop)
        self.view_layout.setContentsMargins(5,5,5,5)

        view_tab.setLayout(self.view_layout)

        self.update_view_settings()

        return view_tab
    
    def update_view_settings(self):
        if getattr(self, 'view_grid_layout', None) is not None:
            while self.view_grid_layout.count():
                item = self.view_grid_layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()

        self.view_grid_layout = QGridLayout()
        self.view_layout.addLayout(self.view_grid_layout)

        self.add_settings_headline(self.view_grid_layout, "View settings")
        
        self.add_key_binding(self.view_grid_layout, "Selected view framework", self.settings.view_framework, False, self.open_view_selector_dialog)

        settings_items = self.controller.view.get_settings_items()
        self.populateSettingsItems(self.view_grid_layout, settings_items, self.update_view_settings)

    def open_view_selector_dialog(self):
        items = {
            constants.VIEW_PYQT5: 'PYQT5'
        }

        dialog = DropdownDialog(items, self.change_selected_view_framework)
        dialog.exec_()

    def change_selected_view_framework(self, view_framework):
        self.settings.view_framework = view_framework
        #TODO Trigger a save and restart dialog thing

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
        
        settings_items = self.controller.executer.get_settings_items()
        self.populateSettingsItems(self.executor_grid_layout, settings_items, self.update_executor_settings)

    def open_executor_selector_dialog(self):
        items = {
            constants.EXECUTOR_PYNPUT: 'pynput',
            constants.EXECUTOR_PYAUTOGUI: 'pyautogui',
            constants.EXECUTOR_ARDUINO: 'Arduino passthrough',
            constants.EXECUTOR_XDOTOOL: 'xdotool',
            constants.EXECUTOR_PICO: 'Pico passthrough'
        }

        dialog = DropdownDialog(items, self.change_selected_executor)
        dialog.exec_()

    def change_selected_executor(self, executor):
        self.settings.selectedExecutor = executor
        self.controller.set_executor()
        self.update_executor_settings()
    
    def populateSettingsItems(self, grid_layout, settings, update_callback):
        previous_item = None
 
        for i, item in enumerate(settings):
            if item.value_type == constants.SETTINGS_VALUE_TYPE_HEADER:
                self.add_settings_headline(grid_layout, item.title)
            else:
                value = getattr(self.settings, item.key, item.default_value)
                show_separator = False if i == 0 or previous_item.value_type == constants.SETTINGS_VALUE_TYPE_HEADER else True

                if item.value_type == constants.SETTINGS_VALUE_TYPE_INT:
                    value_desc = str(value)
                    callback = lambda checked, default_value=value, key=item.key: self.show_number_input_dialog(default_value, SettingsBindingHandler(self.settings, key, update_callback).on_next_value) # noqa: E731
                elif item.value_type == constants.SETTINGS_VALUE_TYPE_BOOL:
                    value_desc = "Yes" if value else "No"
                    callback = lambda checked, current_value=value, key=item.key: SettingsBindingHandler(self.settings, key, update_callback).on_next_value(not current_value) # noqa: E731
                
                self.add_key_binding(grid_layout, item.title, value_desc, show_separator, callback)
            previous_item = item

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
        headline = QLabel(headline.upper())
        headline.setFixedHeight(35)
        headline.setContentsMargins(20,0,0,0)
        headline.setStyleSheet("background-color: "+constants.COLOR_SETTINGS_HEADLINE_BACKGROUND)
        chakra_petch_bold = QFontDatabase.applicationFontFamilies(1)[0]
        font = QFont(chakra_petch_bold, 12)
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
    def __init__ (self, settings_manager, settings_key, callback):
        self.settings_manager = settings_manager
        self.settings_key = settings_key
        self.callback = callback

    def on_next_value(self, value):
        setattr(self.settings_manager, self.settings_key, value)
        self.callback()

class StratagemKeyBindingHandler:
    def __init__ (self, edit_config_dialog, index):
        self.index = index
        self.edit_config_dialog = edit_config_dialog

    def on_next_key(self, key):
        # TODO Maybe check if the key is already used?
        self.edit_config_dialog.settings.stratagemKeys[self.index] = key
        self.edit_config_dialog.update_key_settings()