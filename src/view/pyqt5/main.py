from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QListWidget, QAbstractItemView, QAction, QListWidgetItem
from PyQt5.QtGui import QIcon, QFont, QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtSvg import QSvgWidget
from src import constants
from src.executer_arduino import ArduinoPassthroughExecuter
from src.view.pyqt5.filter_dialog import FilteredListDialog
from src.view.pyqt5.edit_config_dialog import EditConfigDialog
from src.view.pyqt5.edit_loadout_dialog import EditLoadoutDialog

class MainWindow(QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setWindowTitle("Hell snake")
        self.setWindowIcon(QIcon(constants.ICON_BASE_PATH+"hell_snake.png"))
        self.setMinimumSize(350, 225)
        self.resize(350,225)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)

        central_widget = QWidget()
        central_widget.setStyleSheet("background-color: white")
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

        self.loadout = QLabel()
        self.loadout.setFixedHeight(70)
        self.loadout.setAlignment(Qt.AlignVCenter|Qt.AlignLeft)
        font = QFont("Arial", 24)
        font.setBold(True)
        self.loadout.setFont(font)
        self.hBox.addWidget(self.loadout)
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

    def update_macros(self):
        self.listwidget.clear()

        for index, (key, value) in enumerate(self.controller.model.macros.items()):
            listAdapter = QLoadoutListAdapter()
            listAdapter.setKey(key)
            listAdapter.setStyleSheet("background-color: transparent")
            listAdapter.setStratagem(value)

            listAdapterItem = QListWidgetItem(self.listwidget)
            listAdapterItem.setData(Qt.UserRole,key)
            listAdapterItem.setSizeHint(listAdapter.sizeHint())
            self.listwidget.addItem(listAdapterItem)
            self.listwidget.setItemWidget(listAdapterItem, listAdapter)

        height = 115 + (len(self.controller.model.macros)*55)
        self.resize(self.geometry().width(), height)

    def update_armed(self):
        if self.controller.model.isArmed:
            self.armedIcon.setPixmap(QPixmap(constants.ICON_BASE_PATH+"armed.png"))
            self.armedBar.setStyleSheet("background-color: red")
            self.arm_action.setText("Disarm")
        else: 
            self.armedIcon.setPixmap(QPixmap(constants.ICON_BASE_PATH+"disarmed.png"))     
            self.armedBar.setStyleSheet("background-color: gray")
            self.arm_action.setText("Arm")
    
    def update_current_loadout(self):
        currentLoadout = self.controller.model.currentLoadout
        if currentLoadout is not None:
            self.loadout.setText(currentLoadout.name) 
        else:
            self.loadout.setText("")

    def setup_toolbar_menu(self):
        # Create a Files menu
        self.toolbar = self.menuBar()
        files_menu = self.toolbar.addMenu("Files")

        settingsOptions = files_menu.addMenu(QIcon(constants.ICON_BASE_PATH+"settings.svg"), "Settings")

        edit_config_action = QAction(QIcon(constants.ICON_BASE_PATH+"settings_edit_config.svg"), "Edit settings", self)
        edit_config_action.triggered.connect(self.open_edit_config_dialog)
        settingsOptions.addAction(edit_config_action)

        print_action = QAction(QIcon(constants.ICON_BASE_PATH+"settings_print.svg"), "Print settings", self)
        print_action.triggered.connect(self.controller.print_settings)
        settingsOptions.addAction(print_action)

        save_action = QAction(QIcon(constants.ICON_BASE_PATH+"settings_save.svg"), "Save settings", self)
        save_action.triggered.connect(self.controller.save_settings)
        settingsOptions.addAction(save_action)

        files_menu.addSeparator()

        exit_action = QAction(QIcon(constants.ICON_BASE_PATH+"exit.svg"),"Exit", self)
        exit_action.triggered.connect(self.controller.exit)
        files_menu.addAction(exit_action)

        self.arm_action = QAction("Arm", self)
        self.arm_action.triggered.connect(self.controller.toggle_armed)
        self.toolbar.addAction(self.arm_action)

        self.loadout_menu = self.toolbar.addMenu("Loadouts")
        self.update_loadout_menu_items()
    
    def update_loadout_menu_items(self):
        self.loadout_menu.clear()
        for loadoutId, loadout in self.controller.model.settings.loadouts.items():
            loadout_action = QAction(loadout.name, self)
            loadout_action.triggered.connect(lambda checked, loadoutId=loadoutId: self.controller.set_active_loadout(loadoutId))
            self.loadout_menu.addAction(loadout_action)
        
        self.loadout_menu.addSeparator()

        loadout_edit_action = QAction(QIcon(constants.ICON_BASE_PATH+"edit_loadout.svg"), "Edit loadouts", self)
        loadout_edit_action.triggered.connect(self.open_edit_loadout_dialog)
        self.loadout_menu.addAction(loadout_edit_action)

    def update_executor_menu(self):
        executor = self.controller.executer

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
        font = QFont("Arial", 24)
        font.setBold(True)
        self.key.setFont(font)
        self.hBox.addWidget(self.key)
        
        self.name = QLabel()
        self.name.setFixedHeight(50)
        self.hBox.addWidget(self.name)
           
        self.setLayout(self.hBox)

    def setStratagem(self, stratagem):
        self.name.setText(stratagem.name)
        svg_widget = QSvgWidget(constants.STRATAGEM_ICON_PATH+stratagem.icon_name)
        svg_widget.setFixedSize(40,40)
        svg_widget.setStyleSheet("background-color: transparent")
        self.icon.setPixmap(svg_widget.grab())  
    
    def setKey(self, key):
        self.id = key
        self.key.setText(key)