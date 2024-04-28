from view_base import BaseView
from PyQt5.QtWidgets import QApplication, QDialog, QLineEdit, QMainWindow, QAction, QFileDialog, QHBoxLayout,QVBoxLayout, QListWidget, QListWidgetItem, QAbstractItemView, QWidget, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap, QFont
from PyQt5.Qt import QSizePolicy
from strategem import Strategem

class PyQT5View(BaseView):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.gui = QApplication([])
        self.window = MainWindow(controller)
    
    def add_executor_settings(self, executor):
        pass

    def show_interface(self):
        self.window.update_macros()
        self.window.setup_toolbar_menu()
        self.window.update_current_loadout()
        self.window.update_armed()
        self.window.show()
        self.gui.exec()
    
    def update_macros(self):
        self.window.update_macros()
    
    def update_current_loadout(self):
        self.window.update_current_loadout()

    def update_armed(self):
        self.window.update_armed()

class MainWindow(QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setWindowTitle("Hell snake")
        self.setWindowIcon(QIcon('icons/hell_snake.png'))
        self.setMinimumSize(350, 225)
        self.resize(350,225)

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
        font = QFont('Arial', 24)
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
        self.listwidget.itemDoubleClicked.connect(self.on_macro_clicked)
        self.vBox.addWidget(self.listwidget)
    
    def on_macro_clicked(self, item):
        dialog = FilteredListDialog(self.controller, item.data(Qt.UserRole))
        dialog.exec_()

    def update_macros(self):
        self.listwidget.clear()

        for index, (key, value) in enumerate(self.controller.model.macros.items()):
            listAdapter = QLoadoutListAdapter()
            listAdapter.setKey(key)
            listAdapter.setStyleSheet("background-color: transparent")
            listAdapter.setStrategem(value)

            listAdapterItem = QListWidgetItem(self.listwidget)
            listAdapterItem.setData(Qt.UserRole,key)
            listAdapterItem.setSizeHint(listAdapter.sizeHint())
            self.listwidget.addItem(listAdapterItem)
            self.listwidget.setItemWidget(listAdapterItem, listAdapter)

        height = 115 + (len(self.controller.model.macros)*55)
        self.resize(self.geometry().width(), height)

    def update_armed(self):
        if self.controller.model.isArmed:
            self.armedIcon.setPixmap(QPixmap("icons/armed.png"))
            self.armedBar.setStyleSheet("background-color: red")
        else: 
            self.armedIcon.setPixmap(QPixmap("icons/disarmed.png"))     
            self.armedBar.setStyleSheet("background-color: gray")
    
    def update_current_loadout(self):
        currentLoadout = self.controller.model.currentLoadout
        self.loadout.setText(currentLoadout.name)

    def setup_toolbar_menu(self):
        # Create a Files menu
        files_menu = self.menuBar().addMenu("Files")

        dump_action = QAction("Dump settings", self)
        dump_action.triggered.connect(self.controller.dump_settings)
        files_menu.addAction(dump_action)

        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.controller.exit)
        files_menu.addAction(exit_action)

        arm_action = QAction("Arm", self)
        arm_action.triggered.connect(self.controller.toggle_armed)
        self.menuBar().addAction(arm_action)

        loadout_menu = self.menuBar().addMenu("Loadouts")
        for loadoutId, loadout in self.controller.model.settings.loadouts.items():
            loadout_action = QAction(loadout.name, self)
            loadout_action.triggered.connect(lambda checked, loadoutId=loadoutId: self.controller.change_active_loadout(loadoutId))
            loadout_menu.addAction(loadout_action)

class QLoadoutListAdapter(QWidget):
    def __init__ (self, parent = None):
        super(QLoadoutListAdapter, self).__init__(parent)

        self.hBox  = QHBoxLayout()
        self.hBox.setContentsMargins(5,5,5,0)

        self.icon = QLabel()
        self.icon.setFixedSize(50, 50)
        self.icon.setAlignment(Qt.AlignCenter)
        self.icon.setScaledContents(True)
        self.hBox.addWidget(self.icon)
        
        self.key = QLabel()
        self.key.setFixedSize(50, 50)
        self.key.setAlignment(Qt.AlignCenter)
        font = QFont('Arial', 24)
        font.setBold(True)
        self.key.setFont(font)
        self.hBox.addWidget(self.key)
        
        self.name = QLabel()
        self.name.setFixedHeight(50)
        self.hBox.addWidget(self.name)
           
        self.setLayout(self.hBox)

    def setStrategem(self, strategem):
        self.name.setText(strategem.name)
        self.icon.setPixmap(QPixmap("icons/"+strategem.icon_name))     
    
    def setKey(self, key):
        self.id = key
        self.key.setText(key)

class FilteredListDialog(QDialog):
    def __init__(self, controller, key):
        super().__init__()
 
        self.controller = controller
        self.key = key
        self.setMinimumSize(300, 300)
        self.resize(300,800)

        self.setWindowTitle("Select new strategem for: "+self.key)

        # Create a layout for the dialog
        layout = QVBoxLayout(self)

        # Create an edit field
        self.edit_field = QLineEdit()
        self.edit_field.setPlaceholderText("Search...")
        self.edit_field.textChanged.connect(self.filter_items)
        layout.addWidget(self.edit_field)

        # Create a QListWidget for the list of items
        self.list_widget = QListWidget()
        self.list_widget.itemDoubleClicked.connect(self.on_item_clicked)
        layout.addWidget(self.list_widget)

        # Populate the QListWidget with items
        self.update_macros("")
    
    def on_item_clicked(self, item):
        data = item.data(Qt.UserRole)
        self.controller.change_macro_binding(data[0], data[1])
        self.close()

    def filter_items(self, text):
        self.update_macros(text.lower())

    def update_macros(self, filter):
        # Clear the current items in the QListWidget
        self.list_widget.clear()

        # Add all items to the QListWidget
        for id, strategem in self.controller.model.strategems.items():
            if filter in strategem.name.lower():
                listAdapter = QFilterListAdapter()
                listAdapter.setStyleSheet("background-color: transparent")
                listAdapter.setStrategem(strategem)

                listAdapterItem = QListWidgetItem(self.list_widget)
                listAdapterItem.setData(Qt.UserRole, [self.key, id])
                listAdapterItem.setSizeHint(listAdapter.sizeHint())
                self.list_widget.addItem(listAdapterItem)
                self.list_widget.setItemWidget(listAdapterItem, listAdapter)

class QFilterListAdapter(QWidget):
    def __init__ (self, parent = None):
        super(QFilterListAdapter, self).__init__(parent)

        self.hBox  = QHBoxLayout()
        self.hBox.setContentsMargins(5,5,5,0)

        self.icon = QLabel()
        self.icon.setFixedSize(25, 25)
        self.icon.setAlignment(Qt.AlignCenter)
        self.icon.setScaledContents(True)
        self.hBox.addWidget(self.icon)
        
        self.name = QLabel()
        self.name.setFixedHeight(25)
        self.hBox.addWidget(self.name)
           
        self.setLayout(self.hBox)

    def setStrategem(self, strategem):
        self.name.setText(strategem.name)
        self.icon.setPixmap(QPixmap("icons/"+strategem.icon_name))