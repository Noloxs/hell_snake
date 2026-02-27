from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QListWidget, QAbstractItemView, QAction, QListWidgetItem, QFrame, QApplication
from PyQt5.QtGui import QIcon, QFont, QPixmap, QFontDatabase
from PyQt5.QtCore import Qt
from PyQt5.QtSvg import QSvgWidget
import constants
from src.utilities.resource_manager import ResourceManager
from src.controller import Controller
from src.view.pyqt5.util import PyQT5Settings
from src.view.pyqt5.filter_dialog import FilteredListDialog
from src.view.pyqt5.edit_config_dialog import EditConfigDialog
from src.view.pyqt5.edit_loadout_dialog import EditLoadoutDialog
from src.view.pyqt5.theme import ThemeManager

class MainWindow(QMainWindow):
    def __init__(self, controller : Controller):
        super().__init__()
        self.controller = controller
        self.setWindowTitle("Hell snake")
        self.setWindowIcon(QIcon(ResourceManager.get_icon_path("hell_snake.png")))
        self.setMinimumSize(400, 225)
        self.resize(400,225)
        self.update_view_settings()

        central_widget = QWidget()
        self.vBox = QVBoxLayout()
        self.vBox.setSpacing(0)
        self.vBox.setContentsMargins(0,0,0,0)
        central_widget.setLayout(self.vBox)
        self.setCentralWidget(central_widget)

        self.hBox = QHBoxLayout()
        self.hBox.setContentsMargins(0,5,0,0)
        self.armedIcon = QLabel()
        self.armedIcon.setFixedSize(70, 70)
        self.armedIcon.setMargin(5)
        self.armedIcon.setAlignment(Qt.AlignCenter)
        self.armedIcon.setScaledContents(True)
        self.hBox.addWidget(self.armedIcon)

        self.title_box = QVBoxLayout()
        self.title_box.setSpacing(4)
        self.title_box.setContentsMargins(0,0,0,0)

        self.loadout = QLabel()
        self.loadout.setAlignment(Qt.AlignVCenter|Qt.AlignLeft)

        chakra_petch_bold = QFontDatabase.applicationFontFamilies(1)[0]
        font = QFont(chakra_petch_bold, 24)
        font.setBold(True)
        self.loadout.setFont(font)
        self.title_box.addWidget(self.loadout)

        self.title_line = QFrame()
        self.title_line.setFrameShape(QFrame.HLine)
        self.title_line.setFrameShadow(QFrame.Sunken)
        self.title_line.setVisible(False)
        self.title_box.addWidget(self.title_line)

        self.loadout_desc = QLabel()
        self.loadout_desc.setAlignment(Qt.AlignTop|Qt.AlignLeft)
        self.loadout_desc.setVisible(False)
        self.title_box.addWidget(self.loadout_desc)

        self.hBox.addLayout(self.title_box)
        self.vBox.addLayout(self.hBox)

        self.armedBar = QLabel()
        self.armedBar.setFixedHeight(10)
        self.vBox.addWidget(self.armedBar)

        self.listwidget = QListWidget()
        self.listwidget.setSelectionMode(QAbstractItemView.NoSelection)
        self.listwidget.setFocusPolicy(Qt.NoFocus)
        self.listwidget.itemClicked.connect(self.on_macro_clicked)
        self.vBox.addWidget(self.listwidget)

        self.setup_toolbar_menu()
        self.update_armed()
    
    def on_stratagem_selected(self, key, id):
        self.controller.update_macro_binding(key, id)

    def on_macro_clicked(self, item):
        dialog = FilteredListDialog(self.controller, item.data(Qt.UserRole), self.on_stratagem_selected)
        dialog.exec_()
    
    def update_view_settings(self):
        if PyQT5Settings.isAlwaysOnTop(self.controller.get_settings_manager()):
            self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        else:
            self.setWindowFlags(self.windowFlags() & ~Qt.WindowStaysOnTopHint)

    def update_macros(self):
        self.listwidget.clear()

        # Calculate the height of items above the macrolist
        header_height = self.hBox.sizeHint().height()
        header_height += self.armedBar.sizeHint().height()
        header_height += self.toolbar.sizeHint().height()

        # Initial window height
        height = header_height
        for index, (key, value) in enumerate(self.controller.getAllMacros()):
            listAdapter = QLoadoutListAdapter()
            listAdapter.setKey(key)
            listAdapter.setStyleSheet("background-color: transparent")
            listAdapter.setStratagem(value)

            listAdapterItem = QListWidgetItem(self.listwidget)
            listAdapterItem.setData(Qt.UserRole,key)
            listAdapterItem.setSizeHint(listAdapter.sizeHint())

            # Add items to window height
            height += int(listAdapter.sizeHint().height())

            self.listwidget.addItem(listAdapterItem)
            self.listwidget.setItemWidget(listAdapterItem, listAdapter)

        # Resize window
        self.resize(self.geometry().width(), height)

    def update_armed(self):
        theme = ThemeManager.get_current_theme()
        if self.controller.is_armed():
            self.armedIcon.setPixmap(QPixmap(ResourceManager.get_icon_path("armed.png")))
            self.armedBar.setStyleSheet(f"background-color: {theme.colors['armed_bar']}")
            self.arm_action.setText("Disarm")
        else:
            self.armedIcon.setPixmap(QPixmap(ResourceManager.get_icon_path("disarmed.png")))
            self.armedBar.setStyleSheet(f"background-color: {theme.colors['disarmed_bar']}")
            self.arm_action.setText("Arm")
    
    def update_title_description(self, description):
        if description is None:
            self.title_line.setVisible(False)
            self.loadout_desc.setVisible(False)
        else:
            self.title_line.setVisible(True)
            self.loadout_desc.setText(description)
            self.loadout_desc.setVisible(True)

    def update_current_loadout(self):
        currentLoadout = self.controller.get_active_loadout()
        if currentLoadout is not None:
            self.loadout.setText(currentLoadout.name.upper()) 
        else:
            self.loadout.setText("")
        self.update_loadout_menu_items()

    def setup_toolbar_menu(self):
        # Create a Files menu
        self.toolbar = self.menuBar()
        files_menu = self.toolbar.addMenu("Files")

        edit_config_action = QAction(QIcon(ResourceManager.get_icon_path("settings_edit_config.svg")), "Edit settings", self)
        edit_config_action.triggered.connect(self.open_edit_config_dialog)
        files_menu.addAction(edit_config_action)

        save_action = QAction(QIcon(ResourceManager.get_icon_path("settings_save.svg")), "Save settings", self)
        save_action.triggered.connect(self.controller.get_settings_manager().saveToFile)
        files_menu.addAction(save_action)

        files_menu.addSeparator()

        save_action = QAction(QIcon(ResourceManager.get_icon_path("settings_save.svg")), "Save loadouts", self)
        save_action.triggered.connect(self.controller.get_loadouts_manager().saveToFile)
        files_menu.addAction(save_action)

        files_menu.addSeparator()

        exit_action = QAction(QIcon(ResourceManager.get_icon_path("exit.svg")),"Exit", self)
        exit_action.triggered.connect(QApplication.instance().quit)
        files_menu.addAction(exit_action)

        self.arm_action = QAction("Arm", self)
        self.arm_action.triggered.connect(self.controller.toggle_armed)
        self.toolbar.addAction(self.arm_action)

        self.loadout_menu = self.toolbar.addMenu("Loadouts")
        self.update_loadout_menu_items()
    
    def update_loadout_menu_items(self):
        self.loadout_menu.clear()
        for loadoutId, loadout in self.controller.get_loadouts_manager().loadouts.items():
            loadout_action = QAction(loadout.name, self)
            loadout_action.triggered.connect(lambda checked, loadoutId=loadoutId: self.controller.set_active_loadout(loadoutId))
            if self.controller.get_active_loadout_id() == loadoutId:
                loadout_action.setIcon(QIcon(ResourceManager.get_icon_path("serial_connected.svg")))
            self.loadout_menu.addAction(loadout_action)
        
        self.loadout_menu.addSeparator()

        loadout_edit_action = QAction(QIcon(ResourceManager.get_icon_path("edit_loadout.svg")), "Edit loadouts", self)
        loadout_edit_action.triggered.connect(self.open_edit_loadout_dialog)
        self.loadout_menu.addAction(loadout_edit_action)

    def update_executor_menu(self):
        if hasattr(self, "menu_items"):
            for item in self.menu_items:
                for action in self.toolbar.actions():
                    if action.text() == item.title:
                        self.toolbar.removeAction(action)
                        break

        self.menu_items = self.controller.executer.get_menu_items()
        for item in self.menu_items:
            self.add_executor_menu_item(self.toolbar, item)
    
    def add_executor_menu_item(self, parent, menu_item):
        if menu_item.menu_type == constants.MENU_TYPE_MENU:
            if menu_item.icon is None:
                menu = parent.addMenu(menu_item.title)
            else:
                menu = parent.addMenu(QIcon(menu_item.icon), menu_item.title)
            
            for item in menu_item.children:
                self.add_executor_menu_item(menu, item)

        elif menu_item.menu_type == constants.MENU_TYPE_ACTION:
            action = QAction(menu_item.title, self)
            if menu_item.callback is not None:
                action.triggered.connect(menu_item.callback)
            if menu_item.icon is not None:
                action.setIcon(QIcon(menu_item.icon))
            parent.addAction(action)
        
        elif menu_item.menu_type == constants.MENU_TYPE_SEPARATOR:
            parent.addSeparator()

    def open_edit_loadout_dialog(self):
        dialog = EditLoadoutDialog(self.controller)
        dialog.exec_()
    
    def open_edit_config_dialog(self):
        dialog = EditConfigDialog(self.controller)
        dialog.exec_()

class QLoadoutListAdapter(QWidget):
    def __init__ (self, parent = None):
        super(QLoadoutListAdapter, self).__init__(parent)

        self.hBox  = QHBoxLayout()
        self.hBox.setContentsMargins(5,5,5,0)
        
        self.icon = QLabel()
        self.icon.setFixedSize(50, 50)
        self.icon.setAlignment(Qt.AlignCenter)
        self.icon.setStyleSheet("background-color: "+constants.COLOR_STRATAGEM_BACKGROUND)
        self.hBox.addWidget(self.icon)
        
        self.key = QLabel()
        self.key.setFixedSize(50, 50)
        self.key.setAlignment(Qt.AlignCenter)
        chakra_petch_medium = QFontDatabase.applicationFontFamilies(0)[0]
        font = QFont(chakra_petch_medium, 24)
        font.setBold(True)
        self.key.setFont(font)
        self.hBox.addWidget(self.key)
        
        self.name = QLabel()
        self.name.setFixedHeight(50)
        self.hBox.addWidget(self.name)
           
        self.setLayout(self.hBox)

    def setStratagem(self, stratagem):
        self.name.setText(stratagem.name.upper())
        svg_widget = QSvgWidget(ResourceManager.get_stratagem_icon_path(stratagem.icon_name))
        svg_widget.setFixedSize(40,40)
        svg_widget.setStyleSheet("background-color: transparent")
        self.icon.setPixmap(svg_widget.grab())  
    
    def setKey(self, key):
        self.id = key
        self.key.setText(key)