from view_base import BaseView
from PyQt5.QtWidgets import QApplication, QDialog, QLineEdit, QMainWindow, QAction, QFileDialog, QHBoxLayout,QVBoxLayout, QListWidget, QListWidgetItem, QAbstractItemView, QWidget, QLabel, QComboBox, QPushButton
from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtGui import QIcon, QPixmap, QFont, QKeySequence, QColor
from PyQt5.QtSvg import QSvgWidget
from PyQt5.Qt import QSizePolicy
from strategem import Strategem
from executer_arduino import ArduinoPassthroughExecuter
from copy import copy

class PyQT5View(BaseView):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.gui = QApplication([])
        self.window = MainWindow(controller)
    
    def add_executor_settings(self, executor):
        self.window.add_executor_settings(executor)

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
    
    def on_loadout_changed(self, id):
        self.window.update_loadout_menu_items()


class MainWindow(QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setWindowTitle("Hell snake")
        self.setWindowIcon(QIcon('icons/hell_snake.png'))
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
        self.listwidget.itemClicked.connect(self.on_macro_clicked)
        self.vBox.addWidget(self.listwidget)

        self.setup_toolbar_menu()
        self.update_armed()
    
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

        settingsOptions = files_menu.addMenu(QIcon("icons/settings.svg"), "Settings")

        dump_action = QAction(QIcon("icons/settings_print.svg"), "Print settings", self)
        dump_action.triggered.connect(self.controller.dump_settings)
        settingsOptions.addAction(dump_action)

        save_action = QAction(QIcon("icons/settings_save.svg"), "Save settings", self)
        save_action.triggered.connect(self.controller.save_settings)
        settingsOptions.addAction(save_action)

        files_menu.addSeparator()

        # TODO Replace icon
        exit_action = QAction(QIcon("icons/exit.svg"),"Exit", self)
        exit_action.triggered.connect(self.controller.exit)
        files_menu.addAction(exit_action)

        arm_action = QAction("Arm", self)
        arm_action.triggered.connect(self.controller.toggle_armed)
        self.menuBar().addAction(arm_action)

        self.loadout_menu = self.menuBar().addMenu("Loadouts")
        self.update_loadout_menu_items()
    
    def update_loadout_menu_items(self):
        self.loadout_menu.clear()
        for loadoutId, loadout in self.controller.model.settings.loadouts.items():
            loadout_action = QAction(loadout.name, self)
            loadout_action.triggered.connect(lambda checked, loadoutId=loadoutId: self.controller.set_active_loadout(loadoutId))
            self.loadout_menu.addAction(loadout_action)
        
        loadout_edit_action = QAction(QIcon("icons/edit_loadout.svg"), "Edit loadouts", self)
        loadout_edit_action.triggered.connect(self.open_edit_loadout_dialog)
        self.loadout_menu.addAction(loadout_edit_action)

    def add_executor_settings(self, executor):
        if isinstance(executor,ArduinoPassthroughExecuter):
            select_serial = self.menuBar().addMenu("Select serial")

            physical_addresses = executor.get_physical_addresses()
            for port, desc, hwid in sorted(physical_addresses):
                serial = QAction(desc, self)
                serial.triggered.connect(lambda checked, port=port: executor.connect_to_arduino(port))
                select_serial.addAction(serial)
    
    def open_edit_loadout_dialog(self):
        dialog = EditLoadoutDialog(self.controller)
        dialog.exec_()

class QLoadoutListAdapter(QWidget):
    def __init__ (self, parent = None):
        super(QLoadoutListAdapter, self).__init__(parent)

        self.hBox  = QHBoxLayout()
        self.hBox.setContentsMargins(5,5,5,0)
        
        self.icon = QLabel()
        self.icon.setFixedSize(50, 50)
        self.icon.setAlignment(Qt.AlignCenter)
        self.icon.setStyleSheet("background-color: #ff1f2832")
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
        svg_widget = QSvgWidget("icons/strategems/"+strategem.icon_name)
        svg_widget.setFixedSize(40,40)
        svg_widget.setStyleSheet("background-color: transparent")
        self.icon.setPixmap(svg_widget.grab())  
    
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
        # TODO On tab, the first item isn't selected
        self.list_widget = QListWidget()
        self.list_widget.setSelectionMode(QAbstractItemView.SingleSelection)
        self.list_widget.itemClicked.connect(self.on_item_clicked)
        self.list_widget.installEventFilter(self)
        layout.addWidget(self.list_widget)

        # Populate the QListWidget with items
        self.update_macros("")
    
    def eventFilter(self, watched, event):
        if event.type() == QEvent.KeyPress and event.matches(QKeySequence.InsertParagraphSeparator):
            i = self.list_widget.selectedItems()
            if(len(i) > 0):
                self.on_item_clicked(i[0])
                return True
        
        return False

    def on_item_clicked(self, item):
        id = item.data(Qt.UserRole)
        self.controller.update_macro_binding(self.key, id)
        self.close()

    def filter_items(self, text):
        #TODO Filter list here so it can be tested
        #TODO Sort the filtered list before updating macros
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
                listAdapterItem.setData(Qt.UserRole, id)
                listAdapterItem.setSizeHint(listAdapter.sizeHint())
                self.list_widget.addItem(listAdapterItem)
                self.list_widget.setItemWidget(listAdapterItem, listAdapter)
        self.list_widget.setCurrentRow(0)

class QFilterListAdapter(QWidget):
    def __init__ (self, parent = None):
        super(QFilterListAdapter, self).__init__(parent)

        self.hBox  = QHBoxLayout()
        self.hBox.setContentsMargins(5,5,5,0)

        self.icon = QLabel()
        self.icon.setFixedSize(25, 25)
        self.icon.setStyleSheet("background-color: #ff1f2832")
        self.icon.setAlignment(Qt.AlignCenter)
        self.hBox.addWidget(self.icon)
        
        self.name = QLabel()
        self.name.setFixedHeight(25)
        self.hBox.addWidget(self.name)
           
        self.setLayout(self.hBox)

    def setStrategem(self, strategem):
        self.name.setText(strategem.name)
        svg_widget = QSvgWidget("icons/strategems/"+strategem.icon_name)
        svg_widget.setFixedSize(20,20)
        svg_widget.setStyleSheet("background-color: transparent")
        self.icon.setPixmap(svg_widget.grab())

class EditLoadoutDialog(QDialog):
    def __init__(self, controller):
        super().__init__()

        self.controller = controller
        
        self.setWindowTitle("Edit loadouts")

        # Layout
        layout = QVBoxLayout(self)

        # Dropdown selector
        self.dropdown = QComboBox()
        self.loadouts = self.controller.model.settings.loadouts
        for id, loadout in self.loadouts.items():
            self.dropdown.addItem(loadout.name, id)
        self.dropdown.setCurrentIndex(0)
        self.dropdown.currentIndexChanged.connect(self.set_loadout)
        layout.addWidget(self.dropdown)

        # Edit field
        self.edit_field = QLineEdit()
        self.edit_field.textChanged.connect(self.on_loadout_name_changed)
        layout.addWidget(self.edit_field)

        # List widget
        self.list_widget = QListWidget()
        layout.addWidget(self.list_widget)

        buttons_layout = QHBoxLayout()
        layout.addLayout(buttons_layout)
        
        self.btn_cancel = QPushButton("Cancel")
        self.btn_save = QPushButton("Save")
        buttons_layout.addStretch(1)
        buttons_layout.addWidget(self.btn_cancel)
        buttons_layout.addWidget(self.btn_save)

        self.set_loadout()

        self.btn_cancel.clicked.connect(self.close)
        self.btn_save.clicked.connect(self.update_loadout)

    def update_loadout(self):
        self.controller.update_loadout(self.loadoutId, self.editLoadout)

    def set_loadout(self):
        self.loadoutId = self.dropdown.currentData()
        self.editLoadout = copy(self.loadouts[self.loadoutId])
        self.edit_field.setText(self.editLoadout.name)

        # Update list widget based on selected item
        self.list_widget.clear()
        self.list_widget.addItems([f"{self.editLoadout.name} - Item {i}" for i in range(1, 6)])

    def on_loadout_name_changed(self, name):
        self.editLoadout.name = name